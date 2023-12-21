import pandas as pd
import datetime as dt

class User():
    def __init__(self,
             usr_name:str,
             usr_id:int):
        
        #initializing the class
        
        self.usr_name = usr_name
        self.usr_id = usr_id

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
                 mtn_int:dt,
                 first_mtn:dt,
                 next_mtn:dt,
                 mtn_cost:float):
    
        #initializing the class

        self.mtn_int = mtn_int
        self.first_mtn = first_mtn
        self.next_mtn = next_mtn
        self.mtn_cost = mtn_cost
    

class Device():
    def __init__(self,
                 res_usr:User,
                 id:int,
                 name:str,
                 last_upd:dt,
                 creation_d:dt,
                 end_of_life:dt,
                 MTN:MTN_Plan):
        
        #initializing the class
        
        reservations = []

        self.res_usr = res_usr 
        self.id = id
        self.name = name
        self.last_upd = last_upd
        self.creation_d = creation_d
        self.end_of_life = end_of_life
        self.MTN = MTN

    def add_reservation(self, Reservation:Reservation):
        self.reservations.append(Reservation)
    
    def del_reservation(self, Reservation:Reservation):
        self.reservations.remove(Reservation)

