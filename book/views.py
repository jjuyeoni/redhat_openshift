from django.shortcuts import render, redirect
from  . import dao
from book.models import *
from django.conf import settings

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
import html5lib
from django.http import HttpResponse

# bestseller crawling
def bestSeller():
    title = []
    author_info = []
    href = []
    img_path = []

    url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf?orderClick=d79"
    html = urlopen(url)
    soup = bs(html, "html.parser")
    tmp = soup.find_all('ul', 'list_type01')[0]

    i = 0

    while i < 12:
        for t in tmp.find_all('li'):
            img = t.find('div', 'cover')
            if (img != None):
                img_path.append(img.find('img')['src'])
                title.append(t.find(class_="title").find('strong').get_text())
                href.append(t.find(class_="title").get('href'))
                a = t.find(class_="author").get_text().split()
                author_info.append(a)
                i += 1

    data = {'Title': title, 'Author_info': author_info, 'img_path': img_path}
    df = pd.DataFrame(data)
    df = df.reset_index()
    return df


# recommendation with vetorized category
def similar_recommend_by_cats(booklens_id):
    result = []
    s = np.load('book/matrix/cats_matrix.npy')
    s = np.asmatrix(s)
    book_sim = cosine_similarity(s)

    book_index = booklens_id
    similar_books = sorted(list(enumerate(book_sim[book_index])),key=lambda x:x[1], reverse=True)
    recommended=1

    for book_info in similar_books[1:5]:
        recommended+=1
        result.append(book_info[0])
    return result

# recommendation with vetorized content
def similar_recommend_by_content(booklens_id):
    result = []
    s = np.load('book/matrix/story_matrix.npy')
    s = np.asmatrix(s)
    book_sim = cosine_similarity(s)

    book_index = booklens_id
    similar_books = sorted(list(enumerate(book_sim[book_index])),key=lambda x:x[1], reverse=True)
    recommended=1

    for book_info in similar_books[1:5]:
        recommended+=1
        result.append(book_info[0])
    return result

def parseContent(url, title):
    try :
        html = urlopen(url)
        htmldata = html.read()
        soup = bs(htmldata, "html5lib")

        fb_metas = soup.find_all('meta', attrs={'property':True})
        cats = soup.select('.basicListType ul li a')
        author_trl = soup.select('span.gd_auth a')
        pub_corp = soup.select('span.gd_pub a')
        pub_date = soup.select('span.gd_date')
        pub_ori_title = soup.select('span.gd_origin a')
        book_cont = {}
        prd_sdata =  soup.select('#contents .basicListType td.cell_2col')
        cm = soup.select('div.communtyHide')
    except :
        print('Unexpected Error ', sys.exc_info())
        return False;
    # book_cateogory
    bcats = []
    for c in cats:
        bcats.append(c.text)
    bauthors = []
    for p in author_trl:
        bauthors.append(p.text)
    bcorp =  None if pub_corp == None or len(pub_corp)==0 else pub_corp[0].text
    bdate = None if pub_date == None or len(pub_date)==0 else pub_date[0].text
    bsdata = {}
    for idx,tag in enumerate(prd_sdata):
        tag_text = tag.text
        if idx == 1:
            bsdata['bibli'] = re.sub(r'(\n|\s\s)','', tag_text.strip())
    bdata = {}

    for k in bsdata:
        bdata[k]=bsdata[k]
    bdata['cats'] = ",".join(bcats)
    bdata['authors'] = ",".join(bauthors)
    bdata['corp'] = bcorp
    bdata['pub_date'] = bdate

    if soup.find('a',attrs={'name':'contentsIntro'}) != None:
        t_cnt = 0
        for tag in soup.find('a',attrs={'name':'contentsIntro'}).next_elements:
            t_cnt +=1
            if(t_cnt==2):
                book_intro = re.sub(r'(\n|\s\s)','',tag.text.strip())
                break
    else :
        book_intro = None

    if soup.select('#contents_author') != None and len(soup.select('#contents_author')) != 0:
        author_intro = re.sub(r'(\n|\s\s)','',soup.select('#contents_author')[0].text.strip())
    else :
        author_intro = None
    #출판사 리뷰 파싱
    if( soup.find('a', attrs={'name' : 'contentsMakerReview'}) != None):
        t_cnt = 0
        for tag in soup.find('a', attrs={'name' : 'contentsMakerReview'}).next_elements:
            t_cnt+=1
            if t_cnt == 2:
                maker_review = tag.text
                break
        maker_review = re.sub(r'(\n|\s\s)','',maker_review.strip())
    else :
        maker_review = None

    bdata['book_intro'] = book_intro
    bdata['author_intro'] = author_intro
    bdata['maker_review'] = maker_review
    bdata['title'] = title
    return bdata

# Create your views here.
def book_list(request):
    df = bestSeller()
    bookList=[]
    for i in range(0, 12) :
        a = {'index':df['index'][i] + 1, 'Title':df['Title'][i], 'Author':df['Author_info'][i],'img_path':df['img_path'][i]}
        bookList.append(a)
    return render(request, 'book/book_list.html', {'bookList':bookList})

def search(request):
    if request.method == 'POST' :
        title = request.POST['title']
        bookid = dao.selectBook(title)
        cats = similar_recommend_by_cats(bookid)
        cont = similar_recommend_by_content(bookid)
        cats_result = []
        for i in cats:
            cats_result.append(dao.selectResultBook(str(i+1)))
        cont_result = []
        for i in cont:
            cont_result.append(dao.selectResultBook(str(i+1)))
        return render(request, 'book/search.html', {'cats':cats_result, 'cont':cont_result})

def mybook(request, num):
    b = Blike(u = request.user, b_id = num)
    b.save()
    return redirect(book_list)

def detail(request, title):
    book = dao.selectBookbytitle(title)
    data = parseContent(book['url'], title)
    data['image'] = book['image']
    data['id'] = book['id']
    ganglist = gangnam(title)
    return render(request, 'book/detail.html', {'data':data, 'ganglist':ganglist})

#책검색
def b_search(request):
    return render(request, 'book/book_search.html')

def bAjax(request):
    if request.method == 'POST':
        data = request.POST['title']
        return detail(request, data)
    return render(request, 'book/book_search.html', {'time':time})

import urllib.parse

def gangnam(title):

    url1 = "http://library.gangnam.go.kr/search/tot/result?q="
    url2 = urllib.parse.quote_plus(title)
    url3 = "&st=EXCT&si=TOTAL&oi=&os=&cpp=50"

    pageurl = url1+url2+url3
    Url = urlopen(pageurl)
    soup1 = bs(Url, "html.parser")

    g_library = soup1.select("dd.bookline.locCursor > span")

    liblist_list =[]
    liblist = {
        'libname':'',
        'libstatus':'',
    }
    for library in g_library:
        libname = library.contents[0]
        libstatus = library.contents[1].text
        liblist = {
            'libname' : libname,
            'libstatus' : libstatus
            }
        liblist_list.append(liblist)
    return liblist_list
