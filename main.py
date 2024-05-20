import telebot
import sqlite3 # Підключення бібліотек
from telebot import types
import datetime


token_bot = '6718419367:AAEPYpR16FdsGkv3fhQQR19k9-T4oaFllMI' # Токен бота та підключення до бази даних
admin_chat_id = '873491826'
admin_authenticated = False  # Додаємо змінну для визначення статусу аутентифікації

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        car_model TEXT,
        part_name TEXT,
        price REAL,
        appointment_date TEXT,
        appointment_time TEXT
    )
''')
conn.commit()
conn.close()

conn = sqlite3.connect('orders.db') # таблиці для користувачів у базі даних:
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        phone TEXT
    )
''')

conn.commit()
conn.close()

def create_reviews_table():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            review_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            review_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Виклик функції створення таблиці при запуску програми
create_reviews_table()


bot = telebot.TeleBot(token_bot)


catalog = {
    "Daewoo Lanos": [
        {"name": "Глушник", "photo_url": "https://images.prom.ua/371231445_glushitel-lanos-zaporozhe.jpg", "price": 214},
        {"name": "Диск гальма перід", "photo_url": "https://a.allegroimg.com/original/11bf97/e97c99d24b929d097e0807a48045/TARCZA-HAM-OPEL-PRZOD-ASTRA", "price": 1008 },
        {"name": "Литой диск", "photo_url": "https://krainashin.com/image/cache/tk/16389.109.1000x1000-400x400.jpg", "price": 2550},
        {"name": "Комплект зчеплення", "photo_url": "https://demex.com.ua/imgs/000/107/938/520791_460x330.jpg", "price": 3441 },
        {"name": "Акумулятор Bosch 6 CT-77-R S5 Silver Plus", "photo_url": "https://eshop.elit.ua/imgbank/rgcmedia/o/019/096/48bf56dea2394d66a863ff55e4a2e19a.jpg", "price": 4685},
        {"name": "Паливний фільтр", "photo_url": "https://content1.rozetka.com.ua/goods/images/big_tile/10733684.jpg", "price": 193 },
        {"name": "Каталізатор", "photo_url": "https://images.prom.ua/4069724123_katalizator-daewoo-lanos.jpg", "price": 6394},
        {"name": "Прокладка ГБЦ", "photo_url": "https://images2.exist.ua/media/images/products/2019/09/7102877_15591924_nf8tmne.jpg", "price": 550 },
    ],
    "Audi A3": [
        {"name": "Глушник", "photo_url": "https://helpauto.ua/uploads//products/48/73/00/01/70/48730001703255wT.jpg", "price": 3024},
        {"name": "Амортизатор передній", "photo_url": "https://images.prom.ua/4461827479_amortizator-perednij-audi.jpg", "price": 1912},
        {"name": "Комплект зчеплення", "photo_url": "https://automira.com.ua/Images/Product/359914812/1.jpg", "price": 7553},
        {"name": "Патрубок інтеркулера", "photo_url": "https://autobonus.com.ua/imgs/jp-group/1117702800_460x330.jpg", "price": 893},
        {"name": "Комплект важелів передньої підвіски Raiso", "photo_url": "https://images.prom.ua/4000426685_komplekt-rychagov-perednej.jpg", "price": 8925},
        {"name": "Двигун 8V", "photo_url": "https://a.allegroimg.com/s690/117b9a/f7324d544365a33ba3d9b980b66a/Silnik-AUDI-A3-8V-VW-GOLF-VII-LEON-ST-2-0-TDI-150KM-CRB-POMIAR-KOMPRESJI", "price": 70000},
    ],
    "Chrysler 300M": [
        {"name": "Коробка передач 3.5 v6", "photo_url": "https://a.allegroimg.com/s500/1180b6/d768839a4942bcc27651941c533d/SKRZYNIA-BIEGOW-CHRYSLER-300M-3-5-V6", "price": 12121},
        {"name": "Комплект зчеплення", "photo_url": "https://img.autoklad.ua/imgbank/Image/Article_pic/group_pic/LUK.jpg", "price": 25769},
        {"name": "Поліклиновий ремінь", "photo_url": "https://leoparts.com.ua/imgs/contitech/6pk1570_460x330.jpg", "price": 465},
        {"name": "Стійка стабілізатора", "photo_url": "https://images.prom.ua/4476326569_w200_h200_tyaga-stojkaya-stabilizatora.jpg", "price": 483},
        {"name": "Болт головки циліндра", "photo_url": "https://media.renix.ua/139/139_81050400.jpg", "price": 1592},
        {"name": "Коромисло", "photo_url": "https://leoparts.com.ua/imgs/bga/ra0901_460x330.jpg", "price": 319},
        {"name": "Паливний насос", "photo_url": "https://a.allegroimg.com/s600/114520/a06c8e9c460db7285586a619dee8/POMPA-PALIWA-CHRYSLER-300M-3-5-V6", "price": 1635},
        {"name": "Прокладка турбіни 3.5", "photo_url": "https://yii.dbroker.com.ua/img/mini/280x280/10/00100662501255.jpg?t=1699537809", "price": 315},
        {"name": "Комплект ступиці", "photo_url": "https://yii.dbroker.com.ua/img/mini/280x280/4693/46930171103255.jpg?t=1699537912", "price": 2481},
    ],
    "Ford Sierra": [
        {"name": "Амортизатор задній", "photo_url": "https://images.prom.ua/4749709063_w200_h200_stojkaamortizator-zadnij-saks.jpg", "price": 1275},
        {"name": "Граната", "photo_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcSRJ9W0vE-CmsQk2R6dokjCzuxt0WRvy8eRnIUB0GmUPeE0OcTkU9eojWInMXN67wGHVN4wZKjrmKUsA5N87C1LscyuTsSL40kz6WK52F_wqyhYNY565j_uHJ3_VbpsFv-xijyVfp4&usqp=CAc", "price": 1008},
        {"name": "Підкрилки 2 шт.", "photo_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSTvfn7HFpZ9tP5sJ-y_iLcQl8i1WkKFIstSOmhC_j-MsoTOy3EbU7KPe-A0u7_NBWKDe-kqfsYtvCp99D0Hi3WXge8flm-7tkZ48EqXoGFKOaxv2G546am3qe8fDTZH9rbbY-Mtd8&usqp=CAc", "price": 700},
        {"name": "Резонатор", "photo_url": "https://encrypted-tbn0.gstatic.com/shopping?q=tbn:ANd9GcRbOabY0RXu1aob3pqE0hQ6KzYHxF41Puje0P2jzYFyaaeNvKmHQaz8C5QLy4jhksCw5JLkmVf-SQAxZFNqnbxPKC6L1TQlLwU_2c75kFcMu8deAlxVX_KXNeGYLDrE3F1Vmg3xFQ&usqp=CAc", "price": 2288},
        {"name": "Комплект прокладок", "photo_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcRxHkFrxDSBXnwXZSHiaegzXY-ULMq9mVjEq3CfFojeNqeRx_mBWlJzLaGtyvKvRaj61A5omxpvcvuzLLs_tBLuQJBaOBufCYSAynEYQzfFJqDUAQCFyUBuC5JoBQ47GTsl17zciLw&usqp=CAc", "price": 579},
        {"name": "Підлокітник", "photo_url": "https://encrypted-tbn2.gstatic.com/shopping?q=tbn:ANd9GcSiC_bROVuihcm4uZqMQun66eUFqFEmC6mhOHXiN0IKnQ4SRszOoTskZeTyaeI1EZ0IZvgRBXwYyynYd1dVa6-3FX8jbOXHMXGws7jBXSLoAPUU9oE1FzbBCnZeeZMZJ6SVV1tFDQ&usqp=CAc", "price": 1050},
        {"name": "Поршні", "photo_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcS-xx2WdhsqHG6PNOsGRxynq_BUsyt7hB_g4VciExEw3m8m7N8Grkd6t9O4xdJ9c7LMyUj0vtrq6TXeUPPkFdpfGXWD8-CTSU6hAhBugCpb5jzzs98TGapdtA&usqp=CAc", "price": 5080},
        {"name": "Двигун 2.0", "photo_url": "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcTm3vcIfxhoEuPjGH7ifXvrTTH6t-TcwCpFoADz8dqsB_DH6hdnNOj6obGhkaH_nbSfNruglzgVbQTIdLNu7ui9D6nVgNy4bA&usqp=CAE", "price": 16920},
    ],
    "Audi 100": [
        {"name": "Корпус вентиляторів", "photo_url": "https://a.allegroimg.com/s400/1ed81d/738c8f28424b9b4c9702655ef75b/Obudowa-wentylatorow-VW-AUDI-SEAT-SKODA-2-0TDI", "price": 1991},
        {"name": "Диски колодки зад", "photo_url": "https://globalcars-images.com.ua/photos/medium/6141mk42b.jpg", "price": 1600},
        {"name": "Ступиця перед ліва", "photo_url": "https://cdn.riastatic.com/photosnew/general/adv_photos/stupytsa_na_audy_110_a_6__31283428m.jpg", "price": 9400},
        {"name": "Розподільчий вал", "photo_url": "https://i.avto.pro/img/pi/AMC/647012/amc-647012-bp1c65cb.jpg", "price": 2240},
        {"name": "Впускна труба вихлопної системи", "photo_url": "https://glushniki.com.ua/image/cache/catalog/vyhlop-imgs/01-203-image-456x456.png", "price": 1878},
        {"name": "Масляний фільтр", "photo_url": "https://images.prom.ua/4614811730_w640_h640_knecht-oc47-maslyanyj.jpg", "price": 500},
    ],
    "ВАЗ 2115 Samara": [
        {"name": "Трос зчеплення", "photo_url": "https://images.prom.ua/483866690_w640_h640_tros-stsepleniya-vaz.jpg", "price": 152},
        {"name": "Перемикач підрульовий", "photo_url": "https://avtogrand.com.ua/image/cache/catalog/1c/catalog/import_files/d7/cd63ea85-b712-11eb-8122-005056a3722f-1200x800.jpeg", "price": 110},
        {"name": "Радіатор охолодження", "photo_url": "https://images.prom.ua/4794023797_w640_h640_radiator-ohlazhdeniya-vaz.jpg", "price": 989},
        {"name": "Маховик", "photo_url": "https://images.prom.ua/3743344350_w200_h200_mahovik-vaz-2108.jpg", "price": 2100},
        {"name": "Пружина підвіски", "photo_url": "https://images2.exist.ua/media/images/products/4186/20057988/1058197.jpg", "price": 1191},
        {"name": "Шрус", "photo_url": "https://images2.exist.ua/media/images/products/2020/11/45__VX5cNv8.jpg", "price": 539},
        {"name": "Прокладка ГБЦ,комплект", "photo_url": "https://images2.exist.ua/media/images/products/2019/09/7102877_15591924_nf8tmne.jpg", "price": 1380},
    ],
}

