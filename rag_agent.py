import os
import json
from typing import List
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def generate_with_llm(system_prompt: str, user_prompt: str, max_tokens: int = 512) -> str:
    # Try Streamlit secrets first (for cloud deployment)
    try:
        openai_key = st.secrets.get("OPENAI_API_KEY")
    except:
        # Fallback to environment variable (for local development)
        openai_key = os.environ.get('OPENAI_API_KEY')
    
    if openai_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[LLM call failed: {e}]"
    
    return "[LLM not configured] Please set OPENAI_API_KEY"


def build_test_case_prompt(context_chunks: List[str], user_query: str) -> str:
    joined = '\n\n---\n\n'.join(context_chunks)
    prompt = f"""You are a QA engineer. Use only the following context (do not hallucinate):

{joined}

User request: {user_query}

Produce structured test cases in JSON array format where each test case contains: Test_ID, Feature, Test_Scenario, Steps (array), Expected_Result, Grounded_In (source)."""
    return prompt


def build_script_prompt(html_content: str, selected_test_case: dict, context_chunks: List[str]) -> str:
    joined = '\n\n---\n\n'.join(context_chunks)
    prompt = f"""You are a Selenium (Python) expert. Use only the provided HTML and context to generate a runnable Selenium Python script that implements this test case.

HTML:
{html_content}

Context:
{joined}

Test case JSON:
{json.dumps(selected_test_case, indent=2)}

Requirements:
- Use webdriver.Chrome() and selenium best practices (explicit waits)
- Use selectors that exist in the HTML (ID, name, or CSS selectors)
- The script should be runnable as 'python script.py'

Return only the Python script (no explanation)."""
    return prompt