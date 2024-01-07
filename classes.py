import pandas as pd
from datetime import datetime as dt

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
                 res_end:dt,
                 res_id:int,
                 res_device:int):
        
        #initializing the class

        self.res_usr = res_usr
        self.res_start = res_start
        self.res_end = res_end
        self.res_id = res_id
        self.res_device = res_device

class MTN_Plan():
    def __init__(self,
                 mtn_int:int,
                 first_mtn:dt,
                 next_mtn:dt,
                 mtn_cost:float):
    
        #initializing the class

        self.__mtn_int = mtn_int
        self.first_mtn = first_mtn
        self.next_mtn = next_mtn
        self.__mtn_cost = mtn_cost
    

class Device():
    def __init__(self,
                 res_usr:User=None,
                 id:int=None,
                 name:str=None,
                 last_upd:dt=None,
                 creation_d:dt=None,
                 end_of_life:dt=None,
                 MTN:MTN_Plan=None):
        
        #initializing the class
        
        self.reservations = []

        self.res_usr = res_usr 
        self.id = id
        self.name = name
        self.__last_upd = last_upd
        self.__creation_d = creation_d
        self.end_of_life = end_of_life
        self.MTN = MTN

    def add_reservation(self, Reservation:Reservation):
        self.reservations.append(Reservation)
    
    def del_reservation(self, Reservation:Reservation):
        self.reservations.remove(Reservation)

    def change_creation_d(self, new_creation_d:dt):
        self.__creation_d = new_creation_d

    def change_last_upd(self, new_last_upd:dt):
        self.__last_upd = new_last_upd
