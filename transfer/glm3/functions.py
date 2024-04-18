import re


def insert_before_line(original_content, line_content, insert_content):
    lines = original_content.split('\n')
    for i, line in enumerate(lines):
        if line_content in line:
            lines.insert(i, insert_content)
            break
    return '\n'.join(lines)


def insert_behind_line(original_content, line_content, insert_content):
    lines = original_content.split('\n')
    for i, line in enumerate(lines):
        if line_content in line:
            lines.insert(i + 1, insert_content)
            break
    return '\n'.join(lines)


def replace_with_regex(original_content, regex_str, new_content):
    return re.sub(regex_str, new_content, original_content)


def replace_with_full_str(original_content, old_content, new_content):
    return original_content.replace(old_content, new_content)


def delete_with_regex(original_content, regex_str):
    return re.sub(regex_str, '', original_content)


def delete_with_full_str(original_content, delete_content):
    return original_content.replace(delete_content, '')


def call_function_by_name(func_name, **kwargs):
    """
    Calls a function based on its name and provided keyword arguments.

    Args:
    func_name (str): The name of the function to call.
    kwargs (dict): Keyword arguments to pass to the function.

    Returns:
    str: The result from the called function.

    Raises:
    ValueError: If the function name does not correspond to any defined function.
    """
    # Dictionary mapping function names to function objects
    function_map = {
        'insert_before_line': insert_before_line,
        'insert_behind_line': insert_behind_line,
        'replace_with_regex': replace_with_regex,
        'replace_with_full_str': replace_with_full_str,
        'delete_with_regex': delete_with_regex,
        'delete_with_full_str': delete_with_full_str
    }

    # Check if the function name is valid
    if func_name not in function_map:
        raise ValueError(f"Function '{func_name}' is not defined.")

    # Get the function from the map
    function_to_call = function_map[func_name]

    # Call the function with the provided keyword arguments
    return function_to_call(**kwargs)

def execute_function_sequence(function_calls):
    """
    Executes a sequence of function calls based on their names and provided arguments.
    Each function call after the first can use the result of the previous function call
    as its 'original_content' if needed.

    Args:
    function_calls (list of dict): A list of dictionaries, each containing the function name
                                   and its keyword arguments for the call.

    Returns:
    str: The result from the last function call in the sequence.
    """
    # Initial content, if specified in the first function call
    if 'original_content' in function_calls[0]:
        current_content = function_calls[0]['original_content']
    else:
        current_content = None  # Default to None if not specified

    # Iterate through each function call in the list
    for call in function_calls:
        func_name = call['function_name']
        kwargs = {k: v for k, v in call.items() if k != 'function_name'}

        # Update 'original_content' for the current call
        if 'original_content' in kwargs:
            kwargs['original_content'] = current_content

        # Call the function with the provided keyword arguments
        current_content = call_function_by_name(func_name, **kwargs)

    return current_content


if __name__ == "__main__":

    # Example of using the function with the provided format
    function_calls = [{'function_name': 'insert_before_line','original_content': 'First line\nSecond line\nThird line\nFourth line', 'line_content': 'Second line', 'insert_content': 'Newly added line'}, {'function_name': 'replace_with_full_str', 'original_content': 'First line\nSecond line\nThird line\nFourth line', 'old_content': 'Third line', 'new_content': 'Replaced line'}]

    result = execute_function_sequence(function_calls)
    print(result)



