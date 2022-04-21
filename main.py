# Dependencies
import time

import launch_odibets
import central_processing
import start_browser
from start_browser import browser
# browser = start_browser.browser

if __name__ == '__main__':
    start_browser.start_odibets()
    launch_odibets.launch()

    # This is where it all begins
    browser.switch_to.window(browser.window_handles[0])
    browser.implicitly_wait(10)
    r11 = browser.find_element_by_class_name("lr").text
    print(r11)
    while "LIVE" in r11 or "END" in r11:
        browser.implicitly_wait(10)
        try:
            print("Live Matchday")
            r11 = browser.find_element_by_class_name("lr").text
        except:
            pass
        time.sleep(1)

    r12 = 0
    while r12 < 200:
        browser.implicitly_wait(10)
        r111 = browser.find_element_by_class_name("lr").text
        if ":" in r111:
            print("Countdown ...", r111)
            r12 = r111.split(":")
            r12 = int(str(r12[0]) + str(r12[1]))
            if r12 > 25:
                break
        time.sleep(1)

    central_processing.wheel()
