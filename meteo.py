#!/usr/bin/python3

# Developer : Hamdy Abou El Anein

# This software use wttr.in, look at https://wttr.in/:help for more information about it.
# you need the easygui and wget library for Python 3.


import wget
from easygui import *  # sudo pip3 install pillow if needed and easygui
import unidecode  # sudo pip3 install unidecode
import os

# Weather result


def weather():
    global city
    if city == None:  # if nothing the default city is Bern
        city = "Bern"
    elif city == "":
        city = "Bern"
    unaccent_city = unidecode.unidecode(
        city
    )  # remove accent and all non-ascii characters
    url = (
        ("http://wttr.in/")
        + str(unaccent_city)
        + str("_Fp_lang=")
        + str(lng)
        + str(".png")
    )
    filename = wget.download(url, out="meteo.png")

    image = "meteo.png"
    msg = "This is the weather report for this location"
    choices = ["Change city"]
    reply = buttonbox(msg, image=image, choices=choices)
    if reply == "Change city":
        location()


# Location selection


def location():
    global city

    filePath = "meteo.png"

    if os.path.exists(filePath):
        os.remove(filePath)
    else:
        print("")
    msg = "Enter a city or a location\n\nBy defautl it's Bern - Switzerland"
    title = "Location"
    default = "Bern"
    city = enterbox(msg, title, default)
    if city == None:  # if nothing the default city is Bern
        city == "Bern"
    elif city == "":
        city = "Bern"
    weather()


# Language selection
def language():
    global lng
    msg = "What is your language ?"
    title = "Languages"
    choices = [
        "English",
        "German",
        "French",
        "Danish",
        "Persian",
        "Indonesian",
        "Italian",
        "Norwegian Bokmål",
        "Dutch",
        "Russian",
        "Afrikaans",
    ]
    choice = choicebox(msg, title, choices)

    if choice == "Afrikaans":
        lng = "af"
    elif choice == "Danish":
        lng = "da"
    elif choice == "German":
        lng = "de"
    elif choice == "French":
        lng = "fr"
    elif choice == "Persian":
        lng = "fa"
    elif choice == "Indonesian":
        lng = "id"
    elif choice == "Italian":
        lng = "it"
    elif choice == "Norwegian Bokmål":
        lng = "nb"
    elif choice == "Dutch":
        lng = "nl"
    elif choice == "Russian":
        lng = "ru"
    elif choice == None:  # if nothing it's english
        lng = "en"
    else:
        lng = "en"  # Default is english

    location()


language()