user_cart = {}
user_state = {}

def add_user_info(user_id, name, surname, phone):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Перевіряємо, чи користувач вже існує
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Користувач вже існує, оновлюємо інформацію
        cursor.execute('UPDATE users SET name=?, surname=?, phone=? WHERE user_id=?',
                       (name, surname, phone, user_id))
    else:
        # Користувача не існує, додаємо нового користувача
        cursor.execute('INSERT INTO users (user_id, name, surname, phone) VALUES (?, ?, ?, ?)',
                       (user_id, name, surname, phone))

    conn.commit()
    conn.close()
def add_order(user_id, car_model, part_name, price, appointment_date):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO orders (user_id, car_model, part_name, price, appointment_date) VALUES (?, ?, ?, ?, ?)',
                   (user_id, car_model, part_name, price, appointment_date))

    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text == "Назад" and user_state.get(message.chat.id, {}).get("state") == "catalog")
def handle_catalog_back(message):
    handle_main_menu(message)


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item = types.KeyboardButton("Каталог автомобілів")
    cart_button = types.KeyboardButton("Кошик")
    appointment_button = types.KeyboardButton("Запис на технічне обслуговування")
    review_button = types.KeyboardButton("Залишити відгук")
    view_reviews_button = types.KeyboardButton("Переглянути відгуки")
    markup.row(item)
    markup.row(cart_button)
    markup.row(appointment_button)
    markup.row(review_button)
    markup.row(view_reviews_button)

    user_state[user_id] = {}
    bot.send_message(user_id, "Ласкаво просимо до магазину 'Сто СаРАЙ'!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Переглянути відгуки")
