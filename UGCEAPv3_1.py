from optparse import Values
from tkinter.tix import IMAGE
import webbrowser
import pyperclip
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import chromedriver_binary
import time
import os
import io
from PIL import Image
import cloudscraper
import random as r
import PySimpleGUI as sg
import chromedriver_autoinstaller

from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows


#-------------webdriver auto install before every start-------------

chrome_service = ChromeService(ChromeDriverManager().install())
chrome_service.creationflags = CREATE_NO_WINDOW
options = webdriver.ChromeOptions()
options.headless = True


driver = webdriver.Chrome(service=chrome_service, options=options)



#driver = webdriver.Chrome(options=option, service=chrome_service)

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

    if check_exists_by_xpath("//*[@id='steamids']") == True:

        foundstuff = driver.find_element(By.ID, "steamids").text
    
    else:
        return "Error"

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

    #pyperclip.copy(finalized)

    return finalized

#-------------List a players bans from sourcebans-------------

def bans(id, webpage):

    #-------------Define and get the webpage-------------

    #webpage = r"https://ugc-gaming.net/sourcebans/index.php"

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

def comms(id, webpage):

    #-------------Define and get the webpage-------------

    #webpage = r"https://ugc-gaming.net/sourcebans/index.php"

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


#-------------start tf2-------------

def tf2():

    webbrowser.open('steam://run/440')

#-------------connect to a server by ip-------------

def connect(ip):
    if ip != " " or "":
        webbrowser.open('steam://connect/' + ip)

#-------------Get a random fake name-------------

def fakeName():
    website = r'https://www.spinxo.com/gamertags'
    driver.get(website)
    button = driver.find_element(By.CLASS_NAME, "spin")
    button.click()

    time.sleep(5)

    namenum = r.randint(1,30)

    name = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[1]/div[4]/div[1]/div/ul/li[{}]/a".format(namenum)).get_attribute('textContent')

    #print("\n your generated name is: ", name, ", and it has been added to your clipboard!")

    pyperclip.copy(name)

    return name

#--------------------------serverlist----------------------------

def serverlist():
    webpage = r"https://ugc-gaming.net/servers/tf2/"

    driver.get(webpage)

    serverlist = []

    servernum = 2
    
    while servernum != 74:
        if 'Copy' in driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]'.format(servernum)).get_attribute('textContent'):
            servername = driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]/td[1]'.format(servernum)).get_attribute('textContent')
            serverplayers = driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]/td[2]'.format(servernum)).get_attribute('textContent')
            maxplayers = driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]/td[3]'.format(servernum)).get_attribute('textContent')
            map = driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]/td[4]'.format(servernum)).get_attribute('textContent')
            IP = driver.find_element(By.XPATH, '//*[@id="servers"]/tbody/tr[{}]/td[5]'.format(servernum)).get_attribute('textContent').replace(" ", "")

            finalserver = servername + "   " + serverplayers + " / " + maxplayers + "   " + map + " " + IP
        
            serverlist.append(finalserver)

            servernum += 1
        else:
            servernum += 1
    
    return serverlist

#------------------------------------------------------DEEP PLAYER INFO------------------------------------------------------

def deepinfo(url):

    steamid = steamID(url)

    time.sleep(2)

    avatar = driver.find_element(By.XPATH, "//*[@id='profileavatar']/img").get_attribute('src')

    url = avatar
    jpg_data = (
        cloudscraper.create_scraper(
           browser={"browser": "firefox", "platform": "windows", "mobile": False}
        )
        .get(url)
        .content
    )

    imgsize = (100, 100)

    pil_image = Image.open(io.BytesIO(jpg_data)).resize(imgsize)
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()

    time.sleep(7)

    joined1 = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[3]/table/tbody/tr[1]").get_attribute('textContent')
    steamlvl = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[3]/table/tbody/tr[2]").get_attribute('textContent')
    privacy = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[4]/table/tbody/tr[1]").get_attribute('textContent')
    tradeban = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[4]/table/tbody/tr[2]").get_attribute('textContent')
    vacban = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[4]/table/tbody/tr[3]").get_attribute('textContent')
    communityban = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[3]/div[2]/div[2]/div[4]/table/tbody/tr[4]").get_attribute('textContent')
    name = driver.find_element(By.XPATH, "//*[@id='steamname']").get_attribute('textContent')

    return name, png_data, steamid, joined1, steamlvl, privacy, tradeban, vacban, communityban



#------------------------------------------------------GUI------------------------------------------------------

size1 = (700, 200)

sg.theme('DarkGrey15')

header = [[sg.Text("UGC Admin Panel V3.1", font="Arial 20", auto_size_text=True, justification='center')]]

about = [[sg.Text("Made by Forest \n Language used: Python", size=(20, 2))]]

