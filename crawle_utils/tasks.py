try:
    from whbigdata.crawler.crawle_utils.db_util import DBConnect, select, insert, update
    from whbigdata.crawler.crawle_utils.crawler import get_fh_data, configs, format_get_params
    from whbigdata.crawler.crawle_utils.crawler_task import set_task, run_task
    from whbigdata.crawler.crawle_utils.date_util import *
    from whbigdata.crawler.crawle_utils.zb import pmtobd
except ModuleNotFoundError as e:
    from db_util import DBConnect, select, insert, update
    from crawler import get_fh_data, configs, format_get_params
    from crawler_task import set_task, run_task
    from date_util import *
    from zb import pmtobd
except ImportError as e:
    from db_util import DBConnect, select, insert, update
    from crawler import get_fh_data, configs, format_get_params
    from crawler_task import set_task, run_task
    from date_util import *
    from zb import pmtobd


def get_org_task():
    """
    获取单位信息任务
    """
    req_params = {'orgCode': 'WHXFDD_JT_201910110'}
    map_data = get_fh_data(configs['get_interface_url'], format_get_params(req_params),
                           configs['api_url']['getChildOrg'], appoint_interface='getChildOrg')
    for i in map_data:
        i['log'] = float(i['log'])
        i['lat'] = float(i['lat'])
        i['state'] = 0
        i['lat'], i['log'] = pmtobd(i['lat'], i['log'])
    connect = DBConnect(configs['data_base'])
    with connect as db:
        is_not_new_data(db, map_data)


def monitor_get_count_task():
    search_day = 1
    is_not_get_count_task = True
    connect = DBConnect(configs['data_base'])
    select_sql = '''
        select 
            fi_unit_id,fs_unit_sn,fs_unit_name,fi_unit_monitor_report_count, 
            fi_unit_alarm_review_count,fi_unit_dangers_rectification_count,
            fi_unit_monitor_report_flag,fi_unit_alarm_review_flag,fi_unit_dangers_rectification_flag 
        from 
            t_units
                  '''
    with connect as db:
        all_unit_info = select(db, select_sql)
        if all_unit_info is None:
            return
        alarm_time_start, alarm_time_end = start_and_end_time(search_day, is_not_get_count_task)
        get_monitor_info(db, all_unit_info, alarm_time_start, alarm_time_end,
                         is_not_get_count_task=is_not_get_count_task)


