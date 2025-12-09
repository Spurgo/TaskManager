from pymongo import MongoClient
from datetime import time, datetime, date, timedelta
from bson import ObjectId

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
        
    def update_task_status(self, task_id, new_status):
        try:
            if isinstance(task_id, str):
                obj_id = ObjectId(task_id)
            else:
                obj_id = task_id
        except Exception:
            print(f"Errore: ID non valido: {task_id}")

        query = {
            "_id": obj_id
        }

        update = {
            "$set":{
                "Completed": new_status
            }
        }

        try:
            result = self.task_collection.update_one(query, update)
            if result.modified_count == 1:
                print(f"Task set to DONE")
                return True
            else:
                print(f"Errore durante aggiornamento status")
                return False
        except Exception as e:
            print(f"Errore durante l'aggiornamento del database: {e}")
            return False

        
            
