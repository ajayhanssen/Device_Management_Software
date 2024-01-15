import pandas as pd
from datetime import datetime as dt, timedelta
from tinydb import TinyDB, Query
from serializer import serializer
import streamlit as st

import os

class User():

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')
    def __init__(self,
             name:str=None,
             id:int=None):
        
        #initializing the class
        
        self.name = name
        self.id = id

    def edit_user(self, name:str=None, id:int=None):
        self.name = name
        self.id = id
        self.store_data()

    def add_user(self):
        self.store_data()



    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Users updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Users inserted.")

    @classmethod
    def load_data_by_user_id(cls, id):
        # Load data from the database and create an instance of the Device class
        UserQuery = Query()
        result = cls.db_connector.search(UserQuery.id == id)

        if result:
            data = result[0]
            return cls(data['name'], data['id'])
        else:
            return None
        

class Reservation():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('res')
    

    def __init__(self,
                 res_index:int,
                 res_usr:User,
                 res_start:dt,
                 res_end:dt,
                 device_id:int):
        
        #initializing the class
        self.res_index = res_index
        self.device_id = device_id
        self.res_usr = res_usr
        self.res_start = res_start
        self.res_end = res_end

    #def add_reservation(self, Reservation:Reservation):
        #self.reservations.append(Reservation)
        #self.reservations = sorted(self.reservations, key=lambda x: x.res_start)
     #   pass
    def add_reservation(self):
        self.store_data()

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        ReservationQuery = Query()
        result = self.db_connector.search(ReservationQuery.res_index == self.res_index)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Reservations updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Reservations inserted.")

    @classmethod
    def load_data_by_res_index(cls, res_index):
        # Load data from the database and create an instance of the Device class
        ReservationQuery = Query()
        result = cls.db_connector.search(ReservationQuery.res_index == res_index)

        if result:
            data = result[0]
            return cls(data['res_index'], data['res_usr'], data['res_start'], data['res_end'], data['device_id'])
        else:
            return None

class MTN_Plan():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('mtn')

    def __init__(self,
                 mtn_int:int = None,
                 first_mtn:dt= None,
                 mtn_cost:float= None,
                 last_mtn:dt=None,
                 end_of_life:dt=None,
                 device_id:int=None,
                 next_mtn:dt=None):
    
        #initializing the class
        
        self.device_id = device_id
        self.mtn_int = mtn_int
        self.first_mtn = dt.combine(first_mtn, dt.min.time())
        self.mtn_cost = mtn_cost
        self.last_mtn = dt.combine(last_mtn, dt.min.time())
        self.end_of_life = dt.combine(end_of_life, dt.min.time())
        self.next_mtn = last_mtn + timedelta(days=mtn_int) if last_mtn is not None else None

    def add_new_mtn(self):
        self.store_data()

    def edit_mtn(self, first_mtn:dt=None, last_mtn:dt=None, end_of_life:dt=None, mtn_int:int=None, mtn_cost:float=None, mtn_next:dt=None):
        self.first_mtn = dt.combine(first_mtn, dt.min.time())
        self.last_mtn = dt.combine(last_mtn, dt.min.time())
        self.end_of_life = dt.combine(end_of_life, dt.min.time())
        self.mtn_int = mtn_int
        self.mtn_cost = mtn_cost
        self.next_mtn = dt.combine(mtn_next, dt.min.time())
        self.store_data()



    def store_data(self):
        print("Storing data...")
        # Check if the mtn already exists in the database
        MTNQuery = Query()
        result = self.db_connector.search(MTNQuery.device_id == self.device_id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("MTN-Plan updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("MTN-Plan inserted.")

    @classmethod
    def load_data_by_device_id(cls, device_id):
        # Load data from the database and create an instance of the Device class
        MTNQuery = Query()
        result = cls.db_connector.search(MTNQuery.device_id == device_id)

        if result:
            data = result[0]
            return cls(data['mtn_int'], data['first_mtn'], data['mtn_cost'], data['last_mtn'], data['end_of_life'], data['device_id'], data['next_mtn'])
        else:
            return None

class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')

    def __init__(self, res_usr:str=None, id:int=None, name:str=None, last_update:dt=None, creation_date:dt=None):
        
        #initializing the class
        
        self.res_usr = res_usr 
        self.id = id
        self.name = name
        self.last_update = last_update
        self.creation_date = creation_date
    
    def del_reservation(self, Reservation:Reservation):
        self.reservations.remove(Reservation)

    def edit_device(self, name:str=None, res_usr:str=None):
        self.name = name
        self.res_usr = res_usr
        self.last_update = dt.now()
        self.store_data()

    def set_creation_date(self):
        self.creation_date = dt.now()
        self.last_update = dt.now()
    
    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.id == self.id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")

    def add_new_device(self):
        self.set_creation_date()
        self.store_data()


    @classmethod
    def load_data_by_device_id(cls, id):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.id == id)

        if result:
            data = result[0]
            return cls(data['res_usr'], data['id'], data['name'], data['last_update'], data['creation_date'])
        else:
            return None