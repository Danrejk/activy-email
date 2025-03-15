import subprocess


def isAdbAvailable():
    """ Check if ADB is available in the system PATH """
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False