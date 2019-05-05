import schedule
import threading
from .db_util import DBConnect
from .crawler import get_fh_data, configs, format_get_params
from .zb import pmtobd


# from crawler.crawle_utils.db_util import DBConnect
# from crawler.crawle_utils.crawler import get_fh_data, configs, format_get_params


class Task:

    def __init__(self):
        self._job = None
        self._threads = []
        self._tasks = []

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Task, "_instance"):
            Task._instance = Task(*args, **kwargs)
        return Task._instance

    def set_task(self, task):
        self._tasks.append(task)

    def thread_job(self, job):
        t = threading.Thread(target=job)
        t.setDaemon(True)
        self._threads.append(t)
        t.start()

    def run(self):
        while True:
            schedule.run_pending()
            for t in self._threads:
                t.join()


def insert(db, insert_data, insert_sql='insert into t_units(fs_unit_sn, fs_unit_name, '
                                       'fd_unit_lat, fd_unit_lng, fi_unit_status, fs_unit_addr, fi_unit_type) '
                                       'value (%(orgCode)s, %(orgName)s, %(lat)s, %(log)s, %(state)s, " ", 0)'):
    db.commit(insert_sql, insert_data)


def update(db, data_base_data, web_data, update_sql='update t_units set ', where=' where fi_unit_id=%(id)s'):
    update_sql, update_data_list, update_data = set_update_data(data_base_data, web_data, update_sql)
    if update_data_list.__len__() > 0:
        update_sql = update_sql + where
    db.commit(update_sql, update_data_list)


def set_task(job, every=None, when_time=None, at_day_start_time='', to=None):
    """
    使用示例:
    schedule.every(10).minutes 每隔十分钟执行一次任务
    schedule.every().hour 每隔一小时执行一次任务
    schedule.every().day.at("10:30") 每天的10:30执行一次任务
    schedule.every(5).to(10).days 每隔5到10天执行一次任务
    schedule.every().monday 每周一的这个时候执行一次任务
    schedule.every().wednesday.at("13:15") 每周三13:15执行一次任务

    :param job: 需要运行的任务函数,是一个函数对象
    :type object
    :param every: schedule.every()中的传参
    :type int
    :param when_time: 是schedule中的second,minute,hours，day等
    :type str
    :param at_day_start_time:当schedule使用day时，例如schedule.every().day.at() at()中的传参
    :type str
    :param to: 当schedule需要在某一时间段或每过几天之内执行,例如schedule.every(5).to(10).days
    :type int
    """
    task = Task.instance()
    if when_time == 'day':
        if every is not None:
            sch = schedule.every().day.at(at_day_start_time).do(task.thread_job, job)
        else:
            if to is not None:
                sch = schedule.every(every).to(to).day.do(task.thread_job, job)
            else:
                sch = schedule.every().day.at(at_day_start_time).do(task.thread_job, job)
    else:
        sch = eval('schedule.every({}).{}.do(task.thread_job, job)'.format(every, when_time))
    task.set_task(sch)


def get_org_task():
    req_params = {'orgCode': 'WHXFDD_JT_201910110'}
    map_data = get_fh_data(configs['get_interface_url'], format_get_params(req_params),
                           configs['api_url']['getChildOrg'],
                           appoint_interface='getChildOrg')
    connect = DBConnect(configs['data_base'])
    for i in map_data:
        i['log'] = float(i['log'])
        i['lat'] = float(i['lat'])
        i['state'] = 0
        i['lat'], i['log'] = pmtobd(i['lat'], i['log'])
    with connect as db:
        is_not_new_data(db, map_data)


def is_not_new_data(db, web_data, select_sql='select * from t_units where fs_unit_sn=%(orgCode)s'):
    for i in web_data:
        data_base_data = db.query(select_sql, {'orgCode': i['orgCode']})
        if data_base_data is None:
            insert(db, i)
        else:
            update(db, data_base_data, i)


def set_update_data(data_base_data, web_data, update_sql):
    update_data_list = []
    update_data = {}
    if data_base_data['fs_unit_sn'] == web_data['orgCode']:

        if data_base_data['fs_unit_name'] != web_data['orgName']:
            update_sql += 'fs_unit_name=%(orgName)s'
            update_data['orgName'] = web_data['orgName']

        web_data['lat'] = float(web_data['lat'])
        if data_base_data['fd_unit_lat'] != web_data['lat']:
            if update_data.__len__() != 0:
                update_sql += ', fd_unit_lat=%(lat)s'
            else:
                update_sql += 'fd_unit_lat=%(lat)s'
            update_data['lat'] = web_data['lat']

        web_data['log'] = float(web_data['log'])
        if data_base_data['fd_unit_lng'] != web_data['log']:
            if update_data.__len__() != 0:
                update_sql += ', fd_unit_lng=%(log)s'
            else:
                update_sql += 'fd_unit_lng=%(log)s'
            update_data['log'] = web_data['log']

        web_data['state'] = int(web_data['state'])
        if data_base_data['fi_unit_status'] != web_data['state']:
            if update_data.__len__() != 0:
                update_sql += ', fi_unit_status=%(state)s'
            else:
                update_sql += 'fi_unit_status=%(state)s'
            update_data['state'] = web_data['state']

        if update_data.__len__() > 0:
            update_data['id'] = data_base_data['fi_unit_id']
            update_data_list.append(update_data)
    return update_sql, update_data_list, update_data


def run_task():
    Task.instance().run()


def test():
    print(123456)


def test1():
    print('asdasd')


def test2():
    print('lllllllll')


# set_task(test, when_time='seconds', every=10)
# set_task(test1, when_time='seconds', every=35)
# set_task(test2, when_time='seconds', every=50)
# set_task(get_org_task, when_time=configs['task']['when_time'], at_day_start_time=configs['task']['at_day_start_time'])
set_task(get_org_task, when_time='seconds', every=15)
run_task()
