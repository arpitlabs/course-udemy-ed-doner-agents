from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, OpenAIResponsesModel, function_tool
from openai import AsyncAzureOpenAI
import os

def get_AzureOpenAIChatCompletionsModel(model_name: str=None) -> OpenAIChatCompletionsModel:
    """
    Get the OpenAI Chat Completions model name from environment variables.

    Args:
        model_name (str): The default model name to use if not set in environment variables.

    Returns:
        str: The model name to use for OpenAI Chat Completions.
    """
    # Load environment variables from .env file
    load_dotenv() 

    # Create an instance of AsyncAzureOpenAI with the provided API key, version, and endpoint
    azure_client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    # if model_name is not provided, try to get it from environment variables
    if not model_name:
        model_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")

    # Create an instance of OpenAIChatCompletionsModel with the azure_client and model_name
    azure_chat_model = OpenAIChatCompletionsModel(openai_client=azure_client, model=model_name)
    return azure_chat_model


def get_AzureOpenAIResponsesModel(model_name: str=None) -> OpenAIResponsesModel:
    """
    Get the OpenAI Responses model for Azure OpenAI.

    Returns:
        OpenAIResponsesModel: An instance of OpenAIResponsesModel configured for Azure OpenAI.
    """
    # Load environment variables from .env file
    load_dotenv() 

    # Create an instance of AsyncAzureOpenAI with the provided API key, version, and endpoint
    azure_client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

        # if model_name is not provided, try to get it from environment variables
    if not model_name:
        model_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")


    # Create an instance of OpenAIResponsesModel with the azure_client
    azure_responses_model = OpenAIResponsesModel(openai_client=azure_client, model=model_name)
    return azure_responses_model

@function_tool
async def azure_web_search(query: str) -> str:
    """
    Perform a web search using Azure OpenAI Responses API.

    Args:
        query (str): The search query.

    Returns:
        str: The search results.
    """
    load_dotenv()  # Load environment variables from .env file

    azure_client = AsyncAzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    resp = await azure_client.responses.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        input=query,
        tools=[{"type": "web_search"}],
    )
    parts = []
    for item in resp.output:
        if getattr(item, "type", None) == "message":
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", None) == "output_text":
                    parts.append(getattr(content, "text", ""))
    return "\n".join([p for p in parts if p]).strip() 