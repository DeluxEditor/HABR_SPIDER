"""
Демонстрация работы библиотеки парсера BeautifulSoup на примере получения страницы из сети

Для работы необходима библиотека BeautifulSoup.
Команда для устанкови - "pip.exe install bs4"
"""
import requests # подключить библиотеку для работы с HTTP
from bs4 import BeautifulSoup # подключить библиотеку Парсера

try:
    url = 'http://example.com/'   # URL адрес страницы
    html_doc = requests.get(url)  # получить HTML код страницы

    print("6. crawl - Попытка открыть страницу %s" % url)
    print("\n# Сырой HTML-код -------------------------------------------------------------------")
    print(html_doc.text)
    print("\n# ----------------------------------------------------------------------------------")

    # произвести разбор html-кода на элементы. Переменная soup содержит специальную структуры данных с вложенеми элементами
    soup = BeautifulSoup(html_doc.text, 'html.parser')

    # Найти на странице блоки со скриптами и стилями оформления ('script', 'style')
    listUnwantedItems = ['script', 'style']
    for script in soup.find_all(listUnwantedItems):
        script.decompose()  # очистить содержимое элемента и удалить его из дерева

    # Вывести отдельные элементы из объекта soup
    print("\n# Заголовок -----------------------------------------------------------------------")
    print(soup.title)
    print(soup.title.text)

    print("\n# Заголовок -----------------------------------------------------------------------")
    print(soup.text)


except Exception as e:
    print(e)
    print("  Не могу открыть %s" % html_doc)




# ----------------------------------------------------------------------------------------------------------------
