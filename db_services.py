import pyodbc

class DBServices:
    def __init__(self):
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-ENHKM1F\SQLEXPRESS;'
            r'DATABASE=LinkedIn-Job-Scraping-bot;'
            r'Trusted_Connection=yes;'
        )

    def save_to_sqlserver(self, job_data):
        if job_data is not None:
            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            # Drop and recreate table if schema changed (column count or names)
            table_check_sql = '''
                SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Linkedin_Jobdata'
            '''
            cursor.execute(table_check_sql)
            columns = [row[0] for row in cursor.fetchall()]
            expected_columns = [
                'Id', 'Title', 'Company', 'Location', 'Last_Posting_Date', 'Link', 'Requirements'
            ]
            if set(columns) != set(expected_columns):
                cursor.execute('''
                    IF OBJECT_ID('Linkedin_Jobdata', 'U') IS NOT NULL
                        DROP TABLE Linkedin_Jobdata
                ''')
                conn.commit()
            # Create table if not exists
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Linkedin_Jobdata' AND xtype='U')
                CREATE TABLE Linkedin_Jobdata (
                    Id INT IDENTITY(1,1) PRIMARY KEY,
                    Title NVARCHAR(255),
                    Company NVARCHAR(255),
                    Location NVARCHAR(255),
                    Last_Posting_Date NVARCHAR(50),
                    Link NVARCHAR(500),
                    Requirements NVARCHAR(MAX)
                )
            ''')
            conn.commit()
            # Insert data
            for _, row in job_data.iterrows():
                cursor.execute('''
                    INSERT INTO Linkedin_Jobdata (Title, Company, Location, Last_Posting_Date, Link, Requirements)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', row['Title'], row['Company'], row['Location'], row['Last_Posting_Date'], row['Link'], row.get('Requirements', ''))
            conn.commit()
            cursor.close()
            conn.close()
