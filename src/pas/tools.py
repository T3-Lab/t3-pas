from dotenv import load_dotenv
load_dotenv()

from typing import Dict, Optional
from .state import AgentState

_HAS_REQUESTS = True
_HAS_BS4 = True
try:
    import requests
except Exception:
    _HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
except Exception:
    _HAS_BS4 = False

def calculator(expression):
    """
    Simple calculator.
    """
    import ast

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.FloorDiv
    )

    try:
        node = ast.parse(expression, mode="eval")

        for n in ast.walk(node):
            if not isinstance(n, allowed_nodes):
                return {
                    "type": "error",
                    "success": False,
                    "result": "Unsupported expression"
                }

        compiled = compile(node, filename="<ast>", mode="eval")
        result = eval(compiled, {"__builtins__": {}}, {})

        return {
            "type": "single_dict",
            "success": True,
            "result": f"The answer of {expression} is {result}"
        }

    except Exception as e:
        return {
            "type": "error",
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
        "type": "single_dict",
        "success": True,
        "result": f"What is {num1} + {num2}?",
        "answer": answer
    }

def summarizer(text):
    """
    Summarize text using Hugging Face transformers.
    """
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    
    inputs = tokenizer(f"summarize: {text}", return_tensors="pt")
    
    outputs = model.generate(**inputs, max_new_tokens=60, min_new_tokens=20, do_sample=False)

    summary_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {
        "type": "single_dict",
        "success": True,
        "result": summary_text
    }

def scrape_web(url: str) -> Dict[str, Optional[str]]:
    """
    Do web scrapping.
    """
    fallback_result = {
        "title": None, 
        "content": None, 
        "status": "failed", 
        "error": None
    }
    
    if not url or not isinstance(url, str) or not url.startswith(("http://", "https://")):
        fallback_result["error"] = f"Invalid URL format"
        return {
            "type": "nested_single_dict",
            "success": False,
            "result": fallback_result
        }

    if not _HAS_REQUESTS or not _HAS_BS4:
        fallback_result["error"] = "Missing optional dependencies: requests or bs4"
        return {
            "type": "nested_single_dict",
            "success": False,
            "result": fallback_result
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)

        response.raise_for_status()

    except Exception as e:
        msg = str(e)
        if "timeout" in msg.lower():
            fallback_result["error"] = "Request timeout"
        elif "connection" in msg.lower():
            fallback_result["error"] = "Connection error"
        else:
            status_code = getattr(e, 'response', None)
            if status_code is not None and hasattr(status_code, 'status_code'):
                fallback_result["error"] = f"HTTP Error: {status_code.status_code}"
            else:
                fallback_result["error"] = f"Request Error: {msg}"

        return {
            "type": "nested_single_dict",
            "success": False,
            "result": fallback_result
        }

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        content = soup.get_text(separator="\n", strip=True)
        fallback_result["title"] = title
        fallback_result["content"] = content
        fallback_result["status"] = "success"
        
        return {
            "type": "nested_single_dict",
            "success": True,
            "result": fallback_result
        }
        
    except Exception as parse_err:
        fallback_result["error"] = f"Parsing Error: {str(parse_err)}"
        return {
            "type": "nested_single_dict",
            "success": False,
            "result": fallback_result
        }

TOOLS = {
    "calculator": calculator,
    "math_problem": math_problem_gen,
    "summarizer": summarizer,
    "web_scrapper": scrape_web
}

TOOL_KIND_MAP = {
    "with_input": ["calculator", "summarizer", "web_scrapper"],
    "no_input": ["math_problem"]
}

STATE_MAP = {
    "calculator": AgentState.CALCULATING,
    "math_problem": AgentState.WAITING_ANSWER,
    "summarizer": AgentState.SUMMARIZING,
    "web_scrapper": AgentState.WEB_SCRAPING
}

TYPE_MAP = {
    "calculate": "single_dict",
    "math_problem": "single_dict",
    "summarize_content": "single_dict",
    "web_scrape": "nested_single_dict",
    "analyze_web": "nested_multi_dict"
}