def handle_view_reviews(message):
    user_id = message.chat.id

    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT review_text FROM reviews')
    reviews = cursor.fetchall()
    conn.close()

    if reviews:
        review_text = "Відгуки користувачів:\n\n"
        for review in reviews:
            review_text += f"- {review[0]}\n"
        bot.send_message(user_id, review_text)
    else:
        bot.send_message(user_id, "Наразі немає відгуків.")

@bot.message_handler(func=lambda message: message.text == "Залишити відгук")
def handle_leave_review(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Будь ласка, залиште ваш відгук:")
    bot.register_next_step_handler(message, save_review)

def save_review(message):
    user_id = message.chat.id
    review_text = message.text

    # Збереження відгуку у базу даних
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (user_id, review_text) VALUES (?, ?)', (user_id, review_text))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Дякуємо за ваш відгук!")


@bot.message_handler(commands=['admin_login'])
def handle_admin_login(message):
    global admin_authenticated
    if str(message.chat.id) == admin_chat_id:
        admin_authenticated = True
        bot.send_message(message.chat.id, "Ви успішно увійшли в адмін-панель.")
    else:
        bot.send_message(message.chat.id, "Ви не маєте прав для входу в адмін-панель.")

@bot.message_handler(func=lambda message: message.text == "Головне меню")
def handle_main_menu(message):
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Каталог автомобілів")
    cart_button = types.KeyboardButton("Кошик")
    appointment_button = types.KeyboardButton("Запис на технічне обслуговування")
    markup.row(item)
    markup.row(cart_button)
    markup.row(appointment_button)
    bot.send_message(user_id, "Ласкаво просимо до магазину 'Сто СаРАЙ'!", reply_markup=markup)

    # Очищаємо стан користувача
    user_state[user_id] = {}

@bot.message_handler(commands=['admin_logout'])
def handle_admin_logout(message):
    global admin_authenticated
    if str(message.chat.id) == admin_chat_id:
        admin_authenticated = False
        bot.send_message(message.chat.id, "Ви успішно вийшли з адмін-панелі.")
    else:
        bot.send_message(message.chat.id, "Ви не маєте прав для виходу з адмін-панелі.")

@bot.message_handler(commands=['check_orders'])
def handle_check_orders(message):
    global admin_authenticated
    if admin_authenticated:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT orders.order_id, orders.car_model, orders.part_name, orders.price, users.name, users.surname, users.phone
            FROM orders
            JOIN users ON orders.user_id = users.user_id
        ''')
        orders = cursor.fetchall()
        conn.close()

        if orders:
            order_chunks = [orders[i:i + 7] for i in range(0, len(orders), 7)]
            for chunk in order_chunks:
                order_text = "Список замовлень:\n"
                for order in chunk:
                    order_text += f"ID: {order[0]}, Авто: {order[1]}, Деталь: {order[2]}, Ціна: {order[3]} грн\n"
                    order_text += f"Користувач: {order[4]} {order[5]}, Телефон: {order[6]}\n\n"
                bot.send_message(message.chat.id, order_text)
        else:
            bot.send_message(message.chat.id, "Замовлень поки немає.")
    else:
        bot.send_message(message.chat.id, "Для перегляду замовлень ви повинні увійти в адмін-панель.")

@bot.message_handler(commands=['view_orders'])
def handle_view_orders(message):
    if str(message.chat.id) == admin_chat_id:
        conn = sqlite3.connect('orders.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT o.order_id, o.car_model, o.part_name, o.price, u.name, u.surname, u.phone
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
        ''')
        orders = cursor.fetchall()
        conn.close()

        if orders:
            order_text = "Список замовлень:\n"
            for order in orders:
                order_text += f"ID: {order[0]}, Car: {order[1]}, Part: {order[2]}, Price: {order[3]} грн\n"
                order_text += f"   User: {order[4]} {order[5]}, Phone: {order[6]}\n"
            bot.send_message(message.chat.id, order_text)
        else:
            bot.send_message(message.chat.id, "Замовлень поки немає.")
    else:
        bot.send_message(message.chat.id, "Для перегляду замовлень ви повинні увійти в адмін-панель.")


