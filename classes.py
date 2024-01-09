import pandas as pd
from datetime import datetime as dt, timedelta

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
                 next_mtn:dt= None,
                 mtn_cost:float= None,
                 last_mtn:dt=None,
                 creation_d:dt=None,
                 end_of_life:dt=None,):
    
        #initializing the class

        self.mtn_int = mtn_int
        self.first_mtn = first_mtn
        self.mtn_cost = mtn_cost
        self.last_mtn = last_mtn
        self.creation_d = creation_d
        self.end_of_life = end_of_life
        self.next_mtn = last_mtn + timedelta(days=mtn_int) if last_mtn is not None else None
    

class Device():
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

    def add_reservation(self, Reservation:Reservation):
        self.reservations.append(Reservation)
    
    def del_reservation(self, Reservation:Reservation):
        self.reservations.remove(Reservation)

    def change_creation_d(self, new_creation_d: dt):
        if self.MTN is not None:
            self.MTN.creation_d = new_creation_d  # Corrected this line
        else:
            # Handle the case where there is no MTN_Plan assigned to the Device
            pass

    def change_last_upd(self, new_last_upd: dt):
        if self.MTN is not None:
            self.MTN.last_upd = new_last_upd  # Corrected this line
        else:
            # Handle the case where there is no MTN_Plan assigned to the Device
            pass
