#!/usr/bin/env python3


# EyeZ  - Social Engineering Toolkit app
# Author: Kourva
# GitHub: https://gitub.com/Kourva/EyeZ
#
# Features:
#  - Temporary E-mail service
#  - URL shortener
#  - Valid E-mail check
#
# Works Online with free public APIs
# Version 0.1.1


# All imported Modules
# Basic modules: for basic stuff
import sys
import json
import random
import webbrowser

# Plyer modules: for android functionality
from plyer import vibrator
from plyer import notification
from plyer.utils import platform
from kivy.core.clipboard import Clipboard

# Kivy modules: for the app widgets
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.network.urlrequest import UrlRequest
from kivy.uix.screenmanager import Screen, ScreenManager


# KV config files
# All KV files used in this app
for files in ["mainmenu", "mailmenu", "mailbox", "urlmenu", "mailcheck"]:
    with open("Scripts/%s.kv" % files, "r") as kv:
        Builder.load_string(kv.read())


# ImageButton
# This is for clickable image buttons
class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        pass


# MainMenu class
# This will handle MainMenu stuff
class MainMenu(Screen):
    # Path to Assets
    background = "Assets/background.png"
    font = "Assets/font.ttf"

    # Exit function to exit the app
    def exit_App(self):
        sys.exit()

    # Function for getting your IP address
    def get_ip(self):
        kwargs = {
            "title": "Wait",
            "message": "Getting IP",
            "ticker": "New message",
            "toast": True,
            "app_icon": "Data/notification.png",
        }
        notification.notify(**kwargs)

        try:
            Clock.start_clock()
            req1 = UrlRequest("https://checkip.amazonaws.com", timeout=10)
            while not req1.is_finished:
                Clock.tick()
            Clock.stop_clock()

            result = req1.result
            self.manager.get_screen(
                "MainMenu"
            ).ids.IpAddr.text = (
                f"[ref={result.strip()}][color=00ff00]{result.strip()}[/color][/ref]"
            )
            try:
                vibrator.vibrate(0.1)
            except:
                pass
        except:
            self.manager.get_screen(
                "MainMenu"
            ).ids.IpAddr.text = (
                f"[ref=Are you offline?][color=ff0000]Are you offline?[/color][/ref]"
            )
            try:
                vibrator.vibrate(0.2)
            except:
                pass

    # Function to check exist of email account
    def check_mail(self):
        with open("Data/account.txt", "r") as data:
            lines = data.readlines()
            try:
                addrs = lines[0].split(":")[1].split("\n")[0]
                psswd = lines[1].split(":")[1].split("\n")[0]
                token = lines[2].split(":")[1].split("\n")[0]
                creat = lines[3].split(":", maxsplit=1)[1].split("+")[0]
                dmnnm = lines[4].split(":")[1].split("\n")[0]
                if (
                    addrs == ""
                    or psswd == ""
                    or token == ""
                    or creat == ""
                    or dmnnm == ""
                ):
                    raise
                self.manager.get_screen("MailMenu").ids.MailAddr.text = addrs.strip()
                self.manager.get_screen("MailMenu").ids.CreatedDate.text = creat.strip()
            except:
                self.manager.get_screen("MailMenu").ids.MailAddr.text = "No Account"
                kwargs = {
                    "title": "Error",
                    "message": "Data not found!",
                    "ticker": "New message",
                    "toast": True,
                    "app_icon": "Data/notification.png",
                }
                notification.notify(**kwargs)
                try:
                    vibrator.vibrate(0.1)
                except:
                    pass
                return


