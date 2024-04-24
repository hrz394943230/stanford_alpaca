import difflib
import json

from utils import tools,client,pretty_print_conversation
from tools import execute_function_calls


def get_answer(input_filepath, output_filepath, model_name, tools, client):
    # Load existing output data if available
    try:
        with open(output_filepath, 'r', encoding="utf-8") as output_file:
            existing_data = json.load(output_file)
    except (IOError, ValueError):
        existing_data = []

    existing_ids = set(entry["id"] for entry in existing_data)  # Set of existing IDs for fast lookup

    # Load input data
    with open(input_filepath, encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        if entry["id"] in existing_ids:
            continue  # Skip processing this entry if the ID already exists in the output file

        original_text = entry["original_text"]
        description = entry["description"]
        modified_text = entry["modified_text"]

        current_text = original_text
        messages = []
        messages.append({"role": "system",
                         "content": "In the first time take original_content as original_content, the rest of times the current_content as original_text for tools."})
        messages.append({"role": "user",
                         "content": f"Use the function I give to edit the original_text based on description \noriginal_content:{original_text}\ndescription:{description}"})

        loop_count = 0
        tool_call_messages = []
        while current_text != modified_text:
            print("loop:" + str(loop_count))
            chat_response = client.chat.completions.create(
                messages=messages,
                model=model_name,
                tools=tools
            )
            assistant_message = chat_response.choices[0].message
            tool_calls = assistant_message.tool_calls

            if tool_calls:
                calling_num = 0
                for tool_call in tool_calls:
                    calling_num = calling_num +1
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    function_args["function_name"] = function_name
                    if calling_num > 1:
                        function_args["original_content"] =current_text
                    current_text = execute_function_calls([function_args])# This needs to be a defined function
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "function",
                        "name": function_name,
                        "content": current_text,
                    })
                    tool_call_message = tool_call.function.arguments
                    tool_call_messages.append(tool_call_message)

            if current_text != modified_text:
                # d = difflib.Differ()
                # diff = list(d.compare(modified_text.splitlines(), current_text.splitlines()))
                # diff_str = '\n'.join(diff)
                messages.append({
                    "role": "user",
                    "content": "There is still some difference, here is the target_content: \n" + modified_text + "\n" +
                               "here is the current_content: \n" + current_text,
                })
                print("current:" +current_text)
                print("target:"+modified_text)
            else:
                print("mission complete!")
                entry["stop_reason"] = "success"
                break

            loop_count += 1
            if loop_count > 5:
                entry["stop_reason"] = "loop limit"
                print("Looped more than 5 times, exiting...")
                break

        entry["messages"] = messages
        entry["tool_call_messages"] = tool_call_messages
        existing_data.append(entry)  # Add processed entry to existing data
        # Write the updated data to the file to save progress immediately
        with open(output_filepath, 'w', encoding="utf-8") as output_file:
            json.dump(existing_data, output_file, indent=4)






if __name__ =="__main__":
    filepath = r"data/gen_with_id.json"
    output = r"data/gen_with_tool.json"
    # model_name = "gpt-3.5-turbo-1106"
    # model_name = "gpt-3.5-turbo-0125"
    model_name = "gpt-4-0125-preview"
    get_answer(filepath,output,model_name,tools,client)