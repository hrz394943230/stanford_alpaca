import json
import os
from tqdm import tqdm
from utils import chat_completion_request,generate_user_message


def generate_response():
    instruction_nums = [4, 5, 6, 7]
    languages = ["Chinese", "English"]
    steps = [1, 2, 3]
    lengths = [3, 4, 5]
    content = generate_user_message(instruction_nums,languages,steps,lengths)
    messages = []
    messages.append({"role": "system",
                     "content": "Do as user told to you!"})
    messages.append({"role": "user", "content": f"{content}"})
    chat_response = chat_completion_request(
        messages,
    )
    assistant_message = chat_response.choices[0].message.content
    assistant_message_dict = json.loads(assistant_message)["sets"]
    return assistant_message_dict


def generate_json_data(target_count, file_path):
    try:
        # 尝试打开并读取现有的JSON文件
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                existing_count = len(data)
        except FileNotFoundError:
            # 如果文件不存在，则创建一个新文件并初始化数据为一个空列表
            data = []
            existing_count = 0
            print(f"File {file_path} not found, creating a new file.")

        # 使用tqdm进度条来显示生成进度
        with tqdm(total=target_count, initial=existing_count, desc="Updating JSON data") as pbar:
            while existing_count < target_count:
                response = generate_response()  # 调用生成函数
                needed = target_count - existing_count  # 还需要多少个数据集
                new_data_count = len(response)

                # 如果生成的数据超过所需，只添加所需的部分
                if new_data_count > needed:
                    response = response[:needed]

                data.extend(response)
                existing_count += len(response)
                pbar.update(len(response))

                # 将新数据写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file,ensure_ascii=False, indent=4)

            print("JSON data generated and saved.")

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Check if the file is a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")










if __name__ == "__main__":
    if os.name == 'posix':  # Unix-like OS (e.g., macOS, Linux)
        filepath = r"/Users/huruize/PycharmProjects/stanford_alpaca/transfer/glm3/regen.json"
    elif os.name == 'nt':  # Windows OS
        filepath = r"D:\pyprojects\stanford_alpaca\transfer\glm3\regen.json"
    generate_json_data(1000, filepath)
    # print()
