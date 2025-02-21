import subprocess

def clearChrome():
    subprocess.run(["adb", "shell", "pm", "clear", "com.android.chrome"], check=True)
    print("Cleared Chrome")
