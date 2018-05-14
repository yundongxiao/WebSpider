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
chrome driver bug : no response to any action with driver
[Solution]    
change to firefox to try
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
Result Numbers : 79
URL Count:  86 https://weibo.com/u/5626444759?
blue v no fans link https://weibo.com/u/5626444759?
URL Count:  87 https://weibo.com/szdgtimes?
Result Numbers : 85
URL Count:  88 https://weibo.com/u/3602462451?
Result Numbers : 53
URL Count:  89 https://weibo.com/u/2114535202?
Result Numbers : 74
URL Count:  90 https://weibo.com/u/1672989863?
Result Numbers : 77
URL Count:  91 https://weibo.com/u/5599575452?
Result Numbers : 81
URL Count:  92 https://weibo.com/u/5071998474?
Result Numbers : 39
URL Count:  93 https://weibo.com/zhiningtoys?
Result Numbers : 32
URL Count:  94 https://weibo.com/u/5578616886?
Result Numbers : 87
URL Count:  95 https://weibo.com/u/3260248655?
Result Numbers : 79
URL Count:  96 https://weibo.com/u/3275831174?
Result Numbers : 79
URL Count:  97 https://weibo.com/u/3243785954?
Result Numbers : 74
URL Count:  98 https://weibo.com/u/3219060150?
Result Numbers : 75
URL Count:  99 https://weibo.com/u/3911242548?
Result Numbers : 32
Stop 3 min for rest
URL Count:  100 https://weibo.com/u/2082022743?
No next page:  https://weibo.com/p/1005052082022743/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place
Result Numbers : 1
URL Count:  101 https://weibo.com/u/5543389061?
Result Numbers : 35
URL Count:  102 https://weibo.com/u/3289161511?
Result Numbers : 39
URL Count:  103 https://weibo.com/ctics?
blue v no fans link https://weibo.com/ctics?
URL Count:  104 https://weibo.com/u/1952458120?
Result Numbers : 36
URL Count:  105 https://weibo.com/qq765615207?
Result Numbers : 61
URL Count:  106 https://weibo.com/u/2665639682?
Result Numbers : 76
URL Count:  107 https://weibo.com/u/2243544334?
TimeoutException
Traceback (most recent call last):
  File "C:/Users/Administrator/PycharmProjects/WebSpider/scrawl_by_urls.py", line 239, in <module>
    prepare_scrawl(scrawl_url, result_list, exception_list)
  File "C:/Users/Administrator/PycharmProjects/WebSpider/scrawl_by_urls.py", line 143, in prepare_scrawl
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/\
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\support\wait.py", line 71, in until
    value = method(self._driver)
  File "C:/Users/Administrator/PycharmProjects/WebSpider/scrawl_by_urls.py", line 144, in <lambda>
    div/div/div[2]/div/a[1]'))
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 387, in find_element_by_xpath
    return self.find_element(by=By.XPATH, value=xpath)
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 957, in find_element
    'value': value})['value']
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\remote\webdriver.py", line 312, in execute
    response = self.command_executor.execute(driver_command, params)
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\remote\remote_connection.py", line 472, in execute
    return self._request(command_info[0], url, body=data)
  File "C:\Users\Administrator\PycharmProjects\WebSpider\venv\lib\site-packages\selenium\webdriver\remote\remote_connection.py", line 496, in _request
    resp = self._conn.getresponse()
  File "C:\Python27\Lib\httplib.py", line 1121, in getresponse
    response.begin()
  File "C:\Python27\Lib\httplib.py", line 438, in begin
    version, status, reason = self._read_status()
  File "C:\Python27\Lib\httplib.py", line 394, in _read_status
    line = self.fp.readline(_MAXLINE + 1)
  File "C:\Python27\Lib\socket.py", line 480, in readline
    data = self._sock.recv(self._rbufsize)
socket.error: [Errno 10053] 

Process finished with exit code 1