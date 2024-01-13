import streamlit as st
from queries import find_devices, find_users, find_mtn, find_res
from classes import Device, MTN_Plan, Reservation, User
from datetime import datetime as dt
from datetime import timedelta

users = [User(name="Andreas", id="mr.rioes@gmail.com"),
         User(name="Hannes", id="kompl_kek@yahoo.at"),
         User(name="Samuel", id="fortn_battlepass@outlook.com")]
devices = [Device(name="Nintendo Switch", res_usr="mr.rioes@gmail.com", id=12345, creation_date=dt.now(), last_update=dt.now() + timedelta(days=12)),
           Device(name="Among Us", res_usr="kompl_kek@yahoo.at", id=69420, creation_date=dt.now(), last_update=dt.now() + timedelta(days=1)),
           Device(name="Pro Controller (Luigi Edition)", id=12346, creation_date=dt.now(), last_update=dt.now() + timedelta(days=1))]



MTN_plans = [MTN_Plan(device_id=12345, mtn_int=20, first_mtn=dt(2024, 1, 1), mtn_cost=420.69, last_mtn=dt(2024, 1, 1), end_of_life=dt(2024, 10, 1))]
MTN_plans.append(MTN_Plan(device_id=12346, mtn_int=70, first_mtn=dt(2023, 11, 10), mtn_cost=69.420, last_mtn=dt(2023, 11, 10), end_of_life=dt(2024, 12, 1)))

#testdaten für wartungsplan
        #devices_dict["Nintendo Switch"].MTN=MTN_Plan(mtn_int=20, first_mtn=datetime(2024, 1, 1), mtn_cost=420.69, last_mtn=datetime(2024, 1, 1), end_of_life=datetime(2024, 10, 1))  
        #devices_dict["Pro Controller (Luigi Edition)"].MTN=MTN_Plan(mtn_int=70, first_mtn=datetime(2023, 11, 10), mtn_cost=69.420, last_mtn=datetime(2023, 11, 10), end_of_life=datetime(2024, 12, 1))



reservations = [Reservation(res_index=0, device_id=12345, res_usr="mr.rioes@gmail.com", res_start=dt.now(), res_end=dt.now()+timedelta(hours=1))]
reservations.append(Reservation(res_index=1, device_id=12346, res_usr="kompl_kek@yahoo.at", res_start=dt.now()+timedelta(hours=1), res_end=dt.now()+timedelta(hours=2)))
print(len(reservations))

for usr in users:
    usr.store_data()
for dev in devices:
    dev.store_data()
for res in reservations:
    res.store_data()
for mtn in MTN_plans:
    mtn.store_data()

users_in_db = find_users()
devices_in_db = find_devices()
reservations_in_db = find_res()
mtn_in_db = find_mtn()


