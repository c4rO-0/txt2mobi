# coding=utf8

import os
import sys
# import requests
import configparser
import socket
import http.server
import socketserver
from exceptions import KindleGenNotInstalledError
from main import Txt2mobiPath
import shutil

# def current_working_dir():
#     return os.getcwd()


def init_project(working_dir, fileName, author = '' ):
    book_name = ''
    dir_path = working_dir
    print("working---->")
    print(working_dir)
    book_name = fileName.rsplit('.',1)[0]
    rows = []
    rows.append(u'[txt2mobi]')
    rows.append(u'kindlegen=' + os.path.join(Txt2mobiPath,'resources','kindlegen.exe'))
    rows.append(u'')
    rows.append(u'[book]')
    rows.append(u'cover-img=cover.png')
    rows.append(u'title=%s' % book_name)
    rows.append(u'author='+author)
    rows.append(u'max-chapter=1500')
    with open(os.path.join(working_dir, '.project.ini'), 'w') as f:
        f.write("\n".join([r for r in rows]))
        f.close()

    # 复制封面
    shutil.copy2(os.path.join(Txt2mobiPath,'resources','cover.png'),working_dir)
    # os.system("cp " + os.path.join(Txt2mobiPath,'resources','cover.png') + " " + working_dir)
    # r = requests.get('https://raw.githubusercontent.com/ipconfiger/txt2mobi/master/resources/cover.png')
    # with open(os.path.join(current_working_dir(), 'cover.png'), 'w') as f:
    #     f.write(r.content)
    #     f.close()


def check_kindlgen(command='kindlegen'):
    rt = os.system(command)
    if rt:
        raise KindleGenNotInstalledError()

class ProjectConfig(object):
    def __init__(self,working_dir):
        try:
            self.working_dir = working_dir
            file_path = os.path.join(working_dir, '.project.ini')
            self.cf = configparser.ConfigParser()
            self.cf.read(file_path)
        except Exception:
            print("当前目录未初始化")
            sys.exit(1)


    @property
    def gen_command(self):
        return self.cf.get('txt2mobi', 'kindlegen')

    @property
    def cover_image(self):
        return self.cf.get('book', 'cover-img')

    @property
    def title(self):
        return self.cf.get('book', 'title')

    @property
    def author(self):
        return self.cf.get('book', 'author')

    @property
    def max_chapter(self):
        try:
            return self.cf.getint('book', 'max-chapter')
        except:
            return 1500


def codeTrans(code):
    """
    将chardet返回的coding名字转换成系统用的
    :param code:
    :type code:
    :return:
    :rtype:
    """
    codings = {
        'utf-8': 'utf8',
        'GB2312': 'GBK'
    }
    return codings.get(code, 'utf8')


def no_html(input_str):
    import re
    return re.sub(r'</?\w+[^>]*>', '', input_str)


def getIp():
    """
    获取本机IP地址
    :return:
    :rtype:
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def start_server():
    """
    开启一个HTTP服务器用于Kindle下载生成的.mobi文件
    :return:
    :rtype:
    """
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("打开Kindle:体验版网页浏览器, 输入http://%s:8000 点击project.mobi下载" % getIp())
    httpd.serve_forever()

