import requests

se = requests.session()
url = "https://defendtheweb.net/playground/http-method"
data = {
    "password": "e8bed696bb"
}
re = se.post(url=url, data=data)
print(re.text)
