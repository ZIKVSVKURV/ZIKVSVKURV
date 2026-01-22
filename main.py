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