#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os, stat, shutil
import datetime, time
import sqlite3


def is_BaiduNetdisk_running():
    out = subprocess.getoutput('ps aux | grep BaiduNetdisk_mac | grep -v grep')
    return True if out else False

def getDIR():
    path = os.path.abspath(os.path.expanduser('~') +
        "/Library/Application Support/com.baidu.BaiduNetdisk-mac")
    out = subprocess.getoutput("ls -t '{}'".format(path))
    dirs = [i for i in out.split('\n') if len(i) > 12]
    if dirs: return os.path.join(path, dirs[0])
    else: raise RuntimeError("不能取得 BaiduNetdisk 数据")

def getFiles():
    dbfile = os.path.join(getDIR(),'transmission.db')
    limit = datetime.datetime.now() - datetime.timedelta(minutes=5)
    limit = time.mktime(limit.timetuple())
    with sqlite3.connect(dbfile) as db:
        cursor = db.cursor()
        rows = cursor.execute('SELECT * FROM downloads WHERE task_update_time > {} AND file_name NOT null;'.format(limit))
        files = []  # 'SELECT * FROM downloads ORDER BY fid DESC LIMIT 1;'
        for row in rows:
            d = {col[0]:row[idx] for idx, col in enumerate(cursor.description)}
            files.append(os.path.join(d['local_path'], d['local_name']))
        return files

def rm_rf(path):
    for fileList in os.walk(path):
        for name in fileList[2]:
            os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
            os.remove(os.path.join(fileList[0], name))
    shutil.rmtree(path)

def main():
    echos = ["百度盘高速试用完毕，退出百度盘，运行这个脚本；",
            "再次打开百度盘，重新下载这个文件，然后立即退出百度盘；",
            "再次打开百度盘，你就又可以再次高速下载啦！"]
    for i, s in enumerate(echos): print('{}. {}'.format(i+1, s))
    ori_files, bak_files = None, None
    while 1:
        if not is_BaiduNetdisk_running():
            print('getFiles()')
            # 1. 退出百度盘后，把文件改名（备份）
            # ori_files = getFiles()
            ori_files = [i + '.bdc-downloading' for i in getFiles()]
            bak_files = [i + '.bak' for i in ori_files]
            for ori, bak in zip(ori_files, bak_files):
                os.rename(ori, bak)
            print('os.rename(ori, bak)')
            # 2. 删除百度盘下载数据
            print('rm_rf(getDIR())')
            rm_rf(getDIR())
            print('rm_rf(getDIR())   DONE')
            break
    # 3. 在百度盘退出、重启前，把备份的文件恢复
    while 1:
        if is_BaiduNetdisk_running():
            break
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
