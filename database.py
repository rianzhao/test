# coding=utf-8
import threading
import time
# 使用 sqlalchemy 数据库映射框架，这是一个常用的 ORM 开发库
# 可以将变量直接映射到数据库字段之上，简化 sql 操作。
from sqlalchemy import (
    create_engine,
    exc,
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    Binary,
    BLOB,
    Float,
    BigInteger,
)
from sqlalchemy.dialects.mysql import TINYBLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

# 设定数据库信息
DB_USER = "root"
DB_PASS = "zra19980318"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "mydatabase"
DATABASE_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4&autocommit=true' % (
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
# DATABASE_URI = ""
BaseModel = declarative_base()

# 将sqlAlchemy中的对象转换为dict

# 一个回调操作，可以将数据库的输出最终转换为 dict 字典。


def to_dict(self):
    return {
        c.name: getattr(self, c.name, None)
        for c in self.__table__.columns
        if c.name != "Status"
    }


BaseModel.to_dict = to_dict

# 封装了数据库的 CRUD 操作（create\delete\update\delete）


class CommonDBExecutor:
    db = None

    def __init__(self, db_url=DATABASE_URI, table=None):
        if not CommonDBExecutor.db:
            self.db_url = db_url
            # 使用 create_engine 创建一个数据库连接池
            CommonDBExecutor.db = create_engine(
                db_url,
                pool_size=3,
                max_overflow=100,
                pool_recycle=60,
                encoding="utf8",
                pool_pre_ping=True,
            )
            BaseModel.metadata.create_all(bind=CommonDBExecutor.db)

        self.db = CommonDBExecutor.db
        # 设定该操作类作用的表对象
        if table:
            self.tb = table
        else:
            raise Exception("Failed to get table for executor.")

        self.__session = None

    @property
    def session(self):
        # 方便获取数据库操作会话的方法
        # 可以返回当前数据库的连接会话
        if not self.__session:
            # 如果没有就创建一个
            DBSession = sessionmaker(bind=self.db)
            self.__session = DBSession()
        return self.__session

    def reconnect(self):
        # 如果数据库连接出现异常，可以在这里重连
        if self.db == CommonDBExecutor.db:
            CommonDBExecutor.db = create_engine(
                self.db_url,
                pool_size=3,
                max_overflow=100,
                pool_recycle=60,
                encoding="utf8",
                pool_pre_ping=True,
            )
            BaseModel.metadata.create_all(bind=CommonDBExecutor.db)

        self.db = CommonDBExecutor.db

    def session_close(self):
        # 该对象类注销的时候，需要调用该
        # 方法对其连接进行清理。
        if self.__session:
            self.__session.close()
            self.__session = None

    def insert(self, **kwargs):
        # 数据库插入操作
        for _ in range(3):
            try:
                # 将输入的参数直接写入到表中
                # 注意这里使用的参数要和表字
                # 段中的大小写保持一致。
                service = self.tb(**kwargs)
                self.session.add(service)
                self.session.commit()
                break
            except exc.DBAPIError as e:
                if e.connection_invalidated:
                    self.reconnect()
                    time.sleep(3)
                else:
                    raise e
            except Exception as ex:
                self.session.rollback()
                raise ex
            finally:
                self.session_close()

    # 这里支持设置值为列表，过滤条件将设置为 SQL 的 IN 语句
    # 这里支持在表列名前面加 "not_" 将过滤条件设置为不等于（或 NOT IN）
    # 这个列名对应的值
    def _filter_kwargs_map(self, filter_table):
        new_filter_list = []
        for key, val in filter_table.items():
            filter_expression = None
            if len(key) > 4 and "not_" == key[0:4]:
                class_key = getattr(self.tb, key[4:])
                if isinstance(val, list):
                    filter_expression = class_key.notin_(val)
                else:
                    filter_expression = class_key != val
            else:
                class_key = getattr(self.tb, key)
                if isinstance(val, list):
                    filter_expression = class_key.in_(val)
                else:
                    filter_expression = class_key == val
            new_filter_list.append(filter_expression)
        return new_filter_list

    def query(self, **kwargs):
        # 数据库表的查询方法封装
        ret = None
        data = None
        for _ in range(3):
            try:
                if kwargs:
                    # 这里获取查询的过滤条件，因为多个过滤条件需要使用 AND 进行连接
                    # 这里所以要单独列出处理
                    new_filter_list = self._filter_kwargs_map(kwargs)
                    if len(new_filter_list) > 1:
                        data = (
                            self.session.query(self.tb)
                            .filter(and_(*new_filter_list))
                            .all()
                        )
                    else:
                        # 如果只有一个过滤条件，这里就直接使用它进行查询操作
                        data = (
                            self.session.query(self.tb).filter(
                                *new_filter_list).all()
                        )
                else:
                    # 如果没有过滤条件就进行全量的查询
                    data = self.session.query(self.tb).all()
                if isinstance(data, list):
                    ret = [d.to_dict() for d in data]
                else:
                    ret = data.to_dict()
                self.session.commit()
                break
            except exc.DBAPIError as e:
                if e.connection_invalidated:
                    self.reconnect()
                else:
                    raise e
            except Exception as ex:
                self.session.rollback()
                raise ex
            finally:
                self.session_close()

        return ret

    def update(self, update_dict={}, **kwargs):
        # 数据库的更新操作
        ret = None
        for _ in range(3):
            try:
                if kwargs:
                    # 和查询操作一样，更新操作也支持基于条件变量的过滤
                    new_filter_list = self._filter_kwargs_map(kwargs)
                    if len(new_filter_list) > 1:
                        ret = (
                            self.session.query(self.tb)
                            .filter(and_(*new_filter_list))
                            .update(update_dict)
                        )
                    else:
                        ret = (
                            self.session.query(self.tb)
                            .filter(*new_filter_list)
                            .update(update_dict)
                        )
                else:
                    ret = self.session.query(self.tb).update(update_dict)

                self.session.commit()
                break
            except exc.DBAPIError as e:
                if e.connection_invalidated:
                    self.reconnect()
                    time.sleep(3)
                else:
                    raise e
            except Exception as ex:
                self.session.rollback()
                raise ex
            finally:
                self.session_close()

        return ret

    def delete(self, **kwargs):
        # 对数据库表进行删除操作
        ret = None
        for _ in range(3):
            try:
                if kwargs:
                    # 在删除操作的时候，也可以使用多个条件进行过滤
                    new_filter_list = self._filter_kwargs_map(kwargs)
                    if len(new_filter_list) > 1:
                        ret = (
                            self.session.query(self.tb)
                            .filter(and_(*new_filter_list))
                            .delete(synchronize_session="fetch")
                        )
                    else:
                        ret = (
                            self.session.query(self.tb)
                            .filter(*new_filter_list)
                            .delete(synchronize_session="fetch")
                        )
                else:
                    # 这里是对所有表数据进行全量删除
                    ret = self.session.query(self.tb).delete()

                self.session.commit()
                break
            except exc.DBAPIError as e:
                if e.connection_invalidated:
                    self.reconnect()
                    time.sleep(3)
                else:
                    raise e
            except Exception as ex:
                self.session.rollback()
                raise ex
            finally:
                self.session_close()

        return ret

    def execute(self, sql):
        # 这个是一个扩展方法，当 CRUD 不能解决
        # 问题的时候，可以使用这个方法直接执行
        # sql 语句进行数据库操作
        ret = None
        for _ in range(3):
            try:
                ret = self.session.execute(sql)
                self.session.commit()
                break
            except exc.DBAPIError as e:
                if e.connection_invalidated:
                    self.reconnect()
                    time.sleep(3)
                else:
                    raise e
            except Exception as ex:
                self.session.rollback()
                raise ex
            finally:
                self.session_close()
        return ret


def get_db_uri():
    return DATABASE_URI
