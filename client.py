import requests


# response = requests.post('http://127.0.0.1:5000/users/',
#                          json={'email': 'some1@email.com', 'password': '1234Vova!'})


# response = requests.get('http://127.0.0.1:5000/users/5/')

# response = requests.delete('http://127.0.0.1:5000/users/2/')

response = requests.post('http://127.0.0.1:5000/adv/3/', json={'title': 'MyNew', 'description': 'Some'})

# response = requests.get('http://127.0.0.1:5000/adv/1/')

print(response.status_code)
print(response.json())
