import sys
import time
import re
import subprocess
from os import system
import os
import math
sys.stdout.flush()
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions()
#options.headless = True
options.add_argument(" --mute-audio")
options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36")
system("title SimpleMMO")



def SellsManeger():
    driver.get("https://simple-mmo.com/inventory")
    if ("Inventory Total" in driver.page_source):
        driver.find_element_by_xpath('/html/body/div[1]/main/a[2]/div/i').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[5]/div[1]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[5]/div[2]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[6]/div[2]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[6]/div[3]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[7]/div[1]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[7]/div[3]/label/label/span').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[8]/div[2]/label/label/label').click()
        driver.find_element_by_xpath('//*[@id="swal2-content"]/form/div[1]/div/input').submit()
        result = re.findall('id="item-(.*)-block"', driver.page_source)
        print(result)
        for ItemNum in result:
            driver.find_element_by_id("item-" + ItemNum + "-block").click()
            try:
                rgb = driver.find_element_by_xpath('//*[@id="swal2-content"]/div[2]/strong/i').get_attribute("style")
                r, g, b = map(int, re.search(
                    r'rgb\((\d+),\s*(\d+),\s*(\d+)', rgb).groups())
                color = '#%02x%02x%02x' % (r, g, b)
            except:
                print("Color not found")

            if color == "#c0392b":
                print(str(datetime.now()) + " Lower item found")
                driver.find_element_by_xpath('//*[@id="swal2-content"]/div[4]/div[3]/div[1]/a').click()
                time.sleep(3)
                results = re.search('15px"> (.*)</span><br>Lowest price', driver.page_source)
                while results == None:
                    results = re.search('15px"> (.*)</span><br>Lowest price', driver.page_source)
                print(str(datetime.now()) + " Average price: " + results.group(1))
                CleanPrice = results.group(1).replace(",","")
                NewPrice = int(CleanPrice) * 1.2
                FinallPrice = math.trunc(NewPrice)
                elem = driver.find_element_by_name("quantity")
                elem.clear()
                elem.send_keys(str(FinallPrice))
                driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/button[1]').click()
                time.sleep(2)
                if ("The item has been submitted to the market. It may take a few minutes for it to appear." in driver.page_source):
                    print(str(datetime.now()) + " Item sold for: " + str(FinallPrice))
                    time.sleep(3)
                    driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/button[1]').click()

            if color == "#2ecc71":
                print(str(datetime.now()) + " Higher item found, We will Equip this item")
                driver.find_element_by_xpath('//*[@id="swal2-content"]/div[4]/a').click()
                if ("The item has been equipped." in driver.page_source):
                    print(str(datetime.now()) + " Item Equip successfully")
    global StepsCounter
    StepsCounter = 0
    Bank()

def Bank():
    print(str(datetime.now()) + " Desposit to Bank")
    driver.get("https://simple-mmo.com/bank/deposit?new_page=true")
    if ("Your current bank account balance is" in driver.page_source):
        driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div/div/div[3]/form/a[1]').click()
        driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div/div/div[3]/form/button').click()
        time.sleep(1)
        if ("You have successfully deposited your gold" in driver.page_source):
            print(str(datetime.now()) + " Deposited successfully")
    TaskManeger()

def Attack():
    print(str(datetime.now()) + " Battle Found!")
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div/div/div/div[3]/div[3]/a[1]').click()
    print(str(datetime.now()) + " Start attack")
    while driver.find_element_by_id("attackButton").is_enabled():
        driver.find_element_by_id("attackButton").click()
        time.sleep(4)
    if ("You have won" in driver.page_source):
        print(str(datetime.now()) + " Done attack, Back to TaskManeger")
        driver.get("https://simple-mmo.com/travel")
        time.sleep(5)
        TaskManeger()

