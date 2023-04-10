import requests

url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'
# Запрос без параметра method    В тексте ответа приходит "Wrong method provided" код ответа 200
response_first = requests.post(url)
print(response_first.text)
print(response_first.status_code)

# Запрос методом HEAD    В тексте ответа пусто, код ответа 400
response_second = requests.head(url, data={"method": "HEAD"})
print(response_second.text)
print(response_second.status_code)

# Запрос методом PUT     В тексте ответа "{"success":"!"}" код ответа 200
response_third = requests.put(url, data={"method": "PUT"})
print(response_third.text)
print(response_third.status_code)

# Запрос методами GET, POST, PUT, DELETE
request_types = ["GET", "POST", "PUT", "DELETE"]

for type in request_types:
    print()
    print("sending request with type: ", type)
    for param in request_types:
        print()
        print("Sending requst with parameter ", param)
        if type.__contains__('GET'):
            response = requests.request(type, url, params={"method": param})
        else:
            response = requests.request(type, url, data={"method": param})
        print(response.text)
        print(response.status_code)