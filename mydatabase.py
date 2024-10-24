import mysql.connector


class DB:
    def __init__(self, **kwargs) -> None:
        self.mydb = mysql.connector.connect( host=kwargs["localhost"], user=kwargs["usr"], password=kwargs["pas"])
    
    def print_db(self):
        print(self.mydb)