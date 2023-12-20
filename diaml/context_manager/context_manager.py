import diaml.data
from diaml.context_manager.context_manipulators import ContextManipulatorChain, UnknownPruner

class ContextManager:
    def __init__(self, metadata: str, manipulator: ContextManipulatorChain=ContextManipulatorChain([UnknownPruner()])):
        '''`metadata` must be of the form:
        ```USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_TYPE: OUTBOUND
CALL:
```     Notably, it must end with `\n`!!
        '''
        self.metadata = metadata
        self.context = metadata
        self.manipulator = manipulator

    def stitch_user_message_to_context(
        self,
        user_utterance: str #without <EOS>
    ) -> None:
        '''Method that uses diaml.data.tokens.EOS_TOKEN to stitch context with a new user utterance.'''
        self.context += user_utterance + diaml.data.tokens.EOS_TOKEN + diaml.data.tokens.NEWLINE_TOKEN

    def stitch_bot_message_to_context(
        self,
        bot_utterance: str #without <EOS>
    ) -> None:
        '''Method that uses diaml.data.tokens.EOS_TOKEN to stitch context with a new bot utterance.'''
        self.context += bot_utterance + diaml.data.tokens.EOS_TOKEN + diaml.data.tokens.NEWLINE_TOKEN

    def stitch_system_message_to_context(
        self,
        system_message: str #without <EOS>
    ) -> None:
        '''Method that uses diaml.data.tokens.EOS_TOKEN to stitch context with a new user utterance.'''
        self.context += system_message + diaml.data.tokens.EOS_TOKEN + diaml.data.tokens.NEWLINE_TOKEN

    def get_context(self, use_manipulators: bool=True) -> str:
        context = self.context
        if use_manipulators:
            context = self.manipulator(context)
        return context