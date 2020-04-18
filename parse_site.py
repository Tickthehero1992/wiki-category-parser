from bs4 import BeautifulSoup
import requests as req
path_auto="new_catalog_auto.csv"
url_auto="https://ru.wikipedia.org/wiki/Категория:Автомобили_по_маркам"

path_moto="new_catalog_moto.csv"
url_moto="https://ru.wikipedia.org/wiki/Категория:Мотоциклы_по_маркам"

def Fisrt_tag_parse(tag,name):
    tag = tag.text.replace(name, '')
    tag = tag.replace('[×]', '')
    tag = tag.replace('►', '')
    tag = tag.replace('‎', '')
    tag = tag.split('\n')
    # print(tag)

    tag_created = []
    for t in tag:
        i = 0
        for ch in t:
            if ch == '(':
                tag_created.append(t[:i-1])
            i = i + 1
    return  tag_created
    # print(tag_created)

def Second_tag_parse(tag,name):
    tag = tag.text.replace(name, '')
    tag = tag.split('\n')
    #print(tag)
    tag_created=[]
    for i in range(len(tag)):
        if i==0:
            pass
        elif i==len(tag)-1 or i==1:
            tag_created.append(tag[i])
            #print(tag_created)
        else:
            tag_created.append(tag[i][:-1:])

    return tag_created

def Parser_wiki(url,name,path):
    resp = req.get(url)
    last=0
    # print(resp.text)
    soup = BeautifulSoup(resp.content, 'html.parser')
    tags = soup.find_all('div', {'class': 'mw-category'})
    catalog_of_marks = open(path, mode='w', encoding='utf8')
    first=True
    catalog_of_marks.write('id;name;\n')
    for tag in tags:

        if first==True:
            tag_created=Fisrt_tag_parse(tag, name)
            first=False
        else:
            tag_created=Second_tag_parse(tag, name)

        output = []
        for t in tag_created:
            t = t.replace('   ', '')
            t = t.replace('  ', '')
            if first==True: t = t.replace(' ', '')
            output.append(t)
        #   print(output)



        i = 0
        for k in output:
            outputstr = str(i+last) + ';' + output[i] + ';'+'\n'
                        #+translit(output[i],'ru')+'\n'
            catalog_of_marks.write(outputstr)
            i = i + 1
        last=i
    catalog_of_marks.close()

#Parser_wiki(url_auto,'Автомобили',path_auto)
#Parser_wiki(url_moto,'Мотоциклы', path_moto)
Parser_wiki("https://ru.wikipedia.org/wiki/Категория:Преступления", 'Преступления', "new_catalog_crimes.csv")