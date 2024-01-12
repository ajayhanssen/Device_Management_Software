import pandas as pd
from datetime import datetime as dt, timedelta
from tinydb import TinyDB, Query
import os

class User():
    def __init__(self,
             name:str=None,
             id:int=None):
        
        #initializing the class
        
        self.name = name
        self.id = id

class Reservation():
    def __init__(self,
                 res_usr:User,
                 res_start:dt,
                 res_end:dt):
        
        #initializing the class

        self.res_usr = res_usr
        self.res_start = res_start
        self.res_end = res_end

class MTN_Plan():
    def __init__(self,
                 mtn_int:int = None,
                 first_mtn:dt= None,
                 mtn_cost:float= None,
                 last_mtn:dt=None,
                 end_of_life:dt=None):
    
        #initializing the class

        self.mtn_int = mtn_int
        self.first_mtn = first_mtn
        self.mtn_cost = mtn_cost
        self.last_mtn = last_mtn
        self.end_of_life = end_of_life
        self.next_mtn = last_mtn + timedelta(days=mtn_int) if last_mtn is not None else None
    

class Device():
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')).table('devices')
    def __init__(self,
                 res_usr:User=None,
                 id:int=None,
                 name:str=None,
                 MTN:MTN_Plan=None):
        
        #initializing the class
        
        self.reservations = []

        self.res_usr = res_usr 
        self.id = id
        self.name = name
        self.MTN = MTN
        self.__last_update = dt.now()
        self.__creation_date = dt.now()

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

    def get_creation_date(self):
        return self.__creation_date