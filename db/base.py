# coding: utf-8

"""数据库操作基础"""

import pymysql
from DBUtils.PooledDB import PooledDB
from config import Sql


# ---------------------------------------------------------------------
#   数据库基类 x2
# ---------------------------------------------------------------------
class DB:
    """
    单例模式 + 数据库连接池
    """
    __pool = None
    __conn = None

    def __init__(self):
        self.__conn = DB.__get_conn()

    @staticmethod
    def __get_conn():
        if not DB.__pool:
            DB.__pool = PooledDB(creator=pymysql, mincached=1, maxcached=Sql.max_cached,
                                 host=Sql.host, port=Sql.port, user=Sql.user, passwd=Sql.password,
                                 db=Sql.db, charset='utf8')
        return DB.__pool.connection()

    def connection(self):
        return self.__conn


class DBbase:
    def __init__(self):
        self.__conn = None
        self.__cursor = None

    def __enter__(self):
        self.__conn = DB().connection()
        self.__cursor = self.__conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__conn.close()

    def get_cursor(self):
        return self.__cursor

    def get_con(self):
        return self.__conn

    def commit(self):
        self.__conn.commit()

    def execute(self, sql, commit=False, fetch=False):
        """
        :param sql:
        :param commit:
        :param fetch:
        :return: it's two return types: bool if commit=fetch else ((xxx),(yyy),...)
        """
        r = bool(self.__cursor.execute(sql))
        if commit:
            self.commit()
        if fetch:
            r = self.__cursor.fetchall()
        return r
