import requests, time
from bs4 import BeautifulSoup



def parser_crypto():
    url = 'https://www.binance.com/ru/markets/overview'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # css-xo7uk0 - зеленая
    # css-1kmb4l6 - белая
    # css-ny0kra - красная

    divs = soup.find_all('div', class_=['css-z7d2xh', 'css-xo7uk0', 'css-1kmb4l6', 'css-ny0kra', 'body2 items-center css-18yakpx', 'body3 line-clamp-1 truncate text-t-third css-vurnku'])
    # последние два новые css, не понятно почему они поменялись

    my_dict = dict()
    z = []
    for div in divs:
        # добавить символ: вверх, точка, вниз: ↑, •, ↓
        # Вообщем вариантам с css классами не работает, так что нужно придумать другой способ как парсить данные
        # и как отображать цены в зависимости от цены падает, стоит или поднимается
        tag = div.get_text()
        z.append(tag)

        if len(z) == 2:
            my_dict[z[0]] = z[1]
        else:
            continue
        z.clear()

    return my_dict

print(parser_crypto())

# Не запускается сервер
#while True:
#    parser_crypto()
#    time.sleep(5)


# css-xo7uk0 - зеленая
# css-1kmb4l6 - белая
# css-ny0kra - красная




