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

# ###########################Global Data End

# ###########################Functions
# is_element_exist : Judge if xpath element exist


def is_element_exist(browser, test_element, delay):
    try:
        WebDriverWait(browser, delay).until(lambda x: x.find_element_by_xpath(test_element))
        return True
    except TimeoutException:
        return False

# main scrawl function recursion itself if there is a deep url needed to be scrawled


def scrawl(browser, url, finished_result, unfinished_url):
    try:
        browser.get(url)
        time.sleep(3)

        # Check first element which must have been downloaded is loaded of not
        exist_flag = is_element_exist(browser, '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]\
        /ul/li[1]/dl/dt/a', 3)
        if exist_flag is False:
            # check if page is loaded , three times to reloaded
            max_loop = 3
            while max_loop > 0:
                # check again with other important element
                browser.refresh()
                time.sleep(5)
                exist_flag = is_element_exist(driver, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]\
                /div[2]/h1', 3)
                if exist_flag is True:
                    break
                max_loop -= 1
            if max_loop == 0:
                unfinished_url.append([url, "Unable to load"])
                print "Network unstable ,Unable to load page", url
                return

            # check if is a normal page without fans
            exist_flag = is_element_exist(browser, '//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]\
            /ul/li[1]/dl/dd[1]/div[1]/a[1]', 5)
            if exist_flag is False:
                print "Normal page without fans "
                return
        # get all data
        nickname = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('//*[@id="Pl_Official_\
        Headerv6__1"]/div[1]/div/div[2]/div[2]/h1'))
        list_fans_names = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//*[starts-with\
        (@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[1]/a[1]'))
        list_fans_urls = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//*[starts-with(\
        @id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dt/a'))
        list_fans_concerns = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//*[starts-wit\
        h(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[1]/em/a'))
        list_fans_fans = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//*[starts-with(@\
        id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[2]/em/a'))
        list_fans_weibo = WebDriverWait(driver, 30).until(lambda x: x.find_elements_by_xpath('//*[starts-with(@\
        id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[3]/em/a'))
        # extract
        for i in range(len(list_fans_names)):
            finished_result.append([nickname.text, list_fans_names[i].text, list_fans_urls[i].get_attribute("href"),
                                    list_fans_concerns[i].text, list_fans_fans[i].text, list_fans_weibo[i].text])
        # go to next page to recurse
        exist_flag = is_element_exist(browser, '//*[@class="page next S_txt1 S_line1"]', 2)
        if exist_flag:
            next_page = browser.find_element_by_xpath('//*[@class="page next S_txt1 S_line1"]').get_attribute("href")
            scrawl(browser, next_page, result_list, unfinished_url)
        else:
            print "No next page Or not allowed to fetch that page"
            return
    except TimeoutException as exception_msg:
        print exception_msg

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

        time.sleep(10)
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
    try:
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
        sheets = workbook_write.sheetnames
        sheet_write_result = workbook_write[sheets[0]]
        sheet_write_failed = workbook_write[sheets[1]]

        # For URL in URL_List
        idx_file = 0
        for scrawl_url in urls:
            idx_file += 1
            if idx_file % RECODING_PER_TIME == 0:
                workbook_write.save(Fetch_Result_File)  # append result and failed case into execl
                print "Stop 3 min for rest"
                time.sleep(180)

            print "Node number:", idx_file
            result_list = []
            exception_list = []
            scrawl_url = scrawl_url[0:scrawl_url.find("refer_flag")]
            print scrawl_url
            driver.get(scrawl_url)
            time.sleep(2)

            unregister = False
            # check if loaded success
            loop = 4
            while loop > 0:
                flag = is_element_exist(driver, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1[text()\
                ]', 5)
                if flag is False:
                    driver.refresh()
                    time.sleep(5)
                    flag = is_element_exist(driver, '//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/div/a[1]', 5)
                    if flag is True:
                        unregister = True
                        break
                else:
                    break
                loop -= 1
            if loop == 0:
                print "cant fetch main page", scrawl_url
                continue
            if unregister is True:
                print "unregister case", scrawl_url
                exception_list.append([scrawl_url, "unregister"])
                continue

            # go to fans page
            if is_element_exist(driver, '//*[@class="t_link S_txt1"]', 8) is False:
                driver.refresh()
                if is_element_exist(driver, '//*[@class="t_link S_txt1"]', 12) is False:
                    print "Blue V Member", scrawl_url
                    exception_list.append([scrawl_url, "Blue V"])
                    continue
            scrawl_url_fans_page = WebDriverWait(driver, 30).until(lambda x: x.find_element_by_xpath('\
            //*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[2]/a').get_attribute("href"))
            print
            # scrawl this page
            scrawl(driver, scrawl_url_fans_page, result_list, exception_list)
            print "Element numbers ", len(result_list), "Scrawled url :", scrawl_url_fans_page
            # write to sheet_write
            for element in result_list:
                sheet_write_result.append(element)
            for element in exception_list:
                sheet_write_failed.append(element)
    except TimeoutException as msg:
        print "Time Out in Main Function"

    # Recording end time
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
    print "Scrawl End"
