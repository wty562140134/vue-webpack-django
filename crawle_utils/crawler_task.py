import schedule
import threading
import time
# from whbigdata.crawler.crawle_utils.db_util import DBConnect
# from whbigdata.crawler.crawle_utils.crawler import get_fh_data, configs, format_get_params
# from crawler.crawle_utils.db_util import DBConnect
# from crawler.crawle_utils.crawler import get_fh_data, configs, format_get_params
from crawle_utils.db_util import DBConnect
from crawle_utils.crawler import get_fh_data, configs, format_get_params


class Task:
    def __init__(self, jobs_fun):
        self._jobs = list(jobs_fun)

    def _thread_task(self):
        for job in self._jobs:
            threading.Thread(target=job).start()

    def run(self, task_rule_instance, sleep_time=0):
        task_rule_instance.do(self._thread_task)
        while True:
            schedule.run_pending()
            time.sleep(sleep_time)


def get_org_task():
    req_params = {'orgCode': 'WHXFDD_JT_201910110'}
    map_data = get_fh_data(configs['get_interface_url'], format_get_params(req_params),
                           configs['api_url']['getChildOrg'],
                           appoint_interface='getChildOrg')
    connect = DBConnect(configs['data_base'])
    with connect as db:
        is_not_new_data(db, map_data)


def is_not_new_data(db, map_data, select_sql='select * from t_units where fs_unit_sn=%(orgCode)s'):
    for i in map_data:
        unit = db.query(select_sql, {'orgCode': i['orgCode']})
        if unit is None:
            insert(db, i)
        else:
            update(db, unit, i)


def insert(db, insert_data, insert_sql='insert into t_units(fs_unit_sn, fs_unit_name, '
                                       'fd_unit_lat, fd_unit_lng, fi_unit_status, fs_unit_addr, fi_unit_type) '
                                       'value (%(orgCode)s, %(orgName)s, %(lat)s, %(log)s, %(state)s, " ", 0)'):
    db.commit(insert_sql, insert_data)


def update(db, unit, map_data):
    update_data_list = []
    update_sql = 'update t_units set '
    where = ' where fi_unit_id=%(id)s'
    update_data = {}
    if unit['fs_unit_sn'] == map_data['orgCode']:

        if unit['fs_unit_name'] != map_data['orgName']:
            update_sql += 'fs_unit_name=%(orgName)s'
            update_data = {'orgName': map_data['orgName'], 'id': unit['fi_unit_id']}
            update_data_list.append(update_data)

        map_data['lat'] = float(map_data['lat'])
        if unit['fd_unit_lat'] != map_data['lat']:
            if update_data.__len__() != 0:
                update_sql += ', fd_unit_lat=%(lat)s'
            else:
                update_sql += 'fd_unit_lat=%(lat)s'
            update_data = {'lat': map_data['lat'], 'id': unit['fi_unit_id']}
            update_data_list.append(update_data)

        map_data['log'] = float(map_data['log'])
        if unit['fd_unit_lng'] != map_data['log']:
            if update_data.__len__() != 0:
                update_sql += ', fd_unit_lng=%(log)s'
            else:
                update_sql += 'fd_unit_lng=%(log)s'
            update_data = {'log': map_data['log'], 'id': unit['fi_unit_id']}
            update_data_list.append(update_data)

        map_data['state'] = int(map_data['state'])
        if unit['fi_unit_status'] != map_data['state']:
            if update_data.__len__() != 0:
                update_sql += ', fi_unit_status=%(state)s'
            else:
                update_sql += 'fi_unit_status=%(state)s'
            update_data = {'state': map_data['state'], 'id': unit['fi_unit_id']}
            update_data_list.append(update_data)

    if update_data_list.__len__() > 0:
        update_sql = update_sql + where
        db.commit(update_sql, update_data_list)


def run_task(*job, every=None, when_time=None, at_day_start_time='', to=None):
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
    if when_time == 'day':
        if every is not None:
            sch = eval('schedule.every({}).{}.at("{}")'.format(every, when_time, at_day_start_time))
        else:
            sch = eval('schedule.every().{}.at("{}")'.format(when_time, at_day_start_time))
        if to is not None:
            sch = eval('schedule.every({}).to({}).{}'.format(every, to, when_time))
    else:
        sch = eval('schedule.every({}).{}'.format(every, when_time))
    t = Task(job)
    t.run(sch)


run_task(get_org_task, when_time=configs['task']['when_time'], at_day_start_time=configs['task']['at_day_start_time'])

print('testtest')
