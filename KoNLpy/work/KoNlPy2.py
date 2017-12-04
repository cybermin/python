#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from collections import Counter

from konlpy.corpus import kolaw
from konlpy.tag import Hannanum
from konlpy.utils import concordance, pprint
from matplotlib import pyplot
import codecs
import random
import webbrowser
import pytagcloud # requires Korean font support


# 파일 명
INPUT_FILE_NAME = 'say.txt'

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Nanum Gothic', size=(1024, 768)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)

read_file = codecs.open(INPUT_FILE_NAME, 'r', 'utf-8-sig')
doc = read_file.read()
tags = get_tags(doc)

print(tags)
draw_cloud(tags, 'say.png')