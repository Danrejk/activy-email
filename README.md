# Setting Up Android Virtual Device (AVD)

This guide will help you install and configure an Android Virtual Device (AVD) named `activyAVD` to run Android apps.

## Prerequisites

- **Java Development Kit (JDK) 8 or later**  
  - [Download JDK](https://adoptium.net/) and install it.  
  - Ensure `java` is available in the terminal by running:  
    ```sh
    java -version
    ```
- **Android SDK Command-Line Tools**  
  - Download the [Android Command Line Tools](https://developer.android.com/studio#cmdline-tools) for your OS.  
  - Extract it to a folder of your choice (e.g., `C:\Android\SDK` or `~/Android/SDK`).

## Setup Environment Variables

If you installed the SDK manually, you must add its tools to your system's PATH.

### **Windows**
1. Open **Edit the system environment variables** from the Start menu.
2. Click **Environment Variables**.
3. Under **System Variables**, select `Path` and click **Edit**.
4. Add the following directories (modify paths if needed):
   ```
   C:\Android\SDK\cmdline-tools\latest\bin
   C:\Android\SDK\platform-tools
   C:\Android\SDK\emulator
   ```
5. Click **OK** and restart the terminal.

### **Linux/macOS**
1. Edit `~/.bashrc` or `~/.zshrc` and add:
   ```sh
   export ANDROID_HOME=~/Android/SDK
   export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH
   ```
2. Apply changes:
   ```sh
   source ~/.bashrc  # or source ~/.zshrc
   ```

## Install Android System Image and Create AVD

Run the following commands in a terminal:

```sh
sdkmanager "platform-tools" "platforms;android-30" "system-images;android-30;google_apis_playstore;x86_64" "emulator"
avdmanager create avd -n activyAVD -k "system-images;android-30;google_apis_playstore;x86_64"
```

## Launch the Emulator

```sh
emulator -avd activyAVD
```

## Using Google Play Store

Since the emulator includes **Google Play**, you can install apps directly from the Play Store inside the virtual device.

---

This setup ensures you can run Android apps on an emulator without installing Android Studio.
