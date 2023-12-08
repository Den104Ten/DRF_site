import tkinter as tk
import requests

response = requests.get('http://127.0.0.1:8000/api/v1/post_list/')
result = response.json()

# Открываю список posts чтобы потом можно было его получить циклом
posts = result['posts']

# Вывожу посты по именам полей
"""for post in posts:
    print(post['title'], post['body'])"""

# Создание главного окна
root = tk.Tk()
root.geometry("700x600")
root.title("Пример текстового вывода")

y = 20
for post in posts:
    label_title = tk.Label(root, text=post['title'])
    label_title.pack(side=tk.TOP, fill=tk.X, pady=y)

    # Создаем список из поста
    text = post['body'].split()
    z = []
    num = 0
    # В цикле каждое 5 слово переносим на новую строку
    for i in text:
        z.append(i)
        num += 1
        if num % 5 == 0:
            z.append('\n')
    result = ' '.join(z)

    label_body = tk.Label(root, text=result)
    label_body.pack(side=tk.TOP, fill=tk.X, pady=y)



# Запуск главного цикла обработки событий
root.mainloop()


