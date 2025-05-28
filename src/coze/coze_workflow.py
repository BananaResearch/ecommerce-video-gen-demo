import os 
from typing import Any, Dict
# Our official coze sdk for Python [cozepy](https://github.com/coze-dev/coze-py)
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth

def run_workflow(workflow_id: str,
    parameters: Dict[str, Any] | None = None,
    *,
    bot_id: str | None = None,
    app_id: str | None = None,
    is_async: bool = False,
    ext: Dict[str, Any] | None = None) -> str | None:
    """
    This example describes how to use the workflow interface to chat.
    """


    # Get an access_token through personal access token or oauth.
    coze_api_token = os.getenv('COZE_CN_API_TOKEN', '')
    # The default access is api.coze.com, but if you need to access api.coze.cn,
    # please use base_url to configure the api endpoint to access
    coze_api_base = COZE_CN_BASE_URL


    # Init the Coze client through the access_token.
    coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

    # Call the coze.workflows.runs.create method to create a workflow run. The create method
    # is a non-streaming chat and will return a WorkflowRunResult class.
    workflow = coze.workflows.runs.create(
        workflow_id=workflow_id,
        parameters=parameters,
        bot_id=bot_id,
        app_id=app_id,
        is_async=is_async,
        ext=ext,
    )

    print("workflow.data", workflow.data)

    return workflow.data