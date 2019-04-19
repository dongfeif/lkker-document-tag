import os
import zipfile

class FileLoader(object):
    # 文件解压的路径
    un_zip_dir = os.getcwd() + '/tmp/'
    files = []
    images = []
    texts = []

    def __init__(self, path):
        self.path = path

    def read(self, path=''):
        if path == '':
            path = self.path
        # self.path = self.getLocalFile()
        files = []
        if self.__isZip__(path):
            files = self.read_zip(path)
            # print('读取的压缩包所有的文件', files)
        elif self.__isDir__(path):
            files = self.read_dir(path)
            # print('读取的文件夹所有的文件', files)
        elif self.__isFile__(path):
            # print(path)
            files = [path]
        self.files = [x for x in files]

    def read_zip(self, zip):
        if FileLoader.__isZip__(zip):
            file_dir = self.un_zip(zip)
            # print('解压的zip文件路径', file_dir)
            return self.read_dir(file_dir)

        else:
            raise Exception("不是压缩包", zip)

    def read_dir(self, dir):
        if os.path.isfile(dir):
            return [dir]
        files = []
        for x in os.listdir(dir):
            # print(dir + '/' + x)
            if x.find('__MACOSX') != -1:
                continue
            files = files + self.read_dir(dir + '/' + x)
        return files

    def get_local_file(self):
        return self.path

    @staticmethod
    def __isZip__(path):
        return path.endswith(('zip', 'gz', 'rar', '7z'))

    @staticmethod
    def __isDir__(path):
        return os.path.isdir(path)

    @staticmethod
    def __isFile__(file):
        return os.path.isfile(file)

    def next(self):
        pass

    def close(self):
        pass

    def un_zip(self, file_name):
        zip_file = zipfile.ZipFile(file_name)

        end = file_name.rfind('.')
        start = file_name.rfind('/')
        if end == -1:
            end = file_name.__len__()

        un_zip_name = file_name[start + 1:end]
        if os.path.isdir(self.un_zip_dir + un_zip_name):
            pass
        else:
            os.makedirs(self.un_zip_dir + un_zip_name)
        for names in zip_file.namelist():
            zip_file.extract(names, self.un_zip_dir + un_zip_name)
        zip_file.close()
        return self.un_zip_dir + un_zip_name