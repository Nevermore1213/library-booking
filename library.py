import bs4
import requests, os, time, json, re, sys
from bs4 import BeautifulSoup
from MyUtil import *
import config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Person:
    def __init__(self, username, password, room_id):
        '''
        :param username:  用户账号
        :param password:  密码
        :param room_id:  预约房间
        '''
        self.session = requests.session()
        self.username = username
        self.password = password
        self.room_id = room_id
        self.time_format = "%Y-%m-%d %H:%M"
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
        })

    def login(self):
        '''

        :return:
        '''
        if os.path.exists("cookie"):
            self.session.cookies.update(readCookie("cookie"))

        url = "http://csyy.qdu.edu.cn:8080/ClientWeb/xcus/ic2/Default.aspx"
        soup = BeautifulSoup(self.session.get(url=url).content, "lxml")

        if not "统一身份认证" in soup.find("title"):
            logger.info("已从cookie登录")
            return

        data = {}
        for inTag in soup.findAll("input"):
            try:
                data[inTag["name"]] = inTag["value"]
            except:
                pass

        data["username"] = self.username
        data["password"] = self.password

        url = "http://authserver.qdu.edu.cn/authserver/login"
        soup = BeautifulSoup(self.session.post(url=url, data=data).text, "lxml")

        # 登陆校验
        if not "统一身份认证" in soup.find("title"):
            # saveCookie("cookie", self.session.cookies)
            logger.info("登陆成功")
        else:
            logger.warning("账号密码错误")
            exit(-1)

    def queryRoom(self, roomId, wantSeat=[], start_str="", duration = 60):
        # start_str format 2022-04-01 15:00 , duration: 单位 min
        '''

        :param roomId:
        :param wantSeat:
        :param start_str:
        :param duration:
        :return:
        '''
        now = time.localtime()

        if start_str != "":
            now = time.strptime(start_str, "%Y-%m-%d %H:%M")

        end_hour = 22
        url = f"http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/device.aspx?byType=devcls&classkind=8&display=fp&md=d&room_id={roomId}&purpose=&selectOpenAty=&cld_name=default&date={now.tm_year}-{fmt02(now.tm_mon)}-{fmt02(now.tm_mday)}&fr_start={fmt02(now.tm_hour)}%3A{fmt02(now.tm_min)}&fr_end={fmt02(end_hour)}%3A{fmt02(now.tm_min)}&act=get_rsv_sta&_={int(time.time() * 1000)}"

        logger.debug(url)
        response = json.loads(self.session.get(url).text)
        if response['ret'] == -1:
            logger.info(response['msg'])
            return
        validData = []
        data = response['data']
        for d in data:
            if d['state'] != "close":
                validData.append(d)

        logger.info(f"已检测到 {len(validData)} 个开放座位")

        if len(wantSeat) > 0:
            wantSeat.sort()

            if len(data) < wantSeat[-1]:
                logger.error("预设座位错误")

            found = True
            for seat in wantSeat:
                index = seat - 1
                if self.querySeatIsValid(data[index], start_str, duration):
                    return data[index]

            logger.warning("预设位置不满足!")
        #顺序查询座位
        for index in range(len(data)):
        #逆序查询座位
        # for index in range(len(data)-1, 0, -1):
            if self.querySeatIsValid(data[index], start_str, duration):
                return data[index]

    def querySeatIsValid(self, seatInfo, want_start_str="", duration=60):
        '''

        :param seatInfo:
        :param want_start_str:
        :param duration:
        :return:
        '''
        # duration: 单位min
        if seatInfo['state'] == "close":
            return False

        if seatInfo['freeTime'] < duration:
            logger.warning(f"{seatInfo['name']}: 时间不满足, 您需要的时间 {duration}min, 只有 {seatInfo['freeTime']}min")
            return False

        # 没有人占座
        if len(seatInfo['ts']) == 0:
            return True

        # 时间不冲突, 遍历位置时间段, 有一个冲突直接放弃
        found = True
        for ts in seatInfo['ts']:
            if not self.isvalid(ts['start'], ts['end'], want_start_str, duration * 60):
                found = False
                break

        if found:
            return True

    def showRoom(self, room_id):
        '''

        :param room_id:
        :return: 房间序号
        '''
        #index = 0
        # for key in config.room:
        #     index += 1
        #     print(f'{index}) ' + key['area'] + key['name'])
        id = int(room_id - 1)
        return config.room[id]['id']
        # return config.room[int(input("请输入你需要的房间序号: ")) - 1]['id']

    def isvalid(self, start_str="", end_str="", want_start_str="", want_duration=60 * 60):
        # format 2022-04-01 15:00, want_duration: 单位s, 默认一小时
        if start_str == "" or end_str == "" or want_start_str == "":
            return True

        # 以下时间戳单位: s
        start_time = time.mktime(time.strptime(start_str, self.time_format))
        end_time = time.mktime(time.strptime(end_str, self.time_format))
        real_duration = end_time - start_time

        want_start = time.mktime(time.strptime(want_start_str, self.time_format))
        want_end = want_start + want_duration

        # max_time - min_time 所跨时间段
        min_time = min(start_time, end_time, want_start, want_end)
        max_time = max(start_time, end_time, want_start, want_end)

        # 时间交集
        return max_time - min_time >= real_duration + want_duration

    def submit(self, seatInfo, start_str="", duration=60):
        logger.info(f"正在提交数据至{seatInfo['name']} . . .")
        # duration: 单位 min
        date_str = start_str.split()[0]
        start_time = start_str.split()[-1]
        end_time = time.mktime(time.strptime(start_str, self.time_format)) + duration * 60
        end_time = time.localtime(end_time)

        end_time = f"{end_time.tm_hour}:{end_time.tm_min}"

        logger.info(f"提交时间 {date_str} {start_time} 至 {date_str} {end_time}")

        url = "http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/reserve.aspx"
        data = {
            'dev_id': seatInfo['devId'],  # 房间及座位编号
            'start': f'{date_str} {start_time}',  # 2022-03-31+13%3A56
            'end': f'{date_str} {end_time}',
            'start_time': start_time.replace(":", ""),
            'end_time': end_time.replace(":", ""),
            'act': "set_resv",
            '_': int(time.time() * 1000)
        }
        logger.debug(data)
        response = self.session.get(url, params=data)
        logger.info(response.text)

    def queryHistory(self):
        logger.info("正在查询历史 rsvId: ")
        response = self.session.get(
            f"http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/center.aspx?act=get_History_resv&StatFlag=New&_={int(time.time() * 1000)}")
        msg = json.loads(response.text)['msg']
        rsvIds = re.findall("rsvId='(.*?)' onclick='", msg)
        logger.info(rsvIds)
        return rsvIds

    def deleteSeat(self, rsvId):
        logger.info(f"正在删除 {rsvId}")
        response = self.session.get(
            f"http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/reserve.aspx?act=del_resv&id={rsvId}&_={int(time.time() * 1000)}")
        msg = json.loads(response.text)['msg']
        print(msg)

    def getInfo(self, room_id):
        '''
        获取房间内成员预约信息
        :param room_id:
        :return:
        '''
        roomId = self.showRoom(room_id)
        now = time.localtime()
        url = f"http://csyy.qdu.edu.cn:8080/ClientWeb/pro/ajax/device.aspx?byType=devcls&classkind=8&display=fp&md=d&room_id={roomId}&purpose=&selectOpenAty=&cld_name=default&date={now.tm_year}-{fmt02(now.tm_mon)}-{fmt02(now.tm_mday)}&fr_start=7%3A00&fr_end=22%3A00&act=get_rsv_sta&_={int(time.time() * 1000)}"
        logger.info("正在查询房间")
        print(config.room[room_id-1]['name'])
        response = self.session.get(url)
        data = json.loads(response.text)['data']
        for seatData in data:
            if seatData['state'] != 'close':
                roomName = seatData['name']
                print('--------------------------')
                print(roomName)
                ts = seatData['ts']
                for student in ts :
                    name = student['owner']
                    accno = student['accno'] #可能与学号有关
                    start = student['start']
                    end = student['end']
                    state = student['state']
                    print(name, start, end, state)

    # 以下为可选
    # rsvIds = person.queryHistory() # 查询预约历史
    # if len(rsvIds) > 0:
    #     person.deleteSeat(rsvIds[0]) # 删除刚刚的预约
if __name__ == '__main__':
    test = Person('', '', 4)
    test.login()
    test.getInfo(4)
