"""
С клавиатуры вводится два числа K и N.
Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E заполняется
случайным образом целыми числами в интервале [-10,10].
Для отладки использовать не случайное заполнение, а целенаправленное. Вид матрицы А:
B C
D E
По сформированной матрице F (или ее частям) необходимо вывести не менее 3 разных графиков.

Вариант 7.	Формируется матрица F следующим образом: скопировать в нее А и если в С количество нулевых элементов
в нечетных столбцах, чем количество нулевых  элементов в четных столбцах, то поменять местами С и В симметрично, иначе
С и Е поменять местами несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше
суммы диагональных элементов матрицы F, то вычисляется выражение: A*AT – K * FТ, иначе вычисляется
выражение (AТ +G-F-1)*K, где G-нижняя треугольная матрица, полученная из А. Выводятся по мере формирования А, F
и все матричные операции последовательно.
"""

import random
import sys
import numpy as np
import matplotlib.pyplot as plt

k = input('Введите число K: ')

try:
    k = int(k)
except ValueError:
    sys.exit('Введено не число. Программа завершена.')

n = input('Введите число N > 3: ')

try:
    n = int(n)
    while n < 4:
        n = int(input('Число должно быть больше 3: '))
except ValueError:
    sys.exit('Введено не число. Программа завершена.')

bigger = input('Количество нулей в нечетных стобиках C должно быть больше или меньше чем в четных? (Ответьте 0 - если меньше, 1 - '
               'если больше): ')


try:
    bigger = int(bigger)
    while bigger > 1:
        bigger = int(input('Ответьте 0 - если больше, 1 - если меньше: '))
except ValueError:
    sys.exit('Введено не число. Программа завершена.')
if bigger == 1:
    bigger = True
else:
    bigger = False

main_table = []
for i in range(n):
    work_list = []

    for j in range(n):
        work_list.append(random.randint(-10, 10))  # ------------------------------------------
    main_table.append(work_list)

matrix = np.matrix(main_table)

print(f'Матрица А:\n{matrix}')

if n % 2 == 1:  # Избавление от нечетности столбцов
    skip_number = int(n / 2)
    print(
        f'Так как количество столбцов и строк нечетно, строка и столбец под номерами {skip_number + 1} не будут включены'
        f' в подматрицы\n')
    matrix = np.delete(matrix, skip_number, 0)
    matrix = np.delete(matrix, skip_number, 1)

# print(f'Матрица А:\n{matrix}')

# Разбиение на подматрицы
upper_half = np.hsplit(np.vsplit(matrix, 2)[0], 2)
lower_half = np.hsplit(np.vsplit(matrix, 2)[1], 2)

sub_matrix_b, sub_matrix_c, sub_matrix_d, sub_matrix_e = upper_half[0], upper_half[1], lower_half[0], lower_half[1]

print(f'Подматрица C:\n{sub_matrix_c}')

sub_matrix_c = sub_matrix_c.tolist()
c_odd_null_count = 0
c_even_null_count = 0
for i in range(len(sub_matrix_c)):
    for j in range(len(sub_matrix_c)):
        if j % 2 == 1 and sub_matrix_c[i][j] == 0:
            c_odd_null_count += 1
        if j % 2 == 0 and sub_matrix_c[i][j] == 0:
            c_even_null_count += 1
sub_matrix_c = np.matrix(sub_matrix_c)

if bigger:
    solution = (c_odd_null_count > c_even_null_count)
    if solution:
        print('Нулей больше')
    else:
        print('Нулей меньше или одинаково')
else:
    solution = (c_odd_null_count < c_even_null_count)
    if solution:
        print('Нулей меньше')
    else:
        print('Нулей больше или одинаково')

if not solution:
    print(f'Подматрица С:\n{sub_matrix_c}\nПодматрица E:\n{sub_matrix_e}\n')
    sub_matrix_c, sub_matrix_e = sub_matrix_e, sub_matrix_c
    print('Несимметричное преобразование\n')
    print(f'Подматрица С:\n{sub_matrix_c}\nПодматрица E:\n{sub_matrix_e}\n')
