from typing import List
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.chat import ChatCompletionMessageParam




class DouBaoGLMError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class DouBaoGLM():
    def __init__(self,api_key:str,model:str):
        self.api_key=api_key
        self.model= model
        self.client = Ark(api_key=self.api_key)
    
    def chat(self,messages:List[ChatCompletionMessageParam]):

        completion = self.client.chat.completions.create(
            model=self.model,
            messages = messages,
            max_tokens=4096,
            stream=False
        )
        return completion
