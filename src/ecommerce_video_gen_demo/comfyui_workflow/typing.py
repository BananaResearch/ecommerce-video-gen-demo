from typing import TypedDict, Dict, Any

class ComfyuiWorkflowResult(TypedDict):
    prompt: Dict[str, Any]
    result_node_id: str
    