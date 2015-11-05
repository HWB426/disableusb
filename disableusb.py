# Dis|Enables the USB storage ability in Windows
# disableusb.py

from winreg import *
import os, sys, win32api, socket, win32net

def write_key(value):
    try:
        aKey = OpenKey(HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\services\\USBSTOR", 0, KEY_ALL_ACCESS)
        SetValueEx(aKey, "Start", 4, REG_DWORD, value)
        if value == 3:
            print("USB storage turned on")
        else:
            print("USB storage turned off")
    except:
        print("You must be an Administrator. Permission denied.")
    return () 
    
def check_user(machine_name, user_name):
    # Check if user is part of the administrator's group
    user_name = os.environ['UserDomain'] + '\\' + user_name
    group_membership = groups = win32net.NetUserGetLocalGroups(machine_name, user_name)
    if 'Administrators' in group_membership:
        return True
    else:
        return False

    # based upon what's fed at the command line, let's either turn it on or off
try:
    if sys.argv[1].upper() == "ON":
        write_key(3)
    elif sys.argv[1].upper() == "OFF":
        write_key(4)
    else:
        print("Please use either on or off to change the function.")
except:
    #If being called some other way, let's enable the USB storage based on group membership
    if check_user(socket.gethostname(), os.getlogin()) is True:
        write_key(3)
    else:
        print("You must be an Administrator. Permission denied.")
