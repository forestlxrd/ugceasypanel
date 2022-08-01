import webbrowser
import pyperclip
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
import time
import os
import random as r

import PySimpleGUI as sg

project_dir = os.path.dirname(__file__) + '\\' + "variableStoringFile.dat"

dataloc = project_dir

#-------------webdriver auto install before every start-------------

option = webdriver.ChromeOptions()
option.add_argument('headless')
option.add_argument('--log-level=3')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

#-------------check if xpath exists in HTML-------------

def check_exists_by_xpath(xpath):
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

#-------------Get the steam ID by steam profile URL-------------

def steamID(searchterm):

    if searchterm == "":
        return "No input given"

    #-------------Define and get the webpage-------------

    webpage = r"https://steamrep.com"

    driver.get(webpage)

    #-------------search and submit the terms-------------

    sbox = driver.find_element(By.ID, "findid")
    sbox.send_keys(searchterm)

    submit = driver.find_elements(By.TAG_NAME, "input")[1]
    submit.click()

    #-------------get back the results-------------

    foundstuff = driver.find_element(By.ID, "steamids").text

    finalizer = foundstuff.replace('\n', '')

    #-------------from the results, find the ID-------------

    result1 = finalizer.find("steamID32:")

    num = len("steamID32: ")

    index = result1 + num

    finalid = []

    while finalizer[index] != ' ':
        finalid.append(finalizer[index])
        index += 1


    finalized = ' '.join(finalid).replace(' ', '').replace('|', '')

    #-------------Copy the ID to the clipboard-------------

    pyperclip.copy(finalized)

    return finalized

#-------------List a players bans from sourcebans-------------

def bans(id):

    #-------------Define and get the webpage-------------

    webpage = r"https://ugc-gaming.net/sourcebans/index.php"

    driver.get(webpage)

    #-------------Input the steam ID into BANS-------------

    sboxbans = driver.find_elements(By.CLASS_NAME, "searchbox")[0]
    sboxbans.send_keys(id)

    bansubmit = driver.find_elements(By.NAME, "Submit")[0]
    bansubmit.click()

    #-------------get the items we found on the webpage-------------

    #-------------BAN 1-------------

    bans = []

    n = 3

    if check_exists_by_xpath("//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)) == True:

        while check_exists_by_xpath("//*[@id='banlist']/table/tbody/tr[{}]".format(n)) == True:

            check = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)).get_attribute('textContent')

            if "Web Ban" in check:
                ban1reason = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[10]/td[2]".format(n)).get_attribute('textContent')
            else:
                ban1reason = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)).get_attribute('textContent')
            ban1date= driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[7]/td[2]".format(n)).get_attribute('textContent')
            ban1lenght= driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[8]/td[2]".format(n)).get_attribute('textContent')

            ban1 = "Player banned on: " + ban1date + " | with reason: " + ban1reason + " | for " + ban1lenght.strip()

            n = n+2

            bans.append(ban1)

    else:
        bans.append("No bans")

    return bans

#-------------List a players communication blocks from sourcebans-------------

def comms(id):

    #-------------Define and get the webpage-------------

    webpage = r"https://ugc-gaming.net/sourcebans/index.php"

    driver.get(webpage)

    #-------------Input the steam ID into BANS-------------

    sboxbans = driver.find_elements(By.CLASS_NAME, "searchbox")[1]
    sboxbans.send_keys(id)

    bansubmit = driver.find_elements(By.NAME, "Submit")[1]
    bansubmit.click()

    #-------------get the items we found on the webpage-------------

    #-------------COMMS 1-------------

    mutes = []

    n = 3

    if check_exists_by_xpath("//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)) == True:

        while check_exists_by_xpath("//*[@id='banlist']/table/tbody/tr[{}]".format(n)) == True:

            check = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)).get_attribute('textContent')

            if "Web Ban" in check:
                ban1reason = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[10]/td[2]".format(n)).get_attribute('textContent')
            else:
                ban1reason = driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[12]/td[2]".format(n)).get_attribute('textContent')

            ban1date= driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[7]/td[2]".format(n)).get_attribute('textContent')
            ban1lenght= driver.find_element(By.XPATH, "//*[@id='banlist']/table/tbody/tr[{}]/td/div/table/tbody/tr[8]/td[2]".format(n)).get_attribute('textContent')

            mute1 = "Player muted/gagged on: " + ban1date + " | with reason: " + ban1reason + " | for " + ban1lenght.strip()

            n = n+2

            mutes.append(mute1)

    else:
        mutes.append("No mutes")

    return mutes

#-------------List the tf2 servers from a website-------------
#-------------start tf2-------------

def tf2():

    webbrowser.open('steam://run/440')

#-------------connect to a server by ip-------------

def connect(ip):
    webbrowser.open('steam://connect/' + ip)

#-------------Get a random fake name-------------

def fakeName():
    website = r'https://www.spinxo.com/gamertags'
    driver.get(website)
    button = driver.find_element(By.CLASS_NAME, "spin")
    button.click()

    time.sleep(3)

    namenum = r.randint(1,30)

    name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[4]/div[1]/div/ul/li[{}]/a".format(namenum)).get_attribute('textContent')

    print("\n your generated name is: ", name, ", and it has been added to your clipboard!")

    pyperclip.copy(name)

    return name

