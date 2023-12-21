import streamlit as st
class Device():
   def __init__(self, name) -> None:
        self.name = name


st.write("# Gerätemanagement")

Drucker = Device("Drucker")
Projektor = Device("Projektor")

devices = [Drucker, Projektor]

tab1, tab2, tab3 = st.tabs(["Geräte", "Nutzer", "Wartung"])

with tab1:
    st.header("Geräteverwaltung")
    st.write("Text hallphallp")
    selectbox_options_dev = [device.name for device in devices]
   
    currentdevice_example = st.selectbox('Gerät auswählen', options=selectbox_options_dev, key="sbdevice_example")

    if currentdevice_example == "Gerät 1":
        st.write("Gerät 1 ausgewählt")
        st.button("Do not press")

    with st.expander("Neues Gerät hinzufügen"):
        new_name = st.text_input("Gerätename")
        #new_user
        #alle anderen Attribute
        if st.button("Hinzufügen"):
            st.write("Gerät hinzugefügt")
            devices.append(Device(new_name))
                 

with tab2:
   st.header("Nutzerverwaltung")

with tab3:
   st.header("Wartungsplanung")




#streamlit tabs

# to run, type in terminal: streamlit run main.py
