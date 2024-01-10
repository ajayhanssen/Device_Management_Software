import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from classes import User, Reservation, MTN_Plan, Device
import json
st.set_page_config(layout="wide", page_title="Gerätemanagement", page_icon=":video_game:")

# Placeholder classes
"""
class Device():
    def __init__(self, name) -> None:
        self.name = name
        self.user = None

class User():
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
"""

 

st.write("# Gerätemanagement")

users = [User(name="Andreas", id="mr.rioes@gmail.com"), User(name="Hannes", id="kompl_kek@yahoo.at"), User(name="Samuel", id="fortn_battlepass@outlook.com")]
users_dict = {user.name: user for user in users}
devices = [Device(name="Nintendo Switch", res_usr=users_dict["Andreas"], id=12345), Device(name="Among Us", res_usr=users_dict["Hannes"]), Device(name="Pro Controller (Luigi Edition)")]
devices_dict = {device.name: device for device in devices}
devices_dict["Nintendo Switch"].reservations = [Reservation(res_start=datetime(2021, 10, 1), res_end=datetime(2021, 10, 5), res_usr=users_dict["Andreas"]), Reservation(res_start=datetime(2021, 10, 10), res_end=datetime(2021, 10, 15), res_usr=users_dict["Hannes"])]


col1, col2 = st.columns([0.6, 0.4])

