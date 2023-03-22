<p align="center">
    <img align="left" src="https://user-images.githubusercontent.com/118578799/227053923-2e51426c-f0c2-4e66-a748-0ee0466c8dc7.png" width=120 heigth=120 />
    <h1> EyeZ </h1>
    <p><b> Social Engineering Toolkit app | URL shortener &amp;&amp; Temporary E-mail service</b></p>
</p>


<br><br>

### ▍Features
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Temporary E-mail service <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ URL shortener <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ E-mail Checker <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Works Online with free public APIs <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Version 0.1.1

### ▍Issues & Next features
Will be fixed or added in next updates! <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Can't check the valid url for now <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Can't use verify links from mailbox (only OTP or messages for now) <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ App dark Theme is already cool but it can be better i think <br>
&nbsp;&nbsp;&nbsp;&nbsp; ▣ ~~App may crash due to slow internet connection (request timeout will fix it)~~

### ▍Idea?
So this app works online with public APIs. if you have any idea to add let me know in [Issues](https://github.com/Kourva/EyeZ/issues).

# Setup
#### ⒈ Clone the repository
```bash
git clone https://github.com/Kourva/EyeZ.git
```
#### ⒉ Navigate to Eyez directory
```bash
cd EyeZ
```
#### ⒊ Install the requirements
```bash
chmod +x Lib/install.sh && ./Lib/install.sh
```
#### ⒋ Install python-dbus for notification (optional)
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Debian based
```bash
sudo apt install python-dbus
```
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Arch based
```bash
sudo pacman -S python-dbus
```
#### ⒌ run the app
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Normally
```bash
python main.py
```
&nbsp;&nbsp;&nbsp;&nbsp; ▣ Specific phone
```
python main.py -m screen
```

