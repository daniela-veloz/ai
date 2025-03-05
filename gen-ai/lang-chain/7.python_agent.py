from langchain import hub
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI 


from langchain_experimental.utilities.python import PythonREPL
from langchain.tools import Tool
from base.llm_provider import LLMProvider


import os

"""
Build a Python agent that uses the Python REPL tool to execute Python commands. 
The agent will use the LLMProvider to interact with the deepseek-reasoner model to generate Python code based on the user's task. 
The agent will then execute the generated Python code using the Python REPL tool and return the output to the user.
"""

class PythonAgent:
    def __init__(self, tool):
        self.llm = LLMProvider("deepseek-reasoner").get_chat_open_ai()
        self.tool = tool
        self.tool_prompt_template = """
        Create a Python code to execute the following task:

        {user_task}

        Instructions:
        - Only output the code. Do not include anything else in your output.
        - Make sure python formatting is correct.
        """
        self.script = None # Place holder for the Python script that will be generated during runtime

    def run(self, user_task):
        messages = [{"role": "user", "content": self.tool_prompt_template.format(user_task=user_task)}]
        response = self.llm.invoke(messages)
        python_script = response.content.strip()
        print(f"LLM Response: \n{response.content}")


        input = {
            "input": python_script
        }
        # Execute script using the repl tool
        try:
            result = self.tool.invoke(input)
        except Exception as e:
            result = str(e)

        return result
    
class PythonTool:
    def __init__(self):
        python_repl = PythonREPL()
        self.repl_tool = Tool(
            name = "python_repl",
            description = "A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
            func = python_repl.run,
        )

    def get(self):
        return self.repl_tool
    
# Now let's can create an instance of the agent
python_tool = PythonTool().get()
python_agent = PythonAgent(python_tool)  

# convert 55 degrees Celsius to Farenheit
result = python_agent.run("Convert 55 degrees Celsius to Farenheit.")
print(f"result: {result}")

# Find the sum of the first 100 prime numbers.
result = python_agent.run("Find the sum of the first 100 prime numbers")
print(f"result: {result}")