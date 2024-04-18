import unittest
from functions import insert_before_line, insert_behind_line, replace_with_regex, replace_with_full_str, delete_with_regex, delete_with_full_str,call_function_by_name

# 若你的函数不在单独的模块中，请直接在此文件中定义或粘贴上述函数。


class TestTextEdits(unittest.TestCase):

    def setUp(self):
        """Setup a test text for all tests."""
        self.test_text = """First line
Second line
Third line
Fourth line"""

    def test_insert_before_line(self):
        # Test inserting before a specific line
        expected_result = """First line
Inserted before Second
Second line
Third line
Fourth line"""
        result = insert_before_line(self.test_text, "Second line", "Inserted before Second")
        self.assertEqual(result, expected_result)

        # Test inserting before a non-existent line
        result = insert_before_line(self.test_text, "Fifth line", "Inserted nowhere")
        self.assertEqual(result, self.test_text)

    def test_insert_behind_line(self):
        # Test inserting behind a specific line
        expected_result = """First line
Second line
Inserted behind Second
Third line
Fourth line"""
        result = insert_behind_line(self.test_text, "Second line", "Inserted behind Second")
        self.assertEqual(result, expected_result)

        # Test inserting behind a non-existent line
        result = insert_behind_line(self.test_text, "Fifth line", "Inserted nowhere")
        self.assertEqual(result, self.test_text)

    def test_replace_with_regex(self):
        # Test replacing using regex
        expected_result = """First replaced
Second replaced
Third replaced
Fourth replaced"""
        result = replace_with_regex(self.test_text, r"line", "replaced")
        self.assertEqual(result, expected_result)

        # Test replacing non-existent pattern
        result = replace_with_regex(self.test_text, r"nonexistent", "no effect")
        self.assertEqual(result, self.test_text)

    def test_replace_with_full_str(self):
        # Test replacing full string
        expected_result = """First line
Second line
Third line replaced
Fourth line"""
        result = replace_with_full_str(self.test_text, "Third line", "Third line replaced")
        self.assertEqual(result, expected_result)

        # Test replacing non-existent string
        result = replace_with_full_str(self.test_text, "Fifth line", "No effect")
        self.assertEqual(result, self.test_text)

    def test_delete_with_regex(self):
        # Test deleting with regex
        expected_result = """First line
Second line
Fourth line"""
        result = delete_with_regex(self.test_text, r"Third line\n")
        self.assertEqual(result, expected_result)

        # Test deleting non-existent pattern
        result = delete_with_regex(self.test_text, r"Fifth line\n")
        self.assertEqual(result, self.test_text)

    def test_delete_with_full_str(self):
        # Test deleting full string
        expected_result = """First line
Second line
Fourth line"""
        result = delete_with_full_str(self.test_text, "Third line\n")
        self.assertEqual(result, expected_result)

        # Test deleting non-existent string
        result = delete_with_full_str(self.test_text, "Fifth line\n")
        self.assertEqual(result, self.test_text)


class TestFunctionCaller(unittest.TestCase):
    def test_insert_before_line(self):
        """测试 insert_before_line 函数是否能正确插入文本。"""
        original_text = "First line\nSecond line\nThird line"
        expected_result = "First line\nInserted before Second\nSecond line\nThird line"
        result = call_function_by_name('insert_before_line', original_content=original_text, line_content='Second line', insert_content='Inserted before Second')
        self.assertEqual(result, expected_result)

    def test_replace_with_regex(self):
        """测试 replace_with_regex 函数是否能正确替换文本。"""
        original_text = "First line\nSecond line\nThird line"
        expected_result = "First replaced\nSecond replaced\nThird replaced"
        result = call_function_by_name('replace_with_regex', original_content=original_text, regex_str=r'line', new_content='replaced')
        self.assertEqual(result, expected_result)

    def test_delete_with_full_str(self):
        """测试 delete_with_full_str 函数是否能正确删除文本。"""
        original_text = "First line\nSecond line\nThird line"
        expected_result = "First line\n\nThird line"
        result = call_function_by_name('delete_with_full_str', original_content=original_text, delete_content='Second line')
        self.assertEqual(result, expected_result)

    def test_invalid_function_name(self):
        """测试对不存在的函数名进行调用时是否抛出 ValueError。"""
        original_text = "First line\nSecond line\nThird line"
        with self.assertRaises(ValueError):
            call_function_by_name('non_existent_function', original_content=original_text, line_content='Second line', insert_content='Inserted before Second')

if __name__ == '__main__':
    unittest.main()
