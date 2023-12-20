import re
from diaml.decoding import ValidResponseRegex

# Initialize the RegexGenerator with allowed APIs
allowed_apis = ['Func1', 'Func2', 'Func3', 'SMSPaymentLink', 'telephonyInputDTMF', 'telephonyHangup']
rg = ValidResponseRegex(allowed_apis)

def test_agent_pattern():
    agent_pattern = rg.get_agent_pattern()
    agent_test_strings_match = [
        '<agent>this',
        '<agent>this is a test',
        '<agent>this is a test. Are you [first_name]?',
        '<agent>You owe $[due_amount]',
    ]
    for test_string in agent_test_strings_match:
        match = re.fullmatch(agent_pattern, test_string)
        assert match, f"Didn't match a string. Input: {test_string}"

    agent_test_strings_nomatch = [
        '<agent >this',
        '< agent>this is a test',
        'agent: You owe $[due_amount]',
    ]
    for test_string in agent_test_strings_nomatch:
        match = re.fullmatch(agent_pattern, test_string)
        assert not match, f"Matched a string that shouldn't be! Input: {test_string}"

def test_combined_pattern():
    combined_pattern = rg.get_combined_pattern()

    combined_test_strings_match = [
        '<agent>this',
        '<agent>this is a test. Are you [first_name]?',
        '<agent>You owe $[due_amount]',
        '''<agent>Alright, I am sending the message right away.\n<API>SMSPaymentLink(amount="$[due_amount]")''',
        '''<agent> Great. I’ve sent the payment link to your phone. Please press pound key once payment is completed. If you face any trouble press star key.\n<API>telephonyInputDTMF()''',
        '''<agent>Goodbye, [first_name].\n<API>telephonyHangup()'''
    ]
    for test_string in combined_test_strings_match:
        match = re.fullmatch(combined_pattern, test_string)
        assert match, f"Didn't match a string. Input: {test_string}"

    combined_test_strings_nomatch = [
        '<agent >this',
        '</agent>this is a test. Are you [first_name]?',
        'agent:You owe $[due_amount]',
        '''<agent>Alright, I am sending the message right away. <API>SMSPaymentLink(amount="$[due_amount]")''',
        '''<agent> Great. I’ve sent the payment link to your phone. Please press pound key once payment is completed. If you face any trouble press star key.\n<API>HallucinatedAPI()''',
        '''<agent>Goodbye, [first_name].\n<API>NoMatchFn()''',
        '''<agent>Goodbye, [first_name].\n<API>NoMatchFn(key1="value1")''',
    ]
    for test_string in combined_test_strings_nomatch:
        match = re.fullmatch(combined_pattern, test_string)
        assert not match, f"Matched a string that shouldn't be! Input: {test_string}"

if __name__ == "__main__":
    test_agent_pattern()
    test_combined_pattern()
    