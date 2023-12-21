import streamlit as st
from tinydb import TinyDB, Query
import pandas as pd
import numpy as np

class Device():
    def __init__(self, name) -> None:
        self.name = name

# Open the TinyDB database
device_db = TinyDB('device_db.json')
# Load existing devices from the database
devices = [Device(**entry.get('device', {})) for entry in device_db.all()]
# Close the database connection
device_db.close()

st.set_page_config(layout="wide")
st.write("# Gerätemanagement")

col1, col2 = st.columns(2)

with col1:
    tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Wartung"])

    with tab1:
        st.header("Geräteverwaltung")
        st.write("Text hallphallp")
        selectbox_options_dev = [device.name for device in devices]

        currentdevice = st.selectbox('Gerät auswählen', options=selectbox_options_dev, key="sbdevice_example")

        for device in devices:
            if device.name == currentdevice:
                selected_device = device                

        # Gerätinformationen darstellen
        attribute, value = st.columns(2)
        with attribute:
            st.write("Gerätename")
            st.divider()
            st.write("blebelbele")
        with value:
            st.write(selected_device.name)
            st.divider()
            st.write(42069)

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

    with tab2:
        st.header("Nutzerverwaltung")

    with tab3:
        st.header("Wartungsplanung")

with col2:
    st.write("To be made")


# Open the TinyDB database again
device_db = TinyDB('device_db.json')

# Clear the current entries in the database
device_db.truncate()

# Save devices to the database
device_db.insert_multiple({'device': device.__dict__} for device in devices)

# Close the database connection
device_db.close()