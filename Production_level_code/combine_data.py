"""
def combine_data():
    browser.switch_to.window(browser.window_handles[0])
    result = pd.merge(df_stats, df_ff, on=["Time", "Home team"], how="left")
    pd.set_option('display.max_columns', None)
    return result
"""
