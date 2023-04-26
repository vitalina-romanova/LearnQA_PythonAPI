import time

import requests

# Первый запрос (создание задачи, получение токена)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
first_response = response.json()
main_token = first_response["token"]
print(main_token)

# Второй запрос (получение времени выполнения задачи)
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job",
                         params={f"token": f"{main_token}"})
second_response = response2.json()
time.sleep(first_response["seconds"])
time.sleep(2)

print(second_response)
assert second_response["status"] == 'Job is NOT ready'

# Третий запрос
response3 = requests.get('https://playground.learnqa.ru/ajax/api/longtime_job',
                         params={f"token": f"{main_token}"})
third_response = response3.json()
print(third_response)
assert third_response["status"] == 'Job is ready'
assert response3.text.__contains__("result")