# Dependencies
import time

import main_stats_capture
import get_results_data
import save_to_google_sheets
import start_browser

browser = start_browser.browser
# This is the logical control loop for the scripts
a = []
fresh = []
li = []


def wheel():
    while True:
        # df_stats = pd.DataFrame()
        # final_stats = pd.DataFrame()
        browser.switch_to.window(browser.window_handles[0])
        try:
            browser.implicitly_wait(10)
            r1 = browser.find_element_by_class_name("lr").text
        except:
            browser.refresh()
            time.sleep(1)
            continue
        if ":" in r1 and len(a) < 1:
            print("Counting")
            time.sleep(2)
            df_stats = main_stats_capture.stats_capture()
            a.append('p')

            # When the program does not capture any stats,
            # it returns an empty list len == 0 hence this section to help repeat the process
            if type(df_stats) is list or len(df_stats) == 0:
                browser.switch_to.window(browser.window_handles[0])
                browser.refresh()
                time.sleep(3)
                a.clear()
                continue
            else:
                final_stats = df_stats.sort_values(by='Home team', ignore_index=True)
                final_stats = final_stats.reset_index(drop=True)

        if "LIVE" in r1 and len(li) <1:
            print("Live")
            li.append("jwm")

        time.sleep(2)
        try:
            if "END" in r1 and len(df_stats) == 10 and len(a) >= 1:
                print("ENDED")
                time.sleep(5)
                global df_ff_merged
                df_ff_merged = get_results_data.results_capture(final_stats)
                # time.sleep(2)
                # result = combine_data()
                time.sleep(2)
                pd_list = []
                df_ff_merged = df_ff_merged.astype(str)
                for mtc in range(len(df_ff_merged)):
                    pd_list.append(list(df_ff_merged.iloc[mtc]))
                # save_to_excel(result)
                save_to_google_sheets.write_to_sheets(pd_list, 0)
                a.clear()
                li.clear()
                time.sleep(2)
                fresh.append('jp')
            if len(fresh) > 12:
                browser.refresh()
                fresh.clear()
        except:
            browser.refresh()
        time.sleep(1)
