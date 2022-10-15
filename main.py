import requests, os, time, json, re, sys
import logging
import datetime
import library
import json
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ------------配置区----------------#
def learn_time(*time_tuple):
    # 提前一天预约
    timestamp = (datetime.datetime.now() + datetime.timedelta(days=1)).date()
    # timestamp = (datetime.datetime.now() ).date()
    learn_am = time_tuple[0]
    duration_am = time_tuple[1]
    learn_pm = time_tuple[2]
    duration_pm = time_tuple[3]
    time_str = [[(str(timestamp) + ' ' + learn_pm), duration_pm, 'pm'],
                [(str(timestamp) + ' ' + learn_am), duration_am, 'am']]
    return time_str
    # print(timestamp)

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
    subject = f'{booking_time},预约成功'
    config.sendEMail(subject, content)


if __name__ == '__main__':
    username = config.username
    password = config.password
    room_id = config.room_id
    perfer_seat = config.perfer_seat
    print(config.time_tuple[0])
    print(config.time_tuple[1])
    time_str = learn_time(*config.time_tuple)
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
