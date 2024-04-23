import random
import json
from tqdm import tqdm
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

tools = [
    {
        "type": "function",
        "function": {
            "name": "insert_behind_line",
            "description": "Inserts a specified content behind a specific line in the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "line_content": {
                        "type": "string",
                        "description": "The line content after which the insertion should occur."
                    },
                    "insert_content": {
                        "type": "string",
                        "description": "The content to be inserted behind the specified line."
                    }
                },
                "required": ["original_content", "line_content", "insert_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "insert_before_line",
            "description": "Inserts a specified content before a specific line in the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "line_content": {
                        "type": "string",
                        "description": "The line content before which the insertion should occur."
                    },
                    "insert_content": {
                        "type": "string",
                        "description": "The content to be inserted before the specified line."
                    }
                },
                "required": ["original_content", "line_content", "insert_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_with_regex",
            "description": "Replaces parts of the text that match a specified regular expression with new content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "regex_str": {
                        "type": "string",
                        "description": "The regular expression used to find matching text in the original content."
                    },
                    "new_content": {
                        "type": "string",
                        "description": "The new content that will replace the matched text."
                    }
                },
                "required": ["original_content", "regex_str", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "replace_with_full_str",
            "description": "Replaces an exact substring in the given text with new content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "old_content": {
                        "type": "string",
                        "description": "The exact substring to be replaced."
                    },
                    "new_content": {
                        "type": "string",
                        "description": "The new content that will replace the old substring."
                    }
                },
                "required": ["original_content", "old_content", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_with_regex",
            "description": "Deletes parts of the text that match a specified regular expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "regex_str": {
                        "type": "string",
                        "description": "The regular expression used to find and delete matching text."
                    }
                },
                "required": ["original_content", "regex_str"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_with_full_str",
            "description": "Deletes an exact substring from the given text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "original_content": {
                        "type": "string",
                        "description": "The original text content."
                    },
                    "delete_content": {
                        "type": "string",
                        "description": "The exact substring to be deleted."
                    }
                },
                "required": ["original_content", "delete_content"]
            }
        }
    }
]


api_base = "https://api.openai-proxy.org/v1"
api_key = "sk-oMCjsBS2Osp5lTABMu0Sh41QTE78nmVB8OqsEUSWUxLZ2QM6"
GPT_MODEL = "gpt-4-1106-preview"
client = OpenAI(
    api_key = api_key,
    base_url=api_base
)


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, model=GPT_MODEL):
    try:
        seed = random.randint(0,9999)
        response = client.chat.completions.create(
            seed = seed,
            model=model,
            messages=messages,
            response_format={ "type": "json_object" },
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "function":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))


def generate_user_message(instruction_nums,languages,steps,lengths):
    instruction_num = random.choice(instruction_nums)
    language = random.choice(languages)
    step = random.choice(steps)
    length = random.choice(lengths)
    content = f'''
I need you to generate three segments of text for me: original_text, description, and modified_text. 
I will use these to train my large language model. For these three segments of text, you need to output {instruction_num} sets in JSON format.
Each set of JSON content needs to be wrapped in a list within the "sets" field.

original_text: The original text
description: Description of the editing actions performed on the text
modified_text: The text after editing
Requirements:

The original_text and modified_text need to appear as authentic text, not just fabricated examples created for a demonstration task.
The description should be accurate, clear, and described step-by-step, using prefixes like 1, 2, 3...
These three segments of text must be in {language}.
The description must outline the steps taken to transform the original_text into the modified_text, completing the transformation in {step} steps.
The generated original_text should be at least {length} lines long, with each line ending with a newline character.
    '''
    return content




# 示例使用函数
# generate_json_data(5, 'your_path_to_file.json')


