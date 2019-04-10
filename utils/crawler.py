from urllib.error import URLError, HTTPError
import urllib.parse as parse
import urllib.request as request
import hashlib
import http.cookiejar
import simplejson
import zlib
import chardet
import os


class Crawler:
    def __init__(self, url, header):
        self._url = url
        self._headers = header

    def open_url(self, data, save_cookie_file_name, salt=None):
        if (salt is not None):
            # 把密码加密
            data['password'] = self.md5_passwd(data['password'], salt)
        # 这里判断有没有data是为了区分是post还是get请求
        if (data is None):
            # 创建get请求对象
            req = request.Request(self._url, headers=self._headers)
        else:
            # 创建post请求对象并设置请求头和把请求数据转为byte类型
            req = request.Request(self._url, bytes(parse.urlencode(data), encoding='utf8'),
                                  headers=self._headers)
        response = self.cookies_options(req, save_cookie_file_name)
        return response

    def md5_passwd(self, data, salt):
        md = hashlib.md5()
        data = data + salt
        md.update(data.encode('utf-8'))
        return md.hexdigest()

    def cookies_options(self, req, file_name):
        # 创建cookie对象
        cookie_data = http.cookiejar.MozillaCookieJar(file_name)
        # 创建cookie处理器
        handler = request.HTTPCookieProcessor(cookie_data)
        # 创建发送请求的工具对象
        opener = request.build_opener(handler)
        try:
            # 判断是否有存放cookie的文件
            if (not os.path.exists(file_name)):
                # 进来这里说明没有这个文件,先发送请求,然后储存cookie到cookie文件中
                response = opener.open(req)
                cookie_data.save(ignore_discard=True, ignore_expires=True)
                return response
            # 读取cookie文件
            cookie_data.load(file_name, ignore_discard=True, ignore_expires=True)
            # 使用cookie发送请求
            response = opener.open(req)
            return response
        except HTTPError as e:
            # 请求url如果没错的话请求404一般是应为cookie没有导致的
            if (e.code == 404):
                # 判断是否有储存cookie的文件,有则将文件删除
                if (os.path.exists(file_name)):
                    os.remove(file_name)
                # 从新模拟登陆获取新的cookie
            login()
        except URLError as e:
            print(e.reason)


def action(url, headers, data=None, file_name='./cookie.txt', salt=None):
    c = Crawler(url, headers)
    if (salt is not None):
        return c.open_url(data=data, save_cookie_file_name=file_name, salt=salt)
    else:
        return c.open_url(data=data, save_cookie_file_name=file_name)


def headers():
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Connection': 'keep - alive',
        # 'Referer': 'http//www.gsafetycloud.com/operation-management/index.html',
        'Content - Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'X - Requested - With': 'XMLHttpRequest',
        'Host': 'www.gsafetycloud.com',
        # 'Origin': 'http://www.gsafetycloud.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        # 'cookie':cookie
    }
    return headers


def format_data(data, char_set='utf-8'):
    try:
        data = simplejson.loads(data.read().decode(char_set))
    except AttributeError as e:
        print(e)
    return data


def login():
    data = {
        'loginName': 'km01',
        'password': 'a123456',
        'systemCode': ''
    }
    login_url = 'http://www.gsafetycloud.com/operation-management/login/toLogin1.mvc'
    # 模拟登陆储存cookie
    salt = 'true'
    return format_data(action(login_url, headers(), data=data, salt=salt))


def crawl_data(url, data=None):
    return format_data(action(url=url, headers=headers(), data=data))


if __name__ == '__main__':
    forent_url = {
        'backUrl': 'http://www.gsafetycloud.com/operation-management',
        'operation_url': 'http://www.gsafetycloud.com/api/v1.1/operation-management',
        'base_url': 'http://www.gsafetycloud.com/api/v1/fire-society',
    }

    # # 获取用户信息,如果出错表面未登陆
    # user_msg = crawl_data(forent_url['backUrl'] + '/user/getUserMsg.mvc', data={})
    # print(user_msg)
    #
    # # 获取地图所有数据
    # map_sarch_data = {
    #     'orgCode': user_msg['orgCode'],
    #     "unitState": "",
    #     "queryType": "012"
    # }
    # map_data = crawl_data(forent_url['operation_url'] + '/gisView/mapLocation', map_sarch_data)
    #
    # # 遍历地图数据
    # for i in map_data['data']:
    #     if ('unitType' in i):
    #         print(i)
    #         print('单位编码:[', i['id'], ']', '单位名称:[', i['name'], ']', '单位类型:[', i['unitType'], ']', '单位状态:[',
    #               i['unitState'], ']', '单位地址:[', i['address'], ']', '单位经纬度:[', i['latitude'], '&',
    #               i['longitude'], ']')

    # 获取消防管家地图数据和消防管家实时报警,检测故障,当前隐患数接口
    fire_housekeeper_urls_get = [
        'getChildOrg',  # 地图数据
        'getInfoNum',  # 实时报警,检测故障,当前隐患数
    ]

    # 获取消防管家地图 实时报警 监测故障 当前隐患信息接口
    fire_housekeeper_urls_post = [
        'queryTodayAlarmCountTop5',  # 实时报警
        'queryTodayAccidentCheckCountTop5',  # 监测故障
        'queryTodayHiddenCountTop5',  # 当前隐患
        'queryAlarmInfo',  # 企业报警信息
        'queryThirtyAlarmCountInfo',  # 报警趋势
        'queryThirtyAccidentCountInfo',  # 隐患趋势
    ]
    # 消防管家加载用户信息
    req_user_info_data = {
        'loginName': 'whxfdd'
    }
    user_info = crawl_data(forent_url['base_url'] + '/sys/user/getUserMsg.mvc', data=req_user_info_data)
    print('消防管家加载用户信息:', user_info)

    # 消防管家http头
    http_head_data = crawl_data(forent_url['base_url'] + '/sys/org/' + user_info['orgCode'])
    print('消防管家http头:', http_head_data)

    # 获取消防管家地图数据和消防管家实时报警,检测故障,当前隐患数
    for i in fire_housekeeper_urls_get:
        url = (forent_url['base_url'] + '/group/index/{}?orgCode=' + user_info['orgCode']).format(i)
        data = crawl_data(url)
        print(data)

    # 获取消防管家地图 实时报警 监测故障 当前隐患信息
    for i in fire_housekeeper_urls_post:
        url = (forent_url['base_url'] + '/group/index/{}').format(i)
        print(url)
        data = crawl_data(url=url, data={'orgCode': user_info['orgCode']})
        print(data)

