import sqlite3


import os

def remove_sqlite_database(database_file_path):
    """
    Removes an SQLite3 database file.

    Args:
        database_file_path (str): The path to the SQLite3 database file.
    """
    if os.path.exists(database_file_path):
        try:
            os.remove(database_file_path)
            print(f"Database file '{database_file_path}' removed successfully.")
        except OSError as e:
            print(f"Error removing database file '{database_file_path}': {e}")
    else:
        print(f"Database file '{database_file_path}' does not exist.")



def execute_sql_file(db_path, sql_filepath):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(sql_filepath, 'r') as file:
            sql_script = file.read()

        sql_commands = sql_script.split(';')

        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                    conn.commit()
                    print(f"Executed: {command.strip()[:50]}...")
                except sqlite3.Error as e:
                    print(f"Error executing command: {command.strip()[:50]}... - {e}")
                    conn.rollback() # Rollback on error

    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()

def main():
    # Remove existing database if it exists
    database_name = 'soil_health_reco.db'
    remove_sqlite_database(database_name)

    #database is created in first usage, i.e at the time of connection creation
    
    # Drop and recreate tables by executing SQL files
    sql_files = ['drop_all_tables.sql', 'soil_health_card_schema.sql',   'gen_sample_sahayaks.sql', 'gen_sample_farmers.sql', 'crop_requirements_data.sql', 'gen_soil_sample.sql', 'gen_sample_land_parcels.sql']
    for sql_file in sql_files:
        execute_sql_file(database_name, sql_file)


if __name__ == "__main__":
    main()  