def monitor_send_msg_task():
    search_day = 1
    is_not_get_count_task = False
    connect = DBConnect(configs['data_base'])
    select_sql = '''
        select 
            fi_unit_id,fs_unit_sn,fs_unit_name,fi_unit_monitor_report_count, 
            fi_unit_alarm_review_count,fi_unit_dangers_rectification_count,
            fi_unit_monitor_report_flag,fi_unit_alarm_review_flag,fi_unit_dangers_rectification_flag 
        from 
            t_units
                  '''
    with connect as db:
        all_unit_info = select(db, select_sql)
        if all_unit_info is None:
            return
        alarm_time_start, alarm_time_end = start_and_end_time(search_day, is_not_get_count_task)
        get_monitor_info(db, all_unit_info, alarm_time_start, alarm_time_end,
                         is_not_get_count_task=is_not_get_count_task)


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
            update(db, data_base_data=data_base_data, web_data=i, update_sql=update_sql, where=update_where,
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
    return update_sql, update_data_list


def start_and_end_time(how_many_days, is_not_get_count_task):
    date_format = '%Y-%m-%d'
    str_data = datetime_to_string(datetime.now(), date_format)
    timestamp = datetime_to_timestamp(string_to_datetime(str_data, date_format))
    alarm_time_start = timestamp_to_string(timestamp - how_many_days * 24 * 60 * 60)
    if is_not_get_count_task:
        alarm_time_end = alarm_time_start.split(' ')[0] + ' 23:59:59'
    else:
        alarm_time_end = str_data + ' 23:59:59'
    return alarm_time_start, alarm_time_end


def get_monitor_info(db, all_unit_info, alarm_time_start, alarm_time_end, is_not_get_count_task):
    for unit_info in all_unit_info:
        if unit_info['fs_unit_sn'] == 'WHXFDD_JT_201910110':
            continue
        monitor_report_params = {'unitId': unit_info['fs_unit_sn'], 'deviceTypePid': '02000000', 'buildId': '',
                                 'deviceTypeId': '', 'runState': '2', 'pageNo': '1', 'pageSize': '30'}
        monitor_report = get_fh_data(configs['post_interface_url'], monitor_report_params,
                                     configs['api_url']['getDevicePageByCondition'],
                                     appoint_interface='getDevicePageByCondition')

        alarm_review_params = {'proprietorId': unit_info['fs_unit_sn'], 'alarmTimeStart': alarm_time_start,
                               'alarmTimeEnd': alarm_time_end, 'pageNo': '1', 'pageSize': '30', 'build': '',
                               'alarmState': '2', 'alarmNo': ''}
        alarm_review = get_fh_data(configs['post_interface_url'], alarm_review_params,
                                   configs['api_url']['examineQuery'], appoint_interface='examineQuery')

        dangers_rectification_params = {'pageNo': '1', 'pageSize': '30', 'proprietorId': unit_info['fs_unit_sn'],
                                        'accidentTimeStart': alarm_time_start, 'accidentTimeEnd': alarm_time_end,
                                        'processState': '', 'isOverdued': '1', 'datepicker': '', 'accidentNo': ''}
        dangers_rectification = get_fh_data(configs['post_interface_url'], dangers_rectification_params,
                                            configs['api_url']['accidents'], appoint_interface='accidents')

        monitor_send_or_update(db, is_not_get_count_task, monitor_report['rows'].__len__(),
                               alarm_review['rows'].__len__(), dangers_rectification['rows'].__len__(), unit_info)


def monitor_send_or_update(db, is_not_get_count_task, web_monitor_report_count,
                           web_alarm_review_count, web_dangers_rectification_count, unit_info):
    update_data = {'monitor_report_count': web_monitor_report_count,
                   'alarm_review_count': web_alarm_review_count,
                   'dangers_rectification_count': web_dangers_rectification_count,
                   'id': unit_info['fi_unit_id']}
    if is_not_get_count_task:
        update_sql = '''update 
                                t_units
                            set 
                                fi_unit_monitor_report_count=%(monitor_report_count)s, 
                                fi_unit_alarm_review_count=%(alarm_review_count)s, 
                                fi_unit_dangers_rectification_count=%(dangers_rectification_count)s 
                            where fi_unit_id=%(id)s
                         '''
        update(db, update_date=update_data, update_sql=update_sql)
    else:
        judge_is_not_send(db, unit_info, web_monitor_report_count,
                          web_alarm_review_count, web_dangers_rectification_count)


send_threshold_value = 5


def judge_is_not_send(db, unit_info, web_monitor_report_count, web_alarm_review_count, web_dangers_rectification_count):
    msg = {'msg': '', 'flags': []}
    web_data = {'monitor_report_count': web_monitor_report_count,
                'alarm_review_count': web_alarm_review_count,
                'dangers_rectification_count': web_dangers_rectification_count}
    update(db, data_base_data=unit_info, web_data=web_data, update_data_handle_fun=update_monitor_flag)

    if unit_info['fi_unit_monitor_report_flag'] >= send_threshold_value:
        msg['msg'] += '{}【设备故障】无人处理,请及时督促检查.'.format(unit_info['fs_unit_name'])
        msg['flags'].append('monitor_report')

    if unit_info['fi_unit_alarm_review_flag'] >= send_threshold_value:
        msg['msg'] += '{}【报警复核】无人处理,请及时督促检查.'.format(unit_info['fs_unit_name'])
        msg['flags'].append('alarm_review')

    if unit_info['fi_unit_dangers_rectification_flag'] >= send_threshold_value:
        msg['msg'] += '{}【隐患整改】无人处理,请及时督促检查.'.format(unit_info['fs_unit_name'])
        msg['flags'].append('dangers_rectification')

    if msg['msg'].__len__() > 0:
        send_msg(msg)
        update(db, data_base_data=msg['flags'], web_data=unit_info['fi_unit_id'],
               update_data_handle_fun=reset_update_monitor_flag)


def update_monitor_flag(*args):
    update_sql = 'update t_units set '
    where = ' where fi_unit_id=%(id)s'
    update_data = {}
    if 0 < args[1]['monitor_report_count'] >= args[0]['fi_unit_monitor_report_count']:
        update_sql += 'fi_unit_monitor_report_flag=%(monitor_report_flag)s'
        update_data['monitor_report_flag'] = args[0]['fi_unit_monitor_report_flag'] + 1

    if 0 < args[1]['alarm_review_count'] >= args[0]['fi_unit_alarm_review_count']:
        if update_data.__len__() > 0:
            update_sql += ',fi_unit_alarm_review_flag=%(alarm_review_flag)s'
        else:
            update_sql += 'fi_unit_alarm_review_flag=%(alarm_review_flag)s'
        update_data['alarm_review_flag'] = args[0]['fi_unit_alarm_review_flag'] + 1

    if 0 < args[1]['dangers_rectification_count'] >= args[0]['fi_unit_dangers_rectification_count']:
        if update_data.__len__() > 0:
            update_sql += ',fi_unit_dangers_rectification_flag=%(dangers_rectification_flag)s'
        else:
            update_sql += 'fi_unit_dangers_rectification_flag=%(dangers_rectification_flag)s'
        update_data['dangers_rectification_flag'] = args[0]['fi_unit_dangers_rectification_flag'] + 1

    if update_data.__len__() > 0:
        update_data['id'] = args[0]['fi_unit_id']
        update_sql += where
        return update_sql, update_data
    return None, None


def send_msg(msg):
    print('发送信息!!!!!!!!!!!:', msg)


def reset_update_monitor_flag(*args):
    update_sql = 'update t_units set '
    where = ' where fi_unit_id=%(id)s'
    update_data = {}
    for flag in args[0]:
        if flag == 'monitor_report':
            update_sql += 'fi_unit_monitor_report_flag=%(monitor_report_flag)s'
            update_data['monitor_report_flag'] = 0

        if flag == 'alarm_review':
            if update_data.__len__() > 0:
                update_sql += ',fi_unit_alarm_review_flag=%(alarm_review_flag)s'
            else:
                update_sql += 'fi_unit_alarm_review_flag=%(alarm_review_flag)s'
            update_data['alarm_review_flag'] = 0

        if flag == 'dangers_rectification':
            if update_data.__len__() > 0:
                update_sql += ',fi_unit_dangers_rectification_flag=%(dangers_rectification_flag)s'
            else:
                update_sql += 'fi_unit_dangers_rectification_flag=%(dangers_rectification_flag)s'
            update_data['dangers_rectification_flag'] = 0

    if update_data.__len__() > 0:
        update_data['id'] = args[1]
        update_sql += where
        return update_sql, update_data
    return None, None


set_task(get_org_task, when_time=configs['task']['get_org_task']['when_time'],
         at_day_start_time=configs['task']['get_org_task']['at_day_start_time'])

set_task(monitor_get_count_task, when_time=configs['task']['monitor_task_afternoon']['when_time'],
         at_day_start_time=configs['task']['monitor_task_afternoon']['at_day_start_time'])

set_task(monitor_send_msg_task, when_time=configs['task']['monitor_task_morning']['when_time'],
         at_day_start_time=configs['task']['monitor_task_morning']['at_day_start_time'])

set_task(monitor_send_msg_task, when_time=configs['task']['monitor_task_afternoon']['when_time'],
         at_day_start_time=configs['task']['monitor_task_afternoon']['at_day_start_time'])

run_task()

# set_task(when_time='seconds', every=30, job=monitor_get_count_task)
# set_task(job=monitor_get_count_task, when_time='seconds', every=20)
# set_task(job=monitor_send_msg_task, when_time='seconds', every=43)
# run_task()
# def test():
#     print(123456)
#
#
# def test1():
#     print('asdasd')
#
#
# def test2():
#     print('lllllllll')
#
#
# set_task(test, when_time='seconds', every=10)
# set_task(test1, when_time='seconds', every=35)
# set_task(test2, when_time='seconds', every=50)
# run_task()
# set_task(get_org_task, when_time='seconds', every=15)
# monitor_task(1, True)
# get_org_task()
