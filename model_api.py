import openai
from dotenv import load_dotenv
import time
from openai import OpenAI, AsyncOpenAI
import os
from mistralai.async_client import MistralAsyncClient
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


load_dotenv()
class BaseModelAPI():

    def __init__(self):
        load_dotenv()

    def _mistral_message_transform(self, messages):
        mistral_messages = []
        for message in messages:
            mistral_message = ChatMessage(
                role=message["role"], content=message["content"])
            mistral_messages.append(mistral_message)
        return mistral_messages

class SyncModelAPI(BaseModelAPI):

    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        print(f"OpenAI API Key: {openai_api_key}")
        self.openai_client = OpenAI(
            api_key= openai_api_key,
        )
        

        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.mistral_client = MistralClient(
            api_key = mistral_api_key,
        )

    def model_api(self, api_args):
        model = api_args["model"]
        if model.startswith("gpt"):
            result = self.openai_client.chat.completions.create(**api_args)
            result = result.choices[0].message.content
        elif model.startswith("mistral"):
            api_args["messages"] = self._mistral_message_transform(api_args["messages"])
            result = self.mistral_client.chat(**api_args)
            result = result.choices[0].message.content
        else:
            raise ValueError(f"Model `{model}` is not supported")
        return result

    def with_retry(self, api_args, max_retries=3):
        result = None
        for retry_count in range(1, max_retries):
            try:
                result = self.model_api(api_args)
                break
            except Exception as e:
                print("Error: ", e)
                time.sleep(retry_count)
        return result

class AsyncModelAPI(BaseModelAPI):

    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = AsyncOpenAI(
            api_key= openai_api_key,
        )
        
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        self.mistral_client = MistralAsyncClient(
            api_key = mistral_api_key,
        )

    async def model_api(self, api_args):
        model = api_args["model"]
        if model.startswith("gpt"):
            result =  await self.openai_client.chat.completions.create(**api_args)
            result = result.choices[0].message.content
        elif model.startswith("mistral"):
            api_args["messages"] = self._mistral_message_transform(api_args["messages"])
            result = await self.mistral_client.chat(**api_args)
            result = result.choices[0].message.content
        else:
            raise ValueError(f"Model `{model}` is not supported")
        return result

    async def with_retry(self, api_args, max_retries=3):
        result = None
        for retry_count in range(1, max_retries+1):
            try:
                result = await self.model_api(api_args)
                break
            except Exception as e:
                print("Error: ", e)
                time.sleep(retry_count*0.3)
        return result