@bot.message_handler(func=lambda message: message.text == "Каталог автомобілів" or message.text == "Назад") # обробник переходу до каталога
def handle_catalog(message):
    user_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for car_model in catalog.keys():
        item = types.KeyboardButton(car_model)
        markup.add(item)
    if user_state.get(user_id, {}).get("state") != "search":
        item = types.KeyboardButton("Пошук")
        markup.add(item)
    cart_button = types.KeyboardButton("Кошик")
    markup.add(cart_button)
    item = types.KeyboardButton("Назад")
    markup.add(item)
    user_state[user_id]["state"] = "catalog"
    bot.send_message(user_id, "Оберіть автомобіль:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in catalog.keys()) # обробник вибора автомобіля
def handle_car_selection(message):
    user_id = message.chat.id
    car_model = message.text
    if car_model in catalog:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for part_info in catalog[car_model]:
            part_name = part_info["name"]
            item = types.KeyboardButton(part_name)
            buy_button = types.KeyboardButton(f"Купити {part_name}")
            markup.row(item, buy_button)

        cart_button = types.KeyboardButton("Кошик")
        markup.row(cart_button)
        item = types.KeyboardButton("Назад")
        markup.add(item)

        user_state[user_id]["state"] = "car_selection"
        user_state[user_id]["car_model"] = car_model
        bot.send_message(user_id, f"Запчастини для {car_model}:", reply_markup=markup)


def handle_appointment_name(message):
    user_id = message.chat.id
    user_state[user_id]["name"] = message.text
    bot.send_message(user_id, "Тепер введіть своє прізвище:")
    bot.register_next_step_handler(message, handle_appointment_surname)

def handle_appointment_surname(message):
    user_id = message.chat.id
    user_state[user_id]["surname"] = message.text
    bot.send_message(user_id, "Введіть свій номер телефону:")
    bot.register_next_step_handler(message, handle_appointment_phone)

def handle_appointment_phone(message):
    user_id = message.chat.id
    user_state[user_id]["phone"] = message.text

    # Просимо користувача обрати час та дату прийому
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    available_dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(3)]
    for date in available_dates:
        item = types.KeyboardButton(date.strftime("%Y-%m-%d"))
        markup.row(item)

    bot.send_message(user_id, "Оберіть дату прийому з календаря:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_appointment_date)

def handle_appointment_date(message):
    user_id = message.chat.id
    appointment_date = message.text

    # Тут ви можете використовувати додаткову логіку для перевірки доступності обраної дати
    # Якщо дата зайнята, можете повідомити користувача та попросити обрати іншу

    # Зберігаємо інформацію про обрану дату
    user_state[user_id]["appointment_date"] = appointment_date

    # Просимо користувача обрати годину
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Додайте сюди години, які доступні для обраної дати
    available_hours = ["10:00", "12:00", "14:00", "16:00"]
    for hour in available_hours:
        item = types.KeyboardButton(hour)
        markup.row(item)

    bot.send_message(user_id, "Оберіть годину прийому:", reply_markup=markup)
    bot.register_next_step_handler(message, handle_appointment_time)

@bot.message_handler(func=lambda message: message.text == "Запис на технічне обслуговування")
def handle_appointment_start(message):
    user_id = message.chat.id
    bot.send_message(user_id, "Для запису на технічне обслуговування введіть своє ім'я:")
    bot.register_next_step_handler(message, handle_appointment_name)


@bot.message_handler(func=lambda message: message.text in [part["name"] for part in catalog.get( #обробник вибора запчастин
    user_state.get(message.chat.id, {}).get("car_model", ""), [])])
def handle_part_selection(message):
    user_id = message.chat.id
    part_name = message.text

    # Перевіряємо, чи існує ключ 'car_model' у user_state
    car_model = user_state.get(user_id, {}).get("car_model", "")

    # Перевіряємо, чи існує частина в каталозі для вибраного автомобіля
    if car_model and car_model in catalog and any(part["name"] == part_name for part in catalog[car_model]):
        # Знаходимо відповідну інформацію про запчастину
        part_info = next((part for part in catalog[car_model] if part["name"] == part_name), None)

        if part_info:
            # Надсилаємо фото разом із підписом
            bot.send_photo(user_id, photo=part_info["photo_url"],
                           caption=f"{part_name}\nЦіна: {part_info['price']} грн")
        else:
            bot.send_message(user_id, "Помилка: Запчастина не знайдена в каталозі.")
    else:
        bot.send_message(user_id, "Помилка: Не обрано автомобіль або частина не знайдена в каталозі.")


@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "appointment_time")
def handle_appointment_time(message):
    user_id = message.chat.id
    appointment_time = message.text

    # Перевірка доступності обраної години
    if not is_hour_available(user_state[user_id]["appointment_date"], appointment_time):
        bot.send_message(user_id, "Обрана година вже зайнята. Оберіть іншу годину або поверніться до вибору дати.")
        # Просимо користувача обрати дату прийому знову
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        available_dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(3)]
        for date in available_dates:
            item = types.KeyboardButton(date.strftime("%Y-%m-%d"))
            markup.row(item)

        bot.send_message(user_id, "Оберіть дату прийому з календаря:", reply_markup=markup)
        bot.register_next_step_handler(message, handle_appointment_date)
        return

    # Зберігаємо інформацію про обрану годину
    user_state[user_id]["appointment_time"] = appointment_time

    # Збереження запису в базі даних
    add_appointment_to_database(user_id, user_state[user_id]["appointment_date"], appointment_time)

    # Відправлення повідомлення про успішний запис
    bot.send_message(user_id, f"Ви успішно записані на технічне обслуговування.Дякую!Очікуємо за адресом Олеся Гончара 80/10 {user_state[user_id]['appointment_date']} о {appointment_time}.")

    # Кнопка "Повернутися до головного меню"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back_to_menu_button = types.KeyboardButton("Повернутися до головного меню")
    markup.row(back_to_menu_button)
    bot.send_message(user_id, "Оберіть годину прийому:", reply_markup=markup)

    # Очищення стану користувача
    user_state[user_id] = {}

