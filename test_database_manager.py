import pytest
from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from database_manager import DatabaseManager
from sqlalchemy import create_engine, inspect
import pandas as pd
from sqlalchemy.exc import IntegrityError


def test_database_connection_failure():
    manager = DatabaseManager()

    manager.engine = Mock()
    manager.engine.connect.side_effect = SQLAlchemyError("Simulated connection failure")

    with pytest.raises(RuntimeError, match="Could not connect"):
        manager.check_connection()

def test_mapping_primary_key():
    manager = DatabaseManager()

    manager.engine = create_engine("sqlite:///:memory:")
    manager.metadata.create_all(manager.engine)

    inspector = inspect(manager.engine)
    primary_key = inspector.get_pk_constraint("test_mapping")

    assert primary_key["constrained_columns"] == ["test_row_id"]

def test_mapping_data_saved():
    manager = DatabaseManager()
    manager.engine = create_engine("sqlite:///:memory:")
    manager.metadata.create_all(manager.engine)

    data = pd.DataFrame({"x": [1.0], "y": [5.0], "deviation": [0.2], "ideal_function": ["y13"], "test_row_id": [1]})

    data.to_sql("test_mapping", manager.engine, if_exists="append", index=False)

    saved = pd.read_sql_query("SELECT * FROM test_mapping", manager.engine)

    assert len(saved) == 1
    assert saved["ideal_function"].iloc[0] == "y13"

def test_duplicate_prmary_key():
    manager = DatabaseManager()
    manager.engine = create_engine("sqlite:///:memory:")
    manager.metadata.create_all(manager.engine)

    data = pd.DataFrame({"x": [1.0], "y": [5.0], "deviation": [0.2], "ideal_function": ["y13"], "test_row_id": [1]})
    data.to_sql("test_mapping", manager.engine, if_exists="append", index=False)

    with pytest.raises(pd.errors.DatabaseError, match="UNIQUE constraint failed"):
        data.to_sql("test_mapping", manager.engine, if_exists="append", index=False)

    




