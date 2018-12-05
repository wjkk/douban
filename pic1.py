# coding=utf-8
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import re, os
import sys
import time
import pymysql.cursors
import uuid


if __name__ == '__main__':
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='douban', charset='utf8')
    cursor = conn.cursor()

    # append type
    sql = "SELECT id, m FROM `v_subject_slide` WHERE wm_cleaned=-1 ORDER BY id DESC LIMIT 1000000"
    cursor.execute(sql)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row[1])
            try:
                pic = requests.get(row[1])  # 访问图片
            except Exception as e:
                print(e)
                continue

            string = os.path.splitext(row[1])[-1]
            name = str(row[0]) + string
            fp = open('pics\\' + name, 'wb')
            fp.write(pic.content)
            fp.close

            sql = "UPDATE `v_subject_slide` SET wm_cleaned=2 WHERE id=" + str(row[0])
            cursor.execute(sql)
            conn.commit()

