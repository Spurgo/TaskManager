import streamlit as st
from pymongo import MongoClient
from TaskManager import TaskManager as TM
from datetime import time, datetime, date
from bson import ObjectId

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

today_todo, search_todo, future_todo = st.tabs(["Today's TODO", "Search TODOs", "Future's TODO"])

with today_todo:
    st.header("Today's TODO")

    field = st.text_input("Field:", key="today_field")
    what_todo = st.text_input("Task:", key="today_task")
    completed = False

    if st.button("Save Task", key="today_save_button"):
        if not field or not what_todo:
            st.error("Compila tutti i campi")
            st.stop() #?

        today = date.today()

        task_dict = {'Field': field, 'What_TODO': what_todo, 'Completed': completed, 'Creation_Date': datetime.combine(date.today(), time.min)}

        result = task_manager.add_task(task_dict)

        if result:
            st.success("Task aggiunta con successo")
        else:
            st.error("Errore durante l'inserimento nel database")

    task_today = task_manager.get_tasksby_date(date.today())
    
    st.markdown("---")

    for task in task_today:
        field = task.get('Field', 'N/A')
        todo = task.get('What_TODO', 'Nessuna Descrizione')
        data_creazione = task.get('Creation_Date', 'Data sconosciuta')
        task_status = task.get('Completed')
        task_id = task.get("_id")

        title = f"**[{field}]**"

        with st.expander(title):
            st.markdown(f"**Argument:** `{todo}`")
            st.markdown(f"**Status:** `{'DONE' if task_status else 'PENDING'}`")
            
            if isinstance(data_creazione, datetime):
                st.caption(f"Added: {data_creazione.strftime('%d/%m/%Y')}")
                if not task_status:                    
                    st.button("Mark as completed", key=f"completed_button_{task_id}", on_click=task_manager.update_task_status, args=(task_id, True))
            else:
                st.caption(f"Added: {data_creazione}")
        


with search_todo:
    st.header("Search TODOs")
    date_to_search = st.date_input("Search for date:")

    if st.button("Search", key="search_past"):
        if not date_to_search:
            st.error("insert a date for search")
            st.stop

        task_today = task_manager.get_tasksby_date(date_to_search)
        st.markdown("---")
        
        for task in task_today:
            field = task.get('Field', 'N/A')
            todo = task.get('What_TODO', 'Nessuna Descrizione')
            data_creazione = task.get('Creation_Date', 'Data sconosciuta')

            title = f"**[{field}]**"
            
            with st.expander(title):
                st.markdown(f"**Argument:** `{todo}`")
                
                if isinstance(data_creazione, datetime):
                    st.caption(f"Added: {data_creazione.strftime('%d/%m/%Y')}")
                    st.button("Mark as Complete")
                else:
                    st.caption(f"Added: {data_creazione}")

with future_todo:
    st.header("Future's TODO")

    field = st.text_input("Field:", key="future_field")
    hours = st.text_input("Hours you want to dedicate:", key="future_hours")
    what_todo = st.text_input("Task:", key="future_task")
    when_todo = st.date_input("Due date:", key="future_date")

    if st.button("Save Task"):
        if not field or not hours or not what_todo or not when_todo:
            st.error("Compila tutti i campi")
            st.stop() #?

        try:
            hours_val = float(hours)
        except ValueError:
            st.error("Il campo Hours dev'essere un numero")
            st.stop()
        

        task_dict = {'Field': field, 'Hours': hours_val, 'What_TODO': what_todo, 'Creation_Date': datetime.combine(when_todo, time.min)}

        result = task_manager.add_task(task_dict)

        if result:
            st.success("Task aggiunta con successo")
        else:
            st.error("Errore durante l'inserimento nel database")


