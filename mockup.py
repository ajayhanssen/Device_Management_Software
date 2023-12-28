import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Placeholder classes
class Device():
    def __init__(self, name) -> None:
        self.name = name
        self.user = None

class User():
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id

st.set_page_config(layout="wide")
st.write("# Gerätemanagement")

devices = [Device("Nintendo Switch"), Device("Among Us"), Device("Pro Controller (Luigi Edition)")]
users = [User("Andreas", "mr.rioes@gmail.com"), User("Hannes", "kompl_kek@yahoo.at"), User("Samuel", "fortn_battlepass@outlook.com")]

col1, col2 = st.columns([0.6, 0.4])

with col1:
    tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Wartung"])
    with tab1:
        st.header("Geräteverwaltung", divider="red")
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
                st.write(F"{users[0].name} ({users[0].id})")
                st.write(datetime.now().strftime("%d.%m.%Y"))
        
        with st.expander("Neues Gerät hinzufügen"):
            new_name = st.text_input("Gerätename")
            if st.button("Hinzufügen", key="add_device"):
                if any(device.name == new_name for device in devices):
                    st.warning("Gerät bereits vorhanden!")
                else:
                    st.success("Gerät hinzugefügt")
    
    with tab2:
        st.header("Nutzerverwaltung", divider="red")
        st.write("Übersicht aller registrierten Benutzer")
        for user in users:
            col3, col4, col5 = st.columns([0.8, 0.1, 0.1])
            with col3:
                cont = st.container(border=True)
                with cont:
                    st.write(F"{user.name} \t ({user.id})")
                    #st.markdown(F'<div style="text-align: right;">{user.id}</div>', unsafe_allow_html=True)
                    #st.write(user.id)
            with col4:
                st.button("Editieren", key=F"edit_user_{user.id}")
            with col5:
                st.button("Löschen", key=F"delete_user_{user.id}")

        #Neuen Nutzer hinzufügen
        with st.expander("Neuen Nutzer hinzufügen"):
            new_name = st.text_input("Nutzername", key="new_name")
            new_id = st.text_input("Nutzer-ID", key="new_id")
            if st.button("Hinzufügen", key="add_user"):
                if any(user.name == new_name for user in users):
                    st.warning("User bereits vorhanden!")
                else:
                    st.success("User hinzugefügt")


    with tab3:
        st.header("Wartungsplanung", divider="red")

with col2:
    st.header("Allgemeine Übersicht", divider="red")
    st.write("Hier werden allgemeine Informationen angezeigt.")
    general_overview = pd.DataFrame(np.random.randn(10, 5), columns=('a', 'b', 'c', 'd', 'e'))
    st.dataframe(general_overview, use_container_width=True)


    #st.write("Chat-Bot beta")
    #st.toggle("Chat aktivieren")
    with st.chat_message("assistant"):
        st.write("Hello, how can I assist you today?")
    with st.chat_message("user"):
        st.write("who is hannes unterhuber?")
    with st.chat_message("assistant"):
        st.write("For more information, please see [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ).")
                    