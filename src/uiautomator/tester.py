import uiautomator2 as u2
from login import Login

# connect to the AVD
d = u2.connect()

Login(d, "email@e.com", "password1")