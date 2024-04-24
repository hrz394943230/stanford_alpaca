import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print("Data loaded successfully!")
            new_data =[]
            count = 1
            for entry in data:
                entry["id"] =count
                count = count +1
                new_data.append(entry)
        with open("data/gen_with_id.json","w",encoding='utf-8') as file1:

            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check if the file is a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


def write_json_data(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 设置 ensure_ascii=False 来避免将非ASCII字符转化为\u形式的Unicode转义序列
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Data has been written to file successfully.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {str(e)}")

# 示例用法
file_path = 'regen.json'  # 替换为实际的文件路径
data = read_json_file(file_path)
write_path = 'regen1.json'
write_json_data(data,file_path)

