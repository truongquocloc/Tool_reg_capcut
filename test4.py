import requests

def get_temp_mail_domains():
    url = "https://api.internal.temp-mail.io/api/v4/domains"

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "application-name": "web",
        "application-version": "4.0.0",
        "content-type": "application/json",
        "origin": "https://temp-mail.io",
        "referer": "https://temp-mail.io/",
        "sec-ch-ua": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "x-cors-header": "iaWg3pchvFx48fY"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # báo lỗi nếu HTTP code != 200
    return response.json()

def encode_email( self, email: str) -> str:
    SHIFT = {
        '@': 5,
        '0': 5, '1': 3, '2': 5, '3': 3, '4': -3, '5': -5, '6': -3, '7': -5, '8': 5, '9': 3,
        'a': 3, 'b': 5, 'c': 3, 'd': -3, 'e': -5, 'f': -3, 'g': -5, 'h': 5,
        'i': 3, 'j': 5, 'k': 3, 'l': -3, 'm': -5, 'n': -3, 'o': -5, 'p': 5,
        'q': 3, 'r': 5, 's': 3, 't': -3, 'u': -5, 'v': -3, 'w': -5, 'x': 5, 'y': 3, 'z': 5,
    }

    s = email
    if s.lower().endswith(".com"):
        s = s[:-4]  # bỏ ".com"

    out = []

    for ch in s:
        base = ch.lower()

        if ch.isalpha() and ch.isupper():
            # Chữ hoa: dùng shift của chữ thường rồi TRỪ 32
            encoded = (ord(base) + SHIFT[base] - 32) & 0xFF
        else:
            # Chữ thường, số, @: xử lý như cũ
            encoded = (ord(base) + SHIFT[base]) & 0xFF

        out.append(encoded)

    out += b"+fjh"
    return "".join(f"{b:02x}" for b in out)

def encode_password(self, pw: str) -> str:
    mapping = {
        # letters
        'a': '64',  # d
        'b': '67',  # g
        'c': '66',  # f
        'd': '61',  # a
        'e': '60',  # `
        'f': '63',  # c
        'g': '62',  # b
        'h': '6d',  # m
        'i': '6c',  # l
        'j': '6f',  # o
        'k': '6e',  # n
        'l': '69',  # i
        'm': '68',  # h
        'n': '6b',  # k
        'o': '6a',  # j
        'p': '75',  # u
        'q': '74',  # t
        'r': '77',  # w
        's': '76',  # v
        't': '71',  # q
        'u': '70',  # p
        'v': '73',  # s
        'w': '72',  # r
        'x': '7d',  # }
        'y': '7c',  # |
        'z': '7f',  # DEL

        # digits
        '0': '35',
        '1': '34',
        '2': '37',
        '3': '36',
        '4': '31',
        '5': '30',
        '6': '33',
        '7': '32',
        '8': '3d',
        '9': '3c',

        # specials
        '@': '45',
        # 'T': '51',  # không cần cũng được vì T sẽ được tính từ 't'
    }

    out = []

    for ch in pw:
        if ch in mapping:
            # ký tự thường, số, @,...
            out.append(mapping[ch])
        elif ch.isalpha() and ch.isupper():
            # chữ hoa: dựa vào mapping của chữ thường rồi TRỪ 32
            low = ch.lower()
            if low not in mapping:
                raise ValueError(f"No mapping for lowercase of {ch}")

            base = int(mapping[low], 16)
            up = (base - 0x20) & 0xFF
            out.append(f"{up:02x}")
        else:
            raise ValueError(f"Unknown character: {ch}")

    return "".join(out)

def get_hostmail_messages(email, password, refresh_token, client_id):
      url = "https://tools.dongvanfb.net/api/get_messages_oauth2"
      code = ''
      payload = {
          "email": email,
          "pass": password,
          "refresh_token": refresh_token,
          "client_id": client_id
      }
      for i in range(10):
        try:
          response = requests.post(url, json=payload)
          result = response.json()
          if result['status'] == True:
              if len(result['messages']) > 0:
                  lastMessage = result['messages'][0]
                  if (lastMessage['from'] == 'admin@mail.capcut.com') and ('Welcome to CapCut and your verification code is' in lastMessage['subject']):
                      code = lastMessage['subject'].split()[-1]
                      if code: return code
        except Exception as e:
            pass

      return code


# Ví dụ chạy:
if __name__ == "__main__":
    # data = get_temp_mail_domains()
    # data = data['domains']
    # result = [domain['name'] for domain in data]
    # print(result)
    print(get_hostmail_messages('nkosiwdemuson6y6b@hotmail.com', 'pvkVKOFq6ywM', 'M.C542_BL2.0.U.-CgvZLlh*r4shPYNFczIoGv0rqMZEntNPYycm9i8QEDgSvj8pm2txKYUMsQUNeD5IkgwQws6jO!ltefir78RDdnJMGU052VDFxHLvpxeTnMZumLUGc49M5RLcCnAfeWWkZ2HWvPbpkNTwG0Qc1ND64xnFr85jZVTxCbezkWFgui5btoBafvKDLB1Tew9kw4ktokjCqHAbbUymYmLtSHcPS7o69l88JY*mamDTaDm4t4fFkkTEgW!Rrf7LC1*PTkAho1X6bbyW5iwPSXQlWKor2ZO3WboHWlI3P3jW4dpkcoacuJLEuP1FwhMOeIR6XZ7JjDMGjKWjINAn*jy1IaCtMS7eRHC3VocsnQsYsFy5hk*4cA26I9Pw70dBWRoJ3uf1G2O*ev85tH7pk6tNM5nlO*gp!cNS6QJm0iJJFSixkYwAHfUwIig4OdNkvGHNzAnNPA$$', '9e5f94bc-e8a4-4e73-b8be-63364c29d753'))
