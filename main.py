import streamlit as st

st.write("# Gerätemanagement")


st.write("## Geräteauswahl")

st.write("Text hallphallp")

currentdevice_example = st.selectbox(
    'Gerät auswählen',
    options=['Gerät 1', 'Gerät 2', 'Gerät 3'], key="sbdevice_example"
)

if currentdevice_example == "Gerät 1":
    st.write("Gerät 1 ausgewählt")
    st.button("Do not press")
