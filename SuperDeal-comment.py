from selenium import webdriver
import time 
import selenium.webdriver
from bs4 import BeautifulSoup
import openpyxl
import pandas as pd
from datetime import datetime
from konlpy.tag import *
from konlpy.utils import pprint


wd = openpyxl.load_workbook('test1.xlsx')
ws = wd.active
alldfcontents = []

for r in ws.rows:
    row_index = r[0].row
    kor = r[1].value
    alldfcontents.append(kor)

    if row_index == 40:
        break
tt = list(filter(None.__ne__, alldfcontents))


# 슈퍼딜

    
## 여기서부터
def Superdeal(a):   
    print("wait pleas.....")
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.implicitly_wait(1.5)
    driver.get('http://mitem.gmarket.co.kr/Item?goodsCode='+ a)
    time.sleep(1)   
    driver.find_element_by_xpath('//*[@id="mainTab1"]/button').click()
    time.sleep(1.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser') 
    driver.close()
    #print (soup)
    return soup
## -> 여기까지가 파싱을 받는 부분

def Countt(soup):
##--> 여기는 상품평 수
#contents = soup.find('div', { 'class': 'review' })
    contents5 = soup.find('a', { 'id': 'photoReviewTab' })
    contents6 = soup.find('a', { 'id': 'textReviewTab' })
#상품평 숫자를 가져온다
#프리미엄 상품평 숫자 contents5.span.text
#일반 상품평 숫자 contents6.span.text
    #print(contents5.span.text, contents6.span.text)
    countz = [contents5.span.text, contents6.span.text]
    #print(countz)
    return countz
  
    
    
def Countt2(soup):    
    #soup = BeautifulSoup(html, 'html.parser')
    contents0 = soup.find('div', { 'id': 'photoReviewArea' })
    contents02 = contents0.select('ul > li > a')
   
#상품평을 가져온다

    dfcontent0 = []
    alldfcontents0 = []
    tdst = []
    i = 0
    for content00 in contents02:
        tds=content00.find_all("p")
        tds.pop(0)
        tds.pop(0)
# 옵션,상품평 제목을 지운다
        for td in tds:
            dfcontent0.append(td.text)
    #print(dfcontent0)
    return dfcontent0
    
#check = ['709183717',contents5.span.text,contents6.span.text]
#driver.close()
   
#a = Superdeal()
#a
#Countt(a)
#Countt2(a)

#dfcontent0 =  Countt2(a)
#qq = Countt(a) + Countt2(a)
#print(qq)



#엑셀에 있는 상품 코드를 최대 40개까지 들고와서, 빈칸은 없앤다


#긍정수 카운트
## 긍정 부정 나누는 부분

#-*- coding: utf-8 -*-
 


def monn(dfcontent0):
# get the data
# tag list (보통명사, 동사, 형용사, 보조동사, 명사추정범주) 
# 참고 : https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0
    kkma = Kkma()
    f_pos = open('positive.txt', 'r')
    f_neg = open('negative.txt', 'r')
    f_neu = open('neutral.txt', 'r')
    f_test = open('test.txt', 'r')

    list_tag = [u'NNG', u'VV', u'VA', u'VXV', u'UN']
    list_positive=[]
    list_negative=[]
    list_neutral=[]
    iii = 0  
    Q = 0
    for T in dfcontent0:

        test_s = dfcontent0[Q]
        test_list=kkma.pos(test_s)
    #test_list=kkma.pos(dfcontent0)

        test_output=[]
        for i in test_list:
            if i[1] == u'SW':
                if i[0] in [u'♡', u'♥']:
                    test_output.append(i[0])
            if i[1] in list_tag:
                test_output.append(i[0])

        test_list=kkma.pos(test_s)

    #print(test_s)
    #print(test_list)
        Q = Q + 1    

        list_positive = getting_list(f_pos, list_positive)
        list_negative = getting_list(f_neg, list_negative)
        list_neutral = getting_list(f_neu, list_neutral)
 
        ALL = len(set(list_positive))+len(set(list_negative))+len(set(list_neutral))
 

        result_pos = naive_bayes_classifier(test_output, list_positive, ALL)
        result_neg = naive_bayes_classifier(test_output, list_negative, ALL)
        result_neu = naive_bayes_classifier(test_output, list_neutral, ALL)
    
        if (result_pos > result_neg and result_pos > result_neu):
            #print ('긍정')
            iii = iii + 1
        elif (result_neg > result_pos and result_neg > result_neu):
            c = 1
            #print ('부정')
        else:
            #print ('중립')
            c = 0
    return iii
    print(iii)
    
    f_pos.close()
    f_neg.close()
    f_neu.close()
    f_test.close()


#make lists
def getting_list(filename, listname):
    kkma = Kkma()
    while 1:
        line = filename.readline()
        str = line
        #str = unicode(line, 'utf-8')
        line_parse = kkma.pos(str)
        list_tag = [u'NNG', u'VV', u'VA', u'VXV', u'UN']
        for i in line_parse:
            if i[1] == u'SW':
                if i[0] in [u'♡', u'♥']:
                    listname.append(i[0])
            if i[1] in list_tag:
                listname.append(i[0])
        if not line:
            break
    return listname
 
#naive bayes classifier + smoothing
def naive_bayes_classifier(test, train, all_count):
    counter = 0
    list_count = []
    for i in test:
        for j in range(len(train)):
            if i == train[j]:
                counter = counter + 1
        list_count.append(counter)
        counter = 0
    list_naive = []
    for i in range(len(list_count)):
        try:
            list_naive.append((list_count[i]+1)/float(len(train)+all_count))
        except ZeroDivisionError:
            print("zero")
    result = 1
    for i in range(len(list_naive)):
        result *= float(round(list_naive[i], 6))
    return float(result)*float(1.0/3.0)
    
#a = Superdeal()
#a
#Countt(a)
#Countt2(a)

#dfcontent0 =  Countt2(a)
#qq = Countt(a) + Countt2(a)
#print(qq)


#웹드라이버로 TT를 가져와서 CC2로 하나씩 넘겨 실행 시킨다

ala = []
for i in tt:
    cc2 = str(i)
#    ala.append(Superdeal(cc2))
    a = Superdeal(cc2)
    q2 =  Countt2(a)
    #print(q2)
    cc = monn(q2)
    ee = str(cc)
    cc2 =  Countt(a)
    #print(cc2)
#+ dfcontent0
    cc2.extend(ee)
    yy = cc2
    yy.extend(q2)
    yy.insert(0, i)
    print(yy)
    ala.append(yy)
        

ala2 = ['code', 'premium-coment', 'text-coment', 'possi-coment', 'pre-coment1','pre-coment2', 'pre-coment3', 'pre-coment4', 'pre-coment5', 'pre-coment6', 'pre-coment7', 'pre-coment8', 'pre-coment9', 'pre-coment10']
df=pd.DataFrame(columns=ala2, data=ala)
dd1 = datetime.today().strftime("%Y%m%d")
dd = str(dd1)
da = './' + dd + '.xlsx'
df.to_excel(da,sheet_name='coupon2',header=True, startrow=1, startcol=1)
print(df)
print ('finished -> ' + da + ' <- check this file')

