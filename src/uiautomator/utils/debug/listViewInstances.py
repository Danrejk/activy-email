def ListViewInstances(device):
    # Dump the full hierarchy for context
    print(device.dump_hierarchy())

    # Get all instances of android.view.View
    views = device(className="android.view.View")
    print(f"Found {len(views)} views.\n")

    for i, view in enumerate(views):
        try:
            info = view.info
            print(f"Instance {i}: {info}")
            childCount = info.get("childCount", 0)
            if childCount > 0:
                print(f"  --> This instance has {childCount} child(ren):")
                for j in range(childCount):
                    try:
                        # Use the indexing operator to get the j-th child
                        child = view[j]
                        print(f"      Child {j}: {child.info}")
                    except Exception as ce:
                        print(f"      Child {j}: Error reading child: {ce}")
        except Exception as e:
            print(f"Error reading instance {i}: {e}")
