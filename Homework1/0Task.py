
"""
Вариант 1
Дана целочисленная прямоугольная матрица. Определить:
1) количество строк, не содержащих ни одного нулевого элемента;
2) максимальное из чисел, встречающихся в заданной матрице более одного раза.

Вариант 2
Дана целочисленная прямоугольная матрица.
1) Определить количество столбцов, не содержащих ни
одного нулевого элемента.
Характеристикой строки целочисленной матрицы назовем сумму ее положительных четных
элементов.
2)Pереставляя строки заданной матрицы, располагать их в соответствии с ростом
характеристик.

Вариант 3
Дана целочисленная прямоугольная матрица. Определить:
1) количество столбцов, содержащих хотя бы один нулевой элемент;
2) номер строки, в которой находится самая длинная серия одинаковых элементов

"""
# Вариант 1
#1)
def count_non_zero_rows(matrix):
    count = 0
    for row in matrix:
        if all(elem != 0 for elem in row):
            count += 1
    return count
#2)
def max_of_numbers_once_in_matrix(matrix):
    counts = {} # хеш таблицы, наши любимые
    max_repeated = None

    # Подсчитываем количество встреч каждого числа в матрице
    for row in matrix:
        for num in row:
            counts[num] = counts.get(num, 0) + 1

    # Находим максимальное число встречающееся более одного раза
    for num, count in counts.items():
        if count > 1:
            if max_repeated is None or num > max_repeated:
                max_repeated = num

    return max_repeated

# Вариант 2
#1)
def count_colums_no_zero(matrix):
    num_columns = len(matrix[0]) # Количество столбцов
    count = 0

    for col in range(num_columns):
        has_zero = False
        for row in range(len(matrix)):
            if matrix[row][col] == 0:
                has_zero = True
                break
        if not has_zero:
            count += 1

    return count

#2)
def row_characteristic(row):
    return sum(num for num in row if num > 0 and num % 2 == 0)

def increasing_characteristic_matrix(matrix):
    matrix.sort(key=row_characteristic)
    return matrix

# Вариант 3
#1)
def count_with_only_zero_rows(matrix):
    num_columns = len(matrix[0])  # Количество столбцов
    count = 0

    for col in range(num_columns):
        for row in matrix:
            if row[col] == 0:
                count += 1
                break  # Если найден хотя бы один нулевой элемент в столбце то выходим из внутреннего цикла

    return count
#2)
def number_rows_with_longest_series(matrix):
    max_length = 0
    row_index = -1

    for i, row in enumerate(matrix):
        current_length = 1
        for j in range(1, len(row)):
            if row[j] == row[j - 1]:
                current_length += 1
            else:
                if current_length > max_length:
                    max_length = current_length
                    row_index = i
                current_length = 1

        if current_length > max_length:
            max_length = current_length
            row_index = i

    return row_index

# Матрица
matrix = [
    [11, 2, 3],
    [0, 50, 6],
    [7, 8, 9],
    [10, 58, 6],
    [72, 8, 92],
    [99, 99, 92]
]

non_zero_row_count = count_non_zero_rows(matrix)
max_of_numbers_in_matrix = max_of_numbers_once_in_matrix(matrix)
colums_with_no_zero = count_colums_no_zero(matrix)
matrix_characterisic = increasing_characteristic_matrix(matrix)
zero_row_count = count_with_only_zero_rows(matrix)
number_rows_longest_series = number_rows_with_longest_series(matrix)


print("Количество строк, не содержащих ни одного нулевого элемента:", non_zero_row_count)
print("Максимальное из чисел, встречающихся в заданной матрице более одного раза:", max_of_numbers_in_matrix)
print("Определение количества столбцов, не содержащих ни одного нулевого элемента:", colums_with_no_zero)
print("Переставляем строки заданной матрицы, и располагаем их в соответствии с ростом характеристик:", matrix_characterisic)
print("Количество столбцов, содержащих хотя бы один нулевой элемент:", zero_row_count)
print("Номер строки, в которой находится самая длинная серия одинаковых элементов", number_rows_longest_series)
