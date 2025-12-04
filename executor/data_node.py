from agent_framework import Executor, WorkflowContext, handler
from typing import Dict, Any

class DataNodeExecutor(Executor):

    def __init__(self, id: str, data_tool):
        super().__init__(id=id)
        self.data_tool = data_tool

    @handler
    async def handle(self, payload: Dict[str, Any], ctx: WorkflowContext):
        nl_query = payload["nl_query"]
        result = self.data_tool.nl_query(nl_query)

        updated = dict(payload)
        updated["db_result"] = result
        
        await ctx.send_message(updated) # type: ignore