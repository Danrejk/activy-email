import uiautomator2 as u2
from login import Login
from register import Register
from utils.listViewInstances import ListViewInstances

# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
Register(d, "email@e.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules

ListViewInstances(d)