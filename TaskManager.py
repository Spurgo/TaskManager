from pymongo import MongoClient
from datetime import time, datetime, date, timedelta

class TaskManager:
    def __init__(self):
        url = "mongodb://localhost:27017"
        
        try:
            self.client = MongoClient(url)
            self.client.admin.command('ping')
            print("connessione al database avvenuta con successo")
        except Exception as e:
            print(f"Errore di connessione al database MongoDB: {e}")
            raise

        self.db = self.client["TODO_DB"]
        self.task_collection = self.db["tasks"]
        self.task_collection.create_index([("Creation_Date", 1)], name= "creation_date_index", unique= False) #index per velocizzare query
        print("Indice creato su 'Creation_Date'")

    def add_task(self, task_info: dict):
        try:
            result = self.task_collection.insert_one(task_info)
            print("inserimento dati avvenuto con successo")
            return result
        except Exception as e:
            print(f"Errore inserimento dati all'interno del database: {e}")
            return None
        
    def get_tasksby_date(self, target_day):
        #necessario calcolare l'inizio del giorno target (mezzanotte)
        start_of_day = datetime.combine(target_day, time.min)

        start_next_day = start_of_day + timedelta(days=1)

        query = {
            "Creation_Date":{
                "$gte": start_of_day,
                "$lt" : start_next_day
            }
        }

        try:
            cursor = self.task_collection.find(query)
            return list(cursor)
        except Exception as e:
            print(f"Errore durante la query: {e}")
            return []