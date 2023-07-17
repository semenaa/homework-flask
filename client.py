import requests



# response = requests.post(
#     "http://127.0.0.1:5000/users", json={"name": "user_2", "password": "ff323m3m3232425r2"}
# )
# response = requests.patch(
#     "http://127.0.0.1:5000/users/3", json={"name": "new_name"}
# )
response = requests.delete(
    "http://127.0.0.1:5000/users/1"
)
print(response.status_code)
print(response.json())
response = requests.get(
    "http://127.0.0.1:5000/users/1"
)

print(response.status_code)
print(response.json())
