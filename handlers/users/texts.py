def shartlar(name):
    text = f"""
<b>{name}, muddatli to' lov shartlari bilan tanishing.</b>

📁 <b><i>Kerak bo'ladigan xujjatlar</i></b>:
- 📗 Passport
- 💳 Plastik karta


Rasmiy ish joyi bo'lishi kerak. 
Plastik karta aktiv holatda, 
summa aylanmasi bo'lib turgan bo'lishi kerak.

<b>Oldindan to'lovsiz</b>. 
Boshlang'ich to'lov qilinsa, 
mahsulot tannarxidan ayriladi va qolgan qismi 
belgilangan muddatga bo'lib beriladi.
5 - 72 soat ichida bepul yetkazib 
berish xizmati amal giladi.  
    
    """
    return text


def shartlar_rus(name):
    text = f"""
<b>{name}, ознакомьтесь с условиями оплаты.</b>

📁 <b><i>Необходимые документы</i></b>:
- 📗 Паспорт
- 💳 Пластиковая карта


Должно быть официальное рабочее место.
Пластиковая карта должна быть активна,
сумма в ней должна быть оборотной.

<b>Без предоплаты</b>.
Если сделаете предоплату, сумма 
предоплаты минyсуется,остальное
предоставляется в рассрочку на определенный срок.
Бесплатная доставка в течение 5-72 часов
действует служба доставки.

"""
    return text


def active_card():
    text = """
Muddatli to'lovga olish uchun aktiv plastik
karta bo'lishi shart!

Plastik kartangiz mavjudmi?   
    """
    return text


def active_card_rus():
    text = """
Для покупки продуктов в рассрочку нужна 
активная пластиковая карта. 

У вас есть пластиковая карта?
    """
    return text


def afsus_card():
    text = """
😔 <b>Afsus!</b>

Plastik kartangiz bo'lmagani sababli,
siz muddatli to'lovga narsa xarid qila olmaysiz!  

Yaqinlaringiz orqali sotib olsangiz bo'ladi!
    """

    return text


def afsus_card_rus():
    text = f"""
😔 <b>Извините!</b>

Поскольку у вас нет пластиковой карты,
Вас нельзя покупать вещи в рассрочку!

Можно купить через родственников!

"""

    return text


def afsus_age():
    text = """
😔 <b>Afsus!</b>

Voyaga yetmaganiz sababli,
siz muddatli to'lovga narsa xarid qila olmaysiz!  

Yaqinlaringiz orqali sotib olsangiz bo'ladi!
    """

    return text


def afsus_age_rus():
    text = """
😔 <b>Извините!</b>

Поскольку вы несовершенолетний(я),
Вас нельзя покупать вещи в рассрочку!

Можно купить через родственников!
    """

    return text


def make_order():
    text = """
Buyurtma berish uchun pastdagi    
<b>"✅ Boshlash"</b> tugmasini bosing!
"""
    return text


def make_order_rus():
    text = """
Для заказа Нажмите 
<b>"✅ Старт"</b>!
    """
    return text


def phone():
    text = """
Telefon raqimingizni
+998 <b>XX XXX XX XX</b> formatida, 
yoki <b>"☎️ Raqam yuborish"</b> tugmasi orqali
yuboring!
    """
    return text


def phone_rus():
    text = """
Отправьте свой номер телефона в формате
+998 <b>XX XXX XX XX</b>, или нажмите на
кнопку <b>"☎️ Отправить номер"</b> ниже
    
    """
    return text


def product():
    txt = """
Siz qanday <b>telefon</b> yoki
mahsulotni sotib olmoqchisiz?

Kiriting ⬇️:
    """
    return txt


def product_rus():
    text = """
Какой тип <b>телефона</b> или
товар хотите купить ?

Введите ⬇️
    """
    return text


def send_success():
    text = """
😊 Sizning maʼlumotlaringiz menejerga <b>yetkazildi.</b>

Tez orada menejer siz bilan bogʻlanib, roʻyxatdan oʻtkazadi.
    """

    return text


def send_success_rus():
    text = """
😊 Ваша информация <b>доставлена менеджеру.</b>

В ближайшее время с вами свяжется менеджер для регистрации.
    """
    return text


def lid(name, phone, age, work_status, product, id):
    text = f"""
✅ <b>Yangi xabar!</b>

Sifatli lid:

<b>Ismi:</b> <a href='tg://user?id={id}'>{name}</a>
<b>Raqami:</b> {phone}
<b>Yoshi:</b> {age}
<b>Rasmiy ish joyi bormi?</b> {"Ha" if work_status else "Yo'q"}
<b>Tanlagan mahsulot:</b> {product}
"""

    return text


def frequent():
    text = """
❓ <b>1-Savol: Sizlarda yetkazib berish bormi?</b>

Javob: Bizda butun O'zbekiston bo'ylab tezkor bepul yetkazib berish xizmatimiz mavjud.

❓ <b>2-Savol: Rassrochka faqat Toshkent shahrigami yoki boshqa viloyatlarga ham bormi?</b>

Javob: Butun O'zbekiston bo'ylab halol muddatli to'lov amalga oshiramiz!

❓ <b>3-Savol: Qanday mahsulotlar bor?</b>

Javob: Bizda, smartfonlar, noutbuklar, smartwatchlar va boshqa gadjetlar mavjud.

❓ <b>4-savol: Qanday xujjatlar kerak?</b>

Javob: Pasport va aktiv plastik karta kerak xolos.
    """
    return text

def frequent_rus():
    text = '''
❓ <b>Вопрос 1. Есть ли у вас доставка?</b>

Ответ: У нас есть быстрая бесплатная доставка по Узбекистану.

❓ <b>Вопрос 2: Рассрочка доступна только в Ташкенте или в других регионах?</b>

Ответ: Мы осуществляем честную срочную оплату по всему Узбекистану!

❓ <b>Вопроc 3. Какие есть продукты?</b>

О: У нас есть смартфоны, ноутбуки, умные часы и другие гаджеты.

❓ <b>Вопрос 4: Какие нужны документы?</b>

Ответ: Все, что вам нужно, это паспорт и действующая пластиковая карта.  
    
    '''
    return text


def stats(name, sum, year, month):
    text = f"""
{name}-ismli manager {year}-yilning {month}-oyida
<b>{sum}</b> lid qabul qildi

"""

    return text


def language():
    text = """
Assalomu alaykum!
Tilni tanlang: 👇

--------------------

Здравствуйте!
Выберите язык: 👇
    """
    return text