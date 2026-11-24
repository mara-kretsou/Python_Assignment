"""Manage the SQLite database using SQLAlchemy."""

from sqlalchemy import create_engine, MetaData, Table, Column, Float, String, Integer
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:
    def __init__(self):
        """Initialize the SQLite engine and table metadata."""
        self.engine = create_engine("sqlite:///assignment.db")
        self.metadata = MetaData()
        self.test_mapping_table = Table("test_mapping", self.metadata, Column("x", Float), Column("y", Float), Column("deviation", Float), Column("ideal_function", String), Column("test_row_id", Integer, primary_key=True))


    def reset_mapping_table(self):
        """Drop and recreate the mapping table, deleting existing records."""
        self.test_mapping_table.drop(self.engine, checkfirst=True)
        self.metadata.create_all(self.engine)

    def check_connection(self):
        """
        Check whether the database connection works.

        Raises:
           RuntimeError: If the database connection fails.
        """
        try:
            with self.engine.connect():
                pass
        except SQLAlchemyError as error:
            raise RuntimeError("Could not connect to the database.") from error
        
        