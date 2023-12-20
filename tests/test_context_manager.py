from diaml.context_manager import ContextManager
import diaml.data.tokens

metadata = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
''' 

result1 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
''' 

result2 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
<user>Okay</s>
''' 

result3 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
<user>Okay</s>
<agent>Alright, I am sending the message right away.
<API>SMSPaymentLink(amount="$[due_amount]")</s>
'''

result4 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
<user>Okay</s>
<agent>Alright, I am sending the message right away.
<API>SMSPaymentLink(amount="$[due_amount]")</s>
<system>{status:success}</s>
'''

def test_contextmanager():
    cm = ContextManager(metadata)

    # Njord generates the following:
    message = "<agent>Hello! Am I speaking with [first_name] [last_name]?"

    cm.stitch_bot_message_to_context(message)
    assert cm.get_context() == result1

    # user generates the following:
    message = "<user>Okay"

    cm.stitch_user_message_to_context(message)
    assert cm.get_context() == result2

    # agent generates the following:
    message = '''<agent>Alright, I am sending the message right away.
<API>SMSPaymentLink(amount="$[due_amount]")'''

    cm.stitch_bot_message_to_context(message)
    assert cm.get_context() == result3

    # system generates the following:
    message = '''<system>{status:success}'''

    cm.stitch_system_message_to_context(message)
    assert cm.get_context() == result4
