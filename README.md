# Diaml

### What is this repo?

This repo hosts utilities relating to DiaML, such as the specification, and corresponding parsers and validators.

### DiaML Validator

Check whether a string is a valid DiaML formatted call.
Currently, the validation function is not very strict.
 - It only checks if DiaML is followed for each line independently of other lines.
 - Doesn't check other things, such as:
    1. `<user>` tag always follows `<API>` or `<agent>` tag
    2. `<API>` tag always follows `<system>` tag
    3. `<system>` will only come after an `<API>` tag
    4. etc..

```python
from validator import validate_diaml
    good_call = '''CLIENT_CONFIG: {"Agent Name": "Amanda", "Auth 1": "null", "Auth 2": "null", "Auth required": "No", "Client": "ETG Credit collections", "Creditor": "null", "No. of Auth steps": 0}
USER_METADATA: {"Due Amount": "1500", "First Name": "Surya", "Last Name": "Kant"}
CALL:
<agent>Hello, is this Surya Kant speaking?
<user>Yes, this is Surya speaking. May I know who is calling, please?
<agent>Hi Surya, this is Amanda calling from ETG Credit collections. How are you doing today?
<user>I'm doing good, thank you. But why is the collections department calling me?
<agent>We have sent you letters and emails regarding an unpaid balance on your credit card. Are you aware of this?
<user>Oh yes, I remember getting those. I have been meaning to pay it off, but I haven't had the chance yet.
<agent>I understand that can happen. Before we proceed, I need to verify your identity. Can you please confirm your date of birth for me?
<user>Sure, it's January 12th, 1985.
<API>VerifyDOB(input="12-January-1985")
<system>{status: success}
<agent>Great! Thank you for confirming that. So, your outstanding balance is $1500. Can you make a payment today to settle the account?
<user>Yes, I can pay it in full right now. How can I do that?
<agent>That's great to hear, Surya. You can pay through our online portal, or I can send you a payment link through SMS. Which option do you prefer?
<user>I would prefer the payment link through SMS. That would be easier for me.
<API>SMSPaymentLink()
<system>{status: success}
<agent>You should receive the link in a few moments. Once you have made the payment, please let me know so that I can confirm it on my end.
<user>Alright, I will do that. Thank you for your help, Amanda.
<agent>You're welcome, Surya. Thank you for resolving this matter. Have a great day!
<API>Hangup()
<system>{status: success}'''
    assert(validate_diaml(good_call, verbose=True))
    # no error

    bad_call = '''CLIENT_CONFIG: {"Agent Name": "Amanda", "Auth 1": "null", "Auth 2": "null", "Auth required": "No", "Client": "ETG Credit collections", "Creditor": "null", "No. of Auth steps": 0}
USER_METADATA: {"Due Amount": "1500", "First Name": "Surya", "Last Name": "Kant"}
CALL:
<agent>Hello, is this Surya Kant speaking?
<user>Yes, this is Surya speaking. May I know who is calling, please?
<agent>Hi Surya, this is Amanda calling from ETG Credit collections. How are you doing today?
<user>I'm doing good, thank you. But why is the collections department calling me?
<agent>We have sent you letters and emails regarding an unpaid balance on your credit card. Are you aware of this?
<user>Oh yes, I remember getting those. I have been meaning to pay it off, but I haven't had the chance yet.
<agent>I understand that can happen. Before we proceed, I need to verify your identity. Can you please confirm your date of birth for me?
<user>Sure, it's January 12th, 1985.
<API>VerifyDOB(input="this is an example")
<system>{status: success}
<agent>Great! Thank you for confirming that. So, your outstanding balance is $1500. Can you make a payment today to settle the account?
<user>Yes, I can pay it in full right now. How can I do that?
<agent>That's great to hear, Surya. You can pay through our online portal, or I can send you a payment link through SMS. Which option do you prefer?
<user>I would prefer the payment link through SMS. That would be easier for me.
<API>SMSPaymentLink()
<system>{status: success}
<agent>You should receive the link in a few moments. Once you have made the payment, please let me know so that I can confirm it on my end.
<user>Alright, I will do that. Thank you for your help, Amanda.
<agent>You're welcome, Surya. Thank you for resolving this matter. Have a great day!
<API> Hangup()
<system>{status: success}'''
    assert(not validate_diaml(bad_call, verbose=True))
    '''
    Error on line 23: Invalid API tag format.
    Line:  <API> Hangup()
    Error on line 12: Invalid API tag format.
    Line:  <API>VerifyDOB(input=12-January-1985)
    '''

```