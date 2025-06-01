import pandas as pd
import json

def parse_xlsx_to_json(xlsx_file, output_json):
    df = pd.read_excel(xlsx_file, dtype=str).fillna("")
    
    students = []
    for _, row in df.iterrows():
        student_data = {
            "last_name": row["last_name"],
            "first_name": row["first_name"],
            "middle_name": row["middle_name"],
            "date_birthday": row["date_birthday"],
            "is_learning": "true",  # Значение по умолчанию
            "is_headman": row["is_headman"],
            "group": "",
            "date_input": row["date_input"],
            "date_output": "",  # Значение по умолчанию
            "sub_groups": ""  # Значение по умолчанию
        }
        students.append(student_data)
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    
    return output_json

# Пример использования:
# parse_xlsx_to_json("students.xlsx", "students.json")