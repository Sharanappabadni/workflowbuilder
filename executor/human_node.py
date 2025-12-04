from agent_framework import Executor, WorkflowContext, handler
from typing import Dict, Any

class HumanNodeExecutor(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)

    @handler
    async def handle(self, payload: Dict[str, Any], ctx: WorkflowContext):

        avg = payload["avg_value"]
        print(f"\n🚨 Freight Rate Alert: Average = {avg}")
        approval = input("Send alert email? (y/n): ").lower()

        if approval == "y":
            payload["approved"] = True
        else:
            payload["approved"] = False

        await ctx.yield_output(payload) # type: ignore
