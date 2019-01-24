# BaiduNetdisk-mac-viplimited
python 项目，适用于 MacOS 与 Windows。Mac自带python2，Windows需要安装Python3

用百度网盘时，开始会有“试用极速下载特权”。一会儿后，马上回到 100kb/s 以下的速度了。这个软件，就是为了再次获得试用时长，从而破解限速。

适合应急，比如你要下载一个 5Gb 左右的文件。不适合下载 10Gb 的文件。超大型的批量下载，建议使用proxyee-down https://github.com/proxyee-down-org

使用方法：
1. 打开百度盘，下载一个文件。使用“试用极速下载特权”。试用结束后，退出百度盘。再次打开，有第二次试用。（注意，Windows里要在系统托盘关闭百度盘）
2. `sudo python3 ~/BaiduNetdisk.py`（Windows用cmd 运行 python BaiduNetdisk.py）
3. 重新打开百度盘，重新下载这个文件。然后退出。
4. 再次打开百度盘，就会有“试用极速下载特权”了，继续下载。（python程序会在这个时候退出）

每次试用结束，都用 退出百度盘 >> `sudo python3 ~/BaiduNetdisk.py` >>  重新打开百度盘，重新下载文件，退出百度盘 >> 再次打开百度盘，获取“试用极速下载特权”，继续下载。直到完成下载

