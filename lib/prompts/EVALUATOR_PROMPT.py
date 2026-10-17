EVALUATOR_PROMPT = """
You are a helpful assistant. 
Your job is to determine if the output text answers the question of the input text
or resolves the problem posed by the input text.

If the answer is yes then return 1.
If the answer is no then return 0.

The response should be either 1 or 0 exactly, do not provide additional responses or context.

The texts to evaluate are below:
<input>
{input_prompt}
</input>

<output>
{output}
</output>
"""


# TODO: write unite tests
def get_evaluator_prompt(input_prompt: str, output: str):
    return EVALUATOR_PROMPT.format(input_prompt=input_prompt, output=output)
