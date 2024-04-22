import difflib
import json

from utils import tools,client
from tools import execute_function_calls

def get_answer(filepath,model_name,tools):
    with open(filepath,encoding="utf-8") as f:
        data = json.load(f)
        original_text = data[0]["original_text"]
        description = data[0]["description"]
        modified_text = data[0]["modified_text"]
        print(original_text,description)
        messages= []
        messages.append({"role": "system",
                         "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
        messages.append({"role": "user",
                         "content": "Use the function I give to edit the original_text based on description \n" +
                         "original_text:" + original_text +"\n" +
                         "description:" + description})

        chat_response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            tools=tools
        )
        assistant_message = chat_response.choices[0].message
        tool_calls = assistant_message.tool_calls
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_args["function_name"] = function_name
                current_text = execute_function_calls([function_args])
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": current_text,
                    }
                )

                # 初始化计数器
                loop_count = 0

                # 开始死循环
                while True:
                    if current_text == modified_text:
                        print("make it")
                        break
                    else:
                        # 使用Differ进行比较
                        d = difflib.Differ()
                        diff = list(d.compare(modified_text.splitlines(), current_text.splitlines()))
                        messages.append(
                            {
                                "role": "user",
                                "content":"there is still some difference, here is the diff between current_text and modified_text: \n "+
                                diff. ,
                                "tools":tools
                            }
                        )
                        print(diff)

                    # 更新计数器
                    loop_count += 1

                    # 检查是否达到循环次数限制
                    if loop_count > 5:
                        print("Looped more than 5 times, exiting...")
                        break
                print(messages)







if __name__ =="__main__":
    filepath = r"regen.json"
    model_name= "gpt-4"
    get_answer(filepath,model_name,tools)