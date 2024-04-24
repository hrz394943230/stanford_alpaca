import difflib
import json

from utils import tools,client,pretty_print_conversation
from tools import execute_function_calls


def get_answer(filepath, model_name, tools, client):
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    for entry in data :
        original_text = entry["original_text"]
        description = entry["description"]
        modified_text = entry["modified_text"]

        current_text = original_text
        messages = []
        messages.append({"role": "system",
                         "content": "In the first time take original_text as original_text,the rest of times the current_text as original_text for tools,remember to save the line break."})
        messages.append({"role": "user",
                         "content": f"Use the function I give to edit the original_text based on description \noriginal_text:{original_text}\ndescription:{description}"})

        loop_count = 0
        while current_text != modified_text:
            print("loop:" + str(loop_count))
            chat_response = client.chat.completions.create(
                messages=messages,
                model=model_name,
                tools=tools
            )
            assistant_message = chat_response.choices[0].message
            tool_calls = assistant_message.tool_calls
            print(tool_calls)

            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    function_args["function_name"] = function_name
                    current_text = execute_function_calls([function_args])  # This needs to be a defined function
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "function",
                        "name": function_name,
                        "content": current_text,
                    })

            if current_text != modified_text:
                d = difflib.Differ()
                diff = list(d.compare(modified_text.splitlines(), current_text.splitlines()))
                diff_str = '\n'.join(diff)
                messages.append({
                    "role": "user",
                    "content": "There is still some difference, here is the diff between current_text and target_text: \n" + diff_str +"\n" +
                                "here is the current_text: \n" + current_text,
                })
            else:
                print("mission complete!")
                break

            loop_count += 1
            if loop_count > 5:
                print("Looped more than 5 times, exiting...")
                break
        pretty_print_conversation(messages)






if __name__ =="__main__":
    filepath = r"regen.json"
    model_name= "gpt-3.5-turbo-1106"
    get_answer(filepath,model_name,tools,client)