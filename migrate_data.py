import os
from dotenv import load_dotenv
from migrate_data_functions import SQLDatabase, migrate_table


def run_migration(source_db_url: str, target_db_url: str) -> None:
    """
    Run the migration from source database to target database.
    
    Args:
        source_db_url (str): The URL of the source database.
        target_db_url (str): The URL of the target database.
    """
    try:
        if not isinstance(source_db_url, str) or not isinstance(target_db_url, str):
            raise ValueError("Database URLs must be strings.")
        # Extract database types from the URLs
        source_db_type = "MySQL" if "mysql" in MYSQL_URL else "Unknown"
        target_db_type = "PostgreSQL" if "postgresql" in POSTGRES_URL else "Unknown"

        print(f"Starting data migration from source database ({source_db_type}) to the target database ({target_db_type})...")
        
        source_db = SQLDatabase(source_db_url)
        target_db = SQLDatabase(target_db_url)
        
        # Migrate tables in the correct order
        table_order = ["alembic_version", "accounts", "transactions"]  # Ensure accounts is migrated before transactions
        for table_name in table_order:
            if table_name in source_db.metadata.tables:
                migrate_table(table_name, source_db, target_db)

        print("Data migration completed successfully!")

        # Close sessions
        source_db.session.close()
        target_db.session.close()
    
    except Exception as e:
        print(f"Error during migration setup: {e}")
        return


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Get database URLs from environment variables
    MYSQL_URL = os.getenv("MYSQL_URL")
    POSTGRES_URL = os.getenv("POSTGRES_URL")
    
    source_db_url=MYSQL_URL
    target_db_url=POSTGRES_URL
    
    run_migration(
        source_db_url, 
        target_db_url
    )