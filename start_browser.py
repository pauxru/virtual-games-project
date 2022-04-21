# Dependencies
from selenium import webdriver
import time

global browser


def start_odibets():
    try:
        print("Please Wait. Launching Chrome")
        global browser
        options = webdriver.ChromeOptions()
        options.page_load_strategy = 'normal'
        prefs = {"profile.default_content_setting_values.notifications": 2,
                 "credentials_enable_service": False,
                 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        # options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=options,
                                   executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        time.sleep(2)
        browser.set_window_size(1000, 960)
        print("Browser launched successfully")

    except Exception as e:
        print("Could not start Chrome: ", e)
        # start_odibets()
    return browser
