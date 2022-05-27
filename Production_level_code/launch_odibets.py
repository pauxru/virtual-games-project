
# import start_browser
# browser = start_browser.browser


def launch():
    # Open the first tab for the markets
    browser.switch_to.window(browser.window_handles[0])
    url = "https://odibets.com/league"
    browser.get(url)

    # Open a new window for results
    browser.execute_script("window.open('');")
    # Switch to the new window
    browser.switch_to.window(browser.window_handles[1])
    browser.get(url)
    try:
        browser.find_element_by_xpath('//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[1]/ul[2]/li[2]').click()
    except:
        launch()
    # Open a new window for standings
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[2])
    browser.get(url)
    try:
        browser.find_element_by_xpath('//*[@id="body"]/div/div[1]/div/div[2]/div[1]/div[1]/ul[2]/li[3]/button').click()
    except:
        launch()

