# from django.shortcuts import render
from django.http import HttpResponse
import simplejson


# Create your views here.
def test(request):
    print('>>>>>>>>>>>>>>>>>>', request)
    data = '测试自建组件msg!!!!!!!!'
    return HttpResponse(simplejson.dumps({'result': data}))


def login(request):
    sess = request.session
    print('>>>>>>>>>>>', request.POST)
    sess['user_name'] = request.POST.get('user_name')
    sess.set_expiry(30)
    print('session--------------->', sess['user_name'])
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def sys_home(request):
    sess = request.session
    if sess.get('user_name'):
        return HttpResponse(simplejson.dumps({'result': 'ok'}))
    else:
        return HttpResponse(simplejson.dumps({'result': '请登录'}))


def exit(request):
    sess = request.session
    if sess.get('user_name'):
        del sess['user_name']
    return HttpResponse(simplejson.dumps({'result': 'ok'}))
