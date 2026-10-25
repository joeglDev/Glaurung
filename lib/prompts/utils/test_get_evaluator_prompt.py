from lib.prompts.utils.get_evaluator_prompt import get_evaluator_prompt
import pytest


class TestGetEvaluatorPrompt:
    def test_raises_value_error_when_output_is_whitespace_or_empty(self):
        with pytest.raises(ValueError) as exc:
            get_evaluator_prompt(input_prompt="hello", output="  ")
        assert "Input and output prompts must have string content." in str(exc.value)

        with pytest.raises(ValueError) as exc:
            get_evaluator_prompt(input_prompt="hello", output="")
        assert "Input and output prompts must have string content." in str(exc.value)

    def test_raises_value_error_when_input_is_whitespace_or_empty(self):
        with pytest.raises(ValueError) as exc:
            get_evaluator_prompt(input_prompt=" ", output="b")
        assert "Input and output prompts must have string content." in str(exc.value)

        with pytest.raises(ValueError) as exc:
            get_evaluator_prompt(input_prompt="", output="b")
        assert "Input and output prompts must have string content." in str(exc.value)

    def test_prompt(self):
        result = get_evaluator_prompt(input_prompt="a", output="b")
        assert (
            result
            == """
You are a helpful assistant. 
Your job is to determine if the output text answers the question of the input text
or resolves the problem posed by the input text.

If the answer is yes then return 1.
If the answer is no then return 0.

The response should be either 1 or 0 exactly, do not provide additional responses or context.

The texts to evaluate are below:
<input>
a
</input>

<output>
b
</output>
"""
        )
