import requests
from bs4 import BeautifulSoup
import re
import json
# 将json格式的，添加音标
def SearchWords(Word):
    try:
        url = 'https://www.youdao.com/result?word='+Word+'&lang=en' 
        HttpHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
        Response = requests.get(url, headers=HttpHeaders)
        soup = BeautifulSoup(Response.text, 'html.parser')
        # print("soup",soup)
        # Parse the response to extract phonetic symbols
        PhoneticSymbolUK, PhoneticSymbolUS = RegularFind(soup)
        print(PhoneticSymbolUK,PhoneticSymbolUS)
        return PhoneticSymbolUK, PhoneticSymbolUS
    
    except Exception as e:
        print('Search Words Error!')
        return None, None

def RegularFind(soup):
    # Find all span elements with class 'phonetic'
    phonetic_spans = soup.find_all('span', class_='phonetic')

    if len(phonetic_spans) >= 2:
        # The first div is for UK pronunciation, and the second div is for US pronunciation
        PhoneticSymbolUK = phonetic_spans[0].get_text().strip(' /')
        PhoneticSymbolUS = phonetic_spans[1].get_text().strip(' /')
    else:
        PhoneticSymbolUK = 'NoPhoneticSymbolUK'
        PhoneticSymbolUS = 'NoPhoneticSymbolUS'

    return PhoneticSymbolUK, PhoneticSymbolUS

if __name__ == '__main__':
    # Load the original JSON data
    with open('original_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    num=1
    for item in data:
        Word = item['name']
        num=num+1
        print(num+1)
        PhoneticSymbolUK, PhoneticSymbolUS = SearchWords(Word)
        item['ukphone'] = PhoneticSymbolUK
        item['usphone'] = PhoneticSymbolUS


    # Save the updated JSON data to a new file
    with open('new_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print('Phonetic symbols added to the JSON data and saved in updated_data.json.')

