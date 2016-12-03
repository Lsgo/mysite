# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from .models import UpcCode
from django.shortcuts import redirect
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from ipware.ip import get_ip
from django.core.mail import send_mail


import json
import upcean
import os, tempfile, zipfile  
import MySQLdb
from django.core.servers.basehttp import FileWrapper
from gtin import GTIN
import xlwt   
import time



def upc(request):
    return render(request, 'upc.html')

    
def my_pagination(request, queryset, display_amount=10, after_range_num = 10,bevor_range_num = 4):
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
    
def wish(request):
    # print ('run wish pag')
    db = MySQLdb.connect(user='root', db='pyspider', passwd='24203cjy', host='127.0.0.1')
    cursor = db.cursor()
    cursor.execute('''select a.* ,@x:=ifnull(@x,0)+1 as rownum from (
                    SELECT DISTINCT  id, spu,  title, price, shipfree,  mainimgurl,note,srcsys  
                    FROM wish  WHERE id = 0  order by  inserttime desc  limit 100) a,
                    (select   @x:=0)   as   it ''')
                    
    wishlist = cursor.fetchall()
    db.close()
    print (len(wishlist),wishlist[0][1])
    # return render_to_response('wish.html', {'wishlist': wishlist})
    


    # all_objects = column.article_set.all()

    objects, page_range, total = my_pagination(request, wishlist)

    return render(request, 'wish.html', {

        'objects':objects,
        'page_range':page_range,
        'total': total,
        'wishlist': wishlist
        })

def wishexecl(request):
    
    a = request.GET['a']
    
    print ('run wishexecl pag',a.replace('\t','').replace('\n','').replace(' ',''))
    db = MySQLdb.connect(user='root', db='pyspider', passwd='24203cjy', host='127.0.0.1')
    cursor = db.cursor()
    sqlstr = '''
                    SELECT spu, sku, title, description, tag, brand, upc, lpurl, msrp,
                    color, size, fromurl, price, shipfree, quantity, minday, maxday, 
                    mainimgurl,imgurl1, imgurl2, imgurl3, imgurl4, imgurl5, imgurl6, imgurl7, imgurl8, imgurl9, imgurl10, note,
                    srcsys,inserttime  FROM wish  where  spu in (''' 
    sql = sqlstr +  a.replace('\t','').replace('\n','').replace(' ','') +  ')  and id = 0 order by inserttime,note DESC '
    cursor.execute(sql) 
    wishlist = cursor.fetchall()
    
    sqlstr = "update wish set id = 1 where spu in ('" +  a.replace('\t','').replace('\n','').replace(' ','') + "')"
    db.close()
    
    
    _lst = []  
    _lst.extend(wishlist[:])          
    _lst.insert(0, ['SPU', 'SKU', '名称', '描述', '标签', '商标', '条形码', 'LPURL', '建议售价', '颜色', '尺寸', '来源',
                    '价格', '运费', '数量', '最小天数', '最大天数', '图1', '图2', '图3', '图4', '图5', '图6', '图7',
                    '图8', '图9', '图10', '备注', '系统', '插入时间'])  

    book = xlwt.Workbook(encoding='utf8')   
    sheet = book.add_sheet('untitled')  

    for row, rowdata in enumerate(_lst):  
        for col, val in enumerate(rowdata):  
            sheet.write(row, col, val, style=xlwt.Style.default_style)  

    response = HttpResponse(content_type='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename=wish' + time.strftime('%Y%m%d',time.localtime(time.time())) + '.xls'  
    
  
    
    book.save(response)  
    return response  
    
    
def createCode(request):
    a = int(request.GET['a'])
    b = int(request.GET['b'])
    c = int(request.GET['c'])
    d = int(request.GET['d']) #数量
    e = int(request.GET['e']) #间隔
    
    begCode = int(str(a) + str(b) + str(c))
    endCode = int(str(GTIN(raw=begCode)))
    
    
    # return HttpResponse(str(endCode))
    result = list(range(begCode,begCode + int(d*e),int(e)))
    
    reList= [int(GTIN(raw=i)) for i in result]
    for i in reList:
        upc = str(i)
        barcode = upcean.oopfuncs.barcode('ean13', upc)
        print(barcode.validate_checksum())

        barcode.validate_create_barcode("/home/data/upcImg/"+upc+ ".png", 2)
    return HttpResponse(json.dumps(sorted(reList)), content_type='application/json')
    
def ajax_list(request):

    result = list(range(6907992103136,690799210323,1))
    return HttpResponse(json.dumps(result), content_type='application/json')

def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')

def send_file(request):  
	file_name = 'png.zip'
	file_path = os.path.join('/static/images/upcImg', file_name)
	try:
		tarball_file = open(file_path)
	except IOError:
		raise Http404
	wrapper = FileWrapper(tarball_file)
	response = HttpResponse(wrapper, content_type='application/zip')
# 	response['Content-Encoding'] = 'utf-8'  # 设置该值gzip中间件就会直接返回而不进行后续操作
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	return response

  
  
def send_zipfile(request):  
    """                                                                          
    Create a ZIP file on disk and transmit it in chunks of 8KB,                  
    without loading the whole file into memory. A similar approach can           
    be used for large dynamic PDF files.                                         
    """  
    temp = tempfile.TemporaryFile()  
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    listfile=os.listdir('/static/images/upcImg/')
    for index in listfile:  
        filename = '/static/images/upcImg/' # Select your files here.                             
        archive.write(filename, '%s.png' % index)  
    archive.close()  

    wrapper = FileWrapper(temp)  
    response = HttpResponse(wrapper, content_type='application/zip')  
    response['Content-Encoding'] = 'utf-8'  # 设置该值gzip中间件就会直接返回而不进行后续操
    response['Content-Disposition'] = 'attachment; filename=test.zip'  
    response['Content-Length'] = temp.tell()  
    temp.seek(0)  

    return response  