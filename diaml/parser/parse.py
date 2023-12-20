import re
from pydantic import BaseModel
from typing import Dict, List

import diaml.data.tokens

# this module parses the LLM response (~DiaML)
# before it is consumed by the orchestrator (~Vanir)

class ResponseProcessor(BaseModel):
    """
    Example 1:
        input_str = "<agent>am i speaking with biswaroop?</s>\n<user>yes who is this</s>\n"
        output = LM(input_str)
        print(output)
        ```
        <agent>This is a voice assistant
        ```
    Example 2:
        input_str = "<agent>Can you tell me your date of birth?</s>\n<user>January 19 1999</s>\n"
        output = LM(input_str)
        print(output)
        ```
        <agent>Let me check that for you
        <API>VerifyDOB(1999-01-19)
        ```
    """
    verbose: bool = True
    api_: str = diaml.data.tokens.API_TAG
    agent_: str = diaml.data.tokens.AGENT_TAG
    special_tokens: List = diaml.data.tokens.SPECIAL_TOKENS

    agent_pattern: re.Pattern = re.compile(r'<(\w+)>(.*)')
    api_pattern: re.Pattern = re.compile(r'<([^>]+)>(\w+)\(([^)]*)\)')
    args_pattern: re.Pattern = re.compile(r'(\w+)\s*=\s*(".*?"|[^,$]+)')

    def _remove_tokens(self, text: str):
        for token in self.special_tokens:
            text = text.replace(token, "")
        return text.strip()

    ## parse <API> turn
    def parse_api(self, text: str):
        match = self.api_pattern.match(text)
        assert match
        message_type, message, message_arg = match.groups()

        args = {}
        if message_arg != '':
            message_args = self.args_pattern.findall(message_arg)
            for item in message_args:
                k, v = item
                args[k] = v.strip('\"').strip('\'')  ## remove enclosing double quotes
        return [self._remove_tokens(message), args]

    ## parse <agent> turn
    def parse_agent(self, text: str):
        match = self.agent_pattern.match(text)
        agent, message = match.groups()
        ## keywords are only parsed in <agent> turn
        keywords: List = [token for token in self.special_tokens if token in message]
        # return [agent, self._remove_tokens(message), {}, keywords]
        return [self._remove_tokens(message), keywords]

    def parse_raw_message(self, raw_message: str) -> Dict:
        """
        output: Dict
        Example 1: {"message":"This is a voice assistant", "api_name":"", "api_args":{}, "keywords":[]}
        Example 2: {"message":"Let me check that for you", "api_name":"VerifyDOB", "api_args":{"input": "1999-01-19"}, "keywords":[]}
        """
        if self.verbose:
            print("inside parser:", raw_message)

        messages = raw_message.split('\n')
        parsed = {
            "message": "",
            "api_name": "",
            "api_args": {},
            "keywords": []
        }

        agent_message = messages[0]
        if self.agent_ in agent_message:
            parsed_agent = self.parse_agent(agent_message)
            parsed["message"] = parsed_agent[0]
            parsed["keywords"] = parsed_agent[1]
        else:
            raise Exception(f"Value error. AGENT token not present: {agent_message}")
        
        if len(messages) > 1:
            api_message = messages[1]
            if self.api_ in api_message:
                parsed_api = self.parse_api(api_message)
                parsed["api_name"] = parsed_api[0]
                parsed["api_args"] = parsed_api[1]
            else:
                raise Exception(f"Value error. API token not present: {api_message}")

        return parsed
