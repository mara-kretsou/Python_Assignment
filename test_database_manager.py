"""Unit tests for SQLite database management and operations."""

import pytest
from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from database_manager import DatabaseManager
from sqlalchemy import create_engine, inspect
import pandas as pd
from sqlalchemy.exc import IntegrityError


def test_database_connection_failure():
    """Check that a database connection failure is handled."""
    manager = DatabaseManager()

    manager.engine = Mock()
    manager.engine.connect.side_effect = SQLAlchemyError("Simulated connection failure")

    with pytest.raises(RuntimeError, match="Could not connect"):
        manager.check_connection()


def test_mapping_table_has_four_columns():
    """Check that mapping table contains exactly four columns."""
    manager = DatabaseManager()

    manager.engine = create_engine("sqlite:///:memory:")
    manager.reset_mapping_table()

    inspector = inspect(manager.engine)
    columns = [column["name"] for column in inspector.get_columns("test_mapping")]

    assert columns == ["x", "y", "deviation", "ideal_function"]


def test_mapping_data_saved():
    """Check that mapping data is correctly saved in SQLite."""
    manager = DatabaseManager()
    manager.engine = create_engine("sqlite:///:memory:")
    manager.reset_mapping_table()

    data = pd.DataFrame(
        {"x": [1.0], "y": [5.0], "deviation": [0.2], "ideal_function": ["y13"]}
    )

    data.to_sql("test_mapping", manager.engine, if_exists="append", index=False)

    saved = pd.read_sql_query("SELECT * FROM test_mapping", manager.engine)

    assert len(saved) == 1
    assert saved["ideal_function"].iloc[0] == "y13"


def test_reset_mapping_table_clears_data():
    """Check that resetting the mapping table removes existing records."""
    manager = DatabaseManager()
    manager.engine = create_engine("sqlite:///:memory:")
    manager.reset_mapping_table()

    data = pd.DataFrame(
        {"x": [1.0], "y": [5.0], "deviation": [0.2], "ideal_function": ["y13"]}
    )
    data.to_sql("test_mapping", manager.engine, if_exists="append", index=False)

    manager.reset_mapping_table()

    saved = pd.read_sql_query("SELECT * FROM test_mapping", manager.engine)

    assert len(saved) == 0
