def calculator(expression):
    """
    Simple calculator.
    """

    try:
        result = eval(expression)
        return {
            "success": True,
            "result": f"The answer of {expression} is {result}"
        }

    except Exception as e:
        return {
            "success": False,
            "result": str(e)
        }
    
def math_problem_gen():
    """
    Generate simple math problem with random number generator.
    """
    import random

    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    answer = num1 + num2

    return {
        "success": True,
        "result": f"What is {num1} + {num2}?",
        "answer": answer
    }


TOOLS = {
    "calculator": calculator,
    "math_problem": math_problem_gen
}