from data_handler import DataHandler, TrainingDataHandler, MissingTrainingColumnError
import pytest

def test_load_training_data():
    """Tests loading the training CSV data."""
    handler = DataHandler("train.csv")
    data = handler.load_data()
    assert len(data) == 400
    assert len(data.columns) == 5


def test_load_ideal_data():
    """Tests loading the ideal functions CSV data."""
    handler = DataHandler("ideal.csv")
    data = handler.load_data()
    assert len(data) == 400 
    assert len(data.columns) == 51


def test_load_test_data():
    """Tests loading the test CSV data."""
    handler = DataHandler("test.csv")
    data = handler.load_data()
    assert len(data) == 100 
    assert len(data.columns) == 2


def test_missing_file():
    """Tests that a missing CSV file raises FileNotFoundError."""
    handler = DataHandler("missing.csv")
    with pytest.raises(FileNotFoundError):
        handler.load_data()


def test_validate_training_columns():
    """Tests validation of the required training columns."""
    handler = TrainingDataHandler("train.csv")
    handler.load_data()
    handler.validate_columns()
    

def test_missing_training_column():
    """Tests that a missing training column raises an exeption."""
    handler = TrainingDataHandler("train.csv")
    handler.load_data()
    handler.data = handler.data.drop(columns=["y4"])

    with pytest.raises(MissingTrainingColumnError):
        handler.validate_columns()


    
