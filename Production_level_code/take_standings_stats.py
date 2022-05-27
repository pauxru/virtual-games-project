# Dependencies
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

import main_stats_capture
import check_internet
import central_processing
import take_1X2_stats
import start_browser
browser = start_browser.browser
dct1 = main_stats_capture.dct1


def take_standing():
    browser.switch_to.window(browser.window_handles[2])
    time.sleep(1.2)
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[1]/ul[2]/li[3]/button').click()

    try:
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'l-league-table-standings'))).text

    except TimeoutException:
        while check_internet.is_internet_available() is True:
            if len(dct1['H points']) < 2:
                take_standing()
                time.sleep(5)
                continue
            else:
                central_processing.wheel()

    time.sleep(1.2)
    standings = pd.read_html(browser.page_source)
    stds = standings[0]

    # this is to ensure that all the standings are loaded before continuing
    b = []
    while len(stds) < 20 and len(b) <= 26:
        browser.find_element_by_xpath(
            '//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[1]/ul[2]/li[3]/button').click()
        time.sleep(2)
        standings = pd.read_html(browser.page_source)
        stds = standings[0]
        b.append('j')

    if len(b) > 15:  # if after trying to load all standings fails
        return []
    b.clear()

    for one_hteam in take_1X2_stats.home_teams:
        fd = stds[stds['Team'] == one_hteam].index
        pstn = int(fd[0]) + 1
        dct1["H standing"].append(pstn)

        points = stds.at[int(fd[0]), 'Pts']
        dct1["H points"].append(points)

        form = stds.at[int(fd[0]), 'Form']
        won, draw, lost = form.count('W'), form.count('D'), form.count('L')
        form_points = (won * 3) + (draw * 1) + (lost * -3)
        dct1["H Form points"].append(form_points)
        dct1["H W"].append(won)
        dct1["H D"].append(draw)
        dct1["H L"].append(lost)

    for one_ateam in take_1X2_stats.away_teams:
        fd1 = stds[stds['Team'] == one_ateam].index
        pstn1 = int(fd1[0]) + 1
        dct1["A standing"].append(pstn1)

        points1 = stds.at[int(fd1[0]), 'Pts']
        dct1["A points"].append(points1)

        form = stds.at[int(fd1[0]), 'Form']

        won1, draw1, lost1 = form.count('W'), form.count('D'), form.count('L')
        form_points = (won1 * 3) + (draw1 * 1) + (lost1 * -3)
        dct1["A Form points"].append(form_points)
        dct1["A W"].append(won1)
        dct1["A D"].append(draw1)
        dct1["A L"].append(lost1)
