# IU Python Assignment - Ideal Function Selection and Test Data Mapping

## Project Overview

This project applies ideal function selection and test data mapping using Python. The main goal of this project is to process the training data, determine the suitable ideal functions based on the Sum of Squared Errors, and map the test data based on those functions. The results are stored in a SQLite database and visualized using Bokeh. 

## Project Structure

| File                 | Description                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| main.py              | Main program performing the execution of the workflow                                              |
| data_handler.py      | Responsible for loading and validating CSV data                                                    |
| calculations.py      | Calculates the sum of squared errors (SSE), selects ideal functions, and checks allowed deviations |
| test_calculations.py | Unit tests for the calculation functions                                                           |
| test_data_handler.py | Holds unit tests on data management                                                                |
| train.csv            | The training dataset                                                                               |
| ideal.csv            | Contains the ideal function dataset                                                                |
| test.csv             | The test set file                                                                                  |

## Technologies Used

- Python
- Pandas
- NumPy
- SQLAlchemy
- SQLite
- Bokeh
- Pytest

## Installation

1. Clone the repository by executing the following command:

```
git clone https://github.com/mara-kretsou/Python_Assignment.git
```

2. Change to the project directory:

```
cd Python_Assignment
```

3. Create and activate a virtual environment using the command:

```
python -m venv .venv
```

Activate the virtual environment:

```
.\.venv\Scripts\Activate.ps1
```

4. Run this to install the necessary libraries:

```
python -m pip install pandas numpy sqlalchemy bokeh pytest
```

## Running the Application

To run the main program, utilize the following command:

```
python main.py
```

Will load the CSV data sets, select the best ideal functions, maps the test points, stores the results in SQLite db, and display six Bokeh plots.

## Executing the Tests

Run the automated tests using the command:

```
python -m pytest -v
```

The tests are created to ensure that the calculation and data handling processes work.

## Repository

GitHub: https://github.com/mara-kretsou/Python_Assignment
