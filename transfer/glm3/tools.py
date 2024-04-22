import re


def replace_with_regex(original_content, regex_str, new_content):
    return re.sub(regex_str, new_content, original_content)


def replace_with_full_str(original_content, old_content, new_content):
    return original_content.replace(old_content, new_content)


def delete_with_regex(original_content, regex_str):
    return re.sub(regex_str, '', original_content)


def delete_with_full_str(original_content, delete_content):
    # 删除包含后续换行符的内容（常规情况）
    if delete_content.endswith('\n'):
        modified_content = original_content.replace(delete_content, '')
        return modified_content

    else:
        content_with_line_after = delete_content + '\n'
        modified_content = original_content.replace(content_with_line_after, '')

        # 如果没有变化并且delete_content不是在末尾，尝试删除前面的换行符加delete_content（如果是在中间或开头的行）
        if modified_content == original_content:
            content_with_line_before = '\n' + delete_content
            modified_content = original_content.replace(content_with_line_before, '')

        # 如果还是没有变化，尝试仅删除delete_content（可能是末尾或只有一行的情况）
        if modified_content == original_content:
            modified_content = original_content.replace(content_with_line_after, '')

        return modified_content


def insert_behind_line(original_content, line_content, insert_content):
    lines = original_content.split('\n')
    for i, line in enumerate(lines):
        if line_content in line:
            lines.insert(i + 1, insert_content)
            break
    return '\n'.join(lines)


def insert_before_line(original_content, line_content, insert_content):
    lines = original_content.split('\n')
    for i, line in enumerate(lines):
        if line_content in line:
            lines.insert(i, insert_content)
            break
    return '\n'.join(lines)


def execute_function_calls(function_calls):
    """ Execute a list of function calls with their specified parameters. """
    content = function_calls[0]['original_content']
    for call in function_calls:
        func = globals()[call['function_name']]
        # Adjust function calls based on the type of operation (insert, replace, delete)
        if call['function_name'] in ['replace_with_regex', 'replace_with_full_str']:
            content = func(content, call.get('regex_str') or call.get('old_content'), call.get('new_content'))
        elif call['function_name'] in ['delete_with_regex', 'delete_with_full_str']:
            content = func(content, call.get('regex_str') or call.get('delete_content'))
        else:
            content = func(content, call['line_content'], call['insert_content'])
    return content


# Example usage
if __name__ == "__main__":
    function_calls = [
        {
            "function_name": "insert_behind_line",
            "original_content": "First line\nSecond line\nAdd a line after this.\nLast line",
            "line_content": "Add a line after this.",
            "insert_content": "Newly added line"
        },
        {
            "function_name": "delete_with_full_str",
            "original_content": "",
            "delete_content": "Second line"
        }
    ]

    # Execute the function calls
    modified_content = execute_function_calls(function_calls)
    print(modified_content)
