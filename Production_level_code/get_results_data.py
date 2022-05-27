# Dependencies
import time
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *


import start_browser
import check_internet
browser = start_browser.browser
mx = []
aa11 = []


def results_capture(df_stats1):
    global result_m
    # Results pd.Dataframe is here
    browser.switch_to.window(browser.window_handles[1])
    df_ff = pd.DataFrame(columns=['Home team', 'Scores', 'Away team', 'Week', 'Season', 'Time'])
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[1]/ul[2]/li[2]').click()
    time.sleep(1.8)

    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'results'))).text

    except TimeoutException:
        while check_internet.is_internet_available() is True:
            print("Results not available")
            # if len(df_ff) < 2 and len(aa11) <= 1:
            #     results_capture(df_stats1)
            #     time.sleep(5)
            #     aa11.append(3)
            #     continue
            # else:
            #     wheel()

    for g in pd.read_html(browser.page_source):
        dct = {"Home team": [], "Scores": [], "Away team": [], "Week": [], "Season": [], "Time": []}

        t = g[0][0]
        t = t.split("-")
        week = ''
        for wk in t[0]:
            if wk.isdigit():
                week += wk
        # print(week)
        t = t[1].strip()
        season = int(t[1:6])
        end_time = t.replace(t[:6], "").strip()

        if 'pm' in end_time:
            end_time1 = end_time.split(":")

            if end_time1[0] == '12':
                hrs = str(int(end_time1[0]))
            else:
                hrs = str(int(end_time1[0]) + 12)
            mnts = end_time1[1].replace("pm", "")
            end_time2 = int(hrs + mnts)
        else:
            end_time1 = end_time.replace(":", "")
            end_time2 = end_time1.replace("am", "").strip()
            # print(end_time2)

        # Remove the heading part. Really gave me a hard time figuring it out
        g = g.drop(g.index[0])

        for hm in g[0]:
            # print("Hm",len(hm))
            # hm_lst.append(hm)
            dct["Home team"].append(hm)

        for scr in g[1]:
            # print("Scr",len(scr))
            # hm_lst.append(hm)
            dct["Scores"].append(scr)

        for awy in g[2]:
            # hm_lst.append(hm)
            # print("awy",len(awy))
            dct["Away team"].append(awy)
            dct["Week"].append(week)
            dct["Season"].append(season)
            dct["Time"].append(str(end_time2))

        df_mt = pd.DataFrame.from_dict(dct)
        df_ff = df_ff.append(df_mt, ignore_index=True)
        df_sorted = df_ff[:10].sort_values(by='Home team', ignore_index=True)

    # -------------------------------------------------------
    # df_stats1 = df_stats1.sort_values('Home team')
    df_sorted = df_sorted.drop(['Home team', 'Time'], axis=1)
    df_sorted = df_sorted.reset_index(drop=True)
    time.sleep(2)
    browser.implicitly_wait(10)

    # Checking if the away team in the stats is same as away team
    # in the results. Should be same because we are sorting the two df
    aa11 = []
    for a_stats, a_rslt in zip(df_sorted['Away team'], df_stats1['Away team']):
        # print(a_stats," ",a_rslt)
        if a_stats == a_rslt:
            # print("Okay")
            aa11.append(1)
        else:
            aa11.append(0)

    if 0 in aa11 and len(mx) < 4:
        mx.append('AW')
        results_capture(df_stats1)

    mx.clear()
    # Here sort the two df and then concat better model
    result_m = pd.concat([df_stats1, df_sorted], axis=1)

    if result_m['Scores'].isnull().any() and result_m['Week'].isnull().any():
        print("Results not found \n Trying again...")
        time.sleep(1.8)
        results_capture(df_stats1)
    else:
        browser.switch_to.window(browser.window_handles[0])
    browser.switch_to.window(browser.window_handles[0])
    pd.set_option('display.max_columns', None)
    return result_m