#--------------------------serverlist----------------------------

def serverlist():
    webpage = r"https://ugc-gaming.net/servers/tf2/"

    driver.get(webpage)
    servernum = 2
    storedserverlist = []
    serverlip = []
    fullservername = []

    while servernum < 72:
        time.sleep(0.1)
        server = driver.find_element(By.XPATH, "//*[@id='servers']/tbody/tr[{}]".format(servernum)).get_attribute('textContent')
        if 'Copy' in server:
            finalserver = ('\n' + " ".join(server.split()).replace('Copy', ''))

            storedserverlist.append(finalserver)

            #print(finalserver)

            serverlip.append(finalserver.split()[-1])

            fullservername.append(finalserver)

            servernum += 1
        else:
            servernum += 1

    return storedserverlist


#------------------------------------------------------GUI------------------------------------------------------

sg.theme('DarkGrey15')
layout = [[sg.Text("UGC Easy Admin Panel V2", text_color="orange", font="Arial, 25 bold", justification="center", expand_x=True )],
            [sg.Text("")],
            [sg.Button('Launch Team Fortress 2', size=(20, 1)), sg.Button('Generate a fake name', key="fake", size=(20, 1)), sg.Button('Open sourcebans website', key="sourcebans", size=(20, 1))],
            [sg.Text("Starts TF2", size=(20, 1)), sg.Text(key="fakeName", size=(20, 2), text="Generates a name"), sg.Text(size=(20, 2), text="Opens sourcebans in a new tab")],
            [sg.Text("")],
            [sg.Text("Sourcebans", font="Arial, 20 bold", size=(16, 1)), sg.Text("Steam ID", font="Arial, 20 bold", size=(21, 1)), sg.Text("Servers", font="Arial, 20 bold", size=(16, 1))],
            [sg.Text("ID/URL"), sg.Input(key="IDinput", do_not_clear=False, size=(29, 1)), sg.Text(""), sg.Input(key="profileIn", do_not_clear=False, size=(29, 1)), sg.Text("profile url to\n steamID", font="Arial, 10 italic")],
            [sg.Button("Comms", pad="50, 0", size=(15, 1)), sg.Button("Bans", pad="50, 0", size=(15, 1)), sg.Text(""), sg.Button("Submit", pad="50, 0", size=(25, 1), key="submiturl"),sg.Text("", size=(70, 1)), sg.Text("Input the IP below")],
            [sg.Text("", size=(35, 1)), sg.Text(key="OutputID", size=(25, 2)), sg.Text("", size=(17, 1)), sg.Button("Get server list", key="serverReq", size=(15, 1)), sg.Button("Join selected server", key="serverJoin", size=(15, 1)), sg.Button("Join server by IP", key="JoinIP", size=(15, 1)), sg.Input(key="inIP", size=(20, 1))],
            [sg.Text(key="Output", size=(80, 20)), sg.Listbox(key="serversOut", values="", size=(100, 20), text_color="white")],
            [sg.Text("Total:", size=(80, 1), key="totalbans"), sg.Text("Note: every function in the panel will take some time to load, since it has to reach the websites. If the desired server is not in the servers list, try again by requesting the list again.", font="Arial, 8 italic", size=(100, 2))],
            [sg.Button("Clear", key="Clear"), sg.Text("", size=(160, 1)), sg.Button("Exit panel", key="Exit", button_color="red")]]

window = sg.Window('UGC Easy Admin Panel V2', layout)

#---------------------Run window---------------------

while True:

    event, values = window.read()

#---------------------Run TF2------------------------

    if event == 'Launch Team Fortress 2':
        tf2()

#---------------------Comms--------------------------

    elif event == "Comms":
        ID = values["IDinput"]
        rID = steamID(ID)

        out = comms(rID)

        window["Output"].update("\n".join(out))

        window["totalbans"].update("Total: " + str(len(out)))

#-----------------------Bans-------------------------

    elif event == "Bans":
        ID = values["IDinput"]
        rID = steamID(ID)

        out = bans(rID)

        window["Output"].update("\n".join(out))
    
        window["totalbans"].update("Total: " + str(len(out)))

#---------------------Clear window--------------------------

    elif event == "Clear":
        window["Output"].update("")

#------------------------Fake name--------------------------

    elif event == "fake":
        fake = fakeName()
        window["fakeName"].update(fake + " \n(on clipboard)")

#------------------------Steam ID--------------------------

    elif event == "submiturl":

        url = values["profileIn"]

        ID = steamID(url)

        window["OutputID"].update(ID + " \n(on clipboard)")

#------------------------Server req--------------------------

    elif event == "serverReq":

        serverslist = serverlist()

        window["serversOut"].update(serverslist)

#------------------------Server join--------------------------

    elif event == "serverJoin":

        a = window["serversOut"].get()

        a = a[0].split(" ")[-2]

        webbrowser.open('steam://connect/' + a)

#------------------------server by ip--------------------------

    elif event == "JoinIP":

        if values["inIP"] != "":

            ip = values["inIP"]

            connect(ip)

#------------------------Exit panel--------------------------

    elif event == "Exit":
        break

#------------------------Open sourcebans--------------------------

    elif event == "sourcebans":
        webbrowser.open('https://ugc-gaming.net/sourcebans/index.php')
