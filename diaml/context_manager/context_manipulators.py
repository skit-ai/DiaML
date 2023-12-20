import re
import diaml.data.tokens
from abc import ABC
from typing import List


# this module parses the request content
# before it is consumed by the LLM

class ContextManipulator(ABC):
    def __call__(self, context: str, *args, **kwargs) -> str:
        pass
        

# Define a class to execute a chain of manipulators
class ContextManipulatorChain:
    def __init__(self, manipulators: List[ContextManipulator]=[]):
        self.manipulators = manipulators

    def add_manipulator(self, manipulator):
        self.manipulators.append(manipulator)

    def __call__(self, context: str):
        result = context
        for manipulator in self.manipulators:
            result = manipulator(result)
        return result


class UnknownPruner(ContextManipulator):
    """
    Example 1:
        print(input_text)
        ```
        <agent>am i speaking with biswaroop?
        <user>__unknown__
        <agent>sorry say that again
        <user>yes
        ```
    Example 2:
        print(input_text)
        ```
        <agent>am i speaking with biswaroop?
        <user>__unknown__
        <agent>sorry say that again
        <user>__unknown__
        ```
    """
    def __init__(self, verbose: bool = True):
        super().__init__()

        self.verbose = verbose
        unknown_turn = f"{diaml.data.tokens.USER_TAG}{diaml.data.tokens.UNKNOWN_MESSAGE}"

        self.pattern = re.compile(
            rf'(({unknown_turn}{diaml.data.tokens.EOS_TOKEN}\s*{diaml.data.tokens.AGENT_TAG}.*?{diaml.data.tokens.EOS_TOKEN}\s*)+)(?={diaml.data.tokens.USER_TAG}[^_]|{diaml.data.tokens.AGENT_TAG})'
        )



    def clean_text(self, text):
        return text.replace("<user> ", "<user>")

    ## state: this removes all unknown turns with a turn (agent or API) after it.
    # EOS is defined by '\n'
    def __call__(self, context: str):
        """
        output: str
        Example 1:
            print(output)
            ```
            <agent>am i speaking with biswaroop?
            <user>yes
            ```
        Example 2:
            print(output)
            ```
            <agent>am i speaking with biswaroop?
            <user>__unknown__
            <agent>sorry say that again
            <user>__unknown__
            ```
        """
        if self.verbose:
            print("Inside pre processor:", context)

        processed = self.clean_text(context)

        if self.pattern.search(processed):
            processed = self.pattern.sub("", processed)

            if self.verbose:
                print("Unknown turns being removed..")
                print(f"Processed output: {processed}")
        
        return processed

