"""Unit tests for CSV loading and data validation."""

from data_handler import (
    DataHandler,
    TrainingDataHandler,
    MissingTrainingColumnError,
    TestDataHandler,
)
import pytest


@pytest.fixture
def sample_csv_files(tmp_path):
    """Creates temporary CSV files for testing."""
    files = {
        "train": "x,y1,y2,y3,y4\n0,1,2,3,4\n1,2,3,4,5\n",
        "ideal": "x,y1,y2\n0,1,2\n1,2,3\n",
        "test": "x,y\n0,1\n1,2\n",
    }
    paths = {}

    for name, content in files.items():
        path = tmp_path / f"{name}.csv"
        path.write_text(content, encoding="utf-8")
        paths[name] = path

    return paths


def test_load_training_data(sample_csv_files):
    """Tests loading the training data from a temporary CSV."""
    handler = DataHandler(sample_csv_files["train"])
    data = handler.load_data()

    assert len(data) == 2
    assert len(data.columns) == 5
    assert data["y4"].tolist() == [4, 5]


def test_load_ideal_data(sample_csv_files):
    """Tests loading the ideal data from a temporary CSV."""
    handler = DataHandler(sample_csv_files["ideal"])
    data = handler.load_data()

    assert len(data) == 2
    assert len(data.columns) == 3


def test_load_test_data(sample_csv_files):
    """Tests loading test data from a temporary CSV."""
    handler = DataHandler(sample_csv_files["test"])
    data = handler.load_data()

    assert len(data) == 2
    assert len(data.columns) == 2


def test_missing_file():
    """Tests that a missing CSV file raises FileNotFoundError."""
    handler = DataHandler("missing.csv")
    with pytest.raises(FileNotFoundError):
        handler.load_data()


def test_validate_training_columns(sample_csv_files):
    """Tests validation of the required training columns."""
    handler = TrainingDataHandler(sample_csv_files["train"])
    handler.load_data()
    handler.validate_columns()


def test_missing_training_column(sample_csv_files):
    """Tests that a missing training column raises an exception."""
    handler = TrainingDataHandler(sample_csv_files["train"])
    handler.load_data()
    handler.data = handler.data.drop(columns=["y4"])

    with pytest.raises(MissingTrainingColumnError):
        handler.validate_columns()


def test_validation_without_loading_data():
    """Checks validation fails when data has not been loaded."""
    handler = TrainingDataHandler("example.csv")

    with pytest.raises(ValueError, match="Load the CSV"):
        handler.validate_columns()


def test_missing_test_y_column(tmp_path):
    """Check that a missing test y column raises ValueError."""

    csv_file = tmp_path / "sample_test.csv"
    csv_file.write_text("x\n1\n2\n", encoding="utf-8")

    handler = TestDataHandler(str(csv_file))
    handler.load_data()

    with pytest.raises(ValueError, match="Missing test column: y"):
        handler.validate_columns()
