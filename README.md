# IU Python Assignment - Ideal Function Selection and Test Data Mapping

Project Overview

This project applies a methodology of the ideal functions selection and test data mapping using Python. The main goal of this project is process the training data, determine the suitable ideal functions based on the SSE, and assess the test data based on those functions.

Project Structure

| File | Description |
|---|---|
| main.py | Main program performing the execution of the workflow |
| data_handler.py | Responsible for loading and validating CSV data |
| calculations.py | Calculates the sum of squared errors (SSE) |
| test_calculations.py | Unit tests for the calculation functions |
| test_data_handler.py | Holds unit tests on data management |
| train.csv | The training dataset |
| ideal.csv | Contains the ideal function dataset |
| test.csv | The test set file |

Technologies Used

- Python
- Pandas
- NumPy
- SQLAlchemy
- SQLite
- Bokeh
- Pytest

Installation

1. Clone the repository by executing the following command:

git clone https://github.com/mara-kretsou/Python_Assignment.git

2. Change to the project directory:

cd Python_Assignment

3. Create and activate a virtual environment using the command:

python -m venv .venv

Activate the virtual environment:

`.\.venv\Scripts\Activate.ps1`

4. Run this to install the necessary libraries:

pip install pandas numpy sqlalchemy bokeh pytest

Running the Application

To run the main program, utilize the following command:

python main.py

Will take the data sets, do the calculations, and create the visualizations.

Executing the Tests

Run the automated tests using the command:

python -m pytest -v

The tests are created to ensure that the calculation and data handling processes work.

Repository

GitHub: https://github.com/mara-kretsou/Python_Assignment
