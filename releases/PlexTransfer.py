from os import system, getenv
from time import sleep
import json

localdir = getenv('LOCALAPPDATA') + "\\Plex Transfer\\options.json"


def watermark():
    system('cls')
    print("\033[4;34;40mPlex Transfer by Gullen \033[0;37;40m")
    print()

def setup():
    watermark()

    # Check First Time Setup
    try:
        dataFile = open(localdir, 'r')
        data = getData(dataFile)
    except Exception:
        firstTimeSetup()

    print("Please select one of the options below \n")

    # Option Selector
    print("1 : Transfer Movie")
    print("2 : Transfer Series")
    print("3 : Options")
    print("4 : Exit")
    selector = input("> ")
    print()

    # Options
    if selector == "1":
        transferMovie(data)
    elif selector == "2":
        print()
        print("\033[1;31;40m Option is currently not supported...")
        sleep(3)
    elif selector == "3":
        options(data)
    elif selector == "4":
        pass
    else:
        invalidOption()
        setup()
    setup()

def firstTimeSetup():
    watermark()

    print("\033[1;31;40m")
    print("It looks like this is your first time running Plex Transfer")
    print("We just need to setup a few options...\033[1;37;40m")

    # Ask options
    print()
    print("What is your server username? (Case Sensitive!)")
    username = input("> ")
    print()
    print("What is your server's address?")
    addr = input("> ")
    print()
    print("Where is the location of your plex \033[1;32;40mmovies\033[1;37;40m directory?")
    movies = input("> ")
    print()
    print("Where is the location of your plex \033[1;32;40mseries\033[1;37;40m directory?")
    series = input("> ")

    # Display options
    print()
    print()
    print("\033[1;33;40m")
    print("======== S A V E D  D A T A ======")
    print("Server Username: " + username)
    print("Server Address: " + addr)
    print("Movies Directory Location: " + movies)
    print("Series Directory Location: " + series)
    print()
    print("\033[0;37;40m")
    print("If any details are incorrect, please change them in the options setting")
    print()
    print("\033[1;30;40mPress enter to start again")
    input()

    # Write settings
    data = {"username":username, "address":addr, "movies":movies, "series":series}
    json_string = json.dumps(data)
    saveData(json_string)

    setup()


def getData(file):
    data = json.load(file)
    return data


def options(data):
    watermark()

    # Info
    print("Settings location: " + localdir + "\n")
    printData(data)

    # Option Selector
    print("Please select one of the options below \n")

    print("1: Change Server Username")
    print("2: Change Server Address")
    print("3: Change Movies Location")
    print("4: Change Series Location")
    print("5: Back To Menu")
    selector = input("> ")

    # Options
    print()

    if selector == "1":
        changeData("username", data)
    elif selector == "2":
        changeData("address", data)
    elif selector == "3":
        changeData("movies", data)
    elif selector == "4":
        changeData("series", data)
    elif selector == "5":
        setup()
    else:
        invalidOption()
        options(data)
    setup()


def changeData(toBeChanged, data):
    # Get Question
    if toBeChanged == "username":
        question = "Server Username"
    elif toBeChanged == "address":
        question = "Server Address"
    elif toBeChanged == "movies":
        question = "Movies Location"
    else:
        question = "Series Location"

    # Save choice
    print()
    print("Please enter the new " + question)
    new = input("> ")

    data[toBeChanged] = new
    json_string = json.dumps(data)
    saveData(json_string)

    system('cls')
    print("Changed saved successfully!")
    print()
    printData(data)
    print("\033[1;30;40mPress enter to continue\033[0;37;40m")
    input()


def transferMovie(data):
    system("cls")
    watermark()
    printData(data)

    print("Please give the full location of the movie to transfer")
    loc = input("> ")

    print("\n====== T R A N S F E R R I N G   M O V I E======\033[1;36;40m \n")
    scp(loc, "movies", data)

def scp(file, opt, data):
    command =\
        "scp " + file + " " + data["username"] + "@" + data["address"] + ":" + data[opt]
    print(command)
    system(command)
    print()
    print("\033[1;33;40m Movie Transferred successfully!")
    print("Press Enter To Continue!")
    input()
    setup()

def saveData(data):
    file = open(localdir, 'w')
    file.write(data)
    file.close()


def printData(data):
    print("\033[1;33;40m====== C U R R E N T  S E T T I N G S ======")
    print("Server Username: " + data["username"])
    print("Server Address: " + data["address"])
    print("Movies Location: " + data["movies"])
    print("Series Location: " + data["series"])
    print("\033[0;37;40m \n")


def invalidOption():
    print("\033[1;31;40mUnknown option selected!")
    print("Please try again...\033[1;37;40m")
    sleep(3)

setup()