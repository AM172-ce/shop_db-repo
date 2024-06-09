import psycopg2
import os


procedure_name = "load_all_tables"
database_url = os.environ.get('DATABASE_URL')

def run_stored_procedure(procedure_name, db_url):
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
    
        # Execute the stored procedure
        cursor.execute(f"CALL {procedure_name}()")
        
        # Commit the transaction
        conn.commit()
        print("Stored procedure executed successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error executing stored procedure:", error)
        
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

run_stored_procedure(procedure_name, database_url)