else:
    print(f'Подматрица С:\n{sub_matrix_c}\nПодматрица B:\n{sub_matrix_b}\n')
    sub_matrix_c = sub_matrix_c.tolist()
    sub_matrix_b = sub_matrix_b.tolist()
    length = len(sub_matrix_c) - 1
    for i in range(length):
        sub_matrix_c[i][length], sub_matrix_b[i][0] = sub_matrix_b[i][0], sub_matrix_c[i][length]
        for j in range(length):
            number = length - j
            sub_matrix_c[i][j], sub_matrix_b[i][number] = sub_matrix_b[i][number], sub_matrix_c[i][j]

    sub_matrix_c[i + 1][length], sub_matrix_b[i + 1][0] = sub_matrix_b[i + 1][0], sub_matrix_c[i + 1][length]
    for j in range(length):
        number = length - j
        sub_matrix_c[i + 1][j], sub_matrix_b[i + 1][number] = sub_matrix_b[i + 1][number], sub_matrix_c[i + 1][j]

    sub_matrix_c = np.matrix(sub_matrix_c)
    sub_matrix_b = np.matrix(sub_matrix_b)

    print('Симметричное преобразование\n')
    print(f'Подматрица С:\n{sub_matrix_c}\nПодматрица B:\n{sub_matrix_b}\n')

F_matrix = np.vstack([np.hstack([sub_matrix_b, sub_matrix_c]), np.hstack([sub_matrix_d, sub_matrix_e])])
print(f'Матрица F:\n{F_matrix}\n')

determinant_A = np.linalg.det(matrix)
print(f'Определитель матрицы A: {determinant_A}')

diag_num_list = []
diags = [F_matrix[::-1, :].diagonal(i) for i in range(-F_matrix.shape[0] + 1, F_matrix.shape[1])]
diags.extend(F_matrix.diagonal(i) for i in range(F_matrix.shape[1] - 1, -F_matrix.shape[0], -1))
for matrix_i in diags:
    diag_num_list.append(matrix_i.tolist())

diag_sum = 0
for i in range(len(diag_num_list)):
    for x in range(len(diag_num_list[i])):
        for j in diag_num_list[i][x]:
            diag_sum += int(j)
print(f'Сумма диагональных элементов матрицы F: {diag_sum}')

if determinant_A > diag_sum:
    print('Определитель больше, считаем формулу A * At - K * Ft\n')
    answer = np.dot(matrix, matrix.transpose()) - np.dot(k, F_matrix.transpose())
else:
    print('Определитель меньше, считаем формулу (At + G - F^(-1)) * K\n')
    G_matrix = np.tril(matrix, k=-1)
    print(f'G-нижняя треугольная матрица, полученная из А:\n{G_matrix}')
    answer = (matrix.transpose() + G_matrix - F_matrix.I) * k

answer = answer.tolist()
for i in range(len(answer)):
    for j in range(len(answer)):
        answer[i][j] = int(answer[i][j])
answer = np.matrix(answer)

print(f'Итоговая матрица:\n{answer}')

plt.plot(answer)
plt.title("График")
plt.xlabel("x axis")
plt.ylabel("y axis")
plt.show()

plt.imshow(answer)
plt.colorbar()
plt.title("Тепловая карта")
plt.show()

explode = [0]*(n-2)                                     # отношение средних значений от каждой строки
explode.append(0.1)
plt.title("Круговая диаграмма")
try:
    sizes = [round(np.mean(abs(F_matrix[i, ::])) * 100, 1) for i in range(n)]
except IndexError:
    sizes = [round(np.mean(abs(F_matrix[i, ::])) * 100, 1) for i in range(n - 1)]

plt.pie(sizes, labels=list(range(1, n)), explode=explode, autopct='%1.1f%%', shadow=False)
plt.show()