col1 = [[sg.Button("Launch Team Fortress 2", key="Launch Team Fortress 2", size=(30, 1)), sg.Button("Generate a fake name", key="fake", size=(30, 1))],
        [sg.Text("Starts Team Fortress 2", size=(30, 2), justification='center'), sg.Text("Your fake name", size=(30, 2), key="fakeName", justification='center')],
        [sg.Text("_" * 110)],
        [sg.Input(key="profileIn", size=(35, 1)), sg.Button("Get Steam ID", key="submiturl", size=(20, 1))],
        [sg.Text("Output", key="OutputID", size=(30, 2)), sg.Text("Use STEAM URL")]]

col2 = [[sg.Input("", size=(30, 1), key="deepin"), sg.Button("Request profile info", size=(30, 1), key="getinfo")],
        [sg.Text("STEAM URL/ID32", size=(27, 1), justification='center')],
        [sg.Text("_" * 110)],
        [sg.Image(data="", key="avatar"), sg.Text(key="infooutput1", size=(30,6)), sg.Text(key="infooutput2", size=(30,6))]]

col3 = [[sg.Input(size=(35, 1), key="IDinput"), sg.Button("Check Sourcebans", size=(30, 1), key="Bans")],
        [sg.Text("STEAM URL/ID32", size=(30, 1), justification='center')],
        [sg.Text("")],
        [sg.Text("Total Bans:", key="totalbans")],
        [sg.Text("_" * 110)],
        [sg.Text("Bans", font="Arial 15")],
        [sg.Text("", key="bansout")],
        [sg.Text("")],
        [sg.Text("Comms", font="Arial 15")],
        [sg.Text("", key="comsout")]]

col4 = [[sg.Button("Request server list", size=(20, 1), key="serverReq"), sg.Button("Join server", size=(20, 1), key="serverJoin"), sg.Text("", size=(10, 1)), sg.Input(key="inIP", size=(20, 1)), sg.Text("UDP/IP")],
        [sg.Text("List available servers", size=(20, 1), justification='center'), sg.Text("Join selected server", size=(20, 1), justification='center'), sg.Text("", size=(13, 1)), sg.Button("Join by IP", size=(20, 1), key="JoinIP")],
        [sg.Text("_" * 110)],
        [sg.Listbox(values="", default_values="Servers", size=(96, 23), key="serversOut")]]

layout = [
    [sg.Frame("", [[sg.Column(header)]]),sg.Text("", size=(114, 1)), sg.Frame("", [[sg.Column(about)]])],
    [sg.Frame("Essentials", [[sg.Column(col1, size=size1)]]),
    sg.Frame("Deep Player Info", [[sg.Column(col2, size=size1)]])],

    [sg.Frame("Sourcebans", [[sg.Column(col3, size=(700, 500))]]),
    sg.Frame("Server List", [[sg.Column(col4, size=(700, 500))]])]
    
    ]

window = sg.Window("UGC Admin Panel V3.1", layout, margins=(1, 1), finalize=True)

#---------------------Run window---------------------

while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

#---------------------Run TF2------------------------

    if event == 'Launch Team Fortress 2':
        tf2()

#---------------------Comms--------------------------

    elif event == "Bans":
        ID = values["IDinput"]

        rServer = "https://ugc-gaming.net/sourcebans/index.php"

        rID = steamID(ID)

        out = comms(rID, rServer)

        window["comsout"].update("\n".join(out))

#-----------------------Bans------------------------*

        time.sleep(1)

        out2 = bans(rID, rServer)

        window["bansout"].update("\n".join(out2))
    
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

        pyperclip.copy(ID)

        window["OutputID"].update(ID + " \n(on clipboard)")

#------------------------Server req--------------------------

    elif event == "serverReq":

        serverslist = serverlist()

        window["serversOut"].update(serverslist)

#------------------------Server join--------------------------

    elif event == "serverJoin":

        if len(window["serversOut"].get()) != 0:
            b = window["serversOut"].get()

            a = b[0].split(" ")[-1]

            webbrowser.open('steam://connect/' + a)


#------------------------server by ip--------------------------

    elif event == "JoinIP":

        if values["inIP"] != "":

            ip = values["inIP"]

            connect(ip)

#------------------------Exit panel--------------------------

    elif event == "Exit":
        driver.close()
        break

#------------------------deep player search--------------------------

    elif event == "getinfo":

        if values["deepin"] != "":

            url = window["deepin"].get()

            result = deepinfo(url)

            window["avatar"].update(data=result[1])

            window["infooutput1"].update("Name: " + result[0] + '\n' +
                                        result[2].replace('\n', '') + '\n' +
                                        result[3].replace('\n', '') + '\n' +
                                        result[4].replace('\n', '') + '\n' +
                                        result[5].replace('\n', '') + '\n')
            
            window["infooutput2"].update(result[6].replace('\n', '') + '\n' +
                                        result[7].replace('\n', '') + '\n' +
                                        result[8].replace('\n', '') + '\n')