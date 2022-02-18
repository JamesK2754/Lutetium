import mysql.connector
from datetime import datetime
from os import system
from platform import system as syscheck
from yourls import YOURLSClient

match syscheck():
    case ("Linux"|"Darwin"):
        clear = system("clear")
    case "Windows":
        clear = system("cls")
    case _:
        print("WARNING: We could not determine what OS you are using and so cannot select the appropriate"
              " clear command. We have defaulted to Linux/Darwin 'clear'.")
        clear = system("clear")

mydb = mysql.connector.connect(host="",
                               user='',
                               passwd="",
                               database="Lutetium"
                              )
curs = mydb.cursor()
day = datetime.now().strftime("%d/%m/%Y")
YRLS = YOURLSClient("", signature='')
V = 2.0
def getitems(id):
    if id == "*":
        curs.execute(f"SELECT * FROM `files`")
        return curs.fetchall()
    else:
        curs.execute(f"SELECT * FROM `files` WHERE dlID = {id}")
        return curs.fetchone()


def additem(name, url, hideURL, type):
    if hideURL:
        url = YRLS.shorten(url, title=name).shorturl
    curs.execute("INSERT INTO `files` (dlName, dlURL, Type, Status, dateAdded) VALUES (%s,%s,%s,%s,%s)", (name, url, type, 0, day))
    mydb.commit()

def alteritem(mode, itemid, *arg):
    match mode:
        case "r":
            curs.execute(f"DELETE FROM `files` WHERE `dlID` = {itemid}")
        case "e_u":
            arg = arg[0]
            curs.execute(f"UPDATE `files` SET `dlURL` = '{arg}' WHERE `dlID` = {itemid}")
        case "e_n":
            arg = arg[0]
            curs.execute(f"UPDATE `files` SET `dlName` = '{arg}' WHERE `dlID` = {itemid}")
        case "e_t":
            arg = arg[0]
            curs.execute(f"UPDATE `files` SET `Type` = '{arg}' WHERE `dlID` = {itemid}")
    mydb.commit()

def mainrun():
    running = True
    while running:
        clear
        print("Welcome to Lutetium\nBy James King")
        print('''Please select one of the following options:
    1) Add item
    2) View list
    3) Alter item
    4) About
    5) Exit''')
        selecting = True
        while selecting:
            mmChoice = int(input("[Lu]> "))
            match mmChoice:
                case 1:
                    selecting = False
                    dlName = input("DL name: ")
                    dlLink = input("DL link: ")
                    shortnerBool = bool(input("Would you like to hide the URL by using a shortener? (bool) "))
                    dlMethod = int(input("Select a download method, (0) wget | (1) YTDL: "))
                    additem(dlName, dlLink, shortnerBool, dlMethod)
                    input("Done!")
                case 2:
                    selecting = False
                    print(f"There are currently {len(getitems('*'))} on the database:")
                    print("DLID | Name - Type - Link - Status")
                    for item in getitems("*"):
                        if item[3] == 1:
                            type = "YTDL"
                        elif item[3] == 0:
                            type = "wget"
                        if item[4] == 1:
                            status = "Downloaded"
                        elif item[4] == 0:
                            status = "Awaiting"
                        elif item[4] == 2:
                            status = "An error occurred while downloading"
                        print(f"{item[0]} | {item[1]} - {type} - {item[2]} - {status}")
                    input()
                case 3:
                    selecting = True
                    print("Please enter the ID of the item you wish to edit")
                    while selecting:
                        targID = int(input("[Lu]> "))
                        item = getitems(targID)
                        if item != None:
                            selecting=False
                        else:
                            print("That item was not found on the DB, please try again.")
                    selecting = True
                    print("Please select an option:\n1) Edit Name\n2) Edit URL\n3) Remove\n4) Cancel")
                    while selecting:
                        match int(input("[Lu]> ")):
                            case 1:
                                selecting = False
                                new_name = input(f"{item[1]} or: ") or item[1]
                                alteritem("e_n", targID, new_name)
                            case 2:
                                selecting = False
                                new_url = input(f"{item[2]} or: ") or item[2]
                                alteritem("e_u", targID, new_url)
                            case 3:
                                selecting = False
                                if int(input(f"Are you sure you want to remove '{item[1]}' from the DB? (1/0) ")) == 1:
                                    alteritem("r", targID)
                                    input("Done!")
                                else:
                                     input("Deletion canceled.")
                            case 4:
                                selecting = False
                            case _:
                                print("Choice invalid")
                case 4:
                    selecting = False
                case 5:
                    selecting = False
                    if input("Are you sure you want to exit? ").upper in ["Y", "YES"]:
                        exit()


if __name__ == "__main__":
    mainrun()
