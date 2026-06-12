from dotenv import load_dotenv

load_dotenv(override=True)

# Check Azure OpenAI configuration (see `.env` in the project root).

import os

azure_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")

if azure_key and azure_endpoint:
    print(f"Azure OpenAI API key exists and begins {azure_key[:8]}")
    print(f"Endpoint: {azure_endpoint}")
    if chat_deployment:
        print(f"Chat deployment: {chat_deployment}")
    else:
        print("Set AZURE_OPENAI_CHAT_DEPLOYMENT_NAME (or AZURE_OPENAI_DEPLOYMENT) to your model deployment name.")
else:
    print("Azure OpenAI not configured — set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in `.env` (see setup folder).")


# Import the Azure OpenAI client (OpenAI-compatible chat API on Azure).

from openai import AzureOpenAI

# Azure OpenAI client: endpoint, key, and API version come from `.env`.
# `MODEL` must match the deployment name in Azure OpenAI Studio (one deployment may map to e.g. GPT-4.1 or GPT-5).

import os

azure_client = AzureOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

MODEL = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")