with col1:
    tab1, tab2, tab3, tab4 = st.tabs(["Geräte", "Nutzer", "Wartung", "Reservierungen"])
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
            """
            attribute, value = st.columns(2)
            with attribute:           
                st.write("Gerätename: ")
                st.write("Gerätenummer: ")
                st.write("Verantwortlicher: ")
                st.write("Anschaffungsdatum: ")

            with value:
                st.write(selected_device.name)
                st.write(selected_device.id)
                if selected_device.res_usr is None:
                    st.write("Kein Verantwortlicher")
                else:
                    st.write(F"{selected_device.res_usr.name} ({selected_device.res_usr.id})")
                st.write(datetime.now().strftime("%d.%m.%Y"))
            """
            dev_attributes = pd.DataFrame(columns=["Gerätenummer", "Verantwortlicher", "Anschaffungsdatum"])
            dev_attributes.loc[len(dev_attributes.index)] = [
            selected_device.id, selected_device.res_usr.name if selected_device.res_usr is not None else "Kein Verantwortlicher", datetime.now().strftime("%d.%m.%Y")]
            st.dataframe(dev_attributes, use_container_width=True, hide_index=True)

            # Gerät bearbeiten
            with st.expander("Gerät bearbeiten"):
                new_name = st.text_input("Gerätename", key="edit_name_device", placeholder="Name eingeben", value=selected_device.name)
                new_id = st.text_input("Gerätenummer", key="edit_id_device", placeholder="Nummer eingeben", value=selected_device.id)
                new_user = st.selectbox("Verantwortlicher", options=[user.name for user in users], key="selectbox_edit_device_user", index=None, placeholder="Verantwortlichen auswählen")
                new_date = st.date_input("Anschaffungsdatum", key="edit_date_device")
                if st.button("Speichern", key="edit_device"):
                    st.success("Änderungen gespeichert")
        
        # Neues Gerät hinzufügen
        with st.expander("Neues Gerät hinzufügen"):
            new_name = st.text_input("Gerätename", key="name_new_device")
            new_id = st.text_input("Gerätenummer", key="id_new_device")
            new_user = st.selectbox("Verantwortlicher", options=[user.name for user in users], key="selectbox_new_device_user", index=None, placeholder="Verantwortlichen auswählen")
            new_date = st.date_input("Anschaffungsdatum", key="date_new_device")

            if st.button("Hinzufügen", key="add_device"):
                if any(str(device.id) == new_id for device in devices):
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
                    
            with col4:
                st.button("Editieren", key=F"edit_user_{user.id}")
            with col5:
                st.button("Löschen", key=F"delete_user_{user.id}")

        #Neuen Nutzer hinzufügen
        with st.expander("Neuen Nutzer hinzufügen"):
            new_name = st.text_input("Nutzername", key="new_name", placeholder="Name eingeben")
            new_id = st.text_input("Nutzer-ID", key="new_id", placeholder="ID eingeben")
            if st.button("Hinzufügen", key="add_user"):
                if any(user.name == new_name for user in users):
                    st.warning("User bereits vorhanden!")
                else:
                    st.success("User hinzugefügt")


    with tab3:
        st.header("Wartungsplanung", divider="red")
        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices], key="mtn_selectbox_device", index=None, placeholder="Gerät auswählen")
        
        #testdaten für wartungsplan
        devices_dict["Nintendo Switch"].MTN=MTN_Plan(mtn_int=30, first_mtn=datetime(2021, 10, 1), mtn_cost=420.69, last_mtn=datetime(2021, 10, 1), creation_d=datetime(2021, 10, 1), end_of_life=datetime(2024, 10, 1))  
        
        if sel_dev != None: 
            sel_dev = devices_dict[sel_dev]
            if sel_dev.MTN is None:
                st.write("Kein Wartungsplan vorhanden")
                #mtn hinzufügen
                st.expander("Neuen Wartungsplan hinzufügen")
            else:
                st.write("Wartungsplan vorhanden")
                st.write("Erstellungsdatum:", sel_dev.MTN.creation_d.strftime("%d.%m.%Y"))
                st.write("Erste Instandhaltung:", sel_dev.MTN.first_mtn.strftime("%d.%m.%Y"))
                st.write("Letzte Instandhaltung:", sel_dev.MTN.last_mtn.strftime("%d.%m.%Y"))
                st.write("Kosten der Instandhaltung:", sel_dev.MTN.mtn_cost)
                st.write("Intervall der Instandhaltung:", sel_dev.MTN.mtn_int)
                st.write("Ende der Lebensdauer:", sel_dev.MTN.end_of_life.strftime("%d.%m.%Y"))

            with st.expander("Neuen Wartungsplan hinzufügen"):
                new_start = st.date_input("Anschaffungsdatum", key="new_mtn_start")
                new_end = st.date_input("Ende der Instandhaltung", key="new_mtn_end")
                new_interval = st.number_input("Intervall (Tage)", key="new_mtn_interval", min_value=1, value=1)
                if st.button("Hinzufügen", key="add_mtn_plan"):
                    if new_start > new_end:
                        st.warning("Startdatum muss vor Enddatum liegen!")
                    else:
                        st.success("Wartungsplan hinzugefügt")
                        new_mtn_plan = MTN_Plan(new_start, new_end, new_interval)
                        sel_dev.mtn_plan = new_mtn_plan
                        st.write(sel_dev.mtn_plan.mtn_start)
                        st.write(sel_dev.mtn_plan.mtn_end)
                        st.write(sel_dev.mtn_plan.mtn_interval)
                        st.write(sel_dev.mtn_plan.mtn_last)
    
    with tab4:
        st.header("Reservierungssystem", divider="red")

        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices], key="selectbox_device", index=None, placeholder="Gerät auswählen")
        if sel_dev != None:
            current_reservations=pd.DataFrame(columns=["Nutzer", "Start", "Ende"])
            sel_dev = devices_dict[sel_dev]
            if sel_dev.reservations != []:
                for reservation in sel_dev.reservations:
                    current_reservations.loc[len(current_reservations.index)] = [reservation.res_usr.name, reservation.res_start, reservation.res_end]
            # Check if the device has reservations
                
            st.dataframe(current_reservations, use_container_width=True)
        
        # Neue Reservierung hinzufügen
            with st.expander("Neue Reservierung hinzufügen"):
                start_date = st.date_input("Startdatum", key="new_res_start_date")
                start_time = st.time_input("Startzeit", key="new_res_start_time")
                end_date = st.date_input("Enddatum", key="new_res_end_date")
                end_time = st.time_input("Endzeit", key="new_res_end_time")
                if st.button("Reservieren", key="add_reservation"):
                    if start_date > end_date:
                        st.warning("Startdatum muss vor Enddatum liegen!")
                    else:
                        if start_time > end_time:
                            st.warning("Startzeit muss vor Endzeit liegen!")
                        else:
                            st.success("Reservierung hinzugefügt")
                #st.warning("gewählter Zeitraum nicht mehr verfügbar"")
            

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
        st.write("For more information, please see [here](https://t.ly/IIYqF).")

# This ocmmand can rerun the script (DB-Reload?)
#st.rerun()
                    