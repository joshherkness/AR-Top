# AR-Top

### Define your world

AR-Top is a suite of Augmented Reality (AR) tabletop applications consisting of
two parts.  First, a web experience is used to edit maps within a 3D environment
as well as host session for others to join.  Second, a mobile application is
used to join sessions and view those maps in an augmented reality environment.

1. [To run locally](#to-run-locally)
    1. [Build and deploy the server](#build-and-deploy-the-server)
    2. [Build the viewer](#build-the-viewer)
        1. [Android](#android)
            1. [Install APK](#install-apk)
            2. [Build from source](#build-from-source)
        2. [iOS](#ios)
        3. [Install textmeshpro](#install-textmeshpro)
        4. [Troubleshooting](#troubleshooting)
2. [Usage](#running)
3. [Group members](#group-members)

# To run locally

## Build and deploy the server

1. Download [docker](https://docs.docker.com/install/) for your server.
2. Run our `build-docker` script from the application root. 
    1. Before you run it, you may want to [add docker to
     sudo](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo?answertab=votes#tab-top),
     but this can pose a security risk on your machine. This step is optional.
3. `docker-compose up` will start the server. Run with the `-d` flag to
   daemon it.

## Build the viewer

### Android

You may build from source or directly install the APK found in the Builds Folder

#### Install APK

1. Connect your Android device to your computer.
2. Navigate to the Builds folder in the project source code.
3. Copy the file "AR-Top.apk" and paste it into the folder for your Android
   device.
4. Use any kind of file explorer app (such as "File Commander") to navigate to
   AR-Top.apk on your Android device. Select the file to install it.
5. If prompted, you will need to enable the "Unknown sources" option to install
   AR-Top to your device.
6. When the file runs, allow the permissions to "take pictures and record video"
   as well as "access photos, media, and files on your device". (These are the
   first two prompts that come up. You may deny everything else.) You only need
   to allow the permissions the first time you open the app.
7. The app is now installed and able to run on your device.

#### Build from source

1. Download Unity version 2017.3.1f1 (Follow all download instructions)
2. On the Unity Project Page, select "Open"
3. Navigate to the source folder and select AR-Top-MobileApp folder (Hit "Select
   Folder")
4. Wait for the project to compile and open.
5. See below section titled "Install TextMeshPro" to properly install the
   TextMeshPro Library to the project.
6. Enable your device to be built to either Android or iOS 6.1 If you are using
   Android, go to the following webpage and follow all instructions for enabling
   your device for USB Debugging and enabling Unity to build to your device:
   (https://docs.unity3d.com/Manual/android-sdksetup.html) 6.2 (Note that you
   must be on a Mac to build to iOS devices). If you are using iOS, go to the
   following webpage and follow all instructions to enable Unity to build to
   your iOS device: (https://docs.unity3d.com/Manual/iphone-GettingStarted.html)
7. After enabling your device, click File->Build Settings. In the Build settings
   menu select either Android or iOS underneath the Platform sub-window. Then
   click the "Switch Platform" button.
  1. If in Android: Click the "Add" button for Xiaomi Mi Game Center under the
     "SDKs for App Stores".
8. If you have not done so by now, connect your device to your computer by USB.
9. Click the "Build and Run" button.
10. Navigate to a folder above the AR-Top-MobileApp directory (any folder of
    your choosing but the "Builds" folder is recommended). Click "Save".
11. If building to Android, the app should run after Unity is done building it.
    If you are building to iOS, some additional steps may be required.

### iOS

1. Ensure that Edit > Project Settings > Player > XR Settings > Vuforia
    Augmented Reality is enabled.
2. Ensure that Edit > Project Settings > Player > Other Settings > Auto
    Graphics API is disabled.
3. Ensure that Edit > Project Settings > Player > Other Settings > Graphics
    API's is set to prefer OpenGLES2.
4. Set the Edit > Project Settings > Player > Other Settings > Identification >
   Bundle Identifier to `artop.oakland.edu`.
5. Ensure all dependencies are installed.
6. Ensure the __Login__ scene is selected.
7. Connect your iOS device.
8. File > Build and run


### Install TextMeshPro

1. In Unity, click Window > Asset Store.
2. In the Asset Store Window, go to the search bar and type "TextMesh Pro".
3. Select the first result that comes up (TextMesh Pro).
4. Scroll down and click the "Import" button.
5. In the "Import Unity Package" window, scroll down and uncheck the "Scenes"
   tick box.
6. Make sure everything else is checked.
7. Click "Import".

### Troubleshooting 

If you built from source and nothing renders on the
Image Target after opening a session and connecting to the session on the Mobile
App, follow these steps:

1. Open the project in Unity.
2. In the Project window pane, select the Assets/Resources folder.
3. Click VuforiaConfiguration.
4. In the Inspector window pane, find the "App License Key" box.
5. If the box is empty, paste the following hash into the box.

```
AfeFN4f/////AAAAmWvCodxwZEKFuzyoDVdX5csviCPTDoyj/NS6dysYO6/8uEGWKEK/vz5CcIm5NV09A/5xJ+j6rJ+ykMaDAjowfF2OXoLCwuZYOdYSG1VF6rWPT/IebP+ImDvmVC20gXx9v0dCNGggSB4wN7EsVeSOTFvDMv+PNsR0EeFTWzpOCTBXu+OuzoAFuRsocuv9pJkSUq8Z2eWb3RwqhYOYGkqwRnxtDYl9N/8x0VDZyW9ttv7A4b7NXuPF7kf4j3c2ONTF4tbQmaYVvXaHbrlEXQeaetvBt4bb1K8mpuTm+978icC2utk3CsrkkbB5ynbC0ccw84kbAnT8hBIUGOe1pMPtWDepUiRy5ErXvemRCVh2ne58
```

6. Rebuild the project to your device.

## Running

1. Connect to the server's IP address.
2. Create a map (picture maybe)
3. Create a session (picture maybe)
  1. The session, once created, will generate a code.
4. Use the mobile app to join the session, given the code.

# Group members

[Joshua Herkness](https://github.com/joshherkness)

[KaJuan Johnson](https://github.com/kdjohnson)

[Johnathan Robertson](https://github.com/jjrobertson14)

[Anthony Hewins](https://github.com/AnthonyHewins)

[Neil Ferman](https://github.com/goeteeks)

[Trevor Luebbert](https://github.com/TrevorLuebbert)

## Future plans

While the application is tailored towards use in tabletop games such as Dungeons
& Dragons (D&D), if the design is also altered, it has implications in fields
such as prototyping and architecture.
