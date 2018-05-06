#encoding:utf-8
#Author Yundong.xiao
#Function: Scrawling My first follower's webpage including name id , followers , concerned peoples
#          [transfer,comment,like] for each published weibo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from openpyxl import Workbook
from openpyxl import load_workbook
import time
import csv
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#first output
Gwrite_file_list = ["out_1.xlsx","out_2.xlsx","out_3.xlsx","out_4.xlsx","out_5.xlsx","out_6.xlsx","out_7.xlsx","out_8.xlsx" \
                , "out_9.xlsx","out_10.xlsx","out_11.xlsx","out_12.xlsx","out_13.xlsx","out_14.xlsx","out_15.xlsx","out_16.xlsx"\
                ,"out_17.xlsx","out_18.xlsx","out_19.xlsx","out_20.xlsx","out_21.xlsx","out_22.xlsx","out_23.xlsx","out_24.xlsx"]
#first unfinished
Gunfinished_file_list= ["unfinished_1.csv","unfinished_2.csv","unfinished_3.csv","unfinished_4.csv","unfinished_5.csv","unfinished_6.csv","unfinished_7.csv","unfinished_8.csv" \
                , "unfinished_9.csv","unfinished_10.csv","unfinished_11.csv","unfinished_12.csv","unfinished_13.csv","unfinished_14.csv","unfinished_15.csv","unfinished_16.csv"\
                ,"unfinished_17.csv","unfinished_18.csv","unfinished_19.csv","unfinished_20.csv","unfinished_21.csv","unfinished_22.csv","unfinished_23.csv","unfinished_24.csv"]
#sec unfinished output
Gsec_unfinished_file_list= ["sec_unfinished_1.csv","sec_unfinished_2.csv","sec_unfinished_3.csv","sec_unfinished_4.csv","sec_unfinished_5.csv","sec_unfinished_6.csv","sec_unfinished_7.csv","sec_unfinished_8.csv" \
                , "sec_unfinished_9.csv","sec_unfinished_10.csv","sec_unfinished_11.csv","sec_unfinished_12.csv","sec_unfinished_13.csv","sec_unfinished_14.csv","sec_unfinished_15.csv","sec_unfinished_16.csv"\
                ,"sec_unfinished_17.csv","sec_unfinished_18.csv","sec_unfinished_19.csv","sec_unfinished_20.csv","sec_unfinished_21.csv","sec_unfinished_22.csv","sec_unfinished_23.csv","sec_unfinished_24.csv"]
#sec output
Gsec_write_file_list = ["sec_out_1.csv","sec_out_2.csv","sec_out_3.csv","sec_out_4.csv","sec_out_5.csv","sec_out_6.csv","sec_out_7.csv","sec_out_8.csv" \
                , "sec_out_9.csv","sec_out_10.csv","sec_out_11.csv","sec_out_12.csv","sec_out_13.csv","sec_out_14.csv","sec_out_15.csv","sec_out_16.csv"\
                ,"sec_out_17.csv","sec_out_18.csv","sec_out_19.csv","sec_out_20.csv","sec_out_21.csv","sec_out_22.csv","sec_out_23.csv","sec_out_24.csv"]


Gsuspend_list = []

Gnumber_per_time = 100

# judge if xpath element exist
def is_element_exist(browser, element, delay):
    try:
        WebDriverWait(browser, delay).until(lambda browser: browser.find_element_by_xpath(element))
        return True
    except:
        return False

# main scrawl function recursion itself if there is a deep url needed to be scrawled
def scrawl(browser, url, result_list, name):
    try:
        browser.get(url)
        time.sleep(1)
        Flag = is_element_exist(browser,'//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/li[1]/dl/dt/a',5)
        if Flag is False:
            #check if page is loaded
            loop = 3
            while loop > 0:
                Flag = is_element_exist(driver, '//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1', 2)
                if Flag is False:
                    driver.refresh()
                    time.sleep(5)
                else:
                    break
                loop -= 1
            if loop == 0:
                Gsuspend_list.append(url)
                print "Network unstable store into suspend list", url
                return

            #check if first fan is loaded
            Flag = is_element_exist(browser,'//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/li[1]/dl/dd[1]/div[1]/a[1]',10)
            if Flag is False:
                print "Invalid page return."
                return
        # concat all scrawls urls
        l_fans_names = []
        l_fans_urls  = []
        l_fans_concerns  = []
        l_fans_fans  = []
        l_fans_weibo  = []
        list_fans_names = WebDriverWait(driver, 30).until(lambda browser: browser.find_elements_by_xpath('//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[1]/a[1]'))
        list_fans_urls = WebDriverWait(driver, 30).until(lambda browser: browser.find_elements_by_xpath('//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dt/a'))
        list_fans_concerns = WebDriverWait(driver, 30).until(lambda browser: browser.find_elements_by_xpath('//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[1]/em/a'))
        list_fans_fans = WebDriverWait(driver, 30).until(lambda browser: browser.find_elements_by_xpath('//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[2]/em/a'))
        list_fans_weibo = WebDriverWait(driver, 30).until(lambda browser: browser.find_elements_by_xpath('//*[starts-with(@id,"Pl_Official_")]/div/div/div/div[2]/div[1]/ul/*/dl/dd[1]/div[2]/span[3]/em/a'))
        #extract
        for i in range(len(list_fans_names)):
            l_fans_names.append(list_fans_names[i].text)
            l_fans_urls.append(list_fans_urls[i].get_attribute("href"))
            l_fans_concerns.append(list_fans_concerns[i].text)
            l_fans_fans.append(list_fans_fans[i].text)
            l_fans_weibo.append(list_fans_weibo[i].text)

        for i in range(len(l_fans_names)):
            result_list.append([name, l_fans_names[i], l_fans_urls[i], l_fans_concerns[i] , l_fans_fans[i] , l_fans_weibo[i]])

        Flag = is_element_exist(browser,'//*[@class="page next S_txt1 S_line1"]',2)
        if Flag:
            next_page = browser.find_element_by_xpath('//*[@class="page next S_txt1 S_line1"]').get_attribute("href")
            #if "page=6" in next_page:
            #    print "page=6 return"
            #    return
            scrawl(browser, next_page, result_list, name)
        else:
            print "No next page"
            return

    except TimeoutException as msg:
        print msg

