import pandas as pd
from datetime import datetime as dt, timedelta
from tinydb import TinyDB, Query
from serializer import serializer

import os

class User():

    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')
    def __init__(self,
             name:str=None,
             id:int=None):
        
        #initializing the class
        
        self.name = name
        self.id = id
    
    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.name == self.name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Users updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Users inserted.")

    @classmethod
    def load_data_by_device_name(cls, name):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.name == name)

        if result:
            data = result[0]
            return cls(data['name'], data['id'])
        else:
            return None
        

class Reservation():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('res')

    def __init__(self,
                 res_usr:User,
                 res_start:dt,
                 res_end:dt,
                 device_id:int):
        
        #initializing the class
        device_id = device_id
        self.res_usr = res_usr
        self.res_start = res_start
        self.res_end = res_end

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.device_id == self.device_id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Reservations updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Reservations inserted.")

    @classmethod
    def load_data_by_device_name(cls, device_id):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_id == device_id)

        if result:
            data = result[0]
            return cls(data['device_id'], data['res_usr'], data['res_start'], data['res_end'])
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
        self.first_mtn = first_mtn
        self.mtn_cost = mtn_cost
        self.last_mtn = last_mtn
        self.end_of_life = end_of_life
        self.next_mtn = last_mtn + timedelta(days=mtn_int) if last_mtn is not None else None
    
    def store_data(self):
        print("Storing data...")
        # Check if the mtn already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.device_id == self.device_id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("MTN-Plan updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("MTN-Plan inserted.")

    @classmethod
    def load_data_by_device_name(cls, device_id):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.device_id == device_id)

        if result:
            data = result[0]
            return cls(data['device_id'], data['mtn_int'], data['first_mtn'], data['mtn_cost'], data['last_mtn'], data['end_of_life'], data['next_mtn'])
        else:
            return None

class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices')
    def __init__(self, res_usr:User=None, id:int=None, name:str=None, MTN:MTN_Plan=None, last_update:dt=None, creation_date:dt=None, reservations:list=None):
        
        #initializing the class
        
        self.reservations = []

        self.res_usr = res_usr 
        self.id = id
        self.name = name
        self.MTN = MTN
        self.last_update = last_update
        self.creation_date = creation_date

    def add_reservation(self, Reservation:Reservation):
        self.reservations.append(Reservation)
        self.reservations = sorted(self.reservations, key=lambda x: x.res_start)
    
    def del_reservation(self, Reservation:Reservation):
        self.reservations.remove(Reservation)

    def edit_device(self, name:str=None, id:int=None, MTN:MTN_Plan=None, res_usr:User=None):
        self.name = name if name is not None else self.name
        self.id = id if id is not None else self.id
        self.MTN = MTN if MTN is not None else self.MTN
        self.res_usr = res_usr if res_usr is not None else self.res_usr
        self.__last_update = dt.now()

    def set_creation_date(self):
        self.creation_date = dt.now()
    
    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.name == self.name)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.__dict__, doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.__dict__)
            print("Data inserted.")
    
    @classmethod
    def load_data_by_device_name(cls, name):
        # Load data from the database and create an instance of the Device class
        DeviceQuery = Query()
        result = cls.db_connector.search(DeviceQuery.name == name)

        if result:
            data = result[0]
            return cls(data['res_usr'], data['id'], data['name'], data['MTN'], data['reservations'], data['last_update'], data['creation_date'])
        else:
            return None