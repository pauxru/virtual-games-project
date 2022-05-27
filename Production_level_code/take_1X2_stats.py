# Dependencies
import time
from bs4 import BeautifulSoup
from helium import *
from datetime import date
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


import main_stats_capture
import start_browser
browser = start_browser.browser
dct1 = main_stats_capture.dct1
ind = []
home_teams = []
away_teams = []


def take_1x2(rm1):
    # Click the 1X2 button to make sure we are picking the right table
    browser.implicitly_wait(10)
    try:
        ele3 = browser.find_element_by_xpath(
            '//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/div/button[1]')
        helium.click(ele3)
        time.sleep(1.2)
        browser.implicitly_wait(10)
    except NoSuchElementException:
        browser.refresh()
        time.sleep(2.8)
        main_stats_capture.stats_capture()

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')

    try:  # Look for if the matches are there (1X2) page
        WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-t'))).text

    except TimeoutException:
        pass
    #         while is_internet_available() is True:
    #             break
    #             stats_capture()
    #             if len(df_stats) < 2:
    #                 time.sleep(5)
    #                 continue
    #             else:
    #                 return df_stats

    table = soup.findAll("div", {"class": "event"})

    for matchday in table:  # For 1X2 odds
        matchday = matchday.text
        matchday = matchday.replace(" 1 ", "")
        matchday = matchday.replace("X ", ",")
        matchday1 = matchday.replace("2 ", ",")
        for l, d in enumerate(matchday1):
            odds = []
            if d.isdigit():
                matchday2 = matchday1[l:]
                matchday3 = matchday1[:l]
                break

        odds = matchday2.split(",")
        h_odd = odds[0]
        d_odd = odds[1]
        a_odd = odds[2]

        teams = matchday3.strip().split("—")
        h_team = teams[0].strip()
        home_teams.append(h_team)
        a_team = teams[1].strip()
        away_teams.append(a_team)

        try:
            dct1["Home team"].append(h_team)
            dct1["Away team"].append(a_team)
            dct1["1"].append(h_odd)
            dct1["X"].append(d_odd)
            dct1["2"].append(a_odd)
            dct1["Time"].append(str(rm1[0] - 2))
            dct1["Date"].append(str(date.today()))  # format (year-month-date)
        except IndexError:
            if len(ind) < 2:
                take_1x2(rm1)
                time.sleep(0.5)
        ind.clear()


ind1 = []