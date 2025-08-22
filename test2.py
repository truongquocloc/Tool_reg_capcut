import requests

def register_verify_login():
    url = "https://www.capcut.com/passport/web/email/register_verify_login/"
    params = {
        "aid": "348188",
        "account_sdk_source": "web",
        "sdk_version": "2.1.10-tiktok",
        "language": "en",
        "verifyFp": "verify_men3u373_p4ut0dO9_Xadm_4KY7_92x8_DBDiBq1Y5N52"
    }

    headers = {
        "accept": "application/json, text/javascript",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi,fr-FR;q=0.9,fr;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5,zh;q=0.4",
        "appid": "348188",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "capcut_locale=en; ug_capcut_locale=en; _tea_web_id=7541246988857378320; _gcl_au=1.1.338810972.1755883714; _ga=GA1.1.244476855.1755883714; _ut=...; passport_csrf_token=b7b25f7b7521a6283a46dce9040d7386; passport_csrf_token_default=b7b25f7b7521a6283a46dce9040d7386; ...",
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
        "email": "3753333668077696445756a7260777666770672762b666a68",
        "code": "3c3d33333c37",
        "password": "33464a5e395c26433d39",
        "type": "34",
        "birthday": "1992-02-02",
        "force_user_region": "VN",
        "biz_param": '{"invite_code":""}',
        "fixed_mix_mode": "1"
    }

    response = requests.post(url, params=params, headers=headers, data=data)
    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    register_verify_login()
