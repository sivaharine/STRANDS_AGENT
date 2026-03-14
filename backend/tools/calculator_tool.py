from strands import tool

@tool
def calculate(expression: str):

    result = eval(expression)

    return str(result)