import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from classes import User, Reservation, MTN_Plan, Device

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


# Testdaten für Reservierungen
devices_dict["Nintendo Switch"].add_reservation(Reservation(res_start=datetime(2024, 1, 17), res_end=datetime(2024, 1, 19), res_usr=users_dict["Andreas"]))
devices_dict["Nintendo Switch"].add_reservation(Reservation(res_start=datetime(2024, 3, 21), res_end=datetime(2024, 3, 22), res_usr=users_dict["Hannes"]))
devices_dict["Nintendo Switch"].add_reservation(Reservation(res_start=datetime(2024, 5, 25), res_end=datetime(2024, 5, 26), res_usr=users_dict["Samuel"]))

devices_dict["Among Us"].add_reservation(Reservation(res_start=datetime(2024, 1, 21), res_end=datetime(2024, 1, 22), res_usr=users_dict["Andreas"]))

col1, col2 = st.columns([0.6, 0.4])

with col1:
    tab1, tab2, tab3, tab4 = st.tabs(["Geräte", "Nutzer", "Wartung", "Reservierungen"])
    with tab1:
        st.header("Geräteverwaltung", divider="red")
        st.write("Übersicht aller registrierten Geräte")
        selectbox_options_dev = [device.name for device in devices]

        a = st.empty()

        currentdevice = a.selectbox('Gerät auswählen', options=selectbox_options_dev)

        selected_device = devices_dict[currentdevice]            

        # Gerätinformationen darstellen
        
        container = st.container(border=True)
        with container:
            
            dev_attributes = pd.DataFrame(columns=["Gerätenummer", "Verantwortlicher", "Anschaffungsdatum"])
            dev_attributes.loc[len(dev_attributes.index)] = [selected_device.id, selected_device.res_usr.name if selected_device.res_usr is not None
                                                             else "Kein Verantwortlicher", selected_device.get_creation_date().strftime("%d.%m.%Y")]
            # Dass die Kommas alle drei Nullen im Dataframe verschwinden:
            styled_dev_attr = dev_attributes.style.format({"Expense": lambda x : '{:.4f}'.format(x)})

            st.dataframe(styled_dev_attr, use_container_width=True, hide_index=True)

            # Gerät bearbeiten
            with st.expander("Gerät bearbeiten"):
                new_name = st.text_input("Gerätename", key="edit_name_device", placeholder="Name eingeben", value=selected_device.name)
                new_id = st.text_input("Gerätenummer", key="edit_id_device", placeholder="Nummer eingeben", value=selected_device.id)
                new_user = st.selectbox("Verantwortlicher", options=[user.name for user in users], key="selectbox_edit_device_user", index=None, placeholder="Verantwortlichen auswählen")
                #new_date = st.date_input("Anschaffungsdatum", key="edit_date_device")
                if st.button("Speichern", key="edit_device"):
                    st.success("Änderungen gespeichert")
        
        # Neues Gerät hinzufügen
        with st.expander("Neues Gerät hinzufügen"):
            new_name = st.text_input("Gerätename", key="name_new_device", placeholder="Name eingeben")
            new_id = st.text_input("Gerätenummer", key="id_new_device", placeholder="ID eingeben")
            new_user = st.selectbox("Verantwortlicher", options=[user.name for user in users], key="selectbox_new_device_user", index=None, placeholder="Verantwortlichen auswählen")
            #new_date = st.date_input("Anschaffungsdatum", key="date_new_device")

            if st.button("Hinzufügen", key="add_device"):
                if any(str(device.id) == new_id for device in devices):
                    st.warning("Gerät bereits vorhanden!")
                else:
                    st.success("Gerät hinzugefügt")
    
    with tab2:
        st.header("Nutzerverwaltung", divider="red")
        st.write("Übersicht aller registrierten Benutzer")

        for key in users_dict:
            with st.expander(F"{users_dict[key].name} ({users_dict[key].id})"):
                new_name = st.text_input("Nutzername", key=F"edit_name_user_{users_dict[key].id}", placeholder="Name eingeben", value=users_dict[key].name)
                new_id = st.text_input("Nutzer-ID", key=F"edit_id_user_{users_dict[key].id}", placeholder="ID eingeben", value=users_dict[key].id)
                
                save, delete = st.columns(2)
                with save:
                    if st.button("Speichern", key=F"save_user_{users_dict[key].id}"):
                        st.success("Änderungen gespeichert")
                with delete:
                    if st.button("Löschen", key=F"delete_user_{users_dict[key].id}"):
                        #st.success("Nutzer gelöscht")
                        users_dict.pop(key)
                        #users = [user for user in users_dict.values()]
                        break

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
        st.write("Übersicht der Wartungspläne")

        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices], key="mtn_selectbox_device", index=None, placeholder="Gerät auswählen")
        
        #testdaten für wartungsplan
        devices_dict["Nintendo Switch"].MTN=MTN_Plan(mtn_int=20, first_mtn=datetime(2024, 1, 1), mtn_cost=420.69, last_mtn=datetime(2024, 1, 1), end_of_life=datetime(2024, 10, 1))  
        devices_dict["Pro Controller (Luigi Edition)"].MTN=MTN_Plan(mtn_int=70, first_mtn=datetime(2023, 11, 10), mtn_cost=69.420, last_mtn=datetime(2023, 11, 10), end_of_life=datetime(2024, 12, 1))

        if sel_dev != None: 
            sel_dev = devices_dict[sel_dev]
            if sel_dev.MTN is None:
                with st.container(border=True):
                    st.write("Kein Wartungsplan vorhanden")
                #mtn hinzufügen
                st.expander("Neuen Wartungsplan hinzufügen")
                with st.expander("Neuen Wartungsplan hinzufügen"):
                    new_start = st.date_input("Erste Wartung", key="new_mtn_start")
                    new_end = st.date_input("Ende der Lebensdauer", key="new_mtn_end")
                    new_interval = st.number_input("Wartungsintervall (Tage)", key="new_mtn_interval", min_value=1, value=1)
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
            else:
                mtn_df = pd.DataFrame(columns=["Erste Wartung", "Letzte Wartung", "Nächste Wartung", "Kosten einer Wartung", "Wartungsintervall", "Ende der Lebensdauer"])
                mtn_df.loc[len(mtn_df.index)] = [sel_dev.MTN.first_mtn.strftime('%d.%m.%Y'), sel_dev.MTN.last_mtn.strftime('%d.%m.%Y'), sel_dev.MTN.next_mtn.strftime('%d.%m.%Y'),sel_dev.MTN.mtn_cost, sel_dev.MTN.mtn_int, sel_dev.MTN.end_of_life.strftime('%d.%m.%Y')]
                st.dataframe(mtn_df, use_container_width=True, hide_index=True)

                # Kosten Wartung ----------------------------funkt no nit ganz
                costs_quarter = pd.DataFrame(columns=["Quartal 1", "Quartal 2", "Quartal 3", "Quartal 4"])
                

                current_maint_time = sel_dev.MTN.first_mtn
                while current_maint_time.year < datetime.now().year:
                    current_maint_time = current_maint_time + timedelta(days=sel_dev.MTN.mtn_int)
                
                end_of_year = datetime(datetime.now().year, 12, 31)
                costs_quarter_values = [0,0,0,0]
                while current_maint_time < end_of_year:
                    current_maint_time = current_maint_time + timedelta(days=sel_dev.MTN.mtn_int)
                    if current_maint_time.month in [1,2,3]:
                        costs_quarter_values[0] += sel_dev.MTN.mtn_cost
                    elif current_maint_time.month in [4,5,6]:
                        costs_quarter_values[1] += sel_dev.MTN.mtn_cost
                    elif current_maint_time.month in [7,8,9]:
                        costs_quarter_values[2] += sel_dev.MTN.mtn_cost
                    else:
                        costs_quarter_values[3] += sel_dev.MTN.mtn_cost

                costs_quarter.loc[len(costs_quarter.index)] = costs_quarter_values
                st.write("Kosten pro Quartal in Euro:")
                st.dataframe(costs_quarter, use_container_width=True, hide_index=True)

                
                with st.expander("Wartungsplan bearbeiten"):
                    new_start = st.date_input("Erste Wartung", key="new_mtn_start")
                    new_end = st.date_input("Ende der Lebensdauer", key="new_mtn_end")

                    next_mtn_string = sel_dev.MTN.next_mtn.strftime("%d.%m.%Y")
                    new_next = st.date_input(F"Nächsten Wartungstermin ändern (geplant: {next_mtn_string})", key="new_mtn_next")

                    new_interval = st.number_input("Wartungsintervall (Tage)", key="new_mtn_interval", min_value=1, value=1)
                    new_cost = st.number_input("Kosten einer Wartung", key="new_mtn_cost", value=sel_dev.MTN.mtn_cost)
                    if st.button("Speichern", key="save_mtn_plan"):
                        if new_start > new_end:
                            st.warning("Startdatum muss vor Enddatum liegen!")
                        else:
                            st.success("Wartungsplan gespeichert")
                            sel_dev.MTN.mtn_start = new_start
                            sel_dev.MTN.mtn_end = new_end
                            sel_dev.MTN.mtn_interval = new_interval
            
    
    with tab4:
        st.header("Reservierungssystem", divider="red")
        st.write("Übersicht aller Reservierungen")

        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices], key="selectbox_device", index=None, placeholder="Gerät auswählen")
        if sel_dev != None:
            current_reservations=pd.DataFrame(columns=["Nutzer", "Start", "Ende"])
            sel_dev = devices_dict[sel_dev]
            if sel_dev.reservations != []:
                for reservation in sel_dev.reservations:
                    current_reservations.loc[len(current_reservations.index)] = [reservation.res_usr.name, reservation.res_start.strftime('%d.%m.%Y %H:%M'), reservation.res_end.strftime('%d.%m.%Y %H:%M')]
            # Check if the device has reservations

            current_reservations = current_reservations.rename_axis("Index")  
            with st.container(border=True):  
                st.dataframe(current_reservations, use_container_width=True)


                with st.expander("Reservierung löschen"):
                    if sel_dev.reservations != []:
                        reserv_index = st.number_input("Index der Reservierung", key="reserv_index", min_value=0, max_value=len(sel_dev.reservations)-1, value=0)
                        if st.button("Löschen", key="delete_reservation"):
                            sel_dev.reservations.pop(reserv_index)
                            st.success("Reservierung gelöscht")


        # Neue Reservierung hinzufügen
            with st.expander("Neue Reservierung hinzufügen"):
                start, end = st.columns(2)
                with start:
                    start_date = st.date_input("Startdatum", key="new_res_start_date")
                    start_time = st.time_input("Startzeit", key="new_res_start_time")
                with end:
                    end_date = st.date_input("Enddatum", key="new_res_end_date")
                    end_time = st.time_input("Endzeit", key="new_res_end_time")
                if st.button("Reservieren", key="add_reservation"):
                    if start_date > end_date:
                        st.warning("Startdatum muss vor Enddatum liegen!")
                    else:
                        if start_time > end_time and start_date == end_date:
                            st.warning("Startzeit muss vor Endzeit liegen!")
                        else:

                            for reserv in sel_dev.reservations:
                                if reserv.res_start <= datetime.combine(start_date, start_time) <= reserv.res_end or reserv.res_start <= datetime.combine(end_date, end_time) <= reserv.res_end:
                                    st.warning("Gewählter Zeitraum nicht mehr verfügbar")
                                    break
                                else:
                                    new_reservation = Reservation(res_start=datetime.combine(start_date, start_time), res_end=datetime.combine(end_date, end_time), res_usr=users_dict["Andreas"])
                                    sel_dev.reservations.append(new_reservation)
                                    st.success("Reservierung hinzugefügt")
                                    break
            

