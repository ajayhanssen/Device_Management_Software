import streamlit as st
from tinydb import TinyDB, Query
import pandas as pd
import numpy as np
#from classes import User, Reservation, MTN_Plan, Device

class Device():
    def __init__(self, name) -> None:
        self.name = name

class User():
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id

# Open the TinyDB database
device_db = TinyDB('device_db.json')
user_db = TinyDB('user_db.json')
# Load existing devices from the database
devices = [Device(**entry.get('device', {})) for entry in device_db.all()]
users = [User(**entry.get('user', {})) for entry in user_db.all()]

st.set_page_config(layout="wide")
st.write("# Gerätemanagement")

#users = [User("Hannes", 1), User("Max", 2), User("Moritz", 3)]

col1, col2 = st.columns([0.6, 0.4])

def delete_user(id):
    user_db = TinyDB('user_db.json')
    for user in users:
        if user.id == id:
            Users = Query()
            user_db.remove(Users.user.id == id)
            user_db.close()


def add_user(user_name, user_id):
    new_user = User(new_name, new_id)
    user_db = TinyDB('user_db.json')
    user_db.insert({'user': new_user.__dict__})
    user_db.close()

with col1:
    tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Wartung"])

    with tab1:
        st.header("Geräteverwaltung")
        st.write("Übersicht aller registrierten Geräte")
        selectbox_options_dev = [device.name for device in devices]

        a = st.empty()

        currentdevice = a.selectbox('Gerät auswählen', options=selectbox_options_dev)

        for device in devices:
            if device.name == currentdevice:
                selected_device = device                

        # Gerätinformationen darstellen
        container = st.container(border=True)
        with container:
            attribute, value = st.columns(2)
            with attribute:           
                st.write("Gerätename: ")
                st.write("Gerätenummer: ")
                st.write("Verantwortlicher: ")
                st.write("Anschaffungsdatum: ")

            with value:
                st.write(selected_device.name)
                st.write("123456789")      
        
            
        # Neues Gerät hinzufügen
            
        with st.expander("Neues Gerät hinzufügen"):
            new_name = st.text_input("Gerätename")
            if st.button("Hinzufügen"):
                if any(device.name == new_name for device in devices):
                    st.warning("Gerät bereits vorhanden!")
                else:
                    st.write("Gerät hinzugefügt")
                    new_device = Device(new_name)
                    devices.append(new_device)
                    selectbox_options_dev = [device.name for device in devices]
                    currentdevice = a.selectbox('Gerät auswählen', options=selectbox_options_dev)

    with tab2:
        st.header("Nutzerverwaltung")
        st.write("Übersicht aller registrierten Benutzer")
        for user in users:
            col3, col4, col5 = st.columns([0.8, 0.1, 0.1])
            with col3:
                cont = st.container(border=True)
                with cont:
                    st.write(user.name)
            with col4:
                st.button("Editieren", key=f"edit-btn-{user.id}")
            with col5:
                st.button("Löschen", key=f"delete-btn-{user.id}", on_click=delete_user, args=[user.id])

        #Neuen Nutzer hinzufügen
        with st.expander("Neuen Nutzer hinzufügen"):
            new_name = st.text_input("Nutzername")
            new_id = st.text_input("Nutzer-ID")
            if st.button("Hinzufügen", key="add-user", on_click=add_user, args=[new_name, new_id]):
                if any(user.name == new_name for user in users):
                    st.warning("User bereits vorhanden!")
                else:
                    st.write("User hinzugefügt")


    with tab3:
        st.header("Wartungsplanung")

with col2:
    st.write("Chat-Bot beta")
    #st.toggle("Chat aktivieren")
    with st.chat_message("assistant"):
        st.write("Hello, how can I assist you today?")
    with st.chat_message("user"):
        st.write("who is hannes unterhuber?")
    with st.chat_message("assistant"):
        st.write("For more information, please see [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ).")


# Clear the current entries in the database
device_db.truncate()
user_db.truncate()

# Save devices to the database
device_db.insert_multiple({'device': device.__dict__} for device in devices)
print(users)
user_db.insert_multiple({'user': user.__dict__} for user in users)

# Close the database connection
device_db.close()
user_db.close()