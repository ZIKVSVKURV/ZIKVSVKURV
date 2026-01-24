#Ввод чисел a и b
a = int(input())
b = int(input())

# Вычисление F(x) = (a+b)^3 = (a+b)*(a+b)*(a+b)
a_plus_b = a + b
a_plus_b_cubed = a_plus_b * a_plus_b * a_plus_b

# Вычисление b^2 = b*b
b_squared = b * b

# Вычисление всего выражения
result = 3 * a_plus_b_cubed + 275 * b_squared - 127 * a - 41

# Вывод результата
print(result)