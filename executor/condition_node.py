from agent_framework import Executor, WorkflowContext, handler
from typing import Dict, Any

class ConditionNodeExecutor(Executor):

    def __init__(self, id: str, threshold: float):
        super().__init__(id=id)
        self.threshold = threshold

    @handler
    async def handle(self, payload: Dict[str, Any], ctx: WorkflowContext):
        stats = payload["db_result"]["stats"]
        avg = list(stats.values())[0]["avg"]  # auto pick first numeric column

        payload["avg_value"] = avg

        if avg > self.threshold:
            # Go to human approval
            await ctx.send_message(payload, target_id="human_node") # type: ignore
        else:
            # End workflow cleanly
            await ctx.yield_output(payload) # type: ignore
