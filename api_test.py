import requests

response = requests.get('http://127.0.0.1:8000/api/v1/post_list/')
result = response.json()

# Открываю список posts чтобы потом можно было его получить циклом
posts = result['posts']

# Вывожу посты по именам полей
for post in posts:
    print(post['title'], post['body'])
