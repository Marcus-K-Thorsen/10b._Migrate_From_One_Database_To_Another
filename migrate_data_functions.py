from sqlalchemy import create_engine, MetaData, Table, Column
from typing import Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import NullType, Float


class SQLDatabase():
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)()
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)


def adapt_column_for_target(source_column: Column[Any]) -> Column[Any]:
    """
    Simplify column adaptation for the target database.

    Args:
        source_column (Column): The source column to adapt.

    Returns:
        Column: The adapted column for the target database.
    """
    column_type = source_column.type or NullType()

    # Handle Float type for PostgreSQL
    if isinstance(column_type, Float):
        column_type = Float(asdecimal=False)  # Ensure compatibility with PostgreSQL

    # Return the adapted column
    return Column(
        source_column.name,
        column_type,
        primary_key=source_column.primary_key,
        nullable=source_column.nullable,
        default=source_column.default,
        autoincrement=source_column.autoincrement,
    )

def insert_data_into_table(source_table: Table, target_table: Table, source_db: SQLDatabase, target_db: SQLDatabase) -> None:
    """
    Insert data from the source table into the target table.

    Args:
        source_table (Table): The source table to fetch data from.
        target_table (Table): The target table to insert data into.
        source_db (SQLDatabase): The source database object.
        target_db (SQLDatabase): The target database object.
    """
    # Fetch data from the source table
    rows = source_db.session.execute(source_table.select()).fetchall()

    # Prepare and insert rows into the target table
    for row in rows:
        insert_data = {}
        source_columns = source_table.columns
        for column in source_columns:
            column_name = column.name
            insert_data[column_name] = row._mapping[column_name]
        
        target_db.session.execute(target_table.insert().values(**insert_data))

    # Commit the transaction
    target_db.session.commit()
    print(f"Inserted {len(rows)} rows into target table: {target_table.name}")


def migrate_table(table_name: str, source_db: SQLDatabase, target_db: SQLDatabase) -> None:
    """
    Migrate a single table from the source database to the target database.

    Args:
        table_name (str): The name of the table to migrate.
        source_db (SQLDatabase): The source database object.
        target_db (SQLDatabase): The target database object.
    """
    source_table = source_db.metadata.tables[table_name]
    print(f"Migrating table: {table_name}")

    # Create the table in the target database
    target_columns = []
    for column in source_table.columns:
        adapted_column = adapt_column_for_target(column)
        target_columns.append(adapted_column)

    target_table = Table(table_name, target_db.metadata, *target_columns)
    target_table.create(target_db.engine)

    # Insert data into the target table
    insert_data_into_table(source_table, target_table, source_db, target_db)
