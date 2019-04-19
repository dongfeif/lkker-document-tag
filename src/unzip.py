import os
import zipfile

un_zip_dir = './../tmp/'


def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)

    end = file_name.rfind('.')
    start = file_name.rfind('/')
    if end == -1:
        end = file_name.__len__()

    un_zip_name = file_name[start + 1:end]
    if os.path.isdir(un_zip_dir + un_zip_name):
        pass
    else:
        os.mkdir(un_zip_dir + un_zip_name)
    for names in zip_file.namelist():
        zip_file.extract(names, un_zip_dir + un_zip_name)
    zip_file.close()


inputname = "./../zzzz.zip"
un_zip(inputname)
