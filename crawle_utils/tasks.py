from whbigdata.crawler.crawle_utils.db_util import DBConnect, select, insert, update
from whbigdata.crawler.crawle_utils.crawler import get_fh_data, configs, format_get_params
from whbigdata.crawler.crawle_utils.crawler_task import set_task, run_task
from whbigdata.crawler.crawle_utils.date_util import *
from whbigdata.crawler.crawle_utils.zb import pmtobd


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


def is_not_new_data(db, web_data):
    select_sql = 'select * from t_units where fs_unit_sn=%(orgCode)s'
    insert_sql = '''
                    insert into 
                        t_units(
                        fs_unit_sn, fs_unit_name, fd_unit_lat, 
                        fd_unit_lng, fi_unit_status, fs_unit_addr, fi_unit_type
                        ) 
                    value 
                        (%(orgCode)s, %(orgName)s, %(lat)s, 
                        %(log)s, %(state)s, " ", 0)
                '''
    update_sql = 'update t_units set '
    update_where = ' where fi_unit_id=%(id)s'
    for i in web_data:
        data_base_data = select(db, select_sql, {'orgCode': i['orgCode']})
        if data_base_data is None:
            insert(db, i, insert_sql=insert_sql)
        else:
            update(db, data_base_data, i, update_sql=update_sql, where=update_where,
                   update_data_handle_fun=set_update_data)


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


def monitor_task(how_many_days):
    connect = DBConnect(configs['data_base'])
    with connect as db:
        unit_ids = select(db, 'select fs_unit_sn,fs_unit_name from t_units')
    if unit_ids is None:
        return
    date_format = '%Y-%m-%d'
    str_data = datetime_to_string(datetime.now(), date_format)
    alarm_time_end = str_data + ' 23:59:59'
    timestamp = datetime_to_timestamp(string_to_datetime(str_data, date_format))
    alarm_time_start = timestamp_to_string(timestamp - how_many_days * 24 * 60 * 60)

    for i in unit_ids:
        if i['fs_unit_sn'] == 'WHXFDD_JT_201910110':
            continue
        monitor_report_params = {'unitId': i['fs_unit_sn'], 'deviceTypePid': '02000000', 'buildId': '',
                                 'deviceTypeId': '',
                                 'runState': '2', 'pageNo': '1', 'pageSize': '30'}
        monitor_report = get_fh_data(configs['post_interface_url'], monitor_report_params,
                                     configs['api_url']['getDevicePageByCondition'],
                                     appoint_interface='getDevicePageByCondition')

        alarm_review_params = {'proprietorId': i['fs_unit_sn'], 'alarmTimeStart': alarm_time_start,
                               'alarmTimeEnd': alarm_time_end, 'pageNo': '1',
                               'build': '', 'alarmState': '2', 'alarmNo': '', 'pageSize': '30'}
        alarm_review = get_fh_data(configs['post_interface_url'], alarm_review_params,
                                   configs['api_url']['examineQuery'],
                                   appoint_interface='examineQuery')

        dangers_rectification_params = {'pageNo': '1', 'pageSize': '30', 'proprietorId': i['fs_unit_sn'],
                                        'accidentTimeStart': alarm_time_start, 'accidentTimeEnd': alarm_time_end,
                                        'processState': '',
                                        'isOverdued': '1', 'datepicker': '', 'accidentNo': ''}
        dangers_rectification = get_fh_data(configs['post_interface_url'], dangers_rectification_params,
                                            configs['api_url']['accidents'],
                                            appoint_interface='accidents')


# set_task(get_org_task, when_time=configs['task']['get_org_task']['when_time'],
#          at_day_start_time=configs['task']['get_org_task']['at_day_start_time'])
#
# set_task(monitor_task, when_time=configs['task']['monitor_task_morning']['when_time'],
#          at_day_start_time=configs['task']['monitor_task_morning']['at_day_start_time'])
#
# set_task(monitor_task, when_time=configs['task']['monitor_task_afternoon']['when_time'],
#          at_day_start_time=configs['task']['monitor_task_afternoon']['at_day_start_time'])
# run_task()
# def test():
#     print(123456)
# def test1():
#     print('asdasd')
# def test2():
#     print('lllllllll')
# set_task(test, when_time='seconds', every=10)
# set_task(test1, when_time='seconds', every=35)
# set_task(test2, when_time='seconds', every=50)
# set_task(get_org_task, when_time='seconds', every=15)
# monitor_task(7)
# get_org_task()
