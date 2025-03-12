import subprocess

# WARNING!
# THIS WILL HAVE ISSUES WORKING IF ADB ISN'T ADDED TO THE SYSTEM PATH
def clearChrome():
    subprocess.run(["adb", "shell", "pm", "clear", "com.android.chrome"], check=True)
    print("Cleared Chrome")
