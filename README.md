# Diaml

![GitHub tag](https://img.shields.io/github/v/tag/skit-ai/diaml)

### What is this repo?

This repo hosts utilities relating to DiaML, such as the specification, and corresponding parsers and validators.

### DiaML Specification
To be written or linked.

### DiaML Parser
To be added.

### DiaML Validator
Check whether a string is a valid DiaML formatted call. Use the function
`diaml.validator.validate_diaml`.

Currently, the validation function is not very strict.
 - It only checks if DiaML is followed for each line independently of other lines.
 - Doesn't check other things, such as:
    1. `<user>` tag always follows `<API>` or `<agent>` tag
    2. `<API>` tag always follows `<system>` tag
    3. `<system>` will only come after an `<API>` tag
    4. etc..

Check out the tests (`poetry run pytest`) for good and bad cases for validator.
