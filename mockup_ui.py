import streamlit as st
import pandas as pd
from queries import find_devices, find_users, find_mtn, find_res
from datetime import datetime, timedelta
from classes import User, Reservation, MTN_Plan, Device

st.set_page_config(layout="wide", page_title="Gerätemanagement", page_icon=":video_game:")


st.write("# Gerätemanagement")

users_in_db = find_users()
devices_in_db = find_devices()
reservations_in_db = find_res()
mtn_in_db = find_mtn()

# users_dict = {}
# for user_db in users_in_db:
#     current_user = User.load_data_by_user_id(user_db)
#     users_dict[current_user.id] = current_user
#
devices_dict = {}
for device_db in devices_in_db:
    current_device = Device.load_data_by_device_id(device_db)
    devices_dict[current_device.name] = current_device
device_id_list = [device.id for device in devices_dict.values()]

users_dict = {}
for user_db in users_in_db:
    current_user = User.load_data_by_user_id(user_db)
    users_dict[current_user.name] = current_user
user_id_list = [user.id for user in users_dict.values()]

all_reservations = [Reservation.load_data_by_res_index(reservation_db) for reservation_db in reservations_in_db]
all_mtn = [MTN_Plan.load_data_by_device_id(mtn_db) for mtn_db in mtn_in_db]


col1, col2 = st.columns([0.6, 0.4])

