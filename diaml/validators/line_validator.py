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