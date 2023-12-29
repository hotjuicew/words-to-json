import json

# 读取文本文件内容
def read_txt_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ')
            english = ' '.join(parts[:-1])  # 取除了最后一个词的所有英文部分
            chinese = parts[-1]  # 最后一个词是中文部分
            data.append({"name": english, "trans": [chinese], "usphone": "", "ukphone": ""})
    return data

# 生成JSON文件
def generate_json_file(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 文件路径
file_path = 'zh_en.txt'  # 替换为你的文件路径
output_json_file = 'output.json'  # 生成的JSON文件名

# 读取文件并生成JSON
data = read_txt_file(file_path)
generate_json_file(data, output_json_file)
