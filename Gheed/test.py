import time

from pynput.keyboard import Key, Controller
from selenium import webdriver as driver
from selenium.webdriver.common.keys import Keys
from time import sleep
import sys
from selenium.webdriver.common.by import By


fenster = driver.Firefox()
fenster.get('https://www.youtube.com/')

while True:
    button = driver.find_element(By.XPATH, '//*[@id="button"]')
    try:
        button.click()
    except:
        time.sleep(0.1)
    else:
        break