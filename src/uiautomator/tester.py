import uiautomator2 as u2
from login import Login
from register import Register
from utils.listViewInstances import ListViewInstances
from src.avd.runAVD import runAVD


# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
Register(d, "email@e2.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules

ListViewInstances(d)

# runAVD()
