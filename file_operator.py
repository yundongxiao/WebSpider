#encoding:utf-8
import csv
import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

csv_file = csv.reader(open("link.csv", 'r'))
for ele in csv_file:
    for i in range(5):
        print ele[0]
    break


out_csv_file = codecs.open('scrawl_out.csv', 'ab', "gbk")
csv_write = csv.writer(out_csv_file, dialect='excel')
csv_write.writerow(["哈哈" , "https://weibo.com/kxuane?refer_flag=1005050008_"])
csv_write.writerow(["中文狗sss￥#￥@——_", "https://weibo.com/kxuane?refer_flag=1005050008_1"])
print ("write over")




