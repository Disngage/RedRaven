import time, os, json
from colorama import Fore, Style, init

formatted_date = time.strftime("%d.%m.%Y")
formatted_time = time.strftime("%H:%M")

init()


def bmi(weight, height):  # ИМТ
    height_in_meters = height / 100
    bmi_value = weight / (height_in_meters**2)

    categories = {
        (0, 18.5): Fore.MAGENTA + "Недостаточный" + Style.RESET_ALL,
        (18.5, 25.0): Fore.GREEN + "Нормальный" + Style.RESET_ALL,
        (25.0, 30.0): Fore.YELLOW + "Избыточный" + Style.RESET_ALL,
        (30.0, float("inf")): Fore.RED + "Ожирение" + Style.RESET_ALL,
    }

    for (lower, upper), category in categories.items():
        if lower < bmi_value <= upper:
            return category


def bmr(sex, age, weight, height):  #  Расчёт базального метаболизма (BMR)
    match sex:
        case 0:
            return (10 * weight) + (6.25 * height) - (5 * age) + 5  # men
        case 1:
            return (10 * weight) + (6.25 * height) - (5 * age) - 161  # women


def pal(activity):  # Учёт физической активности (Physical Activity Level)
    match activity:
        case 0:
            return 1.2  # Сидячий образ жизни (мало или нет упражнений)
        case 1:
            return 1.375  # Лёгкая активность (лёгкие упражнения 1–3 дня в неделю)
        case 2:
            return 1.55  # Умеренная активность (умеренные упражнения 3–5 дней в неделю)
        case 3:
            return 1.725  # Высокая активность (тяжёлые упражнения 6–7 дней в неделю)
        case 4:
            return 1.9  #  Очень высокая активность (тяжёлая физическая работа или тренировки 2 раза в день)


def perfection_weight(sex, height):  #  Идеальный вес по формуле Купера
    match sex:
        case 0:
            return height - 100 - (height - 150) / 4  # men
        case 1:
            return height - 100 - (height - 150) / 2  # women


def road_to_perfection(func):
    difference = weight - func
    if difference > 0:
        output = f"Для идеального веса необходимо: - {difference} кг"
    elif difference < 0:
        output = f"Для идеального веса необходимо: + {-difference} кг"
    else:
        output = "Невероятно! Вы уже имеете идеальный вес!"
    return output


def clear_console():
    # Проверяем операционную систему
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Linux/MacOS
        os.system("clear")


while True:
    sex = (
        input("Укажите Ваш пол мужчина / женщина (в формате: m / w): ").strip().upper()
    )
    if sex == "M":
        sex = 0
        break
    elif sex == "W":
        sex = 1
        break
    else:
        print("Некорректный ввод. Пожалуйста, введите m или w.")

age = int(input("Укажите Ваш возраст: "))
weight = float(input("Укажите Ваш вес в килограммах: "))
height = float(input("Укажите Ваш рост в сантиметрах: "))

while True:
    try:
        activity = int(
            input(
                """\nНеобходимо указать уровень Вашей физической активности: 
\t0 - Cидячий образ жизни (мало или нет упражнений)
\t1 - Лёгкая активность (лёгкие упражнения 1–3 дня в неделю)
\t2 - Умеренная активность (умеренные упражнения 3–5 дней в неделю)
\t3 - Высокая активность (тяжёлые упражнения 6–7 дней в неделю)
\t4 - Очень высокая активность (тяжёлая физическая работа или тренировки 2 раза в день)
\tВведите цифру: """
            )
        )
        if 0 <= activity < 5:
            break
    except ValueError:
        print(Fore.RED + "Ошибка. Значение не является числом" + Style.RESET_ALL)
    finally:
        print("Некорректный ввод. Пожалуйста, введите цифру от 0 до 4.")

clear_console()

result = bmi(weight, height)
bmi_value = weight / ((height / 100) ** 2)

print(
    f"""\nСегодня - {formatted_date}г., {formatted_time}
Индекс массы тела: {bmi_value:.2f} ({result})
Базальный метаболизм: {bmr(sex, age, weight, height)}
Общий расход ккал/день: {(bmr(sex, age, weight, height) * pal(activity)):.2f}
Идеальный вес для Вашего роста составляет: {perfection_weight(sex, height)} кг
{Fore.BLUE + road_to_perfection(perfection_weight(sex, height)) + Style.RESET_ALL}"""
)

path = "C:/Users/rkayd/OneDrive/Рабочий стол/MyBMI.txt"
line = 0

try:
    with open(path, "r", encoding="utf-8") as file:
        line = len(file.readlines())
except FileNotFoundError as error:
    print(Fore.RED + f"Файл не найден или отсутствует" + Style.RESET_ALL)
finally:
    with open(path, "a", encoding="utf-8") as file:
        file.writelines(
            f"№{line + 1} Дата: {formatted_date}, Время: {formatted_time}, ИМТ: {bmi_value:.2f}, Вес: {weight} кг, Цель: {road_to_perfection(perfection_weight(sex, height))[-9:]}\n"
        )
