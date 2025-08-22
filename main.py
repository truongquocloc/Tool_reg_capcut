import requests
import random
from datetime import datetime, timedelta
import string
import time
from reg_mail_tm import regMail, get_messages_code
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

lock = threading.Lock()

def encode_email( email: str) -> str:
    SHIFT = {
        '@': 5,
        '0': 5, '1': 3, '2': 5, '3': 3, '4': -3, '5': -5, '6': -3, '7': -5, '8': 5, '9': 3,
        'a': 3, 'b': 5, 'c': 3, 'd': -3, 'e': -5, 'f': -3, 'g': -5, 'h': 5,
        'i': 3, 'j': 5, 'k': 3, 'l': -3, 'm': -5, 'n': -3, 'o': -5, 'p': 5,
        'q': 3, 'r': 5, 's': 3, 't': -3, 'u': -5, 'v': -3, 'w': -5, 'x': 5, 'y': 3, 'z': 5,
    }
    s = email.lower()
    if s.endswith(".com"):
        s = s[:-4]  # bỏ ".com"
    out = []
    for ch in s:
        out.append((ord(ch) + SHIFT[ch]) & 0xFF)
    out += b"+fjh"
    return "".join(f"{b:02x}" for b in out)
# Bảng ánh xạ ký tự -> hex 

def encode_password( pw: str) -> str:
    mapping = {
# letters
'a': '64',  # a +3 -> 'd'
'b': '67',  # b +5 -> 'g'
'c': '66',  # c +3 -> 'f'
'd': '61',  # d -3 -> 'a'
'e': '60',  # e -5 -> '`'
'f': '63',  # f -3 -> 'c'
'g': '62',  # g -5 -> 'b'
'h': '6d',  # h +5 -> 'm'
'i': '6c',  # i +3 -> 'l'
'j': '6f',  # j +5 -> 'o'
'k': '6e',  # k +3 -> 'n'
'l': '69',  # l -3 -> 'i'
'm': '68',  # m -5 -> 'h'
'n': '6b',  # n -3 -> 'k'
'o': '6a',  # o -5 -> 'j'
'p': '75',  # p +5 -> 'u'
'q': '74',  # q +3 -> 't'
'r': '77',  # r +5 -> 'w'
's': '76',  # s +3 -> 'v'
't': '71',  # t -3 -> 'q'
'u': '70',  # u -5 -> 'p'
'v': '73',  # v -3 -> 's'
'w': '72',  # w -5 -> 'r'
'x': '7d',  # x +5 -> '}'
'y': '7c',  # y +3 -> '|'
'z': '7f',  # z +5 -> DEL

# digits
'0': '35',  # 0 +5 -> '5'
'1': '34',  # 1 +3 -> '4'
'2': '37',  # 2 +5 -> '7'
'3': '36',  # 3 +3 -> '6'
'4': '31',  # 4 -3 -> '1'
'5': '30',  # 5 -5 -> '0'
'6': '33',  # 6 -3 -> '3'
'7': '32',  # 7 -5 -> '2'
'8': '3d',  # 8 +5 -> '='
'9': '3c',  # 9 +3 -> '<'

# specials / uppercase seen in your data
'@': '45',  # @ +5 -> 'E'
'T': '51',  # T -3 -> 'Q'
}

    """Mã hóa password thành hex theo mapping"""
    return "".join(mapping[ch] for ch in pw)

def random_date(start_year=1990, end_year=2005):
    # Tạo ngày bắt đầu và ngày kết thúc
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    
    # Tính số ngày giữa 2 mốc
    delta_days = (end_date - start_date).days
    
    # Chọn ngẫu nhiên số ngày bù thêm
    random_days = random.randint(0, delta_days)
    
    # Sinh ra ngày ngẫu nhiên
    date_random = start_date + timedelta(days=random_days)
    
    return date_random.strftime("%Y-%m-%d")

def random_password(length=7):
    characters = string.digits + string.ascii_lowercase + string.digits  # chữ thường + số
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def getUserAgent():
    with open('useragent.txt', 'r', encoding='utf-8') as file:
        data = file.readlines()
    return random.choice(data).strip()

def updateAccountReg(account):
  with open('account_reg.txt', 'a') as f:
    f.write(account + '\n')

def registerCC(email_encode, password_encode):
    
    url = "https://www.capcut.com/passport/web/email/send_code/"
    params = {
        "aid": "348188",
        "account_sdk_source": "web",
        "sdk_version": "2.1.10-tiktok",
        "language": "en"
    }

    payload = {
        "mix_mode": "1",
        "email": email_encode,
        "password": password_encode,
        "type": "34",
        "fixed_mix_mode": "1"
    }

    headers = {
        "accept": "application/json, text/javascript",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "appid": "348188",
        "content-type": "application/x-www-form-urlencoded",
        "did": "7541246988857378320",
        "origin": "https://www.capcut.com",
        "referer": "https://www.capcut.com/signup?current_page=landing_page&from_page=landing_page&enter_from=a1.b1.c1.0",
        "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "store-country-code": "vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-tt-passport-csrf-token": "b7b25f7b7521a6283a46dce9040d7386"
    }

    response = requests.post(url, params=params, data=payload, headers=headers)
    return response.json()['message']

def register_verify_login(email_encode, password_encode, code_encode):
    url = "https://www.capcut.com/passport/web/email/register_verify_login/"
    params = {
        "aid": "348188",
        "account_sdk_source": "web",
        "sdk_version": "2.1.10-tiktok",
        "language": "en"
    }

    headers = {
        "accept": "application/json, text/javascript",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "appid": "348188",
        "content-type": "application/x-www-form-urlencoded",
        "did": "7541246988857378320",
        "origin": "https://www.capcut.com",
        "referer": "https://www.capcut.com/signup?current_page=landing_page&from_page=landing_page&enter_from=a1.b1.c1.0",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "store-country-code": "vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "x-tt-passport-csrf-token": "b7b25f7b7521a6283a46dce9040d7386"
    }

    data = {
        "mix_mode": "1",
        "email": email_encode,
        "code": code_encode,
        "password": password_encode,
        "type": "34",
        "birthday": random_date(),
        "force_user_region": "VN",
        "biz_param": '{"invite_code":""}',
        "fixed_mix_mode": "1"
    }

    response = requests.post(url, params=params, headers=headers, data=data)
    result = response.json()
    if result['message'] == 'success':
        return result['data']['user_id']
    else:
        return None


def regAccountCC():
    while True:
      try:
        userAgent = getUserAgent()
        email = regMail(userAgent)
        password = random_password()
        # print(email + '|' + password)
        email_encode = encode_email(email)
        password_encode = encode_password(password)
        result = registerCC(email_encode, password_encode)
        if result != 'success':
            print("Bị lỗi trong quá trình đăng ký account !!!")
        # print(result)
        time.sleep(5)
        for i in range(10):
          code = get_messages_code(email, '123456a@', userAgent)
          # print('Code: ', code)
          if code and code != 'watting':
            code_encode = encode_password(code)
            userID = register_verify_login(email_encode, password_encode, code_encode)
            if userID:
                line = email + '|' + password + '|' + str(userID)
                print(line)
                with lock:
                    updateAccountReg(line)
                break
          time.sleep(2)
          # print("Đang đợi code")
      except Exception as error:
          pass

if __name__ == "__main__":
    num_threads = 20  # số luồng muốn chạy song song
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_threads):
            future = executor.submit(regAccountCC)
            futures.append(future)
            time.sleep(1)
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("Có lỗi:", e)


      





