from src import ImageLoader,imgTag
from src.wordCut import WorldsToWord
from src.imgTag import HttpClient
from src.ImageLoader import ImageLoader
import base64
import json
from src import config
from src import FileLoader


class ExtractFile:

    def __init__(self, path):
        self.file = path

    def handle(self):
        if self.file.endswith((".jpg", '.peg', '.png', '.jpeg')):
            return self.extract_img()
        elif self.file.endswith((".pdf", ".words", "xls", "ptx", "doc", "psx", "ppt", "xlsx")):
            return self.extract_doc()
        elif self.file.endswith((".zip")):
            return self.extract_zip()
        else:
            return '对于 ".pdf", ".words", "xls", "ptx", "doc", "psx", "ppt", ".jpg", ".peg", ".png", ".jpeg", ".zip" 之外的文件 暂时没有友好的方案，请转换格式处理 '

    def extract_zip(self):
        tags = {}
        fileLoader = FileLoader.FileLoader(self.file)
        fileLoader.read()
        for file in fileLoader.files:
            if file.endswith((".words", "xls", "ptx", "doc", "psx", "ppt")):
                tags[file] = self.extract_doc(file)
            elif file.endswith((".jpg", '.peg', '.png', '.jpeg')):
                tags[file] = self.extract_img(file)
            elif file.endswith((".pdf",)):
                images = ImageLoader(file)
                images.handle()
                for image in images.images:
                    img_64 = base64.b64encode(open(image, 'rb').read())
                    # 获取图片的标签
                    tags[image] = HttpClient().post(config.IMG_URL, {
                        "type": 1,
                        "content": img_64.decode()
                    })
        return json.dumps(tags)

    def extract_img(self, file=''):
        if file == '':
            file = self.file
        img_64 = base64.b64encode(open(file, 'rb').read())
        return json.dumps(HttpClient().post(config.IMG_URL, {
            "type": 1,
            "content": img_64.decode()
        }))

    def extract_doc(self, file=''):
        if file == '':
            file = self.file
        fileTagLoader = WorldsToWord()
        return json.dumps(fileTagLoader.handle(self.file))  # TODO::类型问题 稍后会同步

