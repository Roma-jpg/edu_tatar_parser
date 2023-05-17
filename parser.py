from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': '_ym_uid=1676574290233522544; _ym_d=1676574290; DNSID=a058e0e7b3a7d65874158d1d0eac55f5da0061bf; HLP=4855814%7C%242y%2410%24ghilzoCbi4w1A04ImC1yh.Llg85UEDw2JdtsPIyEeCzpYNN%2Fa3eky; _ym_isad=2; _ym_visorc=b',
        'Origin': 'https://edu.tatar.ru',
        'Referer': 'https://edu.tatar.ru/login/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
        'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }


def generate_schedule_link(year, month, day):
    dt = datetime(year, month, day)
    timestamp = int(dt.timestamp())
    link = f'https://edu.tatar.ru/user/diary/week?date={timestamp}'
    return link


def parse_diary_entries(soup):
    # Extract information about the student from the top panel
    student_name = soup.find('strong').text
    class_name = soup.find('span').text.split(',')[-1].strip()

    # Extract the date from the week selector
    week_selector = soup.find('div', {'class': 'week-selector'})
    month_name = week_selector.find('span').text

    # Extract the diary entries
    diary_entries = []
    day_entries = []
    day_counter = 1

    for entry in soup.find_all('tr'):
        if entry.find('td', {'class': 'tt-subj'}):
            subject = entry.find('td', {'class': 'tt-subj'}).text.strip()
            task = entry.find('td', {'class': 'tt-task'}).text.strip()
            mark = entry.find('td', {'class': 'tt-mark'}).text.strip()
            day_entries.append([subject, task, mark])

            if len(day_entries) == 9:
                day_label = f"Day {day_counter}"
                diary_entries.append([day_label] + day_entries)
                day_counter += 1
                day_entries = []

    # Add the last day's entries, if any
    if day_entries:
        day_label = f"Day {day_counter}"
        diary_entries.append([day_label] + day_entries)

    # Return the parsed diary entries
    return {'student_name': student_name, 'class_name': class_name, 'month_name': month_name,
            'diary_entries': diary_entries}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Простая HTML-страница</title>
    <style>
        /* Контейнер */
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }

        /* Заголовок */
        h1 {
            font-size: 3rem;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #333;
            text-align: center;
        }

        /* Текст */
        p {
            font-size: 1.25rem;
            margin-bottom: 2rem;
            color: #555;
            text-align: center;
        }

        /* Ссылка */
        a {
            color: #ff7300;
            text-decoration: none;
        }

        /* При наведении на ссылку */
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Привет, мир!</h1>
    <p>Это простая HTML-страница, отображаемая с помощью Flask.</p>
    <p>Нравится? <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Попробуй Flask</a> сегодня!</p>
</body>
</html>
        """

    if request.method == 'POST':
        year = 2023
        month = 3
        day = 30
        url = "https://edu.tatar.ru/login"
        url2 = generate_schedule_link(year, month, day)
        login = request.form.get('login')
        password = request.form.get('password')

        # check if login and password are provided in the request
        if not login or not password:
            return jsonify({'error': 'Login and password are required.'}), 400

        login_data = {"main_login2": login, "main_password2": password}
        try:
            with requests.Session() as s:
                s.post(url, data=login_data, headers=headers)
                diary_page = s.get(url2, headers=headers)
                soup = BeautifulSoup(diary_page.content, "html.parser")
        except Exception as ex:
            return str(ex)

        parsed_diary_entries = parse_diary_entries(soup)

        # Create a JSON response
        response = {
            'student_name': parsed_diary_entries['student_name'],
            'class_name': parsed_diary_entries['class_name'],
            'month_name': parsed_diary_entries['month_name'],
            'diary_entries': parsed_diary_entries['diary_entries']
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
