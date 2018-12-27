#coding=utf-8
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from models import *
from django.db.models import Q

#from hashlib import sha1
def register(request):
	return render(request,'df_user/register.html')
def register_handle(request):
	#接收用户输入
	post = request.POST
	uname = post.get('user_name')
	upwd = post.get('pwd')
	upwd2 = post.get('cpwd')
	uemail = post.get('email')
	#判断两次密码
	if upwd!=upwd2:
		return redirect('/user/register/')
	#密码加密
	#s1 =sha1()
	#s1.update(upwd)
	#upwd3=s1.hexdigest()
	#创建对象
	user=UserInfo()
	#给对象的属性赋值
	user.uname=uname
	user.upwd=upwd
	user.uemail=uemail
	#保存到数据库中
	user.save()
	#注册成功，转到登陆页面
	return redirect('/user/login/')
def register_exist(request):
	uname = request.GET.get('uname')
	count=UserInfo.objects.filter(uname=uname).count()
	return JsonResponse({'count':count})

def login(request):
	uname=request.COOKIES.get('uname','')
	context={'title':'用户登陆','error_name':0,'error_pwd':0,'uname':uname}
	return render(request,'df_user/login.html',context)

def  login_handle(request):
	#接受请求信息
	post=request.POST
	uname=post.get('username')
	upwd=post.get('pwd')
	jizhu=post.get('jizhu',0)
	#根据用户名查询对象
	users=UserInfo.objects.filter(uname=uname)
	#判断：如果未查到用户信息，则用户名错误。如果查到用户信息，存储到session中，并跳转到用户信息界面
	if len(users)!=0:
		
		if upwd==users[0].upwd:
			red = HttpResponseRedirect('/user/info/')
			if jizhu!=0:
				red.set_cookie('uname',uname)
			else :
				red.set_cookie('uname','',max_age=-1)
			request.session['user_id']=users[0].id
			request.session['user_name']=uname
			return red
		else:
			context={'title':'用户登陆','error_name':0,'error_pwd':1,'uname':uname}
			return render(request,'df_user/login.html',context)
	else:
		context={'title':'用户登陆','error_name':1,'error_pwd':0,'uname':uname}
		return render(request,'df_user/login.html',context)
def info(request):
	id=request.session['user_id']
	user_name=request.session['user_name']
	user_email=UserInfo.objects.get(id=id).uemail
	user_address=UserInfo.objects.get(id=id).uaddress
	context={'title':'用户中心',
			 'user_email':user_email,
			 'user_name':user_name,
			 'uaddress':user_address
			 }
	return render(request,'df_user/user_center_info.html',context)

def site(request):
	id=request.session['user_id']
	user=UserInfo.objects.get(id=id)
	context={'title':'用户中心',
			 'ushou':user.ushou,
			 'uaddress':user.uaddress,
			 'uyoubian':user.uyoubian,
			 'uphone':user.uphone
			}
	return render(request,'df_user/user_center_site.html',context)
def site_handle(request):
	post=request.POST
	id=request.session['user_id']
	user=UserInfo.objects.get(id=id)
	user.ushou=post.get('ushou')
	user.uaddress=post.get('uaddress')
	user.uyoubian=post.get('uyoubian')
	user.uphone=post.get('uphone')
	user.save()
	context={'title':'用户中心',
			 'ushou':user.ushou,
			 'uaddress':user.uaddress,
			 'uyoubian':user.uyoubian,
			 'uphone':user.uphone
			}
	return render(request,'df_user/user_center_site.html',context)