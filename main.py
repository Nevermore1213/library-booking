import requests, os, time, json, re, sys
import logging
import datetime
import library
import json
import send_email

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ------------配置区----------------#
def learn_time():
    # 提前一天预约
    timestamp = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    # timestamp = (datetime.datetime.now() ).date()
    learn_am = "9:00"
    duration_am = 350
    learn_pm = "15:00"
    duration_pm = 350
    time_str = [[(str(timestamp) + ' ' + learn_pm), duration_pm, 'pm'],
                [(str(timestamp) + ' ' + learn_am), duration_am, 'am']]
    return time_str
    # print(timestamp)


def sendEMail(content):
    '''

    :param content: 邮件内容
    :return:
    '''
    # 发件人-填写自己的邮箱
    userName_SendMail = ''
    # 邮箱发件授权码-为发件人生成的授权码
    userName_AuthCode = ''
    # 定义邮件的接收者
    received_mail = ['']
    #发送邮件
    smtp = send_email.SendMsg(userName_SendMail, received_mail, userName_AuthCode, content)
    smtp.send_msg()


def save_json_file(log):
    '''
    将预约信息存为json文件，相对路径Booking\2022-09-29.json
    :param log:
    :return:
    '''
    booking_time = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    # booking_time = (datetime.datetime.now() ).date()
    txt = json.dumps(log, indent=2, ensure_ascii=False)
    with open(f'Booking/{booking_time}.json', 'w', encoding='utf-8') as f:
        f.write(txt)
    content = str(log)
    sendEMail(f'预约成功！{booking_time} {content} ')


if __name__ == '__main__':
    # 学号密码
    username = ""
    password = ""
    # 想要的房间座位
    room_id = 4
    perfer_seat = []

    time_str = learn_time()
    # -------------------------------#
    try:
        username = sys.argv[1]
        password = sys.argv[2]
        print("使用传入信息")
    except:
        if username == "" and password == "":
            logger.warning("账号或密码为空")

    print(f"👉账号:{username}")
    # print(f"👉密码:{password}")

    person = library.Person(username, password, room_id)
    person.login()
    # log列表储存上午、下午两个时间段的预约信息 [{'am':'008'},{'pm':'009'}]
    log = []
    print(time_str)
    for i in time_str:
        '''
        i[0] 开始时间
        i[1] 持续时间
        '''
        try:
            seatInfo = person.queryRoom(person.showRoom(room_id), perfer_seat, str(i[0]), i[1])
            if seatInfo is None:
                logger.warning("找不到位置")
                seat_id = ' '
            else:
                print(f"查询到 {seatInfo['name']} 位置满足要求")
                duration = i[1]
                person.submit(seatInfo, str(i[0]), duration)
                seat_id = str(seatInfo['name'][-3:])
            if i[2] == 'am':
                get_time_duration = 'am'
            else:
                get_time_duration = 'pm'

            dict = {get_time_duration: seat_id}
            log.append(dict)
        except:
            logger.warning('pass')
            pass
    save_json_file(log)
