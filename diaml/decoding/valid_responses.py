class ValidResponseRegex:
    def __init__(self, allowed_apis):
        self.allowed_apis = allowed_apis

    def get_agent_pattern(self):
        return r'<agent>[^<]+(?:\s*\.?\s*\w+\s*(?:\[[^\]]*\])?)?'

    def get_agent_and_api_pattern(self):
        partial_regex = []
        for fn in self.allowed_apis:
            api_pattern = f'(<agent>[^<]+(?:\s*\n<API>{fn}\((?:\s*\w*="\$?\[[^\]]*\]"\s*,?\s*)*\))?)'
            partial_regex.append(api_pattern)
        return "|".join(partial_regex)

    def get_combined_pattern(self):
        agent_pattern = self.get_agent_pattern()
        agent_and_api_pattern = self.get_agent_and_api_pattern()
        combined_pattern = f'(?:{agent_pattern})|(?:{agent_and_api_pattern})'
        return combined_pattern