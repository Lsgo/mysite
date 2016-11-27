# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import Column, Article, User
from django.shortcuts import redirect
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator



def my_pagination(request, queryset, display_amount=20, after_range_num = 5,bevor_range_num = 4):
    #按参数分页
    paginator = Paginator(queryset, display_amount)
    try:
        #得到request中的page参数
        page =int(request.GET.get('page'))
    except:
        #默认为1
        page = 1
    try:
        #尝试获得分页列表
        objects = paginator.page(page)
        total = paginator.num_pages
    #如果页数不存在
    except EmptyPage:
        #获得最后一页
        objects = paginator.page(paginator.num_pages)
    #如果不是一个整数
    except:
        #获得第一页
        objects = paginator.page(1)
    #根据参数配置导航显示范围
    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:page+bevor_range_num]

    return objects,page_range,total



class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())


class UserRegistForm(forms.Form):
    username = forms.CharField(label='Username',max_length=100)
    password = forms.CharField(label='Password',widget=forms.PasswordInput())
    checkpwd = forms.CharField(label='checkpwd',widget=forms.PasswordInput())

#注册
def regist(request):
    if request.method == 'POST':
        uf = UserRegistForm(request.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            checkpwd = uf.cleaned_data['checkpwd']

            if password == checkpwd:
            #添加到数据库
                User.objects.create(username= username,password=password)
                return HttpResponse('regist success!!')
            else:
                return HttpResponse('两次密码不一致!!')
    else:
        uf = UserRegistForm()
    return render_to_response('regist.html',{'uf':uf}, context_instance=RequestContext(request))

#登陆
def login_view(request):
    uf =UserLoginForm(request.POST)
    if uf.is_valid():
        username = uf.cleaned_data['username']
        password = uf.cleaned_data['password']
        user = authenticate(username =username, password = password)
        if user is not None:
            if user.is_active:
                m = User.objects.get(username=username )

                login(request, user)
                #比较成功，跳转index
                response = HttpResponseRedirect('/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                request.session['member_id'] = m.id
                return response
            else:
                print ("Your account has been disabled!")
                return HttpResponseRedirect('/login')
        else:
            print ("Your username and password were incorrect.")
    else:
        uf = UserLoginForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(request))

#退出
def logout_view(request):
    logout(request)
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return HttpResponseRedirect('/login')


def index(request):
    print (request.session.get('member_id'))
    print ('index username ', request.COOKIES.get('username',''))
    print ('is_authenticated', request.user.is_authenticated())
    if request.user.is_authenticated():
        print ('go to index')
        home_display_columns = Column.objects.filter(home_display=True)
        nav_display_columns = Column.objects.filter(nav_display=True)


        return render(request, 'news.html', {
            'home_display_columns': home_display_columns,
            'nav_display_columns': nav_display_columns,
            'username':request.user.username
        })
    print ('go to login from index')
    return HttpResponseRedirect('/login')

def column_detail(request, column_slug):
    if request.user.is_authenticated():
        column = Column.objects.get(slug=column_slug)

        all_objects = column.article_set.all()
        home_display_columns = Column.objects.filter(home_display=True)
        nav_display_columns = Column.objects.filter(nav_display=True)
        objects, page_range, total = my_pagination(request, all_objects)

        return render(request, 'himg/column.html', {
            'column': column,
            'objects':objects,
            'page_range':page_range,
            'total': total,
            'home_display_columns': home_display_columns,
            'nav_display_columns': nav_display_columns,
            'username':request.user.username,
            })
    return HttpResponseRedirect('/login')

def article_detail(request, pk, article_slug):
    if request.user.is_authenticated():
        article = Article.objects.get(pk=pk)

        if article_slug != article.slug:
            return redirect(article, permanent=True)

        return render(request, 'himg/article.html', {'article': article})
    return HttpResponseRedirect('/login')


def declaration(request):
    # return HttpResponseRedirect('/disclaimer.html')
    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)
    return render(request, 'disclaimer.html', {
            'home_display_columns': home_display_columns,
            'nav_display_columns': nav_display_columns,
            'username':request.user.username
        })

def aboutus(request):
    # return HttpResponseRedirect('/disclaimer.html')
    home_display_columns = Column.objects.filter(home_display=True)
    nav_display_columns = Column.objects.filter(nav_display=True)
    return render(request, 'aboutus.html', {
            'home_display_columns': home_display_columns,
            'nav_display_columns': nav_display_columns,
            'username':request.user.username
        })
        
