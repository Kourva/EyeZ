<p align="center">
    <img align="left" src="https://user-images.githubusercontent.com/118578799/224209203-f9ced760-7111-4f32-9aec-073eb893dfd8.png" width=150 heigth=150 />
    <h1> EyeZ </h1>
    <p><b> Social Engineering Toolkit app | URL shortener &amp;&amp; Temporary E-mail service</b></p>
</p>

<br><br>

# About The app
### Features:
+ Temporary E-mail service
+ URL shortener
+ Works Online with free public APIs <br>
+ Version 0.0.0 (demo)

### Issues:
Will be fixed in next updates!
+ Can't check the valid url for now
+ Can't use verify links from mailbox (only OTP for now)
+ App may crash due to slow internet connection (request timeout will fix it)

### Idea?
so this app works online with public APIs. if you have any idea to add let me know in 'Issues' section in repository

# Setup
#### Clone the repository
```bash
git clone https://github.com/Kourva/EyeZ.git
```
#### navigate to Eyez
```bash
cd EyeZ
```
#### install the requirements
```bash
chmod +x Lib/install.sh && ./install.sh
```
#### install python-dbus for notification (optional)
+ Debian based
```bash
sudo apt install python-dbus
```
+ Arch based
```bash
sudo pacman -S python-dbus
```
#### run the app
+ Normally
```bash
python main.py
```
+ Specific phone
```
python main.py -m screen
```

