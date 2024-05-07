import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Функция получения информации с сайта
def write_cmc_top(path):
    # считываем данные с сайта
    webd = webdriver.Chrome()
    webd.get(path)
    pause_time = 3
    counter = 14
    while counter != 0:
        webd.execute_script("window.scrollBy(0,window.innerHeight)")
        time.sleep(pause_time)
        counter -= 1
    html_text = webd.page_source
    parser = BeautifulSoup(html_text, "html.parser")
    # выбираем наименование и капитализацию
    list_of_values = parser.find_all('span', {'class': 'sc-7bc56c81-1 bCdPBp'})
    list_of_names = parser.find_all('p', {'class': 'sc-4984dd93-0 kKpPOn'})
    #  первые 12 названий не входят в таблицу
    del list_of_names[:12]

    summa = 0                         #  общая сумма капитализации по всем прочитанным строкам
    result = []                        #  результирующий файл
    pat = r'[^$]\S+'                    # паттерн для выделения числа капитализации:
    # перебираем полученную информацию из таблицы
    for names, values in zip(list_of_names, list_of_values):
        matched = re.search(pat, values.text)
        val_res = matched.group()
        val = int(val_res.replace(',', ''))
        summa += val
        result.append(({
            'Name': names.text,
            'MC': val_res,
            'MP': val,
        }))


     # расчет и занесение процента

    for item in result:
        m = item['MP']
        percent = round((m / summa) * 100)
        item['MP'] = (f'{percent}%')
    # формируем имя файла
    now = datetime.now()
    formatted_date = f"{now.hour:02d}.{now.minute:02d} {now.day:02d}.{now.month:02d}.{now.year}"
    # запись результата в файл
    with open(f'{formatted_date}.csv', 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, delimiter=' ', fieldnames=['Name', 'MC', 'MP'])
        writer.writeheader()
        writer.writerows(result)
# Вызывыем функцию
write_cmc_top('https://coinmarketcap.com')