import os
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import CreateTable
from sqlalchemy.sql.sqltypes import NullType
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
MYSQL_URL = os.getenv("MYSQL_URL")
POSTGRES_URL = os.getenv("POSTGRES_URL")

# Create engines and sessions
source_engine = create_engine(MYSQL_URL)
target_engine = create_engine(POSTGRES_URL)
SourceSession = sessionmaker(bind=source_engine)
TargetSession = sessionmaker(bind=target_engine)
source_session = SourceSession()
target_session = TargetSession()

# Reflect tables
source_metadata = MetaData()
source_metadata.reflect(bind=source_engine)
target_metadata = MetaData()
target_metadata.reflect(bind=target_engine)

# Extract database types from the URLs
source_db_type = "MySQL" if "mysql" in MYSQL_URL else "Unknown"
target_db_type = "PostgreSQL" if "postgresql" in POSTGRES_URL else "Unknown"

# Updated print statement
print(f"Starting data migration from source database ({source_db_type}) to the target database ({target_db_type})...")

# Loop through all tables in the source database
for table_name, source_table in source_metadata.tables.items():
    # Skip if the table already exists in the target database
    if table_name in target_metadata.tables:
        print(f"Table {table_name} already exists in {target_db_type}. Skipping.")
        continue

    print(f"Migrating table: {table_name}")

    # Create the table in the target database
    target_columns = [
        Column(column.name, column.type if column.type is not None else NullType(), primary_key=column.primary_key)
        for column in source_table.columns
    ]
    target_table = Table(table_name, target_metadata, *target_columns)
    target_table.create(target_engine)

    # Fetch data from the source table
    rows = source_session.execute(source_table.select()).fetchall()

    # Insert data into the target table
    for row in rows:
        insert_data = {column.name: row._mapping[column.name] for column in source_table.columns}
        target_session.execute(target_table.insert().values(**insert_data))

    # Commit the transaction
    target_session.commit()

print("Data migration completed successfully!")

# Close sessions
source_session.close()
target_session.close()