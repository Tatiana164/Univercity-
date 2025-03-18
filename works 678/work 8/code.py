import pymorphy3
from deep_translator import GoogleTranslator

perevodchik = GoogleTranslator(source='auto', target='en')
morph = pymorphy3.MorphAnalyzer()
dc = {}
temp = []
fin = []
cnt = 0

with open(r'сюда вставляешь путь к файлу с диалогом с расширением txt', encoding='utf-8') as f: #перед тем как вставить путь к жтому файлу перемести его в папку в которой будет лежать код для 8 работы
    ls = []

    for line in f:
        lst = line.split()
        words = []
        
        for word in lst:
            p = morph.parse(word)[0]
            words.append(p.normal_form)
        ls.append(words)

f.close()

for line in ls:
    for i in line:

        if dc.get(i) is None:
            dc[i] = 1

        else:
            dc[i] = 1 + dc[i]

file = open(r'сюда вставляешь путь к файлу с результатами с разрешением txt', 'w', encoding='utf-8') #перед тем как вставлять путь к этому файлу нужно в папке с проектом где лежит код и файл с диалогом создать файл с результатами с форматом txt
file.write('Start word | Translate | Number of Mentions')

for iter in sorted(list(dc.items()), key=lambda k: k[1], reverse=True):

    itrnsl = perevodchik.translate(iter[0])
    file.write(f'\n{iter[0]} | {itrnsl} | {iter[1]}')

file.close()