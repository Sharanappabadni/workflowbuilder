# db_workflow/llm.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

openai_api_key = os.getenv("OPEN_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openai_api_key
)

SQL_SYSTEM_PROMPT = """
        You are an expert SQL generator.
        Generate SQL **ONLY for PostgreSQL**. 
        Use PostgreSQL syntax for dates, intervals, functions.

        Rules:
        - For intervals, ALWAYS use: INTERVAL '<number> <unit>'
        Example: CURRENT_DATE - INTERVAL '90 days'
        - Do NOT use MySQL functions like CURDATE(), DATE_SUB(), NOW() - INTERVAL 90 DAY.
        - Do NOT add backticks.
        Return ONLY SQL without comments.
    """


def generate_sql(nl_query: str, schema: str) -> str:
    prompt = f"""
    Natural language request:
    {nl_query}

    Table schema:
    {schema}

    Return ONLY SQL:
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SQL_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip() # type: ignore
    return sql
