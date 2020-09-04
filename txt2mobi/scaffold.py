# coding=utf8

import os
import sys
import shutil
from txt2mobi.exceptions import EncodingError
# from utilities import init_project
from txt2html import Book
import subprocess 



# def op_init_project():
#     """
#     初始化项目目录
#     :return:
#     :rtype:
#     """
#     init_project()


# def generate_project(title,working_dir,filename):
#     """
#     生成项目文件
#     :return:
#     :rtype:
#     """
#     book = test_project(title,working_dir,filename)
#     if(book != None):
#         book_count = book.book_count()
#         for idx in range(1, book_count + 1):
#             print('--------生成执行命令-------------')
#             print(book.gen_command(idx))
#             os.system(book.gen_command(idx))
#             src_path = os.path.join(working_dir, 'project-%s.mobi' % idx)
#             des_path = os.path.join(working_dir, '%s-%s.mobi' % (book.config.title, idx))



# def test_project(title,working_dir,filename):
#     """
#     测试项目, 跑一遍, 生成文件但是不调用kindlegen
#     :return:
#     :rtype:
#     """
#     print("-----开始测试---------")
#     book = Book(working_dir, filename, title)
#     print("------去掉空章节--------")
#     book.trim()
#     print("-------生成opf------")
#     # 生成opf文件
#     book_count = book.book_count()
#     for idx in range(1, book_count+1):
#         try:
#             opf_path = os.path.join(working_dir, 'project-%s.opf' % idx)
#             with open(opf_path, 'w') as f:
#                 f.write(book.gen_opf_file(idx))
#                 f.close()
#             print("opf文件生成完毕")

#             # 生成ncx文件
#             ncx_path = os.path.join(working_dir, 'toc-%s.ncx' % idx)
#             with open(ncx_path, 'w') as f:
#                 f.write(book.gen_ncx(idx))
#                 f.close()
#             print("ncx文件生成完毕")

#             # 生成book.html
#             book_path = os.path.join(working_dir, 'book-%s.html' % idx)
#             with open(book_path, 'w') as f:
#                 f.write(book.gen_html_file(idx))
#                 f.close()
#             print("book-%s.html生成完毕" % idx)
#         except (EncodingError):
#             print("文件编码异常无法解析,请尝试用iconv来转码成utf8后再试,或者提交issuse")
#             return None
#     return book

def genTOC(title,working_dir,filename, ChapterMaxLength):
    """
    只生成ncx文件
    :return:
    :rtype:
    """
    print("-----开始TOC---------")
    book = Book(working_dir, filename, title, ChapterMaxLength)
    # print("------去掉空章节--------")
    # book.trim()
    # 生成opf文件
    book_count = book.book_count()
    # TOC = []
    
    # index =0
    print("----genTOC-----")
    # print(book.chapters[0].title)
    # print("----title-----")
    # try:
    #     # 生成目录
    #     for chapter in book.chapters:
    #         TOC.append([index, chapter.title])
    #         # print( chapter.title)
    #         index = index +1

    # except (EncodingError):
    #     print("文件编码异常无法解析,请尝试用iconv来转码成utf8后再试,或者提交issuse")
    #     return None, None
    TOC = book.gen_TOChtml()
    TOChtml_path = os.path.join(working_dir, 'project-TOC.html')
    with open(TOChtml_path, 'w', encoding='utf-8') as f:
        f.write(TOC)
        f.close()
    

    return book, TOC

def gen_project(book,title,working_dir,filename):
    """
    生成项目
    :return:
    :rtype:
    """
    print("-----开始测试---------")
    print("-------生成opf------")
    # 生成opf文件
    book_count = book.book_count()
    for idx in range(1, book_count+1):
        try:
            toc_path = os.path.join(working_dir, 'project-TOC-%s.html' % idx)
            with open(toc_path, 'w', encoding='utf-8') as f:
                f.write(book.gen_TOChtml(idx))
                f.close()
            print("TOC文件生成完毕")

            opf_path = os.path.join(working_dir, 'project-%s.opf' % idx)
            with open(opf_path, 'w', encoding='utf-8') as f:
                f.write(book.gen_opf_file(idx))
                f.close()
            print("opf文件生成完毕")

            # 生成ncx文件
            ncx_path = os.path.join(working_dir, 'toc-%s.ncx' % idx)
            with open(ncx_path, 'w', encoding='utf-8') as f:
                f.write(book.gen_ncx(idx))
                f.close()
            print("ncx文件生成完毕")

            # 生成book.html
            book_path = os.path.join(working_dir, 'book-%s.html' % idx)
            with open(book_path, 'w', encoding='utf-8') as f:
                f.write(book.gen_html_file(idx))
                f.close()
            print("book-%s.html生成完毕" % idx)
        except (EncodingError):
            print("文件编码异常无法解析,请尝试用iconv来转码成utf8后再试,或者提交issuse")
            return None

    for idx in range(1, book_count + 1):
        print('--------生成执行命令-------------')
        print(book.gen_command(idx))

        # os.system(book.gen_command(idx))

        try:
            output = subprocess.run(book.gen_command(idx), timeout=10*60) # 10 min max
            # src_path = os.path.join(working_dir, 'project-%s.mobi' % idx)
            # des_path = os.path.join(working_dir, '%s-%s.mobi' % (book.config.title, idx))
        except subprocess.TimeoutExpired:
            print('--------超时-------------')
            raise

