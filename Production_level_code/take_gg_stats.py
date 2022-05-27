# Dependencies
import time
from bs4 import BeautifulSoup
from helium import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


import main_stats_capture
import start_browser
browser = start_browser.browser
dct1 = main_stats_capture.dct1
ind1 = []


def take_gg():
    # Get GG/NG odds
    browser.switch_to.window(browser.window_handles[0])
    browser.implicitly_wait(10)
    try:
        ele1 = browser.find_element_by_xpath(
            '//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/button[2]')
        helium.click(ele1)
        time.sleep(1.8)
    except:
        pass
    page1 = browser.page_source
    soup = BeautifulSoup(page1, 'lxml')
    try:  # Look for if the matches are there (GG) page
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-t'))).text
    except TimeoutException:
        pass
    #         while is_internet_available() is True:
    #             stats_capture()
    #             if len(df_stats) < 2:
    #                 time.sleep(5)
    #                 continue
    #             else:
    #                 return df_stats

    ggs = soup.findAll("div", {"class": "d-1"})

    for gg in ggs:
        gg = gg.text
        gg = gg.replace("Yes ", "")
        gg = gg.replace("No ", "")
        ggyes = gg[:-4]
        ggno = gg[-4:]

        try:
            dct1["GG"].append(ggyes)
            dct1["NG"].append(ggno)
        except IndexError:
            if len(ind1) < 2:
                take_gg()
                time.sleep(0.5)
        ind1.clear()