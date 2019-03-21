# from django.shortcuts import render
from django.http import HttpResponse
import simplejson


# Create your views here.
def test(request):
    print('>>>>>>>>>>>>>>>>>>', request)
    data = '测试自建组件msg!!!!!!!!'
    return HttpResponse(simplejson.dumps({'result': data}))


def login(request):
    print('>>>>>>>>>>>', request.POST)
    login_data = request.POST
    print(login_data.get('user_name'))
    print('user_name:{}    ,password:{}'.format(login_data['user_name'], login_data['password']))
    return HttpResponse(simplejson.dumps({'result': 'ok'}))
