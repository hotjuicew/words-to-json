file_name = 'words.txt'
with open(file_name, 'r') as file:
    lines = file.readlines()
    num_lines = len(lines)

print(f"文件 '{file_name}' 中有 {num_lines} 行。")
