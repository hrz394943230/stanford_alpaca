import os

from functions import call_function_by_name
import json
import re
def transfer_data_to_glm(filepath,despath):
    pass

# def safe_json_loads(input_str):
#     # 首先，正确处理特殊字符，例如转义符和双引号
#     input_str = input_str.replace('\\"', '\\\\"')  # 转义内部的双引号
#     # 替换所有单引号为双引号
#     input_str = input_str.replace("'", '"')
#     # 尝试加载处理过的字符串为JSON
#     try:
#         return json.loads(input_str)
#     except json.JSONDecodeError as e:
#         print(f"JSON 解析错误: {e}" +input_str)
#         return None


def check_data_quality(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            try:
                # 处理 'input' 字段
                if 'input' in entry:
                    input_data = json.loads(convert_quotes(entry['input']))
                    print(f"Processed Input: {input_data}")

                # 处理 'output' 字段
                # if 'output' in entry:
                #     output_data = json.loads(convert_quotes(entry['output']))
                #     print(f"Processed Output: {output_data}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in entry {entry}: {e}")

    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except FileNotFoundError as e:
        print("File not found:", e)


def convert_quotes(text):
    # 首先将已经转义的单引号（\'）替换为一个临时的占位符
    text = re.sub(r"\\'", "TEMP_SINGLE_QUOTE", text)

    # 然后将所有非转义的单引号替换为双引号
    text = re.sub(r"'", '"', text)

    # 最后将临时占位符替换回一个单引号
    text = re.sub(r"TEMP_SINGLE_QUOTE", "'", text)

    return text






if __name__=="__main__":
    if os.name == 'posix':  # Unix-like OS (e.g., macOS, Linux)
        filepath = r"/Users/huruize/PycharmProjects/stanford_alpaca/output/regen.json"
    elif os.name == 'nt':  # Windows OS
        filepath = r"D:\pyprojects\stanford_alpaca\output\regen.json"
    check_data_quality(filepath)