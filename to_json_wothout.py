import json
# 打开原始文件和目标文件
with open('new.txt', 'r', encoding='utf-8') as source_file:
    lines = source_file.readlines()

# 存储结果的列表
result = []

# 逐行处理文本
for line in lines:
    word = line.strip()  # 去掉行尾的换行符和空白
    if not word:
        continue  # 跳过空行
    # 每行只有一个单词

    # 添加到结果列表
    result.append({
        "name": word,
        "trans": "",
        "usphone": "",
        "ukphone": ""
    })

# 将结果保存为JSON文件
with open('output.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)
