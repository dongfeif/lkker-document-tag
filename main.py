import base64
import os
import socket

from src import FileLoader
from src.ImageLoader import ImageLoader
from src import config
from src.imgTag import HttpClient
from src.wordCut import WorldsToWord

file = os.getcwd() + '/zzzz.zip'

fileLoader = FileLoader.FileLoader(file)
fileLoader.read()

for file in fileLoader.files:
    # 获取图片标签
    images = ImageLoader(file)
    images.handle()
    for image in images.images:
        print('image', image)
        img_64 = base64.b64encode(open(image, 'rb').read())
        # 获取图片的标签
        tags = HttpClient().post(config.IMG_URL, {
            "type": 1,
            "content": img_64.decode()
        })
        print(tags)

    # 获取关键字
    print('file', file)
    fileTagLoader = WorldsToWord()
    tags = fileTagLoader.handle(file)
    print(tags)

if __name__ == "__main__":
    print(111)
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('127.0.0.1', 9999))
    # s.listen(5)
    # while True:
    #     # 接受一个新连接:
    #     sock, addr = s.accept()
    #     # 创建新线程来处理TCP连接:
    #     t = threading.Thread(target=tcplink, args=(sock, addr))
    #     t.start()

