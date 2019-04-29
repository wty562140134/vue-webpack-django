import pymysql
from pymysql.err import DatabaseError, ProgrammingError


class DBConnect:
    def __init__(self, config):
        self._config = config
        self._connect = None
        self._cursor = None
        self._conn()

    def _conn(self):
        self._connect = pymysql.connect(**self._config)
        self._cursor = self._connect.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql, args=None):
        try:
            if args is None:
                count = self._cursor.execute(sql)
                if count > 1:
                    data = self._cursor.fetchall()
                else:
                    data = self._cursor.fetchone()
            else:
                if isinstance(args, (list, tuple)):
                    count = self._cursor.executemany(sql, args)
                else:
                    count = self._cursor.execute(sql, args)
                if count > 1:
                    data = self._cursor.fetchall()
                else:
                    data = self._cursor.fetchone()
            return data
        except DatabaseError as e:
            print(e)

    def commit(self, sql, args=None):
        try:
            if args is not None:
                if isinstance(args, (list, tuple)):
                    count = self._cursor.executemany(sql, args)
                elif isinstance(args, dict):
                    count = self._cursor.execute(sql, args)
                else:
                    count = self._cursor.execute(sql, args)
            else:
                count = self._cursor.execute(sql)
            self._connect.commit()
            return count
        except DatabaseError and ProgrammingError as e:
            print(e)
            self._connect.rollback()

    def close(self):
        self._cursor.close()
        self._connect.close()

    def __enter__(self):
        print('connect start')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('close execute')
        self.close()


def format_sql_params(sql_params, place_holder='&'):
    params = ''
    index = 1
    for k, v in sql_params.items():
        sql_str = '{}={}'
        if index == len(sql_params):
            sql_str = sql_str.format(k, v)
        else:
            sql_str = sql_str.format(k, v)
            sql_str += place_holder
        params += sql_str
        index += 1
    return params


# str1 = format_sql_params({'name': 'asd', 'age': 14, 'address': 'asd'}, 'and')
# print(str1)
#
# Demo
# sql_str = 'select * from test_table where name="fuck"'  # 查询所有
# sql_str = 'select * from test_table where name=%(name)s'  # 条件查询所有
# sql_str = 'insert into test_table(name, age) value ("%s", %d)' % ("张二", 18) # 使用sql插入
# sql_str = 'insert into test_table(name, age) value (%s, %s)' # 使用元组批量插入
# sql_str = 'insert into test_table(name, age) value (%(name)s, %(age)s)'  # 使用字典插入
# update_sql_str = 'update test_table set name=%(name)s where id=%(id)s'
#
# from whbigdata.crawler.crawle_utils.crawler import configs
#
# connect = DBConnect(configs['data_base'])
# with connect as db:
#     data = db.query(sql_str)
#     print(data)
# query_data = db.query(sql_str)
# query_data = db.query(sql_str, [{'name': 'ddsa'}, {'name': 'haaaa'}])
# print(query_data)
# print(query_data)
# query_count = db.commit(sql_str, ('张一', 19))# 使用元组单个插入
# query_count = db.commit(sql_str, [('张一', 19), ('张二', 18)])# 使用元组批量插入
# print(query_count)
# arg = {'name': 'asdddd', 'age': 19, 'fuck': 1}  # 使用字典插入
# count = db.commit(sql_str, arg)  # 使用字典批量插入
# count = db.commit(sql_str, [{'name': 'ahhhh', 'age': 20}, {'name': 'ddddd', 'age': 10}])  # 使用字典批量插入
# print(count)
# pass
# count = db.commit(update_sql_str, [{'id': '2', 'name': 'ddsa'}, {'name': 'jkr', 'id': 1}])
# print(count)
