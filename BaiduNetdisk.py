# !/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os, stat, platform
import datetime, time
import sqlite3

plat = platform.platform()[0]

def is_BaiduNetdisk_running():
    cmd = {'D': 'ps aux |grep BaiduNetdisk_mac |grep -v grep',
           'W': 'tasklist | findstr BaiduNetdisk.exe'}
    return True if subprocess.getoutput(cmd[plat]) else False

def getDIR():
    BaiduPath = {'D': "Library/Application Support/com.baidu.BaiduNetdisk-mac",
                 'W': r'AppData\Roaming\baidu\BaiduNetdisk\users'}
    path = os.path.join(os.path.expanduser('~'), BaiduPath[plat])
    dirs = [i for i in os.listdir(path) if len(i) > 12]
    if dirs:
        return os.path.join(path, dirs[0])
    else:
        raise RuntimeError("不能取得 BaiduNetdisk 数据文件夹。您的百度盘安装路径很独特")

def getFiles(dbpath):
    limit = datetime.datetime.now() - datetime.timedelta(minutes=5)
    limit = int(time.mktime(limit.timetuple()))
    # 'SELECT * FROM downloads ORDER BY fid DESC LIMIT 1;'
    sql = {'D': 'SELECT local_path, local_name FROM downloads WHERE task_update_time > {} AND file_name NOT null;',
           'W': 'SELECT local_path FROM download_file WHERE status_changetime > {} AND local_path NOT null;'}
    files = None
    with sqlite3.connect(dbpath) as db:
        cursor = db.cursor()
        rows = cursor.execute(sql[plat].format(limit))
        if plat == 'D':
            files = [os.path.join(row[0], row[1]) for row in rows]
        elif plat == 'W':
            files = [os.path.join(row[0]) for row in rows]
    return files

def rm_dbfile(path, file):
    for fileList in os.walk(path):
        files = [f for f in fileList[2] if file in f]
        for name in files:
            os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
            os.remove(os.path.join(fileList[0], name))

def main():
    echos = ["百度盘高速试用完毕，退出百度盘，运行这个脚本；",
             "再次打开百度盘，重新下载这个文件，然后立即退出百度盘；",
             "再次打开百度盘，你就又可以再次高速下载啦！"]
    for i, s in enumerate(echos): print('{}. {}'.format(i + 1, s))
    BdNdisk_path = getDIR()
    extension = {'D': '.bdc-downloading', 'W': ''}
    dbfiles = {'D': 'transmission.db', 'W': 'BaiduYunGuanjia.db'}
    ori_files, bak_files = None, None
    while 1:
        if not is_BaiduNetdisk_running():
            # 1. 退出百度盘后，把文件改名（备份）
            dbpath = os.path.join(BdNdisk_path, dbfiles[plat])
            downloadFiles = getFiles(dbpath)
            ori_files = [i + extension[plat] for i in downloadFiles]
            bak_files = [i + '.bak' for i in downloadFiles]
            for ori, bak in zip(ori_files, bak_files):
                os.rename(ori, bak)
            # 2. 删除百度盘下载数据
            rm_dbfile(BdNdisk_path, dbfiles[plat])
            break
    # 3. 在百度盘退出、重启前，把备份的文件恢复
    while 1:
        if is_BaiduNetdisk_running(): break
    while 1:
        if not is_BaiduNetdisk_running():
            try:
                for ori, bak in zip(ori_files, bak_files):
                    os.remove(ori)
                    os.rename(bak, ori)
            except FileNotFoundError as e:
                print(e, '\n', '重新下载这个文件，之后，再退出百度盘')
            break

if __name__ == "__main__":
    main()