@bot.message_handler(func=lambda message: message.text == "Повернутися до головного меню")
def handle_back_to_menu(message):
    user_id = message.chat.id
    handle_main_menu(message)


@bot.message_handler(func=lambda message: message.text.startswith("Купити")) #обробник команди купити
def handle_buy(message):
    user_id = message.chat.id
    item_to_buy = message.text.split("Купити ")[-1]

    if user_id not in user_cart:
        user_cart[user_id] = []
    user_cart[user_id].append(item_to_buy)
    bot.send_message(user_id, f"{item_to_buy} додана до кошика.")

@bot.message_handler(commands=['cart']) #команда cart
def handle_cart(message):
    user_id = message.chat.id
    if user_id in user_cart and user_cart[user_id]:
        cart_contents = "\n".join(user_cart[user_id])
        bot.send_message(user_id, f"Ваш кошик містить:\n{cart_contents}")
    else:
        bot.send_message(user_id, "Ваш кошик пустий.")

@bot.message_handler(func=lambda message: message.text == "Кошик") #обробка кошика
def handle_view_cart(message):
    user_id = message.chat.id
    if user_id in user_cart and user_cart[user_id]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for item in user_cart[user_id]:
            item_button = types.KeyboardButton(item)
            markup.add(item_button)
        checkout_button = types.KeyboardButton("Оформити замовлення")
        markup.add(checkout_button)
        back_button = types.KeyboardButton("Назад")
        markup.add(back_button)
        bot.send_message(user_id, "Ваш кошик містить наступні товари:", reply_markup=markup)
    else:
        bot.send_message(user_id, "Ваш кошик пустий.")


