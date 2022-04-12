import sys
import ddddocr
import requests
from hashlib import md5
from base64 import b64decode

from django.shortcuts import render, redirect
from datetime import datetime, timedelta, timezone
from django.http import HttpResponse, JsonResponse

from .models import User


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getToken(phone, password):
    # 输出调试信息，并及时刷新缓冲区
    def log(content):
        print(getTimeStr() + ' ' + str(content))
        sys.stdout.flush()

    # 获取当前 utc 时间，并格式化为北京时间
    def getTimeStr():
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        return bj_dt.strftime("%Y-%m-%d %H:%M:%S")

    # 获取验证码
    def getAuthCode():
        res = requests.post(url="https://hwy.328ym.com/member/verification/getAuthcode/register",
                            data={'deviceId': "ffffffff-a90f-1796-0000-000074d104dc"})
        if res.json()['success']:
            log("获取验证码图片 Base64 成功")
        else:
            log("获取验证码图片 Base64 失败")
            exit(-1)

        # 获取图片 Base64，并转为图片
        imgBase64 = res.json()['data']['imgBase64'].split(',')[1]
        captchaImg = b64decode(imgBase64)
        with open('captcha.png', 'wb') as f:
            f.write(captchaImg)
        with open('captcha.png', 'rb') as f:
            img_bytes = f.read()
        ocrres = ddddocr.DdddOcr().classification(img_bytes)

        # 将识别出的数字转为列表存储
        numstr = list(filter(str.isdigit, ocrres))
        log("验证码两个数字分别为 " + numstr[0] + " 和 " + numstr[1])
        return ocrres

    # 登录
    def loginUMeng():
        # 将识别出的数字转为列表存储
        numstr = list(filter(str.isdigit, getAuthCode()))
        numint0, numint1 = int(numstr[0]), int(numstr[1])

        # 懒得做训练了，直接识别出两个数字做加减乘除运算
        picCodeList = [numint0 + numint1, numint0 - numint1, numint0 * numint1, numint0 // numint1]
        headers = {
            "phoneModel": "Xiaomi%20Redmi%20K20%20Pro",
            "phoneSystemVersion": "11",
            "appVersion": "2.3.6",
            "Host": "hwy.328ym.com",
            "systemtype": "android",
            "content-type": "application/x-www-form-urlencoded",
            "content-length": '151',
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.2.2"
        }
        data = {
            'phone': phone,
            'passwordMD5': md5(password.encode("utf-8")).hexdigest(),
            'deviceId': "ffffffff-a90f-1796-0000-000074d104dc",
            'deviceType': 'android', 'pushClientId': '',
            'picCode': picCodeList[0]
        }

        # 将 picCode 四种可能分别拼接到 data 中验证
        res = requests.post(headers=headers,
                            url="https://hwy.328ym.com/member/member/authen/login/mphone2",
                            data=data)
        return res.json()

    res = loginUMeng()
    while not res['success']:
        log(res['msg'] + "\n-------------------------------------------\n\n\n"
                         "-------------------------------------------")
        res = loginUMeng()
    return res


token = ''


def login(request):
    # global phone, password
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        res = getToken(phone, password)
        if res['success']:
            global token
            token = res['data']['token']
            User.objects.create(phone=phone, password=password, token=token)
            userList = User.objects.all()
            return redirect('../show', {'userList': userList})

    return render(request, "login.html")


def show(request):
    headers = {
        'Host': "hwy.328ym.com",
        'systemtype': 'android',
        "content-type": "application/x-www-form-urlencoded",
        # "content-length": '160',
        "accept-encoding": 'gzip',
        "user-agent": "okhttp/4.2.2"
    }
    facultyId = "a44c19b0056f11ecbebffa163e5db904"
    if request.method == 'POST':
        gradeNumber = request.POST['gradeNumber']
        classNumber = request.POST['classNumber']
        # 判断性别赋值
        if request.POST['sex'] == "男":
            sex = '1'
            print("查询男生")
        elif request.POST['sex'] == '女':
            sex = '0'
            print("查询女生")
        else:
            sex = None
            print("查询所有")
        # 判断运动类型赋值
        if request.POST['typeValue'] == "长跑":  # typeValue 值，0：计步、 1：健走、 2：跑步、 3：骑行、 4：晨跑、 5：阳光长跑
            typeValue = 5
        else:
            typeValue = 4
            print(typeValue)

        # 获取用户列表
        def getMemberList():
            data = {
                'groupId': "e44ade15f26211ebbebffa163e5db904",  # 学校 ID
                'facultyId': facultyId,  # 院系 ID
                'gradeNumber': gradeNumber,  # 年级
                'gender': sex,  # 性别
                'pageNo': '1',
                'pageSize': '545',
            }

            res = requests.post(headers=headers, url="https://hwy.328ym.com/find/groupMember/memberList", data=data)
            r = res.json()['data']

            # 获取用户
            memberId = []
            realName = []
            gender = []
            for i in range(r['total']):
                if r['result'][i]['classNumber'] == classNumber:
                    memberId.append(r['result'][i]['memberId'])
                    realName.append(r['result'][i]['realName'])
                    gender.append(r['result'][i]['gender'])
            return memberId, realName, gender

        ID, name, gender = getMemberList()

        # 获取用户运动信息
        # typeValue 值，0：计步、 1：健走、 2：跑步、 3：骑行、 4：晨跑、 5：阳光长跑
        def getUserSportsInfo(memberId, typeValue):
            memberList = {'users': []}
            # print(token)
            if typeValue == 5:
                for i in range(len(memberId)):
                    res = requests.post(headers=headers,
                                        url="https://hwy.328ym.com/member/member/sevenDaySportData",
                                        data={'type': typeValue, 'token': token,
                                              'otherMemberId': memberId[i]})
                    # print(res.json())
                    r = res.json()['data']['ldrunning']
                    memberList['users'].append(r)
                    memberList['users'][i]['name'] = name[i]
                    if gender[i] == '1':
                        memberList['users'][i]['gender'] = "男"
                    else:
                        memberList['users'][i]['gender'] = "女"
            else:
                for i in range(len(memberId)):
                    res = requests.post(headers=headers,
                                        url="https://hwy.328ym.com/member/member/sevenDaySportData",
                                        data={'type': typeValue, 'token': token,
                                              'otherMemberId': memberId[i]})
                    r = res.json()['data']['mrunning']
                    memberList['users'].append(r)
                    memberList['users'][i]['name'] = name[i]
                    if gender[i] == '1':
                        memberList['users'][i]['gender'] = "男"
                    else:
                        memberList['users'][i]['gender'] = "女"
            print(memberList)
            return memberList

        userList = getUserSportsInfo(ID, typeValue)
        return render(request, "show.html", {"userList": userList['users'], 'typeValue': typeValue})
    return render(request, "show.html")


def infoJson(request):
    info = {
        'data': [
            {
                'phone': 'admin',
                'password': "admin",
            }
        ]
    }

    return JsonResponse(info, safe=False)
