from langchain import hub
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI 


from langchain_experimental.utilities.python import PythonREPL
from langchain.tools import Tool

from dotenv import load_dotenv


import os

load_dotenv()

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
API_KEY = os.getenv("OPENAI_API_KEY")
TOOL_PROMT_TEMPLATE = """
Create a Python code to execute the following task:

{user_task}

Only output the code. Do not include anything else in your output.
"""

llm = ChatOpenAI(api_key=API_KEY, model_name="gpt-4")

# Invoke llm to create code
task = "Convert 39 degrees Celsius to Farenheit."
prompt = TOOL_PROMT_TEMPLATE.format(user_task=task)
print(f"Prompt: {prompt}")
response = llm.invoke(prompt)
print(f"Response: \n{response.content}")
code = response.content

# create and invoke repl tool to execute created code
python_repl = PythonREPL()
repl_tool = Tool(
    name = "python_repl",
    description = "A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func = python_repl.run,
)

input = {
    "input": code
}
code_result = repl_tool.invoke(input)
print(f"Result: \n{code_result}")

"""
Output:

Prompt: 
Create a Python code to execute the following task:

Convert 39 degrees Celsius to Farenheit.

Only output the code. Do not include anything else in your output.

Response: 
celsius = 39
fahrenheit = (celsius * 9/5) + 32
print(fahrenheit)
Python REPL can execute arbitrary code. Use with caution.
Result: 
102.2


"""