with col2:
    st.header("Allgemeine Übersicht", divider="red")
    st.write("Anstehende Reservierungen in nächsten 2 Wochen:")

    next_reservations = pd.DataFrame(columns=["Gerät", "Nutzer", "Start", "Ende"])
    for device in devices:
        if device.reservations != []:
            for reservation in device.reservations:
                if datetime.now() <= reservation.res_start <= datetime.now() + timedelta(days=14):
                    next_reservations.loc[len(next_reservations.index)] = [device.name, reservation.res_usr.name, reservation.res_start.strftime('%d.%m.%Y %H:%M'), reservation.res_end.strftime('%d.%m.%Y %H:%M')]
    
    st.dataframe(next_reservations, use_container_width=True, hide_index=True)

    st.write("Anstehende Wartungen in nächsten 2 Wochen:")
    next_mtn = pd.DataFrame(columns=["Gerät", "Wartungstermin"])
    for device in devices:
        if device.MTN is not None and device.MTN.next_mtn is not None:
            if datetime.now() <= device.MTN.next_mtn <= datetime.now() + timedelta(days=14):
                next_mtn.loc[len(next_mtn.index)] = [device.name, device.MTN.next_mtn.strftime('%d.%m.%Y')]
    
    st.dataframe(next_mtn, use_container_width=True, hide_index=True)


# This ocmmand can rerun the script (DB-Reload?)
#st.rerun()
                    