from diaml.parser import ResponseProcessor

p = ResponseProcessor(verbose=False)

def test_postprocessor():
    # print("doing test....")
    func1 = p.parse_raw_message

    text = '<agent>Let me verify this.\n<API>VerifySSN(input=8898, number=1123)'
    assert func1(text) == {'message':'Let me verify this.', 'api_name':'VerifySSN', 'api_args':{'input': '8898', 'number': '1123'}, 'keywords': []}

    text = '<agent>Let me process this request for you\n<API>VerifyDOB(key="this is, a value", 3213=2312)'
    assert func1(text) == {'message':'Let me process this request for you', 'api_name':'VerifyDOB', 'api_args':{'key': 'this is, a value', '3213': '2312'}, 'keywords': []}

    text = '<agent>I am calling about a debt'
    assert func1(text) == {'message':'I am calling about a debt', 'api_args':{}, 'api_name':'', 'keywords': []}

    text = '<agent>Sorry agents not available. Hanging up'
    assert func1(text) == {'message':'Sorry agents not available. Hanging up', 'api_args':{}, 'api_name':'', 'keywords':[]}

    text = '<agent>Please press pound key once payment is completed. If you face any trouble press star key.\n<API>telephonyInputDTMF(num_digits=1, dtmf_max_wait_time=10)'
    assert func1(text) =={'message':'Please press pound key once payment is completed. If you face any trouble press star key.', 'api_name':'telephonyInputDTMF', 'api_args':{'num_digits': '1', 'dtmf_max_wait_time': '10'}, 'keywords':[]}

    text = '<agent>Please press pound key once payment is completed. If you face any trouble press star key.\n<API>telephonyInputDTMF(num_digits=1)'
    assert func1(text) == {'message': 'Please press pound key once payment is completed. If you face any trouble press star key.', 'api_name':'telephonyInputDTMF', 'api_args':{'num_digits': '1'}, 'keywords':[]}

    text = '<agent>I will transfer you to one of our agents to assist with the payment. Just a moment, please.\n<API>telephonyAgentTransfer()'
    assert func1(text) == {'message':'I will transfer you to one of our agents to assist with the payment. Just a moment, please.', 'api_name':'telephonyAgentTransfer', 'api_args':{}, 'keywords':[]}

    text = '<agent>Of course, [first_name]. May I send the payment link to your cell phone number ending in [last_4_digits]?'
    assert func1(text) == {'message':'Of course, [first_name]. May I send the payment link to your cell phone number ending in [last_4_digits]?', 'api_name':'', 'api_args':{}, 'keywords': []}
    # print("All tests passed")