@bot.message_handler(commands=['view_appointments'])
def handle_view_appointments(message):
    user_id = message.chat.id
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Отримуємо поточну дату
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Отримуємо записи на сьогодні
    cursor.execute('''
        SELECT users.name, users.surname, users.phone, orders.appointment_date, orders.appointment_time
        FROM orders
        JOIN users ON orders.user_id = users.user_id
        WHERE orders.appointment_date LIKE ?
    ''', (f'{current_date}%',))

    appointments = cursor.fetchall()
    conn.close()

    if appointments:
        appointment_text = "Записи на технічне обслуговування сьогодні:\n"
        for appointment in appointments:
            appointment_text += f"Ім'я: {appointment[0]}, Прізвище: {appointment[1]}, Телефон: {appointment[2]}, Дата і час: {appointment[3]} {appointment[4]}\n"
        bot.send_message(user_id, appointment_text)
    else:
        bot.send_message(user_id, "На сьогодні записів на технічне обслуговування немає.")

@bot.message_handler(func=lambda message: message.text == "Оформити замовлення") #оформити замовлення
def handle_checkout(message):
    user_id = message.chat.id
    if user_id in user_cart and user_cart[user_id]:
        user_state[user_id]["state"] = "checkout"
        bot.send_message(user_id, "Для оформлення замовлення введіть своє ім'я:")
    else:
        bot.send_message(user_id, "Ваш кошик пустий.")

