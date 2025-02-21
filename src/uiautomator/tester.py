import uiautomator2 as u2
from src.opencv.getStage import getStage, load_templates

# connect to the AVD
d = u2.connect()

# Login(d, "email@e.com", "password1")
# Register(d, "email@e3.com", "Password1", "Andrzej", "Pliszka", "AndrzejPliszka") # make sure the password complies with their password rules

print(getStage(d, templates=load_templates("../opencv/registration"), debug=True))

# ListViewInstances(d)
# print_view_nodes(d)

# runAVD()