with (col1):
    tab1, tab2, tab3, tab4 = st.tabs(["Geräte", "Nutzer", "Wartung", "Reservierungen"])
    with tab1:
        st.header("Geräteverwaltung", divider="red")
        st.write("Übersicht aller registrierten Geräte")

        selectbox_options_dev = [device.name for device in devices_dict.values()]
        currentdevice = st.selectbox('Gerät auswählen', options=selectbox_options_dev)
        #print(F"Selected device: {currentdevice}")
        selected_device = devices_dict[currentdevice]            
        #print(F"Current device: {selected_device}")

        # Gerätinformationen darstellen
        container = st.container(border=True)
        with container:
            
            dev_attributes = pd.DataFrame(columns=["Gerätenummer", "Verantwortlicher", "Erstelldatum", "Zuletzt bearbeitet"])
            selected_device_user = User.load_data_by_user_id(selected_device.res_usr)
            dev_attributes.loc[len(dev_attributes.index)] = [selected_device.id, selected_device_user.name if selected_device.res_usr is not None
                                                             else "Kein Verantwortlicher", selected_device.creation_date.strftime("%d.%m.%Y"), selected_device.last_update.strftime("%d.%m.%Y")]
            # Dass die Kommas alle drei Nullen im Dataframe verschwinden:
            styled_dev_attr = dev_attributes.style.format({"Expense": lambda x : '{:.4f}'.format(x)})

            st.dataframe(styled_dev_attr, use_container_width=True, hide_index=True)

            # Gerät bearbeiten
            with st.expander("Gerät bearbeiten"):

                with st.form(key="edit_device_form", border=False):
                    new_name = st.text_input("Gerätename", key="edit_name_device", placeholder="Name eingeben", value=selected_device.name)
                    # new_id = st.text_input("Gerätenummer", key="edit_id_device", placeholder="Nummer eingeben", value=selected_device.id)
                    new_user = st.selectbox("Verantwortlicher", options=[user.name for user in users_dict.values()], key="selectbox_edit_device_user", index=None, placeholder="Neuen Verantwortlichen auswählen")

                    for user in users_dict.values():
                        if user.name == new_user:
                            new_user = user.id
                    speichern,löschen = st.columns(2)

                    
                    if speichern.form_submit_button("Speichern"):
                        selected_device.edit_device(new_name, new_user)
                        st.success("Änderungen gespeichert")
                        st.rerun()

                    if löschen.form_submit_button("Löschen"):
                        loadeddev = Device.load_data_by_device_id(selected_device.id)
                        loadeddev.delete_device(loadeddev.doc_index)

                        st.success("Gerät gelöscht")
                        st.rerun() 

        
        # Neues Gerät hinzufügen
        with st.expander("Neues Gerät hinzufügen"):

            with st.form(key="add_device_form", clear_on_submit=True, border=False):
                new_dev_name = st.text_input("Gerätename", key="name_new_device", placeholder="Name eingeben")
                new_dev_id = st.number_input("Gerätenummer *", key="id_new_device", placeholder="ID eingeben", min_value=0)
                new_dev_user = st.selectbox("Verantwortlicher", options=[user.name for user in users_dict.values()], key="selectbox_new_device_user", index=None, placeholder="Verantwortlichen auswählen")
                new_dev_user_id = None
                if new_dev_user != None:
                    new_dev_user_id = users_dict[new_dev_user].id
                new_device = Device(name=new_dev_name, id=new_dev_id, res_usr=new_dev_user_id)

                if st.form_submit_button("Gerät hinzufügen"):
                    if new_device.id in device_id_list:
                        st.warning("Gerätenummer bereits vergeben!")
                    elif new_device.id == None:
                        st.warning("Bitte eine Gerätenummer eingeben!")
                    else:
                        new_device.add_new_device(forbidden_ids=device_id_list)
                        st.success("Gerät hinzugefügt")
                        st.rerun()

    
    with tab2:
        st.header("Nutzerverwaltung", divider="red")
        st.write("Übersicht aller registrierten Benutzer")

        # Nutzer bearbeiten
        for key in users_dict:
            with st.expander(F"{users_dict[key].name} ({users_dict[key].id})"):
                with st.form(key=F"edit_user_form_{users_dict[key].id}", border=False):

                    new_name = st.text_input("Nutzername", key=F"edit_name_user_{users_dict[key].id}", placeholder="Name eingeben", value=users_dict[key].name)
                    new_id = st.text_input("Nutzer-ID", key=F"edit_id_user_{users_dict[key].id}", placeholder="ID eingeben", value=users_dict[key].id)

                    save, delete = st.columns(2)
                    with save:
                        if st.form_submit_button("Speichern"):
                            if new_id not in [name for name in user_id_list if name != users_dict[key].id] and new_id is not None:
                                users_dict[key].edit_user(new_name, new_id)
                                st.success("Änderungen gespeichert")
                                st.rerun()
                        
                            else:
                                st.warning("Bitte eine eindeutige ID eingeben!")


                    with delete:
                        if st.form_submit_button("Löschen"): ################################################################################################
                            loadeduser= User.load_data_by_user_id(users_dict[key].id)
                            loadeduser.delete_usr(loadeduser.doc_index)
                            st.rerun()

                            

        #Neuen Nutzer hinzufügen
        with st.expander("Neuen Nutzer hinzufügen"):
            with st.form(key="add_user_form", clear_on_submit=True, border=False):
                new_user_name = st.text_input("Nutzername", key="new_name", placeholder="Name eingeben")
                new_user_id = st.text_input("Nutzer-ID", key="new_id", placeholder="ID eingeben")
                new_user = User(name=new_user_name, id=new_user_id)

                if st.form_submit_button("Hinzufügen"):
                    if new_user.id in user_id_list:
                        st.warning("Nutzer-ID bereits vergeben!")
                    else:
                        new_user.add_user(forbidden_ids=user_id_list)
                        st.success("Nutzer hinzugefügt")
                        st.rerun()


    with tab3:
        st.header("Wartungsplanung", divider="red")
        st.write("Übersicht der Wartungspläne")

        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices_dict.values()], key="mtn_selectbox_device", index=None, placeholder="Gerät auswählen")
        
        #testdaten für wartungsplan
        #devices_dict["Nintendo Switch"].MTN=MTN_Plan(mtn_int=20, first_mtn=datetime(2024, 1, 1), mtn_cost=420.69, last_mtn=datetime(2024, 1, 1), end_of_life=datetime(2024, 10, 1))
        #devices_dict["Pro Controller (Luigi Edition)"].MTN=MTN_Plan(mtn_int=70, first_mtn=datetime(2023, 11, 10), mtn_cost=69.420, last_mtn=datetime(2023, 11, 10), end_of_life=datetime(2024, 12, 1))

        if sel_dev != None: 
            sel_dev = devices_dict[sel_dev]
            sel_dev_mtn = MTN_Plan.load_data_by_device_id(sel_dev.id)
            if sel_dev_mtn is None:
                with st.container(border=True):
                    st.write("Kein Wartungsplan vorhanden")
                #mtn hinzufügen
                st.expander("Neuen Wartungsplan hinzufügen")
                with st.expander("Neuen Wartungsplan hinzufügen"):
                    with st.form(key="add_mtn_form", clear_on_submit=False, border=False):
                        new_mtn_start = st.date_input("Erste Wartung", key="new_mtn_start", format="DD.MM.YYYY")
                        new_mtn_last = st.date_input("Zuletzt gewartet", key="new_mtn_last", format="DD.MM.YYYY")
                        new_mtn_end = st.date_input("Ende der Lebensdauer", key="new_mtn_end", format="DD.MM.YYYY")
                        new_mtn_int = st.number_input("Wartungsintervall (Tage)", key="new_mtn_interval", min_value=1, value=1)
                        new_mtn_cost = st.number_input("Kosten einer Wartung", key="new_mtn_cost", min_value=0.0)
                        new_mtn_plan = MTN_Plan(new_mtn_int, new_mtn_start, new_mtn_cost, new_mtn_last, new_mtn_end, sel_dev.id, None)
                        if st.form_submit_button("Hinzufügen"):
                            for key, value in new_mtn_plan.__dict__.items():
                                if value is None:
                                    st.warning(f"Bitte alle Felder ausfüllen.")
                                elif new_mtn_start > new_mtn_last:
                                    st.warning("Erste Wartung kann nicht nach letzter Wartung stattfinden.")
                                else:
                                    new_mtn_plan.add_new_mtn()
                                    st.success("Wartungsplan wurde erfolgreich hinzugefügt.")
                                    st.rerun()

            else:
                mtn_df = pd.DataFrame(columns=["Erste Wartung", "Letzte Wartung", "Nächste Wartung", "Kosten einer Wartung", "Wartungsintervall", "Ende der Lebensdauer"])
                mtn_df.loc[len(mtn_df.index)] = [sel_dev_mtn.first_mtn.strftime('%d.%m.%Y'), sel_dev_mtn.last_mtn.strftime('%d.%m.%Y'), sel_dev_mtn.next_mtn.strftime('%d.%m.%Y'), sel_dev_mtn.mtn_cost, sel_dev_mtn.mtn_int, sel_dev_mtn.end_of_life.strftime('%d.%m.%Y')]
                st.dataframe(mtn_df, use_container_width=True, hide_index=True)

                # Kosten Wartung ----------------------------funkt no nit ganz(?)
                costs_quarter = pd.DataFrame(columns=["Quartal 1", "Quartal 2", "Quartal 3", "Quartal 4"])

                current_maint_time = sel_dev_mtn.first_mtn
                while current_maint_time.year < datetime.now().year:
                    current_maint_time = current_maint_time + timedelta(days=sel_dev_mtn.mtn_int)
                
                end_of_year = datetime(datetime.now().year, 12, 31)
                end_of_calc = sel_dev_mtn.end_of_life if sel_dev_mtn.end_of_life < end_of_year else end_of_year
                costs_quarter_values = [0,0,0,0]
                while current_maint_time < end_of_calc:
                    current_maint_time = current_maint_time + timedelta(days=sel_dev_mtn.mtn_int)
                    if current_maint_time.month in [1,2,3]:
                        costs_quarter_values[0] += sel_dev_mtn.mtn_cost
                    elif current_maint_time.month in [4,5,6]:
                        costs_quarter_values[1] += sel_dev_mtn.mtn_cost
                    elif current_maint_time.month in [7,8,9]:
                        costs_quarter_values[2] += sel_dev_mtn.mtn_cost
                    else:
                        costs_quarter_values[3] += sel_dev_mtn.mtn_cost

                costs_quarter.loc[len(costs_quarter.index)] = costs_quarter_values
                st.write("Kosten pro Quartal in Euro:")
                st.dataframe(costs_quarter, use_container_width=True, hide_index=True)

                
                with st.expander("Wartungsplan bearbeiten"):
                    with st.form(key="edit_mtn_form", clear_on_submit=False, border=False):
                        new_mtn_start = st.date_input("Erste Wartung", key="new_mtn_start", format="DD.MM.YYYY", value=sel_dev_mtn.first_mtn)
                        new_mtn_last = st.date_input("Zuletzt gewartet", key="new_mtn_last", format="DD.MM.YYYY", value=sel_dev_mtn.last_mtn)
                        new_mtn_end = st.date_input("Ende der Lebensdauer", key="new_mtn_end", format="DD.MM.YYYY", value=sel_dev_mtn.end_of_life)

                        next_mtn_string = sel_dev_mtn.next_mtn.strftime("%d.%m.%Y")
                        new_next = st.date_input(F"Nächsten Wartungstermin ändern (geplant: {next_mtn_string})", key="new_mtn_next", format="DD.MM.YYYY", value=sel_dev_mtn.next_mtn)

                        new_interval = st.number_input("Wartungsintervall (Tage)", key="new_mtn_interval", min_value=1, value=sel_dev_mtn.mtn_int)
                        new_cost = st.number_input("Kosten einer Wartung", key="new_mtn_cost", value=sel_dev_mtn.mtn_cost, min_value=0.0)

                        if st.form_submit_button("Speichern"):
                            if any(arg is None for arg in [new_mtn_start, new_mtn_last, new_mtn_end, new_interval, new_cost, new_next]):
                                st.warning("Bitte alle Felder ausfüllen.")
                            elif new_mtn_start > new_mtn_last:
                                st.warning("Erste Wartung kann nicht nach letzter Wartung stattfinden.")
                            elif new_mtn_last > new_next:
                                st.warning("Letzte Wartung kann nicht nach nächster Wartung stattfinden.")
                            elif new_next > new_mtn_end:
                                st.warning("Nächste Wartung kann nicht nach Ende der Lebensdauer stattfinden.")
                            elif new_mtn_start > new_mtn_end:
                                st.warning("Erste Wartung kann nicht nach Ende der Lebensdauer stattfinden.")
                            else:
                                sel_dev_mtn.edit_mtn(new_mtn_start, new_mtn_last, new_mtn_end, new_interval, new_cost, new_next)
                                st.success("Änderungen gespeichert")
                                st.rerun()

    with tab4:
        st.header("Reservierungssystem", divider="red")
        st.write("Übersicht aller Reservierungen")

        sel_dev = st.selectbox("Gerät auswählen", options=[device.name for device in devices_dict.values()], key="selectbox_device", index=None, placeholder="Gerät auswählen")
        if sel_dev is not None:
            sel_dev = devices_dict[sel_dev]
            sel_dev_reservations = []
            for reservation in all_reservations:
                if reservation.device_id == sel_dev.id:
                    sel_dev_reservations.append(reservation)
            sel_dev_reservations.sort(key=lambda x: x.res_start)
            for index, reservation in enumerate(sel_dev_reservations):
                reservation.res_index = index
                reservation.store_data()

            current_reservations = pd.DataFrame(columns=["Index", "Nutzer", "Start", "Ende"])

            if sel_dev_reservations != []:
                for reservation in sel_dev_reservations:
                    res_user = User.load_data_by_user_id(reservation.res_usr)
                    current_reservations.loc[len(current_reservations.index)] = [reservation.res_index, res_user.name, reservation.res_start.strftime('%d.%m.%Y %H:%M'), reservation.res_end.strftime('%d.%m.%Y %H:%M')]

            with st.container(border=True):
                st.dataframe(current_reservations, use_container_width=True, hide_index=True)


                with st.expander("Reservierung löschen"):
                    with st.form(key="delete_reservation_form", clear_on_submit=True, border=False):
                        if sel_dev_reservations != []:
                            reserv_index = st.number_input("Index der Reservierung", key="reserv_index", min_value=0, max_value=len(sel_dev_reservations)-1, value=0)
                            if st.form_submit_button("Löschen"):
                                ###################################################################################################################
                                st.success("Reservierung gelöscht")


        # Neue Reservierung hinzufügen
            with st.expander("Neue Reservierung hinzufügen"):
                with st.form(key="add_new_reservation_form", clear_on_submit=False, border=False):
                    start, end = st.columns(2)
                    with start:
                        res_start_date = st.date_input("Startdatum", key="new_res_start_date", format="DD.MM.YYYY")
                        res_start_time = st.time_input("Startzeit", key="new_res_start_time")
                    with end:
                        res_end_date = st.date_input("Enddatum", key="new_res_end_date", format="DD.MM.YYYY")
                        res_end_time = st.time_input("Endzeit", key="new_res_end_time")
                    new_res_user = st.selectbox("Nutzer auswählen", options=[user.name for user in users_dict.values()], key="selectbox_new_res_user", index=None, placeholder="Nutzer auswählen")

                    is_available = True
                    for reserv in sel_dev_reservations:
                        if reserv.res_start <= datetime.combine(res_start_date, res_start_time) <= reserv.res_end or reserv.res_start <= datetime.combine(res_end_date, res_end_time) <= reserv.res_end:
                            is_available = False

                    if st.form_submit_button("Reservierung hinzufügen"):
                        if res_start_date > res_end_date:
                            st.warning("Startdatum muss vor Enddatum liegen!")
                        elif res_start_time > res_end_time and res_start_date == res_end_date:
                            st.warning("Startzeit muss vor Endzeit liegen!")
                        elif not is_available:
                            st.warning("Gewählter Zeitraum nicht mehr verfügbar")
                        elif new_res_user == None:
                            st.warning("Bitte einen Nutzer auswählen!")
                        else:
                            new_reservation = Reservation(res_index=len(sel_dev_reservations),
                                                          res_start=datetime.combine(res_start_date, res_start_time),
                                                          res_end=datetime.combine(res_end_date, res_end_time),
                                                          res_usr=users_dict[new_res_user].id, device_id=sel_dev.id)
                            new_reservation.add_reservation()
                            st.success("Reservierung hinzugefügt")
                            st.rerun()


