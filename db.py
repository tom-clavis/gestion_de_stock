import mysql.connector

class DatabaseHandler:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, data=None):
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête : {str(e)}")
            return False

    def fetch_data(self, query, data=None):
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {str(e)}")
            return []

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
