import os

from pdf2image import convert_from_path


class ImageLoader:
    images = []
    output_dir = os.getcwd() + '/img/'

    def __init__(self, file):
        self.file = file

    def next(self):
        pass

    def handle(self):
        print('是否是图片', self.file.endswith((".jpg", '.peg', '.png')))
        if self.file.endswith((".jpg", '.peg', '.png')):
            # 是否是图片
            self.images = [self.file]
        elif self.file.endswith((".pdf")):
            # pdf
            self.images = self.pdf2img(self.file)
            # print(self.images)
            pass
        elif self.file.endswith((".ppt", 'pptx')):
            # ppt
            # raise Exception("暂时还不接受ppt文件的处理，请将文件站化成ppt再来尝试", zip)
            print("暂时还不接受ppt文件的处理，请将文件站化成ppt再来尝试")
            pass

    def pdf2img(self, pdf_file):
        output_dir = self.output_dir + pdf_file[pdf_file.rfind('/')+1:pdf_file.rfind('.')]
        if os.path.isdir(output_dir):
            pass
        else:
            os.makedirs(output_dir)
        convert_from_path(pdf_file, 500, output_dir, None, None, 'jpg')
        images = []
        for image in os.listdir(output_dir):
            # print(image)
            images.append(output_dir + '/' + image)
        return images

    # TODO 因为linux没有很好的操作ppt的python插件，所以暂时先不解决ppt的问题，如果有需要可以用docker跑个windows的容器
    def ppt2img(self, pdf_file):
        pass

        # prs = Presentation(pdf_file)
        #
        # # text_runs will be populated with a list of strings,
        # # one for each text run in presentation
        # text_runs = []
        #
        # for slide in prs.slides:
        #     for shape in slide.shapes:
        #         if not shape.has_textframe:
        #             continue
        #         for paragraph in shape.textframe.paragraphs:
        #             for run in paragraph.runs:
        #                 text_runs.append(run.text)
