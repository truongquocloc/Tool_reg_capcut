import requests
import re


def create_temp_mail(userAgent=None, payload=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    url = "https://api.internal.temp-mail.io/api/v3/email/new"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "application-name": "web",
        "application-version": "4.0.0",
        "content-type": "application/json",
        "origin": "https://temp-mail.io",
        "referer": "https://temp-mail.io/",
        "user-agent": userAgent
    }
    if not payload:
      payload = {
          "min_name_length": 20,
          "max_name_length": 25
      }
    
    
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    if response.status_code == 200:
        try:
            if 'email' in result:
              return result['email']
            else: return ""
        except:
            return ""
    else:
        return ""
    
def get_temp_mail_messages(email, userAgent=None):
    if not userAgent:
      userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    url = f"https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "application-name": "web",
        "application-version": "4.0.0",
        "content-type": "application/json",
        "origin": "https://temp-mail.io",
        "referer": "https://temp-mail.io/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": userAgent,

        }
    
    response = requests.get(url, headers=headers)
    result = response.json()
    try:
        if len(result) == 0:
            return "waitting"
        else:
            title = result[0]["subject"]
            match = re.search(r'\b\d{6}\b', title)  # tìm 6 chữ số liên tiếp
            if match:
               return match.group()
            else:
                return "waitting"
    except Exception:
        return ''  
    
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
    data = response.json()
    data = data['domains']
    result = [domain['name'] for domain in data]
    return result

# Test thử
if __name__ == "__main__":
    print(create_temp_mail())
