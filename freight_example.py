import asyncio
from workflow_builder import build_freight_workflow
from tools.data_tool import DataTool

async def main():

    db_url = "postgresql://airflow:airflow@localhost:5432/postgres"
    schema = """
        freight_rates(
        origin VARCHAR,
        destination VARCHAR,
        rate FLOAT,
        contract_date DATE
        )
    """

    tool = DataTool(db_url, schema)

    workflow = build_freight_workflow(data_tool=tool, threshold=670.0)

    input_payload = {
        "nl_query": "Find average freight rate between Houston and Amsterdam in last 90 days"
    }

    async for event in workflow.run_stream(input_payload):
        print("[EVENT]", event)

if __name__ == "__main__":
    asyncio.run(main())
