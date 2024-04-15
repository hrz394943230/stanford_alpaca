import unittest
from unittest.mock import patch

import openai

from utils import openai_completion, OpenAIDecodingArguments  # 确保导入函数和所需的类

api_base = "https://api.openai-proxy.org/v1"
api_key = "sk-oMCjsBS2Osp5lTABMu0Sh41QTE78nmVB8OqsEUSWUxLZ2QM6"
class TestOpenAICompletion(unittest.TestCase):
    def setUp(self):
        # 设置测试用的解码参数
        self.decoding_args = OpenAIDecodingArguments(max_tokens=50)
        self.api_key = "sk-oMCjsBS2Osp5lTABMu0Sh41QTE78nmVB8OqsEUSWUxLZ2QM6"
        self.api_base = "https://api.openai-proxy.org/v1"

    @patch('utils.OpenAI')
    def test_single_string_prompt(self, MockClient):
        # 测试单个字符串提示
        prompt = "Hello, world!"
        mock_response = MockClient.return_value.chat.completions.create.return_value
        mock_response.choices = [{'text': 'Hello, indeed!'}]

        result = openai_completion(prompt, self.decoding_args, "text-davinci-003", 2, 1, 100, 100, True)
        self.assertEqual(result, "Hello, indeed!")

    @patch('utils.OpenAI')
    def test_multiple_string_prompts(self, MockClient):
        # 测试多个字符串提示
        prompts = ["Hello, world!", "How are you?"]
        mock_response = MockClient.return_value.chat.completions.create.return_value
        mock_response.choices = [{'text': 'Hello, indeed!'}, {'text': 'I am fine, thank you!'}]

        results = openai_completion(prompts, self.decoding_args, "text-davinci-003", 1, 1, 100, 100, True)
        self.assertEqual(results, ["Hello, indeed!", "I am fine, thank you!"])

    @patch('utils.OpenAI')
    def test_rate_limit_handling(self, MockClient):
        # 测试速率限制的处理
        MockClient.return_value.chat.completions.create.side_effect = [
            openai.OpenAIError("Hit request rate limit; retrying..."),
            None  # 假设重试后成功
        ]
        prompt = "Hello, world!"
        result = openai_completion(prompt, self.decoding_args, "text-davinci-003", 2, 1, 100, 100, True)
        self.assertIsNotNone(result)

    # 可以继续添加更多测试用例来检验错误处理、边界条件等


if __name__ == '__main__':
    unittest.main()
