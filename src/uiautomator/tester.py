import uiautomator2 as u2

from src.opencv.getStage import getStage, load_templates
from src.uiautomator.checkPoints import checkPoints
from src.uiautomator.connectStrava import connectStrava
from src.uiautomator.login import Login
from src.uiautomator.logout import Logout
from src.uiautomator.update import UpdateApp
from src.uiautomator.utils.checkStage import checkStage
from src.uiautomator.utils.debug.drawNodeBoundaries import drawNodeBoundaries
from src.uiautomator.utils.debug.dumpHierarchy import dumpHierarchy
from src.uiautomator.utils.debug.listViewInstances import ListViewInstances
from src.uiautomator.utils.getCurretlyOpenApp import getCurrentlyOpenApp

# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
# Register(d, "email@e6.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules
# connectStrava(d, "email@e1.com", "Password1")
# print(checkPoints(d, "Kręć kilometry dla Gdańska 2024"))
# UpdateApp(d)
Logout(d)

# print(getStage(d, templates=load_templates("../opencv/connectStrava"), debug=True))
# checkStage(d, 2, templates=load_templates("../opencv/connectStrava"), debug=True)
# tryCheckStage(d, 2, templates=load_templates("../opencv/registration"), debug=True)

dumpHierarchy(d)
# ListViewInstances(d)

print(getCurrentlyOpenApp(d))

drawNodeBoundaries(d)

# runAVD()
