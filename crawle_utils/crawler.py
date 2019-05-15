from urllib.error import HTTPError
import urllib.parse as parse
import urllib.request as request
import hashlib
import http.cookiejar
import simplejson
import os

try:
    from .config_util import yaml_util
except ModuleNotFoundError as e:
    from config_util import yaml_util
except ImportError as e:
    from config_util import yaml_util

# 获取本模块路径
current_path = os.path.abspath(os.path.dirname(__file__))
# 获取本模块下配置文件中的数据对象
configs = yaml_util.YamlLoadUtil(current_path + '/crawle_config.yaml').get_config_data()


class Crawler:
    """
    爬取数据的类
    """

    def __init__(self, url, header):
        """
        爬取数据类构造函数
        :param url: 需要爬取的数据的url
        :param header: 爬取数据的header信息
        """
        self._url = url
        self._headers = header

    def open_url(self, data, save_cookie_file_name, salt=None):
        """
        发送请求的函数
        :param data: 发送请求的参数
        :param save_cookie_file_name: 需要将cookie保存到文件的文件名
        :param salt: 如果是登录,则需要将密码加密,密码加密所用的盐
        :return: http响应对象
        """
        if salt is not None:
            # 把密码加密
            data['password'] = self.md5_password(data['password'], salt)
        # 这里判断有没有data是为了区分是post还是get请求
        if data is None:
            # 创建get请求对象
            req = request.Request(self._url, headers=self._headers)
        else:
            # 创建post请求对象并设置请求头和把请求数据转为byte类型
            req = request.Request(self._url, bytes(parse.urlencode(data), encoding='utf8'),
                                  headers=self._headers)
        response = self.cookies_options(req, save_cookie_file_name)
        return response

    def md5_password(self, password, salt):
        """
        使用md5将密码加密函数
        :param password: 登录的密码
        :param salt: 将密码加密用的盐
        :return: 加密后的密码
        """
        md = hashlib.md5()
        password_md5 = password + salt
        md.update(password_md5.encode('utf-8'))
        return md.hexdigest()

    def cookies_options(self, req, file_name):
        """
        操作cookie的函数
        :param req: http请求对象
        :param file_name: 保存cookie的文件名称
        :return: http响应对象
        """
        # 创建cookie对象
        cookie_data = http.cookiejar.MozillaCookieJar(file_name)
        # 创建cookie处理器
        handler = request.HTTPCookieProcessor(cookie_data)
        # 创建发送请求的工具对象
        opener = request.build_opener(handler)
        try:
            # 判断是否有存放cookie的文件
            if not os.path.exists(file_name):
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
            if e.code == 404:
                # 判断是否有储存cookie的文件,有则将文件删除
                if os.path.exists(file_name):
                    os.remove(file_name)
                    # 从新模拟登陆获取新的cookie
                    login()
            e.msg


def action(url, headers, data=None, file_name='cookie.txt', salt=None):
    """
    执行整个爬取数据的函数
    :param url: 需要爬取数据的url
    :param headers: 爬取数据的http的header
    :param data: 请求的参数
    :param file_name: cookie保存的文件,默认是cookie.txt
    :param salt: 将密码加密所用的盐
    :return: http响应对象
    """
    # 获取爬取数据对象
    c = Crawler(url, headers)
    # 判断是否有加密盐,如果有则是登录,没有则是数据爬取
    if salt is not None:
        return c.open_url(data=data, save_cookie_file_name=file_name, salt=salt)
    else:
        return c.open_url(data=data, save_cookie_file_name=file_name)


def headers():
    """
    :return: http请求头
    """
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content - Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'www.gsafetycloud.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        # 'Connection': 'keep - alive',
        # 'Referer': 'http//www.gsafetycloud.com/operation-management/index.html',
        # 'X - Requested - With': 'XMLHttpRequest',
        # 'Origin': 'http://www.gsafetycloud.com',
        # 'cookie':cookie
    }
    return headers


def format_data(data, char_set='utf-8'):
    """
    将响应对象数据格式化为json对象函数
    :param data: 响应对象
    :param char_set: 格式化的编码,默认为utf-8
    :return: 格式化为json的json对象
    """
    try:
        return_data = simplejson.loads(data.read().decode(char_set))
        if 'data' in return_data:
            return return_data['data']
        return return_data
    except AttributeError as e:
        if e.__str__() == "'NoneType' object has no attribute 'read'":
            login()
        else:
            raise e


def fh_send_get(interface, params, api_url):
    """
    爬取消防管家get请求数据函数
    :param interface: 爬取数据接口
    :param params: 发送请求参数
    :param api_url: 发送请求的api_url
    :return: 爬取到的数据
    """
    interface_url = format_url(api_url)
    data = crawl_data(interface_url.format(interface, params))
    return data


def fh_send_post(interface, params, api_url):
    """
    爬取消防管家post请求数据函数
    :param interface: 爬取数据接口
    :param params: 发送请求参数
    :param api_url: 发送请求的api_url 默认是配置文件中的base_url
    :return: 爬取到的数据
    """
    interface_url = format_url(api_url).format(interface)
    data = crawl_data(url=interface_url, data=params)
    return data


