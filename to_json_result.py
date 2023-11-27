import requests
from bs4 import BeautifulSoup
import re
import json


# 将json格式的，添加音标和意思
def SearchWords(Word):
    try:
        url = 'https://www.youdao.com/result?word='+Word+'&lang=en' 
        HttpHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        Response = requests.get(url, headers=HttpHeaders)
        soup = BeautifulSoup(Response.text, 'html.parser')

        meanings, PhoneticSymbolUK, PhoneticSymbolUS = RegularFind(soup)
        return meanings, PhoneticSymbolUK, PhoneticSymbolUS
    
    except Exception as e:
        print('出错了',e)
        return None, None, None

def RegularFind(soup):
    meanings=[]
    meaningsLi = soup.find_all('li', class_='word-exp')
    if len(meaningsLi) >= 0:
    # 只处理meanings中的前三个元素
        for li in meaningsLi[:2]:
            text_parts = [span.get_text() for span in li.find_all('span')]
            combined_text = ''.join(text_parts)
            meanings.append(combined_text)
    else:
        meanings=["没找到释义"]

    phonetic_spans = soup.find_all('span', class_='phonetic')
    if len(phonetic_spans) >= 2:
        PhoneticSymbolUK = phonetic_spans[0].get_text().strip(' /')
        PhoneticSymbolUS = phonetic_spans[1].get_text().strip(' /')
    else:
        PhoneticSymbolUK = 'NoPhoneticSymbolUK'
        PhoneticSymbolUS = 'NoPhoneticSymbolUS'

    return meanings, PhoneticSymbolUK, PhoneticSymbolUS

if __name__ == '__main__':

    # 将提取的英文单词写入到words.txt文件中
    with open('raw.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    english_words = re.findall(r'\b[A-Za-z]+\b', text)
    word_counts = {}
    for word in english_words:
        if len(word) > 2:  # 排除长度为1或2的单词
            word_counts[word] = word_counts.get(word, 0) + 1
    unique_words = [word for word, count in word_counts.items() if count == 1]
    # 将只出现一次的英文单词写入到words.txt文件中
    with open('words.txt', 'w', encoding='utf-8') as output_file:
        for word in unique_words:
            output_file.write(word + '\n')

    # 将干净的txt（每行一个单词）初步转为json
    with open('words.txt', 'r', encoding='utf-8') as source_file:
        lines = source_file.readlines()
    data = []
    for line in lines:
        word = line.strip() 
        if not word:
            continue 
        data.append({
            "name": word,
            "trans": "",
            "usphone": "",
            "ukphone": ""
        })

    num=1
    for item in data:
        Word = item['name']
        num=num+1
        print(num+1)
        meanings, PhoneticSymbolUK, PhoneticSymbolUS = SearchWords(Word)
        item['trans'] = meanings
        item['ukphone'] = PhoneticSymbolUK
        item['usphone'] = PhoneticSymbolUS


    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print('Phonetic symbols added to the JSON data and saved in updated_data.json.')

