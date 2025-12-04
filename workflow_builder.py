from agent_framework import WorkflowBuilder

from executor.data_node import DataNodeExecutor
from executor.condition_node import ConditionNodeExecutor
from executor.human_node import HumanNodeExecutor

def build_freight_workflow(data_tool, threshold=670.0):

    builder = WorkflowBuilder()

    data_node = DataNodeExecutor("data_node", data_tool)
    condition_node = ConditionNodeExecutor("condition_node", threshold)
    human_node = HumanNodeExecutor("human_node")

    builder.set_start_executor(data_node)

    # Graph edges
    builder.add_edge(data_node, condition_node)
    builder.add_edge(condition_node, human_node)

    return builder.build()