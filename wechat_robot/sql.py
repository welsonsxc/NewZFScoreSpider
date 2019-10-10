# -*- coding:utf-8 -*-
import pymysql

# 数据库: qjjw
# 学生账号密码表:stu_pw {OPENID:openid		学号:stu_xh;
# 						密码:stu_pw}
# 学生信息表:stu_info 	{学号:stu_xh		姓名:stu_xm;		
#						学历:stu_xslb;		学院：stu_jgmc;
# 						班级:stu_bj}
# 学生成绩表:stu_score 	{学号:stu_xh;		学年:study_year;
#						学期:study_term;	课程名:class_name;
#						成绩:study_score;	绩点:study_gpa;
#						教师姓名:teacher_name}

host1 = 'localhost'
user1 = 'root'
password1 = 'Scsql2018!'
db1 = 'qjjw'
# 根据openid返回学号密码
def sql_openid(openid):
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    sql = "select * from stu_pw where openid = %s " % openid
    try:
        cur.execute(sql)
        results = cur.fetchall()
        return results
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()

# 查询表(总信息)
def sql_select(db_table_name):
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    sql = "select * from %s" % db_table_name
    try:
        cur.execute(sql)
        results = cur.fetchall()
        return (results)
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()


# 输出表
def sql_print(db_table_name):
    results = sql_select(db_table_name)
    if (db_table_name == 'stu_pw'):
        print('===============账号密码表===============')
        print('学号\t\t 密码')
        for row in results:
            stu_xh = row[1]
            stu_pw = row[2]
            print(stu_xh, '\t', stu_pw)
    elif (db_table_name == 'stu_info'):
        print('===============学生信息表===============')
        print('学号\t\t 姓名\t\t学历\t\t学院\t\t班级')
        for row in results:
            stu_xh = row[0]
            stu_xm = row[1]
            stu_xslb = row[2]
            stu_jgmc = row[3]
            stu_bj = row[4]
            print(stu_xh, '\t', stu_xm, '\t\t', stu_xslb, '\t\t', stu_jgmc, '\t\t', stu_bj)
    elif (db_table_name == 'stu_score'):
        print('===============学生成绩表===============')
        for row in results:
            print(str(row))


# 查询成绩
def sql_search_score(userxh, year_now, term_now):
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    # sql = "select * from stu_score where stu_xh=%s" % userxh
    sql="select * from stu_score a where stu_xh=%s and a.update_time in (select max(b.update_time)from stu_score b where b.stu_xh = a.stu_xh)" % userxh
    try:
        cur.execute(sql)
        results = cur.fetchall()
        return results
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()


# 查询该学生是否存在信息		
def sql_search_info(db_table_name, userxh):
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    sql = "select count(*) from %s where stu_xh=%s" % (db_table_name, userxh)
    try:
        cur.execute(sql)
        results = cur.fetchall()
        if str(results) != '((0,),)':
            return True
        else:
            return False
    except Exception as e:
        raise e
    finally:
        cur.close()
        db.close()


# 保存学号和密码
def insert_pw(openid, userxh, password):
    # 创建数据库游标连接
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    # 格式化传递数据
    fh = r"'"
    openid = fh + openid + fh
    userxh = fh + userxh + fh
    password = fh + password + fh
    # 如果该学生存在则更新密码
    if (sql_search_info('stu_pw', userxh) == True):
        sql = "update stu_pw set stu_pw=%s where stu_xh=%s" % (password, userxh)
    else:
        sql = "INSERT INTO stu_pw (openid,stu_xh,stu_pw) VALUES (%s,%s,%s)" % (openid, userxh, password)
    print('[sql]' + sql)
    # 插入数据
    try:
        cur.execute(sql)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print('插入失败')
        return False
    finally:
        cur.close()
        db.close()


# 保存学生信息
def insert_info(userxh, name, xslb, jgmc, bj):
    # 创建数据库游标连接
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    # 格式化传递数据
    fh = r"'"
    userxh = fh + userxh + fh
    name = fh + name + fh
    xslb = fh + xslb + fh
    jgmc = fh + jgmc + fh
    bj = fh + bj + fh
    # 如果该学生存在则更新信息
    if (sql_search_info('stu_info', userxh) == True):
        sql = "update stu_info set stu_xm=%s,stu_xslb=%s,stu_jgmc=%s,stu_bj=%s where stu_xh=%s" % (
            name, xslb, jgmc, bj, userxh)
    else:
        sql = "INSERT INTO stu_info (stu_xh,stu_xm,stu_xslb,stu_jgmc,stu_bj) VALUES (%s,%s,%s,%s,%s)" % (
            userxh, name, xslb, jgmc, bj)
    print('[sql]' + sql)
    # 插入数据
    try:
        cur.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('[Error]插入失败')
    finally:
        cur.close()
        db.close()


# 保存成绩
def insert_score(userxh, year, term, kcmc, bfzcj, jd, jsxm, datetime):
    # 创建数据库游标连接
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    fh = "'"
    userxh = fh + userxh + fh
    year = fh + year + fh
    # 学期处理
    if term == "3":
        term = "1"
    elif term == "12":
        term = "2"
    term = fh + term + fh
    kcmc = fh + kcmc + fh
    bfzcj = fh + str(bfzcj) + fh
    jd = fh + str(jd) + fh
    jsxm = fh + jsxm + fh
    datetime = fh + datetime + fh
    sql = "INSERT INTO stu_score(stu_xh,study_year,study_term,class_name,study_score,study_gpa,teacher_name,update_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)" % (
        userxh, year, term, kcmc, bfzcj, jd, jsxm, datetime)
    try:
        print('[sql]:' + sql)
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print('[Error]插入失败')
    cur.close()
    db.close()


# 删除某表中某学生的所有信息
def sql_delete(dbtable_name, userxh):
    db = pymysql.connect(host=host1, user=user1,
                         password=password1, db=db1, port=3306)
    cur = db.cursor()
    fh = r"'"
    userxh = fh + userxh + fh
    sql = "delete from %s where stu_xh = %s" % (dbtable_name, userxh)
    try:
        print('[sql]' + sql)
        cur.execute(sql)  # 向sql语句传递参数
        db.commit()
    except Exception as e:
        db.rollback()
        print('[Error]删除失败')
    finally:
        cur.close()
        db.close()


if __name__ == "__main__":
    # sql_delete('stu_score', '2017830402030')
    # Insertpw('2017830402024','SCjiaowu287486.')
    # Insertinfo('2017830402024','盛超')
    # insert_score("2017830402024", "2017", "3", "中国近现代史纲要", "74", "2.40", "江齐里")
    # userxh, year, term, name, kcmc, bfzcj, jd, jsxm)
    # SqlSearchscore('2017830402024','2017-2018','2')
    # print(SqlSelect('stu_info'))
    openid = "obn5X0nLSTNa2Zso_mzbfqmI3pz0"
    fh = r"'"
    openid = fh + openid + fh
    res = sql_openid(openid)[0][2]
    print(res)
    # sql_print('stu_pw')
    # sql_print('stu_info')
    # sql_print('stu_score')
    temp = input()
