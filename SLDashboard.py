import streamlit as st
from pymongo import MongoClient
from TaskManager import TaskManager as TM
from datetime import time, datetime, date

@st.cache_resource
def Get_TaskManager():
    return TM()

task_manager = Get_TaskManager()

st.set_page_config(
    page_title="To-Do List",
    layout="wide",
    initial_sidebar_state="auto"
)

st.title("To-Do List")

today_todo, past_todo, future_todo, add_todo = st.tabs(["Today's TODO", "Past's TODO", "Future's TODO", "ADD TODO"])

with today_todo:
    st.header("Today's TODO")
    task_today = task_manager.get_tasksby_date(date.today())
    
    st.markdown("---")

    for task in task_today:
        field = task.get('Field', 'N/A')
        todo = task.get('What_TODO', 'Nessuna Descrizione')
        hours = task.get('Hours', 0)
        data_creazione = task.get('Creation_Date', 'Data sconosciuta')

        st.subheader(f"{field} - {todo}")

        st.write(f"Ore da dedicare: {hours}")

        if isinstance(data_creazione, datetime):
            st.caption(f"inserita il: {data_creazione.strftime('%d/%m/%Y')}")
        else:
            st.caption(f"Inserita il: {data_creazione}")

with past_todo:
    st.header("Past's TODO")

with future_todo:
    st.header("Future's TODO")

with add_todo:
    st.header("Add New TODO")

    field = st.text_input("Field:")
    hours = st.text_input("Hours you want to dedicate:")
    what_todo = st.text_input("Task:")

    if st.button("Save Task"):
        if not field or not hours or not what_todo:
            st.error("Compila tutti i campi")
            st.stop() #?

        try:
            hours_val = float(hours)
        except ValueError:
            st.error("Il campo Hours dev'essere un numero")
            st.stop()

        today = date.today()
        

        task_dict = {'Field': field, 'Hours': hours_val, 'What_TODO': what_todo, 'Creation_Date': datetime.combine(date.today(), time.min)}

        result = task_manager.add_task(task_dict)

        if result:
            st.success("Task aggiunta con successo")
        else:
            st.error("Errore durante l'inserimento nel database")
