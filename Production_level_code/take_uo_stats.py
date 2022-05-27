# Dependencies
import time
from bs4 import BeautifulSoup
from helium import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

import main_stats_capture
import check_internet
import central_processing
import start_browser
dct1 = main_stats_capture.dct1
browser = start_browser.browser
ind2 = []


def take_uo15():
    # Get over and under 1.5 odds
    browser.implicitly_wait(10)
    try:
        ele2 = browser.find_element_by_xpath(
        '//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/button[3]')
        helium.click(ele2)
        time.sleep(1.8)
    except:
        pass
    page2 = browser.page_source
    soup = BeautifulSoup(page2, 'lxml')

    try:  # Look for if the matches are there (U/O) page
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-t'))).text

    except TimeoutException:
        while check_internet.is_internet_available() is True:
            if len(dct1['OV1.5']) < 2:
                take_uo15()
                time.sleep(5)
                continue
            else:
                central_processing.wheel()

    ovun = soup.findAll("div", {"class": "d-1"})

    for tt in ovun:
        tt = tt.text
        tt = tt.replace("Under ", "")
        tt = tt.replace("Over ", "")
        ov = tt[-4:]
        un = tt[:-4]

        try:
            dct1["OV1.5"].append(ov)
            dct1["UN1.5"].append(un)
        except IndexError:
            if len(ind2) < 2:
                # take_gg()
                time.sleep(0.5)
        ind2.clear()