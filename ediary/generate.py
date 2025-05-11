# import pandas as pd

# # Создаем данные
# data = {
#     "first_name": ["Иван", "Мария", "Алексей", "Ольга"],
#     "middle_name": ["Иванович", "Сергеевна", "Дмитриевич", "Петровна"],
#     "last_name": ["Петров", "Смирнова", "Кузнецов", "Попова"],
#     "date_birthday": ["2005-06-15", "2004-09-22", "2006-03-10", "2005-12-30"],
#     "is_headman": [True, False, False, True],
#     "guardian": ["Петрова Анна", "Смирнов Сергей", "Кузнецова Ирина", "Попов Алексей"],
#     "group": ["ИС-21", "ИС-22", "ИС-23", "ИС-24"],
#     "date_input": ["2022-09-01", "2021-09-01", "2023-09-01", "2022-09-01"],
# }

# # Создаем DataFrame
# df = pd.DataFrame(data)

# # Сохраняем в файл
# file_path = "./students.xlsx"
# df.to_excel(file_path, index=False)

# file_path



import pandas as pd

# Создание данных для куратора
curators_data = {
    "first_name": ["Иван", "Ольга", "Александр"],
    "middle_name": ["Петрович", "Сергеевна", "Викторович"],
    "last_name": ["Иванов", "Смирнова", "Сидоров"],
    "is_curator": [True, True, True],
    "is_discipline": [False, False, False]
}

# Создание данных для предметников
discipline_data = {
    "first_name": ["Дмитрий", "Наталья", "Сергей"],
    "middle_name": ["Михайлович", "Павловна", "Викторович"],
    "last_name": ["Ильин", "Романова", "Волков"],
    "is_curator": [False, False, False],
    "is_discipline": [True, True, True]
}

# Преобразование в DataFrame
curators_df = pd.DataFrame(curators_data)
discipline_df = pd.DataFrame(discipline_data)

# Сохранение в Excel
file_path_curators = "./curators.xlsx"
file_path_discipline = "./discipline_prepods.xlsx"


curators_df.to_excel(file_path_curators, index=False)
discipline_df.to_excel(file_path_discipline, index=False)
