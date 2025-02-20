import uiautomator2 as u2
from login import Login
from register import Register
from src.opencv.registration.getRegistrationStage import getRegistrationStage, load_templates
from utils.listViewInstances import ListViewInstances
from src.avd.runAVD import runAVD


# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
Register(d, "email@e3.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules

# print(getRegistrationStage(d, templates=load_templates("../opencv/registration/progressBarImages")))

# ListViewInstances(d)
# print_view_nodes(d)

# runAVD()