# 若未登陆外部使用login作为登陆模拟的函数
def login():
    """
    模拟登录的函数
    :return: 登录是否成功响应
    """
    data = configs['login_data']
    login_url = format_url(configs['api_url']['toLogin'])
    # 密码加密盐
    salt = configs['salt']
    return format_data(action(login_url, headers(), data=data, salt=salt))


# 外部使用主要函数
def crawl_data(url, data=None):
    """
    外部使用爬取数据主要函数
    :param url: 需要爬取数据的url
    :type url:str
    :param data: 发送请求的参数
    :type data:dict or str
    :return: http请求响应数据
    """
    return format_data(action(url=url, headers=headers(), data=data))


# 外部使用主要函数
def format_url(api_url):
    """
    外部使用格式化url主要函数函数,将系统域名与api_url进行拼接
    :param api_url: 发送请求的url
    :type api_url:str
    :return: 格式化好的url
    """
    return configs['system_url'].format(api_url)


# 外部使用主要函数
def get_fh_data(interface_list, params, api_url, appoint_interface=None):
    """
    外部使用爬取消防管家数据的主要函数
    :param interface_list: 需要爬取数据的接口list
    :type interface_list:list
    :param params: 发送请求的参数
    :type params:dict
    :param api_url: 发送请求的url
    :type api_url:str
    :param appoint_interface: 向指定接口发送请求,默认为None,如果为None则取所有接口数据
    :type appoint_interface:str
    :return: 指定爬取接口数据或者所有接口数据
    """
    all_data = []
    for interface in interface_list:
        # 判断是否有指定接口名,没有则取所有
        if appoint_interface is None:
            # 判断请求参数的类型是str则发送get请求
            if isinstance(params, str):
                data = fh_send_get(interface, params, api_url)
            # 是dict则发送post请求
            elif isinstance(params, dict):
                data = fh_send_post(interface, params, api_url)
            all_data.append(data)
        else:
            # 有指定接口名则只取指定接口数据
            if appoint_interface == interface:
                # 判断请求参数的类型是str则发送get请求
                if isinstance(params, str):
                    return fh_send_get(appoint_interface, params, api_url)
                # 是dict则发送post请求
                elif isinstance(params, dict):
                    return fh_send_post(appoint_interface, params, api_url)
            # 不是指定的接口则跳过该次循环
            else:
                continue
    return all_data


# 外部使用主要函数
def format_get_params(req_params):
    """
    用于格式化GET请求的函数,将dict格式化为字符串: key=value的形式
    :param req_params: GET请求的参数dict类型
    :type req_params:dict
    :return: GET请求的字符串参数
    """
    # 初始化一个GET请求参数的空字符串
    get_params = ''
    # 建立一个索引用于判断是否和字典长度相等
    index = 1
    # 遍历字典
    for k, v in req_params.items():
        # 建立一个GET请求的key=value形式的字符串key和value用placeholder代替
        get_str = '{}={}'
        # 判断index是否等于字典len,如果等于则不需要再末尾添加&,否则需要添加&
        if index == len(req_params):
            # 将key和value分别替换占位符
            get_str = get_str.format(k, v)
        else:
            # 将key和value分别替换占位符
            get_str = get_str.format(k, v)
            # 在末尾添加&符号
            get_str += '&'
        # 把拼接好的字符串拼接到GET请求参数的字符串中
        get_params += get_str
        # 索引+1
        index += 1
    # 返回GET请求参数的字符串
    return get_params


# 外部使用主要函数
def get_img(img_url, save_path=current_path + '/' + 'floor_img'):
    """
    爬取图片函数
    :param img_url:爬取图片的url
    :type img_url:str
    :param save_path: 爬取到的图片保存的位置,默认为爬虫工具类所在的路径下的/floor_img
    :type save_path:str
    :return: 无返回值
    """
    if os.path.exists(save_path):
        pass
    else:
        os.makedirs(save_path)
    img = img_url.split('/')
    img_name = save_path + '\\' + img[-3] + '_' + img[-2] + '_' + img[-1]
    try:
        request.urlretrieve(img_url, img_name)
    except HTTPError as e:
        if e.code == 404:
            print(img_url, '404!!!!!!!!!!')
        e.msg

# if __name__ == '__main__':
#     """
#     使用demo
#     """
# login_data = login()
# print(login_data)
# # 获取用户信息,如果出错表面未登陆
# get_user_msg_url = format_url(configs['api_url']['getUserMsg'])
# user_msg = crawl_data(get_user_msg_url, data={})
# print(user_msg)
#
# # 获取地图所有数据
# map_serch_data = configs['map_serch_data']
# # 替换配置文件中的占位符
# map_serch_data['orgCode'] = map_serch_data['orgCode'].format(user_msg['orgCode'])
# print(map_serch_data)
# map_data = get_fh_data(configs['post_interface_url'], map_serch_data,
#                        configs['api_url']['mapLocation'],
#                        appoint_interface='mapLocation')
# print('map_data', map_data)
#
# # 遍历地图数据
# for i in map_data:
#     if 'unitType' in i:
#         print(i)
#         print('单位编码:[', i['id'], ']', '单位名称:[', i['name'], ']', '单位类型:[', i['unitType'], ']', '单位状态:[',
#               i['unitState'], ']', '单位地址:[', i['address'], ']', '单位经纬度:[', i['latitude'], '&',
#               i['longitude'], ']')
