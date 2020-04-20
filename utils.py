import traceback
import pymysql
import nameMap
from spider import *


# 连接数据库
def get_conn():
    """
    return:连接，游标

    先建立mysql数据库, 库名(cov2019)
    """

    # 创建连接
    conn = pymysql.connect(host='127.0.0.1',
                           user='root', password='123456',
                           db='cov2019', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


# 关闭数据库连接
def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 更新历史数据
def update_history():
    """
    mysql建立history表的sql语句

    create table history(
    ds datetime not null comment'日期',
    confirm int(11) default null comment'累计确诊',
    confirm_add int(11) default null comment'当日新增确诊',
    suspect int(11) default null comment'累计疑似',
    suspect_add int(11) default null comment'当日新增疑似',
    heal int(11) default null comment'累计治愈',
    heal_add int(11) default null comment'当日新增治愈',
    dead int(11) default null comment'累计死亡',
    dead_add int(11) default null comment'当日新增死亡',
    now_confirm int(11) default null comment'累计现有确诊',
    imported_case int(11) default null comment'累计境外输入',
    no_infect int(11) default null comment'累计无症状感染者',
    primary key(ds) using btree
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_history_data()  # 历史数据
        print(f'{time.asctime()} -- 开始更新历史数据')
        conn, cursor = get_conn()
        # 数据不存在, 用于插入数据
        sql_query_insert = 'select confirm from history where ds=%s'
        sql_insert = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        for k, v in dic.items():
            # item{'2020-1-20':{'confirm':,'suspect':,'heal':,'dead':}}
            if not cursor.execute(sql_query_insert, k):
                cursor.execute(sql_insert, [k, v.get('confirm'), v.get('confirm_add'),
                                     v.get('suspect'), v.get('suspect_add'),
                                     v.get('heal'), v.get('heal_add'),
                                     v.get('dead'), v.get('dead_add'),
                                     v.get('now_confirm'), v.get('imported_case'), v.get('no_infect')
                                     ])
        conn.commit()  # 提交事务
        print(f'{time.asctime()} -- 历史数据更新完毕')
    except:
        traceback.print_exc()

    finally:
        close_conn(conn, cursor)


# 更新当日各城市数据
def update_details():
    """
    更新details表，更新当日各城市数据

    mysql建立details表的sql语句:

    create table details(
    id int(11) not null auto_increment,
    update_time datetime default null comment '数据最后更新时间',
    province varchar(50) default null comment'省',
    city varchar(50) default null comment'市',
    confirm int(11) default null comment'累计确诊',
    confirm_add int(11) default null comment'新增确诊',
    heal int(11) default null comment'累计治愈',
    dead int(11) default null comment'累计死亡',
    primary key(id)
    )engine=InnoDB default charset=utf8mb4;

    """

    cursor = None
    conn = None
    try:
        li = get_details_data()  # 当日更新具体数据
        conn, cursor = get_conn()
        # 数据不存在, 用于插入数据
        sql_query_insert = 'select %s=(select update_time from details order by id desc limit 1)'
        sql_insert = 'insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql_query_insert, li[0][0])
        if not cursor.fetchone()[0]:
            print(f'{time.asctime()} -- 开始更新今日最新数据')
            for item in li:
                cursor.execute(sql_insert, item)
            conn.commit()  # 提交事务
            print(f'{time.asctime()} -- 今日最新数据更新完毕')
        else:
            print(f'{time.asctime()} -- 已是今日最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 更新外国数据
def update_fforeign(*country_list):
    """
    插入国外数据，更新当日国外各数据
    mysql建立表fforeign的sql语句：

    create table fforeign(
    id int(11) not null auto_increment,
    update_time datetime default null comment '数据最后更新时间',
    country varchar(50) not null comment'国',
    confirm int(11) default null comment'累计确诊',
    confirm_add int(11) default null comment'新增确诊',
    heal int(11) default null comment'累计治愈',
    dead int(11) default null comment'累计死亡',
    primary key(id)
    )engine=InnoDB default charset=utf8mb4;

    :return:
    """
    cursor = None
    conn = None
    try:
        conn, cursor = get_conn()
        # 数据不存在, 插入数据
        sql_query_insert = 'select confirm from fforeign where country = %s and update_time= %s'
        sql_insert = 'insert into fforeign(country,update_time,confirm_add,confirm,heal,dead) ' \
              'values(%s,%s,%s,%s,%s,%s)'
        # 数据已存在, 更新数据
        sql_query_update = 'select %s=(select confirm from fforeign where country = %s and update_time= %s)'
        sql_update = 'update fforeign set confirm_add=%s,confirm=%s,heal=%s,dead=%s where country = %s and update_time= %s'
        # 请求各国数据，未特指国家，默认指世界各国
        country_data = get_country_data(*country_list)
        print(f'{time.asctime()} -- 正在更新国外数据，数据量较大请稍微等待一会')
        # 更新数据库
        for country, dailyData in country_data.items():  # 迭代国家列表
            # 该国有疫情数据
            for item in dailyData:  # 获取该国每日数据, item 格式['2020-01-28', 0, 5, 0, 0]
                cursor.execute(sql_query_insert, [country, item[0]])  # country代表国家, item[0]代表日期
                # 该日确诊数据为null, 插入数据
                if not cursor.fetchone():
                    cursor.execute(sql_insert, [country, item[0], item[1], item[2], item[3], item[4]])  # 插入数据
                    conn.commit()  # 提交事务
                    continue
                break
        close_conn(conn, cursor)
        conn, cursor = get_conn()
        for country, dailyData in country_data.items():  # 迭代国家列表
            # 该日数据存在，但未更新
            # 更新昨日的最终数据和今日的暂时数据
            for day in dailyData[:2]:
                cursor.execute(sql_query_update, [day[2], country, day[0]])
                if not cursor.fetchone()[0]:
                    cursor.execute(sql_update, [day[1], day[2], day[3], day[4], country, day[0]])  # 更新数据
                    conn.commit()  # 提交事务
        print(f'{time.asctime()} -- 已是国外最新数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_global():
    """
    更新global表

    create table global(
    update_time datetime  comment '数据最后更新时间',
    confirm int(11) default null comment'累计确诊',
    confirm_add int(11) default null comment'新增确诊',
    heal int(11) default null comment'累计治愈',
    dead int(11) default null comment'累计死亡',
    last_update_time datetime  comment '数据最后更新时间',
    primary key(update_time)
    )engine=InnoDB default charset=utf8mb4;
    """
    cursor = None
    conn = None
    try:
        li = get_global_data()[0]  # 获取全球统计数据
        last_update_time = get_global_data()[1]  # 获取最近一次更新时间
        conn, cursor = get_conn()
        # 数据不存在, 用于插入数据
        sql_query_insert = 'select confirm from global where update_time=%s'
        sql_insert = 'insert into global(update_time,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s)'
        # 数据已经存在, 用于更新数据
        sql_query_update = 'select %s=(select confirm_add from global where update_time=%s)'
        sql_update = 'update global set confirm=%s,confirm_add=%s,heal=%s,dead=%s,last_update_time=%s where update_time=%s'
        print(f'{time.asctime()} -- 开始更新全球累计数据')
        # 更新全球累计历史数据
        for item in li:  # 当日之前每日数据
            # 该日确诊为null, 则插入数据
            cursor.execute(sql_query_insert, item[0])
            if not cursor.fetchone():
                cursor.execute(sql_insert, item)
                conn.commit()  # 提交事务
            else:
                break
        close_conn(conn, cursor)
        conn, cursor = get_conn()
        # 更新昨日最终累计数据和今日暂时数据
        for item in li[:2]:
            cursor.execute(sql_update, [item[1], item[2], item[3], item[4], last_update_time, item[0]])
            conn.commit()  # 提交事务
        print(f'{time.asctime()} -- 已经是全球最新累计数据')
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# sql查询
def query(sql, *args):
    """
    :param sql:
    :param args:
    :return:
    """

    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


# 获取china左侧数据，中国疫情地图
def get_china_left():
    """

    :return:返回各省数据
    """
    sql = 'select province, sum(confirm) from details ' \
          'where update_time=(select update_time from details ' \
          'order by update_time desc limit 1) ' \
          'group by province'
    res = query(sql)
    return res


# 获取china右上侧数据，疫情数据
def get_china_top_right():
    """

    :return:返回全国累计数据
    """
    sql = 'select sum(confirm),' \
          '(select confirm_add from history order by ds desc limit 1),' \
          '(select heal_add from history order by ds desc limit 1),' \
          '(select dead_add from history order by ds desc limit 1),' \
          '(select now_confirm from history order by ds desc limit 1),' \
          '(select imported_case from history order by ds desc limit 1),' \
          '(select no_infect from history order by ds desc limit 1),' \
          'sum(heal),' \
          'sum(dead)' \
          'from details ' \
          'where update_time=(select update_time from details order by update_time desc limit 1)'
    res = query(sql)
    # 获取累计境外输入和新增境外输入
    today_new = get_import_case()
    return res[0], today_new


# 获取china右下侧数据，城市排行
def get_china_bottom_right():
    """

    :return:返回城市排行数据
    """
    sql = 'select city,confirm from ' \
          '(select city,confirm from details where update_time =' \
          '(select update_time from details order by update_time desc limit 1)' \
          'and province not in ("湖北","北京","上海","重庆","天津")and city not in ("地区待确认","境外输入") ' \
          'union all select province as city,sum(confirm) as confirm from details ' \
          'where update_time =(select update_time from details order by update_time desc limit 1) ' \
          'and province in("北京","上海","重庆","天津") and city not in ("地区待确认","境外输入") group by province) ' \
          'as a order by confirm desc limit 12'

    res = query(sql)
    return res


# 获取china-trend左上侧数据，全国累计趋势
def get_china_trend_top_left():
    """

    :return:返回全国累计趋势
    """
    sql = 'select ds,confirm,suspect,heal,dead,confirm_add from history'
    res = query(sql)
    return res


# 获取china-trend中上侧数据，全国新增确诊、疑似趋势
def get_china_trend_top_center():
    """

    :return:返回全国新增趋势
    """
    sql = 'select ds,confirm_add,suspect_add from history'
    res = query(sql)
    return res


# 获取china-trend右上侧数据，全国治愈、死亡趋势
def get_china_trend_top_right():
    """

    :return:返回全国境外输入、无症状感染者累计数据
    """
    sql = 'select ds,heal_add,dead_add from history'
    res = query(sql)
    return res


# 获取china-trend左下侧数据，全国境外输入、无症状感染者趋势
def get_china_trend_bottom_left():
    """

    :return:返回全国境外输入、无症状感染者累计数据
    """
    sql = 'select ds,imported_case,no_infect from history'
    res = query(sql)
    return res


# 获取china-trend中下侧数据，累计境外输入省市排行
def get_china_trend_bottom_center():
    """

    :return:返回城市排行数据
    """
    sql = 'select city,confirm, province from ' \
          '(select city,confirm,province from details where update_time =' \
          '(select update_time from details order by update_time desc limit 1)' \
          'and province not in ("湖北","北京","上海","重庆","天津")and city in ("境外输入") ' \
          'union all select province as city,sum(confirm) as confirm,province from details ' \
          'where update_time =(select update_time from details order by update_time desc limit 1) ' \
          'and province in("北京","上海","重庆","天津") and city in ("境外输入") group by province) ' \
          'as a order by confirm desc limit 10'

    res = query(sql)
    return res


# 获取china-trend右下侧数据，累计境外输入省市排行饼图
def get_china_trend_bottom_right():
    """

    :return:返回城市排行数据
    """
    sql = 'select city,confirm, province from ' \
          '(select city,confirm,province from details where update_time =' \
          '(select update_time from details order by update_time desc limit 1)' \
          'and province not in ("湖北","北京","上海","重庆","天津")and city in ("境外输入") ' \
          'union all select province as city,sum(confirm) as confirm,province from details ' \
          'where update_time =(select update_time from details order by update_time desc limit 1) ' \
          'and province in("北京","上海","重庆","天津") and city in ("境外输入") group by province) ' \
          'as a order by confirm desc limit 14'

    res = query(sql)
    return res


# 获取world数据，世界疫情地图
def get_world():
    """

    :return:返回世界各国数据
    """
    conn, cursor = get_conn()
    country_list = list(nameMap.namemap.values())
    global_dict = {}
    for item in country_list:
        sql = 'select confirm from fforeign where country = %s order by update_time desc limit 1'
        if cursor.execute(sql, item):
            res = cursor.fetchall()
            global_dict[item] = res[0][0]
    close_conn(conn, cursor)
    return global_dict


# 获取world-trend数据，国外趋势，不含中国
def get_world_trend_left():
    """

    :return:返回世界趋势数据
    """
    # sql = 'select update_time,sum(confirm),sum(heal),sum(dead) from fforeign group by update_time'
    sql = 'SELECT update_time,confirm,confirm_add,heal,dead FROM global'
    res = query(sql)
    return res


# 获取china-trend右侧数据，国家排行，不含中国
def get_world_trend_right():
    """

    :return:返回国外排行数据
    """
    sql = 'select country, confirm ,confirm_add, heal, dead  from fforeign ' \
          'where update_time =(select update_time from fforeign ' \
          'order by update_time desc limit 1) order by confirm  desc limit 7'

    res = query(sql)
    return res


# 获取国内最近一次更新时间
def get_time_china():
    sql = 'select update_time from details order by update_time desc limit 1'
    res = query(sql)
    res = res[0][0].strftime("%Y-%m-%d %H:%M:%S")
    return res


# 获取全球最近一次更新时间
def get_time_global():
    sql = 'select last_update_time from global order by update_time desc limit 1'
    res = query(sql)
    res = res[0][0].strftime("%Y-%m-%d %H:%M:%S")
    return res