def Gathering():
    print(str(datetime.now()) + " Found Elements!")
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div/div/div/div[3]/div[3]/a[1]').click()
    for x in range(15):
            try:
                ActionChains(driver).click_and_hold(driver.find_element_by_xpath('//*[@id="action_button"]')).perform()
                time.sleep(4)
                ActionChains(driver).release(driver.find_element_by_xpath('//*[@id="action_button"]')).perform()
                print(str(x) + " Elements found")
            except:
                print(str(datetime.now()) + " Done Gathering, Back to TaskManeger")
                driver.get("https://simple-mmo.com/travel")
                time.sleep(5)
                TaskManeger()
                break

def Steps():

  if ("Your skill level isn't high enough" in driver.page_source):  # Gathering
      print(str(datetime.now()) + " Your skill level isn't high enough")
  else:
    if ("/crafting/material/gather/" in driver.page_source):  # Found elements
        Gathering()

  if ("/npcs/attack/" in driver.page_source):  # Found Battle
      Attack()

  if ("You're dead!" in driver.page_source):  # Dead
      print(str(datetime.now()) + " I'm fucking dead")
      time.sleep(60)
      driver.get("https://simple-mmo.com/travel")
      TaskManeger()

  if ("We just need to make sure that you are a human" in driver.page_source):  # Found Captcha
      print(str(datetime.now()) + " Fucking Captcha!")
      result = re.search('<div class="bot-item">(.*)</div>', driver.page_source)
      print(result.group(1))
      os.system(r'D:\Documents\AHK\SimpleMMO_Capcha\KungFOO.exe ' + str(result.group(1)))
      time.sleep(10)
      if ("You have passed the verification" in driver.page_source):
        print(str(datetime.now()) + " My Kung foo is better than yours!")
        driver.get("https://simple-mmo.com/travel")
        time.sleep(3)
        TaskManeger()

  if driver.find_element_by_id("primaryStepButton").is_enabled(): # Running Steps
      print(str(datetime.now()) + " Trying to take a step")
      try:
        global StepsCounter
        time.sleep(1)
        driver.find_element_by_id("primaryStepButton").click()
        StepsCounter += 1
      except:
        print(str(datetime.now()) + " Error in Running Steps")

  else:
      time.sleep(2)
      print(str(datetime.now()) + " Checking if another step is available again - in 2 secound")

  TaskManeger()

def Battlearena():
    print(str(datetime.now()) + " Looking for Battle")
    driver.get("https://simple-mmo.com/battlearena")
    if ("Generate a new enemy" in driver.page_source):
        driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/div/div/div/div[3]/button').click()
        driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[1]').click()
        driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[1]').click()
        time.sleep(1)
        Attack()

def TaskManeger():
    global StepsCounter
    print(str(datetime.now()) + " Looking for new Tasks")
    print(str(datetime.now()) + " StepsCounter: " + str(StepsCounter))

    if StepsCounter > 25:
        print(str(datetime.now()) + " Battle Arena")
        #Battlearena()
        print(str(datetime.now()) + " Sells Maneger")
        SellsManeger()

    try:
        print(str(datetime.now()) + " Steps Trigger")
        Steps()
    except:
        print(str(datetime.now()) + " Steps Failed - Recovering")
        driver.get("https://simple-mmo.com/travel")
        driver.close()
        os.system('taskkill /F /IM chromedriver.exe')
        Start()

#Start HERE!

def Start():
    global driver
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get("https://simple-mmo.com/home")
    global StepsCounter
    StepsCounter = 0
    if ("Press here to enter your email address..." in driver.page_source):
        print(str(datetime.now()) + " Stating login process")
        elem = driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys("EMAIL@gmail.com")
        elem = driver.find_element_by_name("password")
        elem.clear()
        elem.send_keys("PASSWORD")
        elem.submit()
        if ("Press here to start" in driver.page_source):
            print(str(datetime.now()) + " Login Success")
            driver.get("https://simple-mmo.com/travel")
            TaskManeger()



Start()