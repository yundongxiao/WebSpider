# encoding:utf-8
# Author Yundong xiao

# ############################Import Libs
# standard lib
import time

# third party lib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from openpyxl import Workbook
from openpyxl import load_workbook

# self written lib
#
# ###########################Import Libs End

# ###########################Global Data
# output file name
Fetch_Result_File = "./file/fetch_result.xlsx"

RECODING_PER_TIME = 100
ERROR_BLUE_V = "BLUE V"
ERROR_UNREGISTER = "UNREGISTER"
ERROR_NO_NETWORK = "NO NETWORK"
ERROR_LOAD_MAIN_PAGE = "LOAD MAIN PAGE FAIL"
ERROR_TIME_OUT = "TIME OUT"
ERROR_LOAD_FANS_PAGE = "UNABLE TO LOAD FANS PAGE"
# ###########################Global Data End

# ###########################Functions
# is_element_exist : Judge if xpath element exist


def is_element_exist(browser, test_element, delay):
    try:
        WebDriverWait(browser, delay).until(lambda x: x.find_element_by_xpath(test_element))
        return True
    except TimeoutException:
        return False

# try_to_get_element : try_to_get_element with time_try times


def try_to_get_element(browser, test_element, time_try, last_delay, fg_elements):
    exist_element = is_element_exist(browser, test_element, 3)
    if exist_element is False:
        max_loop = time_try
        while max_loop > 0:
            # last time sleep 120 seconds
            if max_loop == 1:
                time.sleep(last_delay)
            browser.refresh()
            exist_element = is_element_exist(browser, test_element, 5)
            if exist_element is True:
                break
            max_loop -= 1
        if max_loop == 0:
            return False
    if fg_elements is True:
        return browser.find_elements_by_xpath(test_element)
    else:
        return browser.find_element_by_xpath(test_element)

# main scrawl function recursion itself if there is a deep url needed to be scrawled


def scrawl(browser, url, finished_result, unfinished_url):
    browser.get(url)
    # check if fans is loaded , three times to reloaded
    exist_flag = try_to_get_element(browser, '//*[starts-with(@id,"Pl_Official")]/div/\
    div/div/div[2]/div[1]/ul/li[1]/dl/dd[1]/div[2]/span[1]', 3, 3, False)
    if exist_flag is False:
        # check if is a normal page without fans
        xpath = '//*[starts-with(@id,"Pl_Official_")]/div[1]/div/div[2]/div[2]/h1'
        exist_flag = is_element_exist(browser, xpath, 3)
        if exist_flag is True:
            print "Normal page without fans"
            return
        unfinished_url.append([url, ERROR_NO_NETWORK])
        print ERROR_NO_NETWORK, url
        time.sleep(3600*24)
        return

    # get all data
    xpath = '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1'
    nickname = try_to_get_element(driver, xpath, 3, 2, False)
    xpath = '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[1]/a[1]'
    list_fans_names = try_to_get_element(driver, xpath, 3, 2, True)
    xpath = '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dt/a'
    list_fans_urls = try_to_get_element(driver, xpath, 3, 2, True)
    xpath = '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[1]/em/a'
    list_fans_concerns = try_to_get_element(driver, xpath, 3, 2, True)
    xpath = '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[2]/em/a'
    list_fans_fans = try_to_get_element(driver, xpath, 3, 2, True)
    xpath = '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[3]/em/a'
    list_fans_weibo = try_to_get_element(driver, xpath, 3, 2, True)

    # extract
    for i in range(len(list_fans_names)):
        finished_result.append([nickname.text, list_fans_names[i].text, list_fans_urls[i].get_attribute("href"),
                                list_fans_concerns[i].text, list_fans_fans[i].text, list_fans_weibo[i].text])

    if is_element_exist(browser, '//*[@class="page next S_txt1 S_line1 page_dis"]', 1):
        print "Not allowed to fetch that page"
        return
    # go to next page to recurse
    exist_element = try_to_get_element(browser, '//*[@class="page next S_txt1 S_line1"]', 3, 2, False)
    if exist_element is not False:
        next_page = exist_element.get_attribute("href")
        scrawl(browser, next_page, result_list, unfinished_url)
    else:
        print "No next page"
        return


