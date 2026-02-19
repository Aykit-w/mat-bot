import telebot
import sympy as sp

API_TOKEN = '8557093140:AAFxPP7WqLTv89oOg5NgRYVf-pzJE7T4G9Y'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне математическое уравнение, и я его решу.")

@bot.message_handler(func=lambda message: True)
def solve_equation(message):
    equation = message.text
    try:
        lhs, rhs = equation.split('=')
        lhs = sp.sympify(lhs)
        rhs = sp.sympify(rhs)

        simplified_eq = sp.simplify(lhs - rhs)

        x = sp.symbols('x')
        solution = sp.solve(simplified_eq, x)

        if solution:
            response = f"Упрощенное уравнение: {simplified_eq}\nРешение уравнения {equation}:\n{x} = {solution}"
        else:
            response = f"Уравнение {equation} не имеет решений."
    except Exception as e:
        response = f"Ошибка: вы ввели уравнение неправильно"

    bot.reply_to(message, response)

bot.polling()