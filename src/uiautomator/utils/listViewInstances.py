def ListViewInstances(device):

    print(device.dump_hierarchy())  # Print all elements on the screen

    views = device(className="android.view.View") # List all instances of android.view.View
    for i, view in enumerate(views):
        print(f"Instance {i}: {view.info}")