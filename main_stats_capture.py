# Dependencies
import time
import pandas as pd
from helium import *


import central_processing
import take_1X2_stats
import take_gg_stats
import take_uo_stats
import take_standings_stats
import start_browser
browser = start_browser.browser


# This is the functions that capture all the data and save them in pandas df
tk1 = []
tk2 = []
tk3 = []
tk4 = []
global dct1


def stats_capture():  # Capture all the data before a match
    # HDW odds
    helium.set_driver(browser)

    dct1 = {"Home team": [], "Away team": [], "1": [], "X": [], "2": [],
            "Time": [], "Date": [], "GG": [], "NG": [],
            "OV1.5": [], "UN1.5": [], "H standing": [], "A standing": [],
            "H points": [], "A points": [], "H Form points": [], "A Form points": [], "H W": [], "H D": [],
            "H L": [], "A W": [], "A D": [], "A L": []}

    # This is for the remaining time
    browser.switch_to.window(browser.window_handles[0])
    rm1 = []
    for rema in browser.find_elements_by_class_name("md"):
        rema = int(rema.text.replace(":", ""))
        rm1.append(rema)

    # FUNCTIONS HERE
    take_1X2_stats.take_1x2(rm1)
    take_gg_stats.take_gg()
    take_uo_stats.take_uo15()
    take_standings_stats.take_standing()

    # Call the other function if the other preceeding one was sucessful
    if len(dct1['1']) == 0 and len(tk1) < 3:
        take_1X2_stats.take_1x2()
        time.sleep(0.5)
    else:
        tk1.clear()
        central_processing.wheel()

    if len(dct1['1']) == 10 and len(tk2) < 3:
        take_gg_stats.take_gg()
        time.sleep(0.5)
    else:
        tk2.clear()
        central_processing.wheel()

    if len(dct1['GG']) == 10 and len(tk3) < 3:
        take_uo_stats.take_uo15()
        time.sleep(0.5)
    else:
        tk3.clear()
        central_processing.wheel()

    if len(dct1['OV1.5']) == 10 and len(tk4) < 3:
        take_standings_stats.take_standing()
        time.sleep(0.5)
    else:
        tk4.clear()
        central_processing.wheel()

    c = []
    for i in list(dct1):
        if len(dct1[i]) < 10:
            stats_capture()
            c.append("judy")
            time.sleep(1.2)
            if len(c) < 3:
                continue
            else:
                break

    if len(c) == 0:
        df_stats = pd.DataFrame.from_dict(dct1)
    else:
        return []

    tk1.clear()
    tk2.clear()
    tk3.clear()
    tk4.clear()
    c.clear()
    return df_stats
