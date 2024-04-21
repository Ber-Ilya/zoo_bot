from my_token import bot_token
import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont




bot = telebot.TeleBot(bot_token.get_token())

with open("quiz_structure.json", 'r') as f:
    quiz_structure = json.load(f)

quiz_structure = quiz_structure

def main_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Начать викторину", callback_data="start_quiz"),
        InlineKeyboardButton("Связаться с сотрудником", callback_data="contact_support"),
        InlineKeyboardButton("Получить обратную связь", callback_data="collect_feedback"),  # Проверьте это значение
        InlineKeyboardButton("Перезапустить викторину", callback_data="restart_quiz")
    )
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)


@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    main_menu(message)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if call.data == "start_quiz":
        start_quiz(call.message)
    elif call.data == "contact_support":
        contact_zoo_staff(call.message)
    elif call.data == "collect_feedback":
        collect_feedback(call.message)
    elif call.data == "restart_quiz":
        start_quiz(call.message, restart=True)
    bot.answer_callback_query(call.id)  # Важно отвечать на callback_query



@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if call.data == "start_quiz":
        start_quiz(call.message)
    elif call.data == "contact_support":
        contact_zoo_staff(call.message)
    elif call.data == "collect_feedback":  # Убедитесь, что используете правильный callback_data
        collect_feedback(call.message)
    elif call.data == "restart_quiz":
        start_quiz(call.message, restart=True)
    bot.answer_callback_query(call.id)  # Ответ на callback_query, чтобы убрать часы загрузки в клиенте


def start_quiz(message, restart=False):
    question_index = 0
    answers = []
    ask_question(message, question_index, answers)
    if restart:
        ask_question(message, question_index, answers)

def ask_question(message, question_index, answers):
    if question_index < len(quiz_structure['questions']):
        question = quiz_structure['questions'][question_index]
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for option in question['options']:
            markup.add(KeyboardButton(option[0]))  # Показываем только текст опции
        bot.send_message(message.chat.id, question['text'], reply_markup=markup)
        bot.register_next_step_handler(message, process_answer, question_index, answers)
    else:
        finalize_quiz(message, answers)

def process_answer(message, question_index, answers):
    user_response = message.text
    # Находим и сохраняем ответ пользователя
    question = quiz_structure['questions'][question_index]
    for option in question['options']:
        if option[0] == user_response:
            answers.append(option[1])  # Сохраняем тег ответа
            break
    question_index += 1
    ask_question(message, question_index, answers)

def finalize_quiz(message, answers):
    # Подсчет самого частого ответа
    answer_count = {tag: answers.count(tag) for tag in set(answers)}
    most_common_tag = max(answer_count, key=answer_count.get)
    result_message = quiz_structure['results'][most_common_tag]
    image_path = f"MZoo-logo-бircle-mono-white-preview.jpg"  # Путь к изображению для каждого тега
    try:
        photo = open(image_path, 'rb')  # Открываем изображение
        bot.send_photo(message.chat.id, photo, caption=result_message)
        photo.close()  # Закрываем файл после отправки
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Изображение не найдено, но вот ваш результат: " + result_message)
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отправке изображения: {str(e)}")



def contact_zoo_staff(message):
    bot.send_message(message.chat.id, "Вы можете связаться с нами по номеру: +123456789 или email@example.com")

def collect_feedback(message):
    bot.send_message(message.chat.id, "Пожалуйста, оставьте ваш отзыв здесь: http://example.com/feedback")


if __name__ == '__main__':
    bot.polling()
