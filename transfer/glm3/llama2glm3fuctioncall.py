from functions import call_function_by_name
import json
import re
def transfer_data_to_glm(filepath,despath):
    pass

def safe_json_loads(input_str):
    # 首先，正确处理特殊字符，例如转义符和双引号
    input_str = input_str.replace('\\"', '\\\\"')  # 转义内部的双引号
    # 替换所有单引号为双引号
    input_str = input_str.replace("'", '"')
    # 尝试加载处理过的字符串为JSON
    try:
        return json.loads(input_str)
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}" +input_str)
        return None


def check_data_quality(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for entry in data:
            input_data = entry.get('input')
            output_data = entry.get('output')
            output_list = safe_json_loads(output_data)

            # 打印输出读取的数据

            # print(output_list)


    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    except FileNotFoundError as e:
        print("File not found:", e)






if __name__=="__main__":
    filepath = r"/Users/huruize/PycharmProjects/stanford_alpaca/output/regen.json"
    check_data_quality(filepath)