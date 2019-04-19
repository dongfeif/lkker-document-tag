#!/usr/bin/python
# -*- coding: utf-8 -*-
from jieba.analyse import *
import textract
from src import pdf_extractor


class WorldsToWord:
    # 根据idf方式切词
    @staticmethod
    def get_contents_key_idf(words):
        return extract_tags(words, topK=10, withWeight=True, allowPOS=('n', 'nr', 'ns'))

    @staticmethod
    def get_contents_key_rank(words):
        return textrank(words, withWeight=True)

    # 获取 pdf
    def pdf_cut(self, pdf):
        # pdfs = glob.glob("{}/*.pdf".format(pdf_path))
        print("format-pdf : ", str(pdf))
        return self.get_contents_key_rank(pdf_extractor.extract_pdf_content(pdf))

    # 获取Word excel pptx
    def text_get_docs(self, path):
        code = textract.process(path).decode('utf-8')
        print("format-other : ", str(path))
        return self.get_contents_key_idf(code)

    def handle(self, path):
        if path.endswith(".pdf"):
            return self.pdf_cut(path)
        else:
            return self.text_get_docs(path)
