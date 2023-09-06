import re

def validate_diaml(call, verbose=False):
    # a loose check on DiaML format
    # only checks if DiaML is followed for each line independently of other lines.
    # doesn't check other things, such as:
    # 1. <user> tag always follows <API> or <agent> tag
    # 2. <API> tag always follows <system> tag
    # 3. <system> will only come after an <API> tag
    # etc..

    valid_tags = {"agent", "user", "API", "system"}

    api_pattern = re.compile(r'<API>[A-Za-z0-9_]+\(([^=]+="[^"]*"(, [^=]+="[^"]*")*)?\)')
    system_pattern = re.compile(r'<system>\{status: (success|fail)(,\s*metadata: "[^"]*")?\}')
    agent_pattern = re.compile(r'<agent>.+')

    current_line = 0
    lines = call.splitlines()
    if lines[0].find("CLIENT_CONFIG: ") == -1:
        if verbose:
            print(f"Error on line {current_line}: Invalid CLIENT_CONFIG format.")
            print("Line: ", lines[0])
        return False

    current_line = 1
    if lines[1].find("USER_METADATA: ") == -1:
        if verbose:
            print(f"Error on line {current_line}: Invalid USER_METADATA format.")
            print("Line: ", lines[1])
        return False

    current_line = 2
    if lines[2].find("CALL:") == -1:
        if verbose:
            print(f"Error on line {current_line}: Invalid USER_METADATA format.")
            print("Line: ", lines[2])
        return False

    current_line = 3
    for line in call.splitlines()[current_line:]:
        current_line += 1
        line = line.strip()

        if line.startswith("<"):
            match = re.match(r'<(agent|user|API|system)>\s*(.+)', line)
            if not match:
                if verbose:
                    print(f"Error on line {current_line}: Invalid tag format.")
                    print("Line: ", line)
                return False
            tag = match.group(1)

            if tag not in valid_tags:
                if verbose:
                    print(f"Error on line {current_line}: Invalid tag '{tag}'.")
                    print("Line: ", line)
                return False

            if tag == "API":
                if not api_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid API tag format.")
                        print("Line: ", line)
                    return False

            if tag == "system":
                if not system_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid system tag format.")
                        print("Line: ", line)
                    return False
                
            if tag == "agent":
                if not agent_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid agent tag format.")
                        print("Line: ", line)
                    return False
        else:
            return False
    return True

if __name__ == "__main__":
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
<API>VerifyDOB(input=12-January-1985)
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
<API>Hangup(abc=surya)
<system>{status: success}'''
    assert(not validate_diaml(bad_call, verbose=True))