with col2:
    st.header("Allgemeine Übersicht", divider="red")

    st.write("Aktive Reservierungen:")
    active_reservations = pd.DataFrame(columns=["Gerät", "Nutzer", "Start", "Ende"])
    for reservation in all_reservations:
        if reservation.res_start <= datetime.now() <= reservation.res_end:
            reservation_user = User.load_data_by_user_id(reservation.res_usr)
            reservation_device = Device.load_data_by_device_id(reservation.device_id)
            active_reservations.loc[len(active_reservations.index)] = [reservation_device.name, reservation_user.name, reservation.res_start.strftime('%d.%m.%Y %H:%M'), reservation.res_end.strftime('%d.%m.%Y %H:%M')]
    st.dataframe(active_reservations, use_container_width=True, hide_index=True)

    st.write("Anstehende Reservierungen in nächsten 2 Wochen:")

    next_reservations = pd.DataFrame(columns=["Gerät", "Nutzer", "Start", "Ende"])

    if reservations_in_db is not []:
        for reservation in all_reservations:
            reservation_user = User.load_data_by_user_id(reservation.res_usr)
            reservation_device = Device.load_data_by_device_id(reservation.device_id)
            if datetime.now() <= reservation.res_start <= datetime.now() + timedelta(days=14):
                next_reservations.loc[len(next_reservations.index)] = [
                    reservation_device.name if reservation_device else "Device not found",
                    reservation_user.name if reservation_user else "User not found",
                    reservation.res_start.strftime('%d.%m.%Y %H:%M'),
                    reservation.res_end.strftime('%d.%m.%Y %H:%M')
                    ]

    st.dataframe(next_reservations, use_container_width=True, hide_index=True)

    st.write("Anstehende Wartungen in nächsten 2 Wochen:")
    next_mtn = pd.DataFrame(columns=["Gerät", "Wartungstermin"])
    for current_mtn in all_mtn:
        if datetime.now() <= current_mtn.next_mtn <= datetime.now() + timedelta(days=14):
            device = Device.load_data_by_device_id(current_mtn.device_id)
            next_mtn.loc[len(next_mtn.index)] = [
                device.name if device else "Device not found",
                current_mtn.next_mtn.strftime('%d.%m.%Y') if current_mtn else "Maintenance details not found"
                ]


    st.dataframe(next_mtn, use_container_width=True, hide_index=True)

    st.write("Registrierte Geräte:")

# This ocmmand can rerun the script (DB-Reload?)
#st.rerun()
                    