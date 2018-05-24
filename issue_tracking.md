# WebSpider
Issue Tracking for all encountered issues

[1]
[Description]
    Can not show other language when using GBK as encoding standard
[Solution]
    Switch from csv to openyxl lib 
[Side effect]
No
[Need improvement]
No
[2]
[Description]
chrome driver bug : no response to any action in driver
[Solution]    
report to chrome driver team
[Side effect]
No
[Need improvement]
No

[3]
[Description]
[Solution]    
[Side effect]
No
[Need improvement]
No

        if idx_file % 10 == 0:
            old_window_handle = driver.window_handles
            script = "window.open();"
            driver.execute_script(script)
            new_window_handle = driver.window_handles
            driver.switch_to.window(old_window_handle[-1])
            driver.close()
            driver.switch_to.window(new_window_handle[-1])
            time.sleep(1)