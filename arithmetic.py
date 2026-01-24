# Задача 1: Стоимость покупки
# Считываем стоимость каждого компонента (каждое с новой строки)
monitor = int(input())
unit = int(input())
keyboard = int(input())
mouse = int(input())

# Считаем стоимость одного комплекта
one_computer = monitor + unit + keyboard + mouse

# Нам нужно 3 таких компьютера
total_cost = one_computer * 3

# Выводим результат
print(total_cost)


# Задача 2: Значение функции f(x)
#Ввод чисел a и b
a = int(input())
b = int(input())

# Вычисление f(x) = (a+b)^3 = (a+b)*(a+b)*(a+b)
a_plus_b = a + b
a_plus_b_cubed = a_plus_b * a_plus_b * a_plus_b

# Вычисление b^2 = b*b
b_squared = b * b

# Вычисление всего выражения
result = 3 * a_plus_b_cubed + 275 * b_squared - 127 * a - 41

# Вывод результата
print(result)


# Задача 3: предыдущее и следующее число
# Считываем целое число
num = int(input())

# Вычисляем следующее и предыдущее числа
next_num = num + 1
prev_num = num - 1

# Выводим результат в требуемом формате
print(f"Следующее за числом {num} число: {next_num}")
print(f"Для числа {num} предыдущее число: {prev_num}")


# Задача 4:  Куб
# Считываем длину ребра куба
a = int(input())

# Вычисляем объем куба: a^3 = a * a * a
volume = a * a * a

# Вычисляем площадь полной поверхности: 6 * a^2 = 6 * a * a
surface_area = 6 * a * a

# Выводим результат в требуемом формате
print(f"Объем = {volume}")
print(f"Площадь полной поверхности = {surface_area}")


# Задача 5: Арифметические операции
# Считываем два числа
a = int(input())
b = int(input())

# Вычисляем сумму, разность и произведение
sum_result = a + b
difference = a - b
product = a * b

# Выводим результаты в требуемом формате
print(f"{a} + {b} = {sum_result}")
print(f"{a} - {b} = {difference}")
print(f"{a} * {b} = {product}")


# Задача 6: Арифметическая прогрессия
# Считываем данные: первый член, разность и номер члена
a1 = int(input())
d = int(input())
n = int(input())

# Вычисляем n-ый член арифметической прогрессии по формуле:
# an = a1 + d * (n - 1)
an = a1 + d * (n - 1)

# Выводим результат
print(an)


# Задача 7: Разделяй и властвуй
# Считываем целое положительное число x
x = int(input())

# Выводим последовательность чисел, разделённых тремя чёрточками
result = []

for i in range(1, 6):
    result.append(str(x * i))

print('---'.join(result))