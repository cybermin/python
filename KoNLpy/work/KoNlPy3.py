"""뉴스 기사 웹 크롤러 모듈"""
from bs4 import BeautifulSoup
import urllib.request
import codecs

# 정규 표현식을 지원하기 위해 re(regular expression의 약어) 모듈을 제공
import re

from collections import Counter
from konlpy.tag import Hannanum
import pytagcloud # requires Korean font support

import random
import webbrowser
import pytagcloud # requires Korean font support

r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())


# 출력 파일 명
OUTPUT_FILE_NAME = 'output.txt'
OUTPUT_FILE_NAME2 = 'output_cleand.txt'

# 긁어 올 URL
#URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055&aid=0000445667'
URL = 'http://news.naver.com/main/read.nhn?oid=421&sid1=100&aid=0003081964&mid=shm&mode=LSD&nh=20171204194457'

# 크롤링 함수
def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('div', id='articleBodyContents'):
        text = text + str(item.find_all(text=True))
    return text


# 클리닝 함수
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text


def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='Nanum Gothic', size=(600,400)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)



# 메인 함수
def main():
    # 뉴스 자료읽어서 텍스트 파일로 저장
    open_output_file = codecs.open(OUTPUT_FILE_NAME, 'w', 'utf-8-sig')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()

    # 뉴스 파일을 텍스트 정제 모듈
    read_file = codecs.open(OUTPUT_FILE_NAME, 'r', 'utf-8-sig')
    write_file = codecs.open(OUTPUT_FILE_NAME2, 'w', 'utf-8-sig')
    text = read_file.read()
    text = clean_text(text)
    write_file.write(text)
    read_file.close()
    write_file.close()

    read_file = codecs.open(OUTPUT_FILE_NAME2, 'r', 'utf-8-sig')
    doc = read_file.read()
    tags = get_tags(doc)

    print(tags)
    draw_cloud(tags, 'new.png')


if __name__ == '__main__':
    main()
