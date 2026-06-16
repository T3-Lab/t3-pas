from dotenv import load_dotenv
load_dotenv()

from typing import Dict, Optional
from dataclasses import dataclass
from enum import StrEnum, auto

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
    
def math_problem_gen(high_difficulty):
    """
    Generate simple math problem with random number generator.
    """
    import random

    if high_difficulty:
        num1 = random.randint(25, 100)
        num2 = random.randint(25, 100)

    else:
        num1 = random.randint(1, 25)
        num2 = random.randint(1, 25)
    
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
    result = {
        "title": None, 
        "content": None,
    }
    
    if not url or not isinstance(url, str) or not url.startswith(("http://", "https://")):
        return {
            "type": "error",
            "success": False,
            "result": "Invalid URL format"
        }

    if not _HAS_REQUESTS or not _HAS_BS4:
        return {
            "type": "error",
            "success": False,
            "result": "Missing optional dependencies: requests or bs4"
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
            result = "Request timeout"

        elif "connection" in msg.lower():
            result = "Connection error"

        else:
            status_code = getattr(e, 'response', None)
            if status_code is not None and hasattr(status_code, 'status_code'):
                result = f"HTTP Error: {status_code.status_code}"

            else:
                result = f"Request Error: {msg}"

        return {
            "type": "error",
            "success": False,
            "result": result
        }

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"
        
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
            
        content = soup.get_text(separator="\n", strip=True)
        result["title"] = title
        result["content"] = content
        
        return {
            "type": "nested_single_dict",
            "success": True,
            "result": result
        }
        
    except Exception as parse_err:
        result = f"Parsing Error: {str(parse_err)}"
        return {
            "type": "nested_single_dict",
            "success": False,
            "result": result
        }


class ToolCategory(StrEnum):
    SUMMARIZATION = auto()
    CALCULATION = auto()
    WEB_SCRAPING = auto()
    INTERACTION = auto()


@dataclass
class ToolSpec:
    name: str
    func: callable
    requires_input: bool
    output_type: str
    category: ToolCategory

TOOLS = {
    "calculator": ToolSpec(
        name="calculator",
        func=calculator,
        requires_input=True,
        output_type="single_dict",
        category=ToolCategory.CALCULATION
    ),
    "math_problem": ToolSpec(
        name="math_problem",
        func=math_problem_gen,
        requires_input=True,
        output_type="single_dict",
        category=ToolCategory.INTERACTION
    ),
    "summarizer": ToolSpec(
        name="summarizer",
        func=summarizer,
        requires_input=True,
        output_type="single_dict",
        category=ToolCategory.SUMMARIZATION
    ),
    "web_scraper": ToolSpec(
        name="web_scraper",
        func=scrape_web,
        requires_input=True,
        output_type="nested_single_dict",
        category=ToolCategory.WEB_SCRAPING
    )
}