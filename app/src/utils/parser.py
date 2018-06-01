"""
Parsers for various sources of data
"""
import re


LOG_MESSAGE_REGEX = re.compile(r"^(?<date>\d{4}\/\d{2}\/\d{2})"
                               r" (?<time>\d{2}:\d{2}:\d{2}) \d{9}"
                               r" [a-z0-9]{2,3} \[.*?\] (?<message>.+)$")
AREA_ENTER_REGEX = re.compile(r"^: You have entered (?P<area_name>.+)$")
LEVEL_UP_REGEX = re.compile(r"^: (?P<character_name>.+) \((?P<ascendency>.+)\)"
                            r" is now level (?P<character_level>.+)$")
SKILL_UP_REGEX = re.compile(r"^Successfully allocated passive skill id: "
                            r"(?P<skill_id>.+), name: (?P<skill_name>.+)$")

LOG_MESSAGE_TYPES = ['invalid', 'area_enter', 'level_up', 'skill_up']
LOG_REGEX_RULES = {
    'area_enter': {
        'regex_str': AREA_ENTER_REGEX,
        'regex_group_data': [
            'area_name',
        ]
    },
    'level_up': {
        'regex_str': LEVEL_UP_REGEX,
        'regex_group_data': [
            'character_name',
            'acendency',
            'character_level'
        ]
    },
    'skill_up': {
        'regex_str': SKILL_UP_REGEX,
        'regex_group_data': [
            'skil_id',
            'skill_name',
        ]
    },
}


class ClientLogParser:
    """ Parses the game client log file """

    def __init__(self):
        self.MESSAGE_TYPES = LOG_MESSAGE_TYPES
        self.LOG_REGEX_RULES = LOG_REGEX_RULES

        self.log = ""
        self.message = ""
        self.message_type = ""
        self.message_data = {}

    def parse_log(self, log):
        """
        Parses out data from a given client log string
        """
        self.log = log
        match = re.match(LOG_MESSAGE_REGEX, log)
        if match:
            self.message = match.group('message')

        self.get_message_data()

        return

    def get_message_data(self):
        self.message_type = ""
        self.message_data = {}
        for type_name, regex_rules in self.LOG_REGEX_RULES:
            match = re.match(regex_rules.regex_str, self.message)
            if match:
                self.message_type = type_name
                for data_name in regex_rules.regex_group_data:
                    self.message_data[data_name] = match.group(data_name)
                return

        self.message_type = 'invalid'
        return