@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "checkout") #обробка ім'я
def handle_checkout_name(message):
    user_id = message.chat.id
    if user_id not in user_state:
        user_state[user_id] = {}
    user_state[user_id]["name"] = message.text
    user_state[user_id]["state"] = "checkout_surname"
    bot.send_message(user_id, "Введіть своє прізвище:")

@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "checkout_surname") # обробка прізвища
def handle_checkout_surname(message):
    user_id = message.chat.id
    user_state[user_id]["surname"] = message.text
    user_state[user_id]["state"] = "checkout_phone"
    bot.send_message(user_id, "Введіть свій номер телефону:")

def is_hour_available(appointment_date, appointment_time):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Перевіряємо, чи існують записи на обрану дату та годину
    cursor.execute('SELECT COUNT(*) FROM orders WHERE appointment_date = ? AND appointment_time = ?', (appointment_date, appointment_time))
    count = cursor.fetchone()[0]

    conn.close()

    # Якщо записів немає, година доступна
    return count == 0

def add_appointment_to_database(user_id, appointment_date, appointment_time):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Додавання запису до бази даних
    cursor.execute('INSERT INTO orders (user_id, appointment_date, appointment_time) VALUES (?, ?, ?)',
                   (user_id, appointment_date, appointment_time))

    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: user_state.get(message.chat.id, {}).get("state") == "checkout_phone")
def handle_checkout_phone(message):
    user_id = message.chat.id
    user_state[user_id]["phone"] = message.text

    # Додаємо appointment_date до стану користувача
    user_state[user_id]["appointment_date"] = "your_appointment_date_value"

    # Отримуємо інформацію про товари в кошику
    cart_contents = user_cart[user_id]
    total_price = 0

    for item in cart_contents:
        for car_model, parts in catalog.items():
            for part_info in parts:
                if part_info["name"] == item:
                    # Оновлення виклику функції add_order
                    add_order(user_id, car_model, item, part_info["price"], user_state[user_id]["appointment_date"])
                    total_price += part_info["price"]

    # Зберігаємо інформацію про користувача у базу даних
    add_user_info(user_id, user_state[user_id]['name'], user_state[user_id]['surname'], user_state[user_id]['phone'])

    # Відправляємо повідомлення про замовлення
    order_text = f"Ваше замовлення:\n"
    for item in cart_contents:
        order_text += f"- {item}\n"
    order_text += f"Загальна вартість: {total_price} грн\n"
    order_text += f"Ім'я: {user_state[user_id]['name']}\n"
    order_text += f"Прізвище: {user_state[user_id]['surname']}\n"
    order_text += f"Номер телефону: {user_state[user_id]['phone']}\n"
    bot.send_message(user_id, order_text)

    # Додаємо повідомлення про очікування за адресою
    bot.send_message(user_id, "Дякуємо за ваш вибір. Очікуємо вас за адресою Олеся Гончара 80/10.")

    # Очищаємо кошик та стан користувача
    user_cart[user_id] = []
    user_state[user_id] = {}

    # Додаємо кнопку "Повернутися до головного меню"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Головне меню")
    markup.add(start_button)
    bot.send_message(user_id, "Дякуємо за замовлення!", reply_markup=markup)


if __name__ == "__main__": # запуск бота
    bot.polling()