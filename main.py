"""
Main program for selecting the best 4 ideal functions,
mapping test data,storing results in SQLite,
and visualizing the results with Bokeh.
"""


import pandas as pd
from sqlalchemy import create_engine
from bokeh.plotting import figure,show, output_file
from bokeh.layouts import column
from data_handler import DataHandler,TrainingDataHandler
from calculations import calculate_allowed_deviation, find_best_ideal
from point_mapper import PointMapper
from database_manager import DatabaseManager
from calculations import validate_matching_x
from sqlalchemy.exc import SQLAlchemyError
from visualizer import create_function_plots

def main():
    #Initialize handles for the 3 CSV files
    training_handler = TrainingDataHandler("train.csv")
    ideal_handler = DataHandler("ideal.csv")
    test_handler = DataHandler("test.csv")
    print(training_handler.filename)

    #Load and validate the training data
    training_data = training_handler.load_data()
    training_handler.validate_columns()
    print("\n---TRAINING DATA---")
    print(training_data.head())
    print(training_data.shape)
    print(training_data.isnull().sum())
    ideal_data = ideal_handler.load_data()
    print("\n---IDEAL FUNCTIONS---")
    print(ideal_data.head())
    print(ideal_data.shape)
    print(ideal_data.isnull().sum())
    test_data = test_handler.load_data()
    print("\n---TEST DATA---")
    print(test_data.head())
    print(test_data.shape)
    print(test_data.isnull().sum())


    #Create the SQL database and establish connection
    db_manager = DatabaseManager()
    db_manager.check_connection()
    engine = db_manager.engine

    print("Database connection successful")
    
    #Store training and ideal data in the SQLite database
    training_data.to_sql("training_data", con=engine, if_exists="replace", index=False )
    result = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM training_data", con=engine)
    print(result)

    ideal_data.to_sql("ideal_data", con=engine, if_exists="replace", index=False)
    ideal_result = pd.read_sql_query("SELECT COUNT(*) AS total_rows FROM ideal_data", con=engine)
    print(ideal_result)

    columns_result = pd.read_sql_query("PRAGMA table_info(ideal_data)", con=engine)
    print("Number of columns:",len(columns_result))

    validate_matching_x(training_data, ideal_data)

    #Find the best ideal function for each training function using SSE
    best_matches = {}

    for training_name in training_data.columns[1:]:
        best_ideal = find_best_ideal(training_data[training_name], ideal_data)
        best_matches[training_name] = best_ideal

    print(best_matches)

    #Calculates the maximum allowed deviation for each selected ideal function
    allowed_differences = {}

    for training_name in best_matches:
        ideal_name = best_matches[training_name]
        allowed_difference = calculate_allowed_deviation(training_data[training_name],ideal_data[ideal_name])
        allowed_differences[ideal_name] = allowed_difference
        print(training_name,ideal_name,allowed_difference)
    print(allowed_differences)
    mapper = PointMapper(ideal_data)
    new_matches = mapper.map_points(test_data, allowed_differences)
        
    final_matches = new_matches
    print("Mapping columns:", final_matches.columns.tolist())
    print(len(final_matches))

    #Save the final test mappings and deviations in the SQLlite database 
    mapping_for_db = final_matches[["x", "y", "deviation", "ideal_function", "test_row_id"]]
    db_manager.reset_mapping_table()
    mapping_for_db.to_sql("test_mapping", engine, if_exists="append", index=False)

    saved_matches = pd.read_sql("SELECT * FROM test_mapping", engine)
    print(len(saved_matches))
    print(saved_matches.head())
    print(pd.read_sql_query("PRAGMA table_info(test_mapping)", engine))

    unmatched_tests = mapper.find_unmatched_points(test_data, final_matches)
    
    #Visualize training data, selected ideal functions, and matched test points using Bokeh 
    plots = create_function_plots(training_data, ideal_data, best_matches, final_matches, allowed_differences,unmatched_tests)
    deviation_plot = figure(title="Deviation of Matched Points")
    deviation_plot.xaxis.axis_label= "Test x-value"
    deviation_plot.yaxis.axis_label= "Absolute Deviation"
    deviation_plot.scatter(final_matches["x"], final_matches["deviation"])

    unmatched_plot = figure(title="Unmatched Test Points")
    unmatched_plot.xaxis.axis_label= "Test x-value"
    unmatched_plot.yaxis.axis_label= "Test y-value"
    unmatched_plot.scatter(unmatched_tests["x"], unmatched_tests["y"])

    all_plots = column(*plots,deviation_plot,unmatched_plot)
    output_file("assignment_plots.html", title="Function Analysis")
    show(all_plots)

if __name__=="__main__":
    main()
