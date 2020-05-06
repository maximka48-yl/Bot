import random


# Проверка на возможность победы
def can_win(a, b, c, char):
    if a == char and b == char and c in '123456789':
        return True
    elif a == char and b in '123456789' and c == char:
        return True
    elif a in '123456789' and b == char and c == char:
        return True
    else:
        return False


# Ход компьютера
def comp_course(field):
    if field[0].count('X') + field[1].count('X') + field[2].count('X') == 1:
        if field[1][1] != 'X':
            field[1][1] = '0'
            return field
    elif can_win(field[0][0], field[0][1], field[0][2], '0'):
        if field[0][0] != '0':
            field[0][0] = '0'
            return field
        elif field[0][1] != '0':
            field[0][1] = '0'
            return field
        elif field[0][2] != '0':
            field[0][2] = '0'
            return field
    elif can_win(field[1][0], field[1][1], field[1][2], '0'):
        if field[1][0] != '0':
            field[1][0] = '0'
            return field
        elif field[1][1] != '0':
            field[1][1] = '0'
            return field
        elif field[1][2] != '0':
            field[1][2] = '0'
            return field
    elif can_win(field[2][0], field[2][1], field[2][2], '0'):
        if field[2][0] != '0':
            field[2][0] = '0'
            return field
        elif field[2][1] != '0':
            field[2][1] = '0'
            return field
        elif field[2][2] != '0':
            field[2][2] = '0'
            return field
    elif can_win(field[0][0], field[1][0], field[2][0], '0'):
        if field[0][0] != '0':
            field[0][0] = '0'
            return field
        elif field[1][0] != '0':
            field[1][0] = '0'
            return field
        elif field[2][0] != '0':
            field[2][0] = '0'
            return field
    elif can_win(field[0][1], field[1][1], field[2][1], '0'):
        if field[0][1] != '0':
            field[0][1] = '0'
            return field
        elif field[1][1] != '0':
            field[1][1] = '0'
            return field
        elif field[2][1] != '0':
            field[2][1] = '0'
            return field
    elif can_win(field[0][2], field[1][2], field[2][2], '0'):
        if field[0][2] != '0':
            field[0][2] = '0'
            return field
        elif field[1][2] != '0':
            field[1][2] = '0'
            return field
        elif field[2][2] != '0':
            field[2][2] = '0'
            return field
    elif can_win(field[0][2], field[1][1], field[2][0], '0'):
        if field[0][2] != '0':
            field[0][2] = '0'
            return field
        elif field[1][1] != '0':
            field[1][1] = '0'
            return field
        elif field[2][0] != '0':
            field[2][0] = '0'
            return field
    elif can_win(field[0][0], field[1][1], field[2][2], '0'):
        if field[0][0] != '0':
            field[0][0] = '0'
            return field
        elif field[1][1] != '0':
            field[1][1] = '0'
            return field
        elif field[2][2] != '0':
            field[2][2] = '0'
            return field
    elif can_win(field[0][0], field[0][1], field[0][2], 'X'):
        if field[0][0] != 'X':
            field[0][0] = '0'
            return field
        elif field[0][1] != 'X':
            field[0][1] = '0'
            return field
        elif field[0][2] != 'X':
            field[0][2] = '0'
            return field
    elif can_win(field[1][0], field[1][1], field[1][2], 'X'):
        if field[1][0] != 'X':
            field[1][0] = '0'
            return field
        elif field[1][1] != 'X':
            field[1][1] = '0'
            return field
        elif field[1][2] != 'X':
            field[1][2] = '0'
            return field
    elif can_win(field[2][0], field[2][1], field[2][2], 'X'):
        if field[2][0] != 'X':
            field[2][0] = '0'
            return field
        elif field[2][1] != 'X':
            field[2][1] = '0'
            return field
        elif field[2][2] != 'X':
            field[2][2] = '0'
            return field
    elif can_win(field[0][0], field[1][0], field[2][0], 'X'):
        if field[0][0] != 'X':
            field[0][0] = '0'
            return field
        elif field[1][0] != 'X':
            field[1][0] = '0'
            return field
        elif field[2][0] != 'X':
            field[2][0] = '0'
            return field
    elif can_win(field[0][1], field[1][1], field[2][1], 'X'):
        if field[0][1] != 'X':
            field[0][1] = '0'
            return field
        elif field[1][1] != 'X':
            field[1][1] = '0'
            return field
        elif field[2][1] != 'X':
            field[2][1] = '0'
            return field
    elif can_win(field[0][2], field[1][2], field[2][2], 'X'):
        if field[0][2] != 'X':
            field[0][2] = '0'
            return field
        elif field[1][2] != 'X':
            field[1][2] = '0'
            return field
        elif field[2][2] != 'X':
            field[2][2] = '0'
            return field
    elif can_win(field[0][2], field[1][1], field[2][0], 'X'):
        if field[0][2] != 'X':
            field[0][2] = '0'
            return field
        elif field[1][1] != 'X':
            field[1][1] = '0'
            return field
        elif field[2][0] != 'X':
            field[2][0] = '0'
            return field
    elif can_win(field[0][0], field[1][1], field[2][2], 'X'):
        if field[0][0] != 'X':
            field[0][0] = '0'
            return field
        elif field[1][1] != 'X':
            field[1][1] = '0'
            return field
        elif field[2][2] != 'X':
            field[2][2] = '0'
            return field
    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if field[row][col] in '123456789':
            field[row][col] = '0'
            return field


# Проверка победы
def won(field):
    if len(set(field[0])) == 1:
        return True, field[0][0]
    elif len(set(field[1])) == 1:
        return True, field[1][0]
    elif len(set(field[2])) == 1:
        return True, field[2][0]
    elif len(set([field[0][0], field[1][0], field[2][0]])) == 1:
        return True, field[2][0]
    elif len(set([field[0][1], field[1][1], field[2][1]])) == 1:
        return True, field[2][1]
    elif len(set([field[0][2], field[1][2], field[2][2]])) == 1:
        return True, field[2][2]
    elif len(set([field[0][0], field[1][1], field[2][2]])) == 1:
        return True, field[2][2]
    elif len(set([field[0][2], field[1][1], field[2][0]])) == 1:
        return True, field[0][2]
    elif all([not field[row][col] in '123456789' for row in range(3) for col in range(3)]):
        return True, 'no'
    else:
        return (False, None)
