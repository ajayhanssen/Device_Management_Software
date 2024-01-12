import streamlit as st
from queries import find_devices, find_users, find_mtn, find_res
from classes import Device, MTN_Plan, Reservation, User
from datetime import datetime as dt, timedelta

test_dev = Device(name="TestDevice", id=1, res_usr=None)

test_user = User(name="TestUser", id=1)
test_mtn = MTN_Plan(device_id=1, mtn_int=30, first_mtn=dt.now(), mtn_cost=10, last_mtn=dt.now(), end_of_life=dt.now() + timedelta(days=365))
#test_dev.res_user = test_user
#test_dev.MTN = test_mtn

#print(test_dev.__dict__)
#print(test_mtn.__dict__)

test_dev.store_data()
test_user.store_data()
test_mtn.store_data()

devices_in_db = find_devices()
users_in_db = find_users()
mtn_in_db = find_mtn()

loaded_device = Device.load_data_by_device_name(devices_in_db[0])
loaded_user = User.load_data_by_device_name(users_in_db[0])
loaded_mtn = MTN_Plan.load_data_by_device_name(mtn_in_db[0])

print(loaded_device.name)
print(loaded_user.name)
print(loaded_mtn.device_id)

