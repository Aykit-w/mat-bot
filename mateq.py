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

        discriminant_info = ""
        if sp.degree(simplified_eq, x) == 2:
            a, b, c = sp.poly(simplified_eq, x).all_coeffs()
            D = b**2 - 4*a*c
            discriminant_info = f"Дискриминант D = {D}\n"
            if D > 0:
                discriminant_info += "Уравнение имеет два различных корня.\n"
            elif D == 0:
                discriminant_info += "Уравнение имеет один корень.\n"
            else:
                discriminant_info += "Уравнение не имеет корней.\n"

        if solution:
            response = f"Упрощенное уравнение: {simplified_eq}\n{discriminant_info}Решение уравнения {equation}:\n{x} = {solution}"
        else:
            response = f"Уравнение {equation} не имеет решений."
    except Exception as e:
        response = f"Ошибка: вы ввели уравнение неправильно"

    bot.reply_to(message, response)

bot.polling()