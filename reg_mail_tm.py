import requests
import random
import time
import string
import re


def get_token(address: str, password: str, userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    url = "https://api.mail.tm/token"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "content-type": "application/json",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent
    }
    
    payload = {"address": address, "password": password}
    
    response = requests.post(url, json=payload, headers=headers)
    if 'token' in response.json():
        return response.json()['token']
    else: ''

def create_account(address: str, password: str, userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    url = "https://api.mail.tm/accounts"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "content-type": "application/json",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent
    }
    
    payload = {"address": address, "password": password}
    
    response = requests.post(url, json=payload, headers=headers)
    

    if response.status_code == 201:
      return response.json()
    elif response.status_code  == 429:
      # print(response)
      time.sleep(random.randint(1,5))
      return create_account(address, password)
    else:
      # print(response)
      return ''

def get_me(token: str, userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    url = "https://api.mail.tm/me"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "authorization": f"Bearer {token}",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent
    }
    
    response = requests.get(url, headers=headers)
    
    return response.json()

def get_domain(userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    url = "https://api.mail.tm/domains"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent
    }
    
    response = requests.get(url, headers=headers)
    result = response.json()
    if 'hydra:totalItems' in result:
        if result['hydra:totalItems'] > 0:
          return result['hydra:member'][0]['domain']
        else:
            time.sleep(2)
            return get_domain()
    else:
      time.sleep(2)
      return get_domain()

def getRandomEmail():
    length = random.randint(18,20)
    characters = string.ascii_lowercase + string.digits  # chữ thường + số
    emailName = ''.join(random.choice(characters) for _ in range(length))
    return emailName

def regMail(userAgent = None, domain = None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    password = '123456a@'
    while True:
      try:
        if not domain:
          domain = get_domain(userAgent)
        randomEmail = getRandomEmail() + '@' + domain
        randomEmail = randomEmail.lower()
        result = create_account(randomEmail, password, userAgent)
        if result:
          if 'address' in result:
            if result['address'] == randomEmail:
              return randomEmail
          time.sleep(1)
        else:
          time.sleep(1)
      except Exception as e:
        print("Lỗi" , e)

def get_messages_code(email, password, userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    token = get_token(email, password, userAgent)
    url = "https://api.mail.tm/messages"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "authorization": f"Bearer {token}",
        "if-none-match": "\"0a4f448ec35e5f2e298782d9de55c215\"",
        "origin": "https://mail.tm",
        "referer": "https://mail.tm/",
        "sec-ch-ua": "\"Not;A=Brand\";v=\"99\", \"Google Chrome\";v=\"139\", \"Chromium\";v=\"139\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if 'hydra:member' in result:
          messages = result['hydra:member']
          if len(messages) > 0:
            message = result['hydra:member'][0]['subject']
            match = re.search(r'\b\d{6}\b', message)  # tìm 6 chữ số liên tiếp
            if match:
               return match.group()
            else: 
               return 'waitting'  
          else:
             return 'watting'
        else:
           return None
    else:
        return None
  

  