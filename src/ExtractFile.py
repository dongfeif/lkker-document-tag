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
        elif self.file.endswith((".pdf", ".words", "xls", "ptx", "doc", "psx", "ppt")):
            return self.extract_doc()
        elif self.file.endswith((".zip")):
            return self.extract_zip()
        else:
            return '对于 ".pdf", ".words", "xls", "ptx", "doc", "psx", "ppt", ".jpg", ".peg", ".png", ".jpeg", ".zip" 之外的文件 暂时没有友好的方案，请转换格式处理 '

    def extract_zip(self):
        tags = {}
        fileLoader = FileLoader.FileLoader(self.file)
        fileLoader.read()
        print('loader file', fileLoader.files)
        for file in fileLoader.files:
            imageLoader = ImageLoader(file)
            imageLoader.handle()
            for image in imageLoader.images:
                img_64 = base64.b64encode(open(image, 'rb').read())
                # 获取图片的标签
                tags[image] = HttpClient().post(config.IMG_URL, {
                    "type": 1,
                    "content": img_64.decode()
                })
        return json.dumps(tags)

    def extract_img(self):
        img_64 = base64.b64encode(open(self.file, 'rb').read())
        return HttpClient().post(config.IMG_URL, {
            "type": 1,
            "content": img_64.decode()
        })

    def extract_doc(self):
        fileTagLoader = WorldsToWord()
        return json.dumps(dict(fileTagLoader.handle(self.file)))  # TODO::类型问题 稍后会同步

