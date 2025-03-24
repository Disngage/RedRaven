import os
from random import sample
from string import ascii_letters, punctuation, digits


def get_password(len, num, char):
    """Генерация нового пароля"""
    return "".join(sample((ascii_letters + num + char), len))


def clear_console():
    # Проверяем операционную систему
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # Linux/MacOS
        os.system("clear")


length = int(input("Укажите длину пароля: "))

while True:
    numbers = input("Использовать в пароле цифры? (y/n): ").strip().lower()
    if numbers == "y":
        numbers = digits
        break
    elif numbers == "n":
        numbers = None
        break
    else:
        print("Некорректный ввод. Повторите попытку")


while True:
    chars = input("Использовать в пароле символы? (y/n):  ").strip().lower()
    if chars == "y":
        chars = punctuation
        break
    elif chars == "n":
        chars = None
        break
    else:
        print("Некорректный ввод. Повторите попытку")

key = get_password(length, numbers, chars)
place = input("Введите название площадки, для которой создан пароль: ")
site = input("Укажите адрес площадки(сайта): ")
path = "C:/Users/rkayd/OneDrive/Рабочий стол/MyKeywords.txt"
line = 0

try:
    with open(path, "r", encoding="utf-8") as file:
        line = len(file.readlines())
except FileNotFoundError as error:
    print(f"Файл не найден или остутствует")
finally:
    with open(path, "a", encoding="utf-8") as file:
        file.writelines(f"№{line + 1} {place} {key} {site}\n")

clear_console()

print(f"Ваш пароль сгенерирован: {key}")
