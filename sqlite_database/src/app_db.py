import sqlite3

def initialize_database(db_name='database.db'):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            time TEXT,
            img_raw BLOB,
            img_detect BLOB,
            defect TEXT,
            barcode TEXT
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize_database()