if __name__ == '__main__':

    # login in page setting
    original_url = 'https://weibo.com/'
    username = "18771038375"
    #"18771038375" 18602710227
    password = "xyd123456"
    #"xyd123456" keke880901

    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.maximize_window()
    driver.set_page_load_timeout(30)
    driver.delete_all_cookies()

    # login start
    try:
        driver.get(original_url)
        WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[1]/div/a[1]'))
        driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(username)
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys(password)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').send_keys(Keys.ENTER)
        time.sleep(3)
        WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/div/a[1]'))
        driver.refresh()
    except TimeoutException as msg:
        print msg
    # login end

    # time calculation start
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())

    #print "open file  in gbk encoding"

    # collect pages start
    try:
        # csv_read_file_open
        # print fifth data
        workbook_r = Workbook()
        workbook_r = load_workbook('last.xlsx')
        # booksheet = workbook.active                #鑾峰彇褰撳墠娲昏穬鐨剆heet,榛樿鏄涓€涓猻heet

        # booksheet = workbook.active                #鑾峰彇褰撳墠娲昏穬鐨剆heet,榛樿鏄涓€涓猻heet
        sheets_r = workbook_r.sheetnames  # 浠庡悕绉拌幏鍙杝heet
        booksheet_r = workbook_r[sheets_r[0]]
        booksheet_r = workbook_r[sheets_r[0]]


        booksheet_r = workbook_r[sheets_r[0]]


        suspend_csv_file = codecs.open('suspend_file.csv', 'wb', "gbk")
        suspend_write = csv.writer(suspend_csv_file, dialect='excel')
        urls = []
        rows = booksheet_r.rows
        # 杩唬鎵€鏈夌殑琛?
        for row in booksheet_r.rows:
            for cell in row:
                urls.append(cell.value)

        # For URL in URL_List
        idx_file = 0
        for scrawl_url in urls:

            if idx_file % Gnumber_per_time == 0 :
                # open write unfinished file
                workbook_w = Workbook()
                booksheet_w = workbook_w.active  # 鑾峰彇褰撳墠娲昏穬鐨剆heet,榛樿鏄涓€涓猻heet
                # 瀛樹竴琛屾暟鎹?
                out_unfinished_csv_file = codecs.open(Gunfinished_file_list[idx_file/Gnumber_per_time], 'wb', "gbk")
                out_unfinished_csv_write = csv.writer(out_unfinished_csv_file, dialect='excel')

            idx_file +=1
            #put here for unregister case continue
            if idx_file % Gnumber_per_time == 0 :
                workbook_w.save(Gwrite_file_list[idx_file/Gnumber_per_time])
                out_unfinished_csv_file.close()
                print "Stop 1 min for rest"
                time.sleep(60)

            print "node number:" , idx_file
            result_list = []
            #scrawl_url = scrawl_url[0:scrawl_url.find("refer_flag")]
            print scrawl_url
            driver.get(scrawl_url)
            time.sleep(2)

            F_unregsiter = False
            # check if we loaded success
            loop = 4
            while loop > 0 :
                Flag = is_element_exist(driver,'//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1[text()]',8)
                if Flag is False:
                    driver.refresh()
                    time.sleep(5)
                    Flag = is_element_exist(driver, '//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/div/a[1]', 8)
                    if Flag is True:
                        F_unregsiter = True
                        break
                else:
                    break
                loop -=1
            if loop == 0 :
                out_unfinished_csv_write.writerow([scrawl_url])
                print "cant fetch main page" , scrawl_url
                continue
            if F_unregsiter is True:
                print "unregister case" , scrawl_url
                out_unfinished_csv_write.writerow([scrawl_url,"unregister"])
                continue

            # get name
            name = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1').text)
            print name
            # go to fans page
            if is_element_exist(driver,'//*[@class="t_link S_txt1"]',8) is False:
                driver.refresh()
                if is_element_exist(driver, '//*[@class="t_link S_txt1"]', 12) is False:
                    print "blue V people can't fetch data" ,scrawl_url
                    out_unfinished_csv_write.writerow([scrawl_url])
                    continue
            scrawl_url_fans_page = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[2]/a').get_attribute("href"))
            print scrawl_url_fans_page
            # scrawl this page  get url, fans, concerns weibos
            scrawl(driver, scrawl_url_fans_page, result_list, name )

            print "len :", len(result_list)
            #write to file
            for element in result_list:
                booksheet_w.append(element)



    except TimeoutException as msg:
        print "Time Out"

    # close suspend file
    for element in Gsuspend_list:
        suspend_write.writerow(element)
    suspend_csv_file.close()

    workbook_w.save(Gwrite_file_list[(idx_file / Gnumber_per_time)+1])
    # consumed time
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
    out_unfinished_csv_file.close()
    print "Scrawl End"

#
