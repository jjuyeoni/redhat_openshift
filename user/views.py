from django.shortcuts import render, redirect
from book.models import Blike
from . import dao
from book.dao import *
from book.views import book_list
from django.contrib.auth import (
    # authenticate,
    # login as django_login,
    logout as django_logout,
)
# Create your views here.
def login(request):
    return render(request, 'user/login.html', {})

def logout(request):
    django_logout(request)
    return redirect(book_list)

def mypage(request):
    b_id = dao.selectBlike(request.user.id)
    cnt = dao.countBlike(request.user.id)
    bList=[]
    for i in b_id:
        bList.append(selectBookbyid(i))
    l_id = dao.selectAllBlike(request.user.id)
    print(l_id)
    fname = "book/static/img/" + str(l_id[len(l_id) - 1]) + "_" + str(request.user.id) + ".png"
    print("fname",fname)
    if os.path.isfile(fname):
        g = "/static/img/" + str(l_id[len(l_id) - 1]) + "_" + str(request.user.id) + ".png"
    else :
        g = "/static/img/book_bg.jpg"

    return render(request, 'user/mypage.html', {'bList':bList, 'cnt':cnt, 'fname':g})

def cancer(request, num):
    dao.deletBlike(num, request.user.id)
    return redirect(mypage)
    
