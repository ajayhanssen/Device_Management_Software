from devices import Device
from users import User
from queries import find_devices
from serializer import serializer


dev = Device("Device1","bla@gmail.com")
dev2 = Device("Device2","bla2@gmai.com")
dev3 = Device("Device3","bla3@gmail.com")
dev4 = Device("Device4","bla4@gmail.com")


dev.store_data()
dev2.store_data()
dev3.store_data()
dev4.store_data()


devices_list = find_devices()
for dev in devices_list:
    loaded_dev = Device.load_data_by_device_name(dev)
    print(loaded_dev.device_name)
    print(loaded_dev.managed_by_user_id)
    print(loaded_dev.is_active)
    print("-------------")