# MailMenu class
# This will handle MailMenu stuff
class MailMenu(Screen):
    # Path to Assets
    background = "Assets/background.png"
    font = "Assets/font.ttf"

    # Function to generate email address
    def generate_email(self):
        try:
            # Creating database
            with open("Data/account.txt", "w") as data:
                data.write(
                    "account_addrs:\naccount_psswd:\naccount_token:\naccount_creat:\nacc_mail_name:\n"
                )

            # Step 1 : Creating account and getting domain name
            kwargs = {
                "title": "Step1",
                "message": "Getting domain name",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)
            try:
                vibrator.vibrate(0.1)
            except:
                pass

            # Sends request and waits to finish
            Clock.start_clock()
            req1 = UrlRequest("https://api.mail.tm/domains", timeout=10)
            while not req1.is_finished:
                Clock.tick()
            Clock.stop_clock()

            result = json.loads(req1.result)
            for key, val in result.items():
                if key == "hydra:member":
                    tmp = result[key][0]
                    if tmp["isActive"]:
                        acc_mail_name = tmp["domain"]
                        with open("Data/account.txt", "w") as data:
                            data.write(
                                f"account_addrs:\naccount_psswd:\naccount_token:\naccount_creat:\nacc_mail_name:{acc_mail_name}\n"
                            )

            # Creates random username and password
            # You don't need to password here
            alpha = "abcdefghijklmnopqrstuvwyz"
            addrs = f"{''.join(random.choices(alpha, k=8))}@{acc_mail_name}"
            paswd = "".join(random.choices(alpha, k=8))

            # Sends request and waits to finish
            Clock.start_clock()
            headers = {"Content-type": "application/json"}
            params = {"address": addrs, "password": paswd}
            req2 = UrlRequest(
                "https://api.mail.tm/accounts",
                req_body=json.dumps(params),
                req_headers=headers,
                timeout=10,
            )
            while not req2.is_finished:
                Clock.tick()
            Clock.stop_clock()

            # Saves created date to database
            result = json.loads(req2.result)
            creat = " ".join(result["createdAt"].split("T"))
            with open("Data/account.txt", "w") as data:
                data.write(
                    f"account_addrs:{addrs}\naccount_psswd:{paswd}\naccount_token:\naccount_creat:{creat}\nacc_mail_name:{acc_mail_name}\n"
                )

            # Sends request and waits to finish
            Clock.start_clock()
            req3 = UrlRequest(
                "https://api.mail.tm/token",
                req_body=json.dumps(params),
                req_headers=headers,
                timeout=10,
            )
            while not req3.is_finished:
                Clock.tick()
            Clock.stop_clock()

            # Saves token to database
            # Token is important to get messages
            result = req3.result
            token = result["token"]
            with open("Data/account.txt", "w") as data:
                data.write(
                    f"account_addrs:{addrs}\naccount_psswd:{paswd}\naccount_token:{token}\naccount_creat:{creat}\nacc_mail_name:{acc_mail_name}\n"
                )
                self.manager.get_screen(
                    "MailMenu"
                ).ids.MailAddr.text = f"[color=009AC2]{addrs}[/color]"

            with open("Data/account.txt", "r") as data:
                lines = data.readlines()
                creat = lines[3].split(":", maxsplit=1)[1].split("+")[0]
                self.manager.get_screen("MailMenu").ids.CreatedDate.text = f"{creat}"

            kwargs = {
                "title": "Done",
                "message": "Account is ready",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

        except:
            kwargs = {
                "title": "Error",
                "message": "unexpected error occurred",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

    # Function to load messages when entering inbox menu
    def load_messages(self):
        try:
            # Gets token from database
            with open("Data/account.txt", "r") as data:
                lines = data.readlines()
                try:
                    token = lines[2].split(":")[1].split("\n")[0].strip()
                except:
                    kwargs = {
                        "title": "Error",
                        "message": "No account found!",
                        "ticker": "New message",
                        "toast": True,
                        "app_icon": "Data/notification.png",
                    }
                    notification.notify(**kwargs)
                    return

                # Sends request and waits to finish
                Clock.start_clock()
                req4 = UrlRequest(
                    "https://api.mail.tm/messages",
                    req_headers={"Authorization": f"Bearer {token}"},
                    timeout=10,
                )
                while not req4.is_finished:
                    Clock.tick()
                Clock.stop_clock()

                # Gets number of messages in inbox
                result = json.loads(req4.result)
                messages = result["hydra:totalItems"]
                self.manager.get_screen(
                    "Mailbox"
                ).ids.Inboxmsg.text = (
                    f"Total messages: [color=009AC2]{messages}[/color]"
                )

                # Gets messages
                if messages != 0:
                    prev = ""
                    for message in result["hydra:member"]:
                        msg_from = (
                            "[color=009AC2]From:[/color]\n"
                            + message["from"]["name"]
                            + " - "
                            + message["from"]["address"]
                        )
                        subject = (
                            "[color=009AC2]Subject:\n[/color]" + message["subject"]
                        )
                        intro = "[color=009AC2]Message:[/color]\n" + message["intro"]
                        crnt = (
                            prev + msg_from + "\n" + subject + "\n" + intro + "\n\n\n\n"
                        )
                        prev += crnt
                    self.manager.get_screen("Mailbox").ids.messages.text = crnt
                    return
                self.manager.get_screen(
                    "Mailbox"
                ).ids.messages.text = "Your messages here\n\nNote that you can read simple OTP codes or messages, NOT links"
        except:
            kwargs = {
                "title": "Error",
                "message": "unexpected error occurred",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

    # Function to copy data of created email address
    def copy_email(self):
        try:
            vibrator.vibrate(0.1)
        except:
            pass
        with open("Data/account.txt", "r") as data:
            Clipboard.copy(data.read())
            kwargs = {
                "title": "Copied",
                "message": "Data copied",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)


# Mailbox class
# This will handle Mailbox stuff
class Mailbox(Screen):
    # Path to Assets
    background = "Assets/background.png"
    font = "Assets/font.ttf"

    # Function to refresh the inbox
    def refresh(self):
        with open("Data/account.txt", "r") as data:
            lines = data.readlines()
            try:
                token = lines[2].split(":")[1].split("\n")[0].strip()
            except:
                kwargs = {
                    "title": "Error",
                    "message": "No account found!",
                    "ticker": "New message",
                    "toast": True,
                    "app_icon": "Data/notification.png",
                }
                notification.notify(**kwargs)
                return

            kwargs = {
                "title": "Wait",
                "message": "Checking Inbox",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

            try:
                # Sends request and waits to finish
                Clock.start_clock()
                req4 = UrlRequest(
                    "https://api.mail.tm/messages",
                    req_headers={"Authorization": f"Bearer {token}"},
                    timeout=10,
                )
                while not req4.is_finished:
                    Clock.tick()
                Clock.stop_clock()

                result = json.loads(req4.result)
                messages = result["hydra:totalItems"]
                self.manager.get_screen(
                    "Mailbox"
                ).ids.Inboxmsg.text = (
                    f"Total messages: [color=009AC2]{messages}[/color]"
                )
                if messages != 0:
                    prev = ""
                    for message in result["hydra:member"]:
                        msg_from = (
                            "[color=009AC2]From:[/color]\n"
                            + message["from"]["name"]
                            + " - "
                            + message["from"]["address"]
                        )
                        subject = (
                            "[color=009AC2]Subject:\n[/color]" + message["subject"]
                        )
                        intro = "[color=009AC2]Message:[/color]\n" + message["intro"]
                        crnt = (
                            prev + msg_from + "\n" + subject + "\n" + intro + "\n\n\n\n"
                        )
                        prev += crnt
                    self.manager.get_screen("Mailbox").ids.messages.text = crnt
                    return
                self.manager.get_screen(
                    "Mailbox"
                ).ids.messages.text = "Your messages here\n\nNote that you can read simple OTP codes or messages, NOT links"
            except:
                kwargs = {
                    "title": "Error",
                    "message": "unexpected error occurred",
                    "ticker": "New message",
                    "toast": True,
                    "app_icon": "Data/notification.png",
                }
                notification.notify(**kwargs)


# URLMenu class
# This will handle URLMenu stuff
class URLMenu(Screen):
    # Path to Assets
    background = "Assets/background.png"
    font = "Assets/font.ttf"

    # Function to short the URL
    def short_it(self):
        url = self.manager.get_screen("URLMenu").ids.URL.text.strip()
        if url == "":
            try:
                vibrator.vibrate(0.1)
            except:
                pass
            kwargs = {
                "title": "Error",
                "message": "No URL detected!",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)
            return
        kwargs = {
            "title": "Wait",
            "message": "Please wait...",
            "ticker": "New message",
            "toast": True,
            "app_icon": "Data/notification.png",
        }
        notification.notify(**kwargs)

        try:
            # Sends request and waits to finish
            Clock.start_clock()
            req1 = UrlRequest(
                f"https://short-link-api.vercel.app/?query={url}", timeout=10
            )
            while not req1.is_finished:
                Clock.tick()
            Clock.stop_clock()

            result = req1.result
            try:
                link1 = result["click.ru"]
            except:
                link1 = "No data"

            try:
                link2 = result["da.gd"]
            except:
                link2 = "No data"

            try:
                link3 = result["is.gd"]
            except:
                link3 = "No data"

            try:
                link4 = result["osdb.link"]
            except:
                link4 = "No data"

            self.manager.get_screen(
                "URLMenu"
            ).ids.Link1.text = f"[ref={link1}]{link1}[/ref]"
            self.manager.get_screen(
                "URLMenu"
            ).ids.Link2.text = f"[ref={link2}]{link2}[/ref]"
            self.manager.get_screen(
                "URLMenu"
            ).ids.Link3.text = f"[ref={link3}]{link3}[/ref]"
            self.manager.get_screen(
                "URLMenu"
            ).ids.Link4.text = f"[ref={link4}]{link4}[/ref]"

            # Saves URLs to database
            with open("Data/url.txt", "w") as data:
                data.write(f"{link1}\n{link2}\n{link3}\n{link4}\n")

            kwargs = {
                "title": "Done",
                "message": "Urls Copied!",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

        except:
            kwargs = {
                "title": "Error",
                "message": "unexpected error occurred",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)

    # Function to open Shorted URLs
    # You can open them by clicking on URLs
    def open_url(self, mode):
        with open("Data/url.txt", "r") as data:
            lines = data.readlines()
            link1 = lines[0].split("\n")[0]
            link2 = lines[1].split("\n")[0]
            link3 = lines[2].split("\n")[0]
            link4 = lines[3].split("\n")[0]

        if mode == 1:
            webbrowser.open(link1) if link1 != "No data" else None
        elif mode == 2:
            webbrowser.open(link2) if link2 != "No data" else None
        elif mode == 3:
            webbrowser.open(link3) if link2 != "No data" else None
        elif mode == 4:
            webbrowser.open(link4) if link2 != "No data" else None


# Mail Check class
# This will handle MailCheck menu stuff
class MailCheck(Screen):
    # Path to Assets
    background = "Assets/background.png"
    font = "Assets/font.ttf"

    def check_mail(self):
        e_mail = self.manager.get_screen("MailCheck").ids.E_mail.text.strip()
        kwargs = {
            "title": "Wait",
            "message": f"Checking {e_mail}",
            "ticker": "New message",
            "toast": True,
            "app_icon": "Data/notification.png",
        }
        notification.notify(**kwargs)
        try:
            Clock.start_clock()
            req1 = UrlRequest(f"https://www.disify.com/api/email/{e_mail}", timeout=10)
            while not req1.is_finished:
                Clock.tick()
            Clock.stop_clock()

            result = req1.result
            if result["format"]:
                try:
                    domain = result["domain"]
                except:
                    domain = "No data"
                try:
                    disposable = result["disposable"]
                except:
                    disposable = "No data"
                try:
                    dns = result["dns"]
                except:
                    dns = "No data"
                try:
                    whitelist = result["whitelist"]
                except:
                    whitelist = False

                self.manager.get_screen(
                    "MailCheck"
                ).ids.mailoutput.text = f"[color=00D1f4]We got the data\n\n{domain = }\n{disposable = }\n{dns = }\n{whitelist = }[/color]"
                try:
                    vibrator.vibrate(0.1)
                except:
                    pass
            else:
                self.manager.get_screen(
                    "MailCheck"
                ).ids.mailoutput.text = "[color=ff5500]Invalid format entered for email address\n\nValid emails looks like this: example@domain.com[/color]"
                try:
                    vibrator.vibrate(0.1)
                except:
                    pass

        except:
            try:
                vibrator.vibrate(0.1)
            except:
                pass
            kwargs = {
                "title": "Error",
                "message": "unexpected error occurred",
                "ticker": "New message",
                "toast": True,
                "app_icon": "Data/notification.png",
            }
            notification.notify(**kwargs)


# Main class of the app
class EyeZ(App):
    # Build method
    def build(self):
        # Root screen
        root = ScreenManager()

        # Main menu screen
        self.MainMenu = MainMenu(name="MainMenu")
        root.add_widget(self.MainMenu)

        # Mail menu screen
        self.MailMenu = MailMenu(name="MailMenu")
        root.add_widget(self.MailMenu)

        # Mailbox menu screen
        self.Mailbox = Mailbox(name="Mailbox")
        root.add_widget(self.Mailbox)

        # URLMenu menu screen
        self.URLMenu = URLMenu(name="URLMenu")
        root.add_widget(self.URLMenu)

        # MailCheck menu screen
        self.MailCheck = MailCheck(name="MailCheck")
        root.add_widget(self.MailCheck)

        # Set current screen to main menu and return root
        root.current = "MainMenu"
        return root


# Run App
if __name__ == "__main__":
    eyez = EyeZ()
    eyez.run()

# End Of Script
