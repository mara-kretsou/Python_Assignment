"""
Main program for selecting the best 4 ideal functions,
mapping test data,storing results in SQLite,
and visualizing the results with Bokeh.
"""


import pandas as pd
from sqlalchemy import create_engine
from bokeh.plotting import figure,show
from bokeh.layouts import column
from data_handler import DataHandler,TrainingDataHandler
from calculations import calculate_allowed_deviation, find_best_ideal


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
engine = create_engine("sqlite:///assignment.db")
with engine.connect() as connection:
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

print("X values match:",training_data["x"].equals(ideal_data["x"]))

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
    
#Map test data to the selected ideal functions using the allowed deviation
matched_tests = []

for test_number in range(100):
    test_point = test_data.iloc[test_number]
    test_x = test_point["x"]
    test_y = test_point["y"]

    for ideal_name in allowed_differences:
        matching_value = ideal_data.loc[ideal_data["x"] == test_x, ideal_name].iloc[0]
        deviation = abs(test_y - matching_value)
        if deviation <= allowed_differences[ideal_name]:
            matched_tests.append([test_x,test_y,ideal_name,deviation])

#Organizes matched test points and remove duplicate mappings
matches_table = pd.DataFrame(matched_tests, columns=["x","y","ideal_function","deviation"])
print(matches_table.head())
print(matches_table.duplicated(subset=["x","y"]).sum())

duplicates = matches_table[matches_table.duplicated(subset=["x","y"],keep=False)]
print(duplicates)

sorted_matches = matches_table.sort_values("deviation")
print(sorted_matches.head())

final_matches = sorted_matches.drop_duplicates(subset=["x","y"],keep="first")
print(len(final_matches))

#Save the final test mappings and deviations in the SQLlite database 
final_matches.to_sql("test_mapping",engine,if_exists="replace", index=False)

saved_matches = pd.read_sql("SELECT * FROM test_mapping", engine)
print(len(saved_matches))
print(saved_matches.head())

test_comparison = test_data.merge(final_matches[["x","y"]], on=["x","y"], how="left", indicator=True)
unmatched_tests = test_comparison[test_comparison["_merge"] == "left_only"]

#Visualize training data, selected ideal functions, and matched test points using Bokeh 
plot = figure(title="Training y1 and Ideal y13")
plot.xaxis.axis_label="x"
plot.yaxis.axis_label="y"
plot.line(training_data["x"], training_data["y1"], legend_label="Training y1")
plot.line(ideal_data["x"],ideal_data["y13"], color="red", legend_label="Ideal y13")
y13_tests = final_matches[final_matches["ideal_function"] == "y13"] 
plot.scatter(y13_tests["x"], y13_tests["y"], legend_label="Matched Test Points")

plot2 = figure(title="Training y2 and Ideal y24")
plot2.xaxis.axis_label="x"
plot2.yaxis.axis_label="y"
plot2.line(training_data["x"], training_data["y2"], legend_label="Training y2")
plot2.line(ideal_data["x"], ideal_data["y24"], color="red",line_dash="dashed",legend_label="Ideal y24")
y24_tests = final_matches[final_matches["ideal_function"] == "y24"]
plot2.scatter(y24_tests["x"],y24_tests["y"], legend_label="Matched Test Points")

plot3 = figure(title="Training y3 and Ideal y36")
plot3.xaxis.axis_label="x"
plot3.yaxis.axis_label="y"
plot3.line(training_data["x"], training_data["y3"], legend_label="Training y3")
plot3.line(ideal_data["x"], ideal_data["y36"], color="red",line_dash="dashed",legend_label="Ideal y36")
y36_tests = final_matches[final_matches["ideal_function"] == "y36"]
plot3.scatter(y36_tests["x"],y36_tests["y"], legend_label="Matched Test Points")

plot4 = figure(title="Training y4 and Ideal y40")
plot4.xaxis.axis_label="x"
plot4.yaxis.axis_label="y"
plot4.line(training_data["x"], training_data["y4"], legend_label="Training y4")
plot4.line(ideal_data["x"], ideal_data["y40"], color="red",line_dash="dashed",legend_label="Ideal y40")
y40_tests = final_matches[final_matches["ideal_function"] == "y40"]
plot4.scatter(y40_tests["x"],y40_tests["y"], legend_label="Matched Test Points")

deviation_plot = figure(title="Deviation of Matched Points")
deviation_plot.xaxis.axis_label= "Test x-value"
deviation_plot.yaxis.axis_label= "Absolute Deviation"
deviation_plot.scatter(final_matches["x"], final_matches["deviation"])

unmatched_plot = figure(title="Unmatched Test Points")
unmatched_plot.xaxis.axis_label= "Test x-value"
unmatched_plot.yaxis.axis_label= "Test y-value"
unmatched_plot.scatter(unmatched_tests["x"], unmatched_tests["y"])

all_plots = column(plot,plot2,plot3,plot4,deviation_plot,unmatched_plot)
show(all_plots)