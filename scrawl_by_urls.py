#encoding:utf-8
#Author Yundong.xiao
#Function: Scrawling My first follower's webpage including name id , followers , concerned peoples
#          [transfer,comment,like] for each published weibo
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
import csv
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

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
    except:
        print "Other Exception"

if __name__ == '__main__':

    # login in page setting
    original_url = 'https://weibo.com/'
    username = "18771038375"
    password = "xyd123456"

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
    # csv_write_file_open
    out_csv_file = codecs.open('scrawl_result100.csv', 'wb', "gbk")
    print "open file scrawl_out.csv in gbk encoding"
    csv_write = csv.writer(out_csv_file, dialect='excel')
    # collect pages start
    try:
        # csv_read_file_open
        # print fifth data
        in_csv_file = codecs.open('100.csv', 'r')
        out_blue_csv_file = codecs.open('bluev100.csv',  'ab', "gbk")
        blue_csv_write = csv.writer(out_blue_csv_file, dialect='excel')
        urls = csv.reader(in_csv_file)
        # For URL in URL_List
        count = 1
        for url in urls:
            #print url[0]
            print count
            count+=1
            result_list = []
            scrawl_url = url[0]
            driver.get(scrawl_url)
            time.sleep(2)
            # get name
            loop = 10
            while loop > 0 :
                Flag = is_element_exist(driver,'//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1',8)
                if Flag is False:
                    driver.refresh()
                    time.sleep(5)
                else:
                    break
                loop -=1
            name = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[2]/h1').text)
            print name
            # go to fans page
            if is_element_exist(driver,'//*[@class="t_link S_txt1"]',8) is False:
                driver.refresh()
                if is_element_exist(driver, '//*[@class="t_link S_txt1"]', 12) is False:
                    print "blue V people can't fetch data"
                    blue_csv_write.writerow([scrawl_url])
                    print scrawl_url
                    continue
            scrawl_url_fans_page = WebDriverWait(driver, 30).until(lambda driver: driver.find_element_by_xpath('//*[@id="Pl_Core_T8CustomTriColumn__3"]/div/div/div/table/tbody/tr/td[2]/a').get_attribute("href"))
            print scrawl_url_fans_page
            # scrawl this page  get url, fans, concerns weibos
            scrawl(driver, scrawl_url_fans_page, result_list, name)

            print "len :", len(result_list)
            #write to file
            for element in result_list:
                csv_write.writerow(element)

    except TimeoutException as msg:
        print "Time Out"

    # csv_read_file_close
    # csv_write_file_close
    # print fifth data
    out_csv_file.close()
    in_csv_file.close()
    out_blue_csv_file.close()

    # consumed time
    print time.strftime("%Y-%m-%d %H:%M %p", time.localtime())
    print "Scrawl End"

#
