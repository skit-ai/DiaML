from diaml.context_manager import ContextManager
import pytest

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
    assert cm.get_context(use_manipulators=True) == result1

    # user generates the following:
    message = "<user>Okay"

    cm.stitch_user_message_to_context(message)
    assert cm.get_context(use_manipulators=True) == result2

    # agent generates the following:
    message = '''<agent>Alright, I am sending the message right away.
<API>SMSPaymentLink(amount="$[due_amount]")'''

    cm.stitch_bot_message_to_context(message)
    assert cm.get_context(use_manipulators=True) == result3

    # system generates the following:
    message = '''<system>{status:success}'''

    cm.stitch_system_message_to_context(message)
    assert cm.get_context(use_manipulators=True) == result4


context5 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>__unknown__</s>
'''

result5 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>Hello! Am I speaking with [first_name] [last_name]?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>__unknown__</s>
'''

context6 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>yes</s>
'''

result6 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>yes</s>
'''

context7 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>yes</s>
'''

result7 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>yes</s>
'''

context8 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>yes</s>
<agent>is your address indiranagar?</s>
<user>__unknown__</s>
<agent>sorry say that again</s>
<user>yes</s>
'''

result8 = '''USER_METADATA: {'first_name': 'Sarah', 'last_name': 'Brown', 'due_amount': 1562, 'last_4_digits_phone_number': 2457, 'user_address': '456 Oakwood Avenue Austin Texas', 'vehicle_details': '2016 Honda Accord'}
CLIENT_CONFIG: {'company_name': 'SameDay Auto', 'first_option': 1328, 'second_option': 1093, 'third_option': 937, 'minimum_acceptable': 781, 'Auth 1': 'address', 'Auth required': 'Yes', 'No. of Auth steps': 1}
CALL_METADATA: {""ALLOWED_API:[SMSPaymentLink, Hangup, CheckAgentAvailability, AgentTransfer, InputDTMF, Callback, CapturePayLaterDate]""}
CALL_TYPE: OUTBOUND
CALL:
<agent>am i speaking with biswaroop?</s>
<user>yes</s>
<agent>is your address indiranagar?</s>
<user>yes</s>
'''
def test_contextmanager_unknown_turns():
    cm = ContextManager("\n")
    cm.context = context5

    assert cm.get_context(use_manipulators=True) == result5

    cm = ContextManager("\n")
    cm.context = context6

    assert cm.get_context(use_manipulators=True) == result6

    cm = ContextManager("\n")
    cm.context = context7

    assert cm.get_context(use_manipulators=True) == result7

    cm = ContextManager("\n")
    cm.context = context8

    assert cm.get_context(use_manipulators=True) == result8

def test_contextmanager_assertion_error():
    with pytest.raises(AssertionError) as excinfo:
        cm = ContextManager("CALL:")

def test_contextmanager_assertion_error2():
    with pytest.raises(AssertionError) as excinfo:
        cm = ContextManager("")
