"""Load CSV files and validate training data."""

import pandas as pd

class MissingTrainingColumnError(ValueError):
   """Raised when a required training column is missing."""


class DataHandler:
    """Handles loading and managing CSV data."""
    def __init__(self, filename):
     """Initializes the data handler with a CSV filename."""
     self.filename = filename
     self.data = None
   
    def load_data(self):
       """"Read the CSV file and return its data."""
       try:  
        self.data = pd.read_csv(self.filename)
       except FileNotFoundError as error:
         raise FileNotFoundError(f"CSV file not found: {self.filename}") from error 
       return self.data
   

class TrainingDataHandler(DataHandler):
   """Handles validation of training data."""
   def validate_columns(self):
      """Checks that all required training columns exist."""
      if self.data is None:
         raise ValueError("Load the CSV before validating columns.")
      required_columns = ["x", "y1", "y2", "y3", "y4"]

      for column in required_columns:
         
         if column not in self.data.columns:
            print("Missing column:", column)
            raise MissingTrainingColumnError("A required column is missing!")

