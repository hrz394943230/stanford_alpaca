import json
import os

from utils import pretty_print_conversation,chat_completion_request
from functions import call_function_by_name


def format_llama_data(filepath):
    with open(filepath) as file :
        data = json.load(file)
        messages = []
        messages.append({"role": "system",
                         "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        messages.append({"role": "user", "content": f"instruntion:{data[0]['instruction']} input :{data[0]['input']}."})
        user_input = json.loads(data[0]['input'])
        print(user_input)
        print(user_input["modified_text"])
        chat_response = chat_completion_request(
            messages
        )
        assistant_message = chat_response.choices[0].message
        messages.append(assistant_message)
        print(assistant_message)










if __name__ == "__main__":
    if os.name == 'posix':  # Unix-like OS (e.g., macOS, Linux)
        filepath = r"/Users/huruize/PycharmProjects/stanford_alpaca/output/regen.json"
    elif os.name == 'nt':  # Windows OS
        filepath = r"D:\pyprojects\stanford_alpaca\output\regen.json"
    format_llama_data(filepath)