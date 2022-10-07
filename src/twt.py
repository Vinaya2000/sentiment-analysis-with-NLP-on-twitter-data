
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
import pymysql

import requests
def readtwitinfo(p,id):
    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="sentiment_analysis")
    cmd = con.cursor()
    res=requests.get("https://www.google.com/search?q="+p+" twitter")

    txt=res.text.split('<div class="BNeawe s3v9rd AP7Wnd">')
    resset=[]
    for i in range(1,len(txt)):
        ii=txt[i].split('</div>')
        rr = cleanhtml(ii[0])
        print(rr)
        row=[]
        row.append(rr)
        rat=sent(rr)
        row.append(rat)
        resset.append(row)
        rr=rr.replace("'"," ")
        if rr!='':
            cmd.execute("INSERT INTO `twitter` VALUES(NULL,'"+id+"','"+rr+"','"+str(rat)+"')")
            con.commit()
    print("============================================================")

    res=requests.get("https://www.google.com/search?q="+p+" twitter,page=2")

    txt=res.text.split('<div class="BNeawe s3v9rd AP7Wnd">')
    print (len(txt))

    for i in range(1,len(txt)):
        ii=txt[i].split('</div>')

        rr=cleanhtml(ii[0])
        print(rr)
        row = []
        row.append(rr)
        rat = sent(rr)
        row.append(rat)
        resset.append(row)
        rr=rr.replace("'"," ")
        if rr!='':
            cmd.execute("INSERT INTO `twitter` VALUES(NULL,'" + id + "','" + rr + "','" + str(rat) + "')")
            con.commit()
    return resset



def sent(k):
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    pstv=0
    ngtv=0
    ntl=0
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(k)
    a = float(ss['pos'])
    c = float(ss['neg'])
    b = float(ss['neu'])

    print(ss)
    rating=0
    if (c >a and c>b) or (a==0.0 and c!=0.0):
        res = "negative"

        rating=(c*5)
        rating=0-rating

    elif (a>b and a>c) or (c==0.0 and a!=0.0):
        if b>a:
            a=b
        rating = (a * 5)
        rating = rating
        res="positive"
    else:
        rating=0
    return  rating
# print(sent("good product with some  qualityes"))