def prepare_scrawl(url, return_list, error_list):
    unregister = False
    # check if loaded success
    loop = 4
    while loop > 0:
        flag = is_element_exist(driver, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1[text()]', 5)
        if flag is False:
            driver.refresh()
            flag = is_element_exist(driver, '//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/div/a[1]', 5)
            if flag is True:
                unregister = True
                break
        else:
            break
        loop -= 1
    if loop == 0:
        print ERROR_LOAD_MAIN_PAGE, url
        error_list.append([url, ERROR_LOAD_MAIN_PAGE])
        return
    if unregister is True:
        print ERROR_UNREGISTER, url
        error_list.append([url, ERROR_UNREGISTER])
        return

    # go to fans page
    exist_element = try_to_get_element(driver, '//*[@class="t_link S_txt1"]', 3, 3, False)
    if exist_element is False:
        print ERROR_BLUE_V, url
        error_list.append([url, ERROR_BLUE_V])
        return
    exist_element = try_to_get_element(driver, '//*[@id="Pl_Core_T8CustomTriColumn__3"]/div\
    /div/div/table/tbody/tr/td[2]/a', 120, 3, False)
    if exist_element is False:
        print ERROR_LOAD_FANS_PAGE, url
        error_list.append([url, ERROR_LOAD_FANS_PAGE])
        return
    else:
        scrawl_url_fans_page = exist_element.get_attribute("href")
    # scrawl this page
    scrawl(driver, scrawl_url_fans_page, return_list, error_list)
    print "Element numbers ", len(result_list), "Scrawled url :", scrawl_url_fans_page

# ###########################Functions End


if __name__ == '__main__':

    # login in page setting
    original_url = 'https://weibo.com/'
    username = "18771038375"
    # 18771038375 18602710227
    password = ""
    # input your password or set it in password
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.delete_all_cookies()

    # login start
    try:
        driver.get(original_url)
        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/\
        div/a[1]'))
        driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(password)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').send_keys(Keys.ENTER)
        time.sleep(3)
        WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/div/div\
        /div[2]/div/a[1]'))
        driver.refresh()
    except TimeoutException as msg:
        print msg
    # login end

    # Recording time start
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())

    # collecting pages start
    workbook_read = load_workbook('./file/urls.xlsx')
    sheets_read = workbook_read.sheetnames
    sheet_read = workbook_read[sheets_read[0]]

    urls = []
    rows = sheet_read.rows
    for row in sheet_read.rows:
        for cell in row:
            urls.append(cell.value)

    # open write unfinished file
    workbook_write = Workbook()
    sheet_write_result = workbook_write.create_sheet(title="results")
    sheet_write_failed = workbook_write.create_sheet(title="failed urls")

    # For URL in URL_List
    idx_file = 0
    for scrawl_url in urls:
        idx_file += 1
        if idx_file % RECODING_PER_TIME == 0:
            workbook_write.save(Fetch_Result_File)  # append result and failed case into execl RECODING_PER_TIME
            print "Stop 3 min for rest"
            time.sleep(180)

        print "Node number:", idx_file
        result_list = []
        exception_list = []
        scrawl_url = scrawl_url[0:scrawl_url.find("refer_flag")]
        print scrawl_url
        driver.get(scrawl_url)
        prepare_scrawl(scrawl_url, result_list, exception_list)
        # write to sheet_write
        for element in result_list:
            sheet_write_result.append(element)
        for element in exception_list:
            sheet_write_failed.append(element)
    workbook_write.save(Fetch_Result_File)

    # Recording end time
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
    print "Scrawl End"
