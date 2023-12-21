import re
import diaml.data.tokens

def validate_diaml(call, verbose=False):
    # a loose check on DiaML format
    # only checks if DiaML is followed for each line independently of other lines.
    # doesn't check other things, such as:
    # 1. <user> tag always follows <API> or <agent> tag
    # 2. <API> tag always follows <system> tag
    # 3. <system> will only come after an <API> tag
    # etc..

    valid_tags = {diaml.data.tokens.AGENT_TAG, diaml.data.tokens.API_TAG, diaml.data.tokens.SYSTEM_TAG, diaml.data.tokens.USER_TAG}
    escaped_eos = re.escape(diaml.data.tokens.EOS_TOKEN)

    api_pattern = re.compile(rf'({diaml.data.tokens.API_TAG}[A-Za-z0-9_]+\(\s*(\w+="[^"]*"\s*,?\s*)*\))' + escaped_eos)
    system_pattern = re.compile(diaml.data.tokens.SYSTEM_TAG + r'\{status:(success|fail)(,\s*metadata: "[^"]*")?\}' + escaped_eos)
    agent_pattern = re.compile(rf'{diaml.data.tokens.AGENT_TAG}.+')

    call_lines = call.splitlines()
    for i, l in enumerate(call_lines):
        if l.find("CALL:") != -1:
            call_block_line = i + 1
            break

    current_line = call_block_line
    for line in call.splitlines()[current_line:]:
        current_line += 1
        line = line.strip()

        if line.startswith("<"):
            match = re.match(f"^{diaml.data.tokens.USER_TAG}|^{diaml.data.tokens.AGENT_TAG}|^{diaml.data.tokens.API_TAG}|^{diaml.data.tokens.SYSTEM_TAG}", line)

            if not match:
                if verbose:
                    print(f"Error on line {current_line}: Invalid tag format.")
                    print("Line: ", line)
                return False
            tag = match.group()

            if tag not in valid_tags:
                if verbose:
                    print(f"Error on line {current_line}: Invalid tag '{tag}'.")
                    print("Line: ", line)
                return False

            if tag == diaml.data.tokens.API_TAG:
                if not api_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid API tag format.")
                        print("Line: ", line)
                    return False

            if tag == diaml.data.tokens.SYSTEM_TAG:
                if not system_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid system tag format.")
                        print("Line: ", line)
                    return False

            if tag == diaml.data.tokens.AGENT_TAG:
                if not agent_pattern.match(line):
                    if verbose:
                        print(f"Error on line {current_line}: Invalid agent tag format.")
                        print("Line: ", line)
                    return False
        else:
            return False
    return True