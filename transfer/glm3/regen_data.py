import json
from utils import pretty_print_conversation,chat_completion_request


def format_llama_data(filepath):
    with open(filepath) as file :
        data = json.load(file)
        messages = []
        messages.append({"role": "system",
                         "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        messages.append({"role": "user", "content": f"instruntion:{data[0]['instruction']} input :{data[0]['input']}."})
        chat_response = chat_completion_request(
            messages
        )
        assistant_message = chat_response.choices[0].message
        messages.append(assistant_message)
        print(assistant_message)










if __name__ == "__main__":
    filepath = r"/Users/huruize/PycharmProjects/stanford_alpaca/output/regen.json"
    format_llama_data(filepath)