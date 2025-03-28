import traceback

import pymysql
# from DBUtils.PooledDB import PooledDB  #旧版本
from dbutils.pooled_db import PooledDB  # 3.0以后版本
import db_config_dev as config_dev
import db_config_test as config_test


class MySQLConnectionPool:

    def __init__(self, env):
        if env == 'test':
            self.pool = PooledDB(
                creator=config_test.DB_CREATOR,  # 使用链接数据库的模块
                mincached=config_test.DB_MIN_CACHED,  # 初始化时，链接池中至少创建的链接，0表示不创建
                maxcached=config_test.DB_MAX_CACHED,
                maxshared=config_test.DB_MAX_SHARED,
                maxconnections=config_test.DB_MAX_CONNECYIONS,  # 连接池允许的最大连接数，0和None表示不限制连接数
                blocking=config_test.DB_BLOCKING,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                host=config_test.DB_HOST,
                port=config_test.DB_PORT,
                user=config_test.DB_USER,
                password=config_test.DB_PASSWORD,
                database=config_test.DB_DBNAME
            )
        else:
            self.pool = PooledDB(
                creator=config_dev.DB_CREATOR,  # 使用链接数据库的模块
                mincached=config_dev.DB_MIN_CACHED,  # 初始化时，链接池中至少创建的链接，0表示不创建
                maxcached=config_dev.DB_MAX_CACHED,
                maxshared=config_dev.DB_MAX_SHARED,
                maxconnections=config_dev.DB_MAX_CONNECYIONS,  # 连接池允许的最大连接数，0和None表示不限制连接数
                blocking=config_dev.DB_BLOCKING,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                host=config_dev.DB_HOST,
                port=config_dev.DB_PORT,
                user=config_dev.DB_USER,
                password=config_dev.DB_PASSWORD,
                database=config_dev.DB_DBNAME
            )

    def open(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 表示读取的数据为字典类型
        return self.conn, self.cursor

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def select_one(self, sql, *args):
        """查询单条数据"""
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def select_all(self, sql, args):
        """查询多条数据"""
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def insert_one(self, sql, args):
        """插入单条数据"""
        self.execute(sql, args, isNeed=True)

    def insert_all(self, sql, datas):
        """插入多条批量插入"""
        conn, cursor = self.open()
        try:
            cursor.executemany(sql, datas)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            conn.rollback()
            return {'result': False, 'err': err}

    def update_one(self, sql, args):
        """更新数据"""
        self.execute(sql, args, isNeed=True)

    def delete_one(self, sql, *args):
        """删除数据"""
        self.execute(sql, args, isNeed=True)

    def execute(self, sql, args, isNeed=False):
        """
        执行
        :param isNeed 是否需要回滚
        """
        conn, cursor = self.open()
        if isNeed:
            try:
                cursor.execute(sql, args)
                conn.commit()
            except Exception as e:
                print(e)
                # 默认在终端打印异常信息, 默认色彩是红色
                traceback.print_exc()
                conn.rollback()
        else:
            cursor.execute(sql, args)
            conn.commit()
        self.close(conn, cursor)

# """
# CREATE TABLE `names` (
#   `id` int(10) NOT NULL AUTO_INCREMENT COMMENT '主键',
#   `name` VARCHAR(30) DEFAULT NULL COMMENT '姓名',
#   `sex` VARCHAR(20) DEFAULT NULL COMMENT '性别',
#   `age` int(5) DEFAULT NULL COMMENT '年龄',
#   PRIMARY KEY (`id`) USING BTREE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='数据导入mysql';
#
# """

#
# mysql = MySQLConnectionPool()
#
# sql_insert_one = "insert into `names` (`name`, sex, age) values (%s,%s,%s)"
# mysql.insert_one(sql_insert_one, ('唐三', '男', 25))
#
# datas = [
#     ('戴沐白', '男', 26),
#     ('奥斯卡', '男', 26),
#     ('唐三', '男', 25),
#     ('小舞', '女', 100000),
#     ('马红俊', '男', 23),
#     ('宁荣荣', '女', 22),
#     ('朱竹清', '女', 21),
# ]
# sql_insert_all = "insert into `names` (`name`, sex, age) values (%s,%s,%s)"
# mysql.insert_all(sql_insert_all, datas)
#
# sql_update_one = "update `names` set age=%s where `name`=%s"
# mysql.update_one(sql_update_one, (28, '唐三'))
#
# sql_delete_one = 'delete from `names` where `name`=%s '
# mysql.delete_one(sql_delete_one, ('唐三',))
#
# sql_select_one = 'select * from `names` where `name`=%s'
# results = mysql.select_one(sql_select_one, ('唐三',))
# print(results)
#
# sql_select_all = 'select * from `names` where `name`=%s'
# results = mysql.select_all(sql_select_all, ('唐三',))
# print(results)
#
