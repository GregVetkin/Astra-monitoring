import psycopg2


class ConnectToDatabase:
    """
    Creating a database class. \n
    Database options are specified as class arguments. \n

    Keys: \n
    ---- \n
    server: 'localhost' \n
    database: 'postgres' \n
    port: '5432' \n
    username: 'postgres' \n
    password: '' \n
    """
    def __init__(self, server='localhost', database='postgres', port='5432', username='postgres', password=''):
        """
        Creating a database class. \n
        Database options are specified as class arguments. \n

        :param server: IP database machine address
        :param database: database name
        :param port: working port
        :param username: user name
        :param password: database password
        """
        self.server = server
        self.database = database
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

# ======================================================================================================================

    def connect(self):
        """
        Database connection function
        """
        self.connection = psycopg2.connect(
            database=self.database,
            user=self.username,
            password=self.password,
            host=self.server,
            port=self.port
        )

# ======================================================================================================================

    def get_all(self, table_name: str):
        """
        Get all data from a table. \n

        :param table_name: target table name
        :return: list with tuples as rows
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            query = "SELECT * FROM "+table_name+" ORDER BY ID;"
            cursor.execute(query)
            result = cursor.fetchall()

        except Exception as err:
            print("Error get_all:")
            print(err)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
            return result

# ======================================================================================================================

    def write_query(self, query: str):
        """
        Submit a query to the database. \n
        The query must be of the string type and fully comply with the PostgreSQL syntax. \n

        :param query: database query
        :return: None
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()

        except Exception as err:
            print("Error write_query:")
            print(err)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

# ======================================================================================================================

    def read_query(self, query: str):
        """
        Get information from the database on request. \n
        The query must be of the string type and fully comply with the PostgreSQL syntax. \n

        :param query: database query
        :return: list
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

        except Exception as err:
            print("Error read_query:")
            print(err)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
            return result

# ======================================================================================================================

    def truncate_table(self, table_name: str):
        """
        !!!WARNING!!! \n
        Completely clears all data in the selected table. \n

        :param table_name: target table name
        :return: None
        """
        try:
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute("TRUNCATE "+table_name+";")
            self.connection.commit()

        except Exception as err:
            print("Error truncate_table")
            print(err)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()

# ======================================================================================================================

    def column_names(self, table_name: str):
        """
        Returns a list with the names of the columns of the target table. \n

        :param table_name: target table name
        :return: list of column names in order
        """

        try:
            name_list = []
            self.connect()
            cursor = self.connection.cursor()
            cursor.execute(f"""SELECT column_name FROM information_schema.columns 
                               WHERE table_name = '{table_name}' ORDER BY ordinal_position;""")
            result = cursor.fetchall()
            for columm in result:
                name_list.append(columm[0])

        except Exception as err:
            print("Error column_names:")
            print(err)

        finally:
            if self.connection:
                cursor.close()
                self.connection.close()
            return name_list

# ======================================================================================================================

