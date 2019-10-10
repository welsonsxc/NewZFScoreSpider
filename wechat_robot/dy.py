import login
from wechat_robot import sql


def login1(xh, pw):
    # 验证账号密码
    try:
        cumt_grades = login.Get_grades(str(xh), str(pw), year="2017", term="3")
    except Exception as e:
        print(e)
        return "[Error]账号密码错误,请重新输入"
    # 爬取成绩数据
    try:
        cumt_grades.post_gradedata()
        cumt_grades.welcome()
        cumt_grades.print_geades()
    except Exception as e:
        print(e)
        return "[Error]爬取成绩错误,请联系管理员"
    # 数据库查询
    try:
        message1 = ""
        result = sql.sql_search_score(cumt_grades.user, cumt_grades.year, cumt_grades.term)
        for i in result:
            message1 = message1 + "@" + str(i[3]) + "\n" + "成绩" + str(i[5]) + "绩点" + str(i[6]) + "\n"
        return message1
    except Exception as e:
        print(e)
        return "[Error]数据库查询错误，请联系管理员"


# except:
#     print("[Error]数据库查询失败")
if __name__ == "__main__":
    xh = "学号"
    pw = "密码"
    print(login1(xh, pw))
