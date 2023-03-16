def FioValidator(input,text):
# Обработчик изменения текста поля ФИО
# Проверяем, содержит ли текст более 2-х пробелов
    if text.count(' ') >= 2:
        # Если содержит, то разбиваем текст на отдельные слова
        parts = text.split(' ')
        input.setText(' '.join(parts[:3]))
    else:
        # Разрешаем вводить текст, если ФИО не полное
       input.setText(text)