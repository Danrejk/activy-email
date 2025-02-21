import uiautomator2 as u2
from src.opencv.getStage import getStage, load_templates
from src.uiautomator.connectStrava import connectStrava
from src.uiautomator.login import Login
from src.uiautomator.register import Register
from src.uiautomator.utils.checkStage import tryCheckStage, checkStage
from src.uiautomator.utils.drawNodeBoundaries import drawNodeBoundaries
from src.uiautomator.utils.listViewInstances import ListViewInstances

# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
# Register(d, "email@e6.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules
connectStrava(d, "email@e1.com", "Password1")

# print(getStage(d, templates=load_templates("../opencv/connectStrava"), debug=True))
# checkStage(d, 2, templates=load_templates("../opencv/connectStrava"), debug=True)
# tryCheckStage(d, 2, templates=load_templates("../opencv/registration"), debug=True)

# ListViewInstances(d)
# drawNodeBoundaries(d)

# runAVD()
