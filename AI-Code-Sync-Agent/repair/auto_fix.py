from repair.error_reader import ErrorReader
from repair.log_parser import LogParser
from repair.fix_generator import FixGenerator


class AutoFix:

    def __init__(self):

        self.reader = ErrorReader()

        self.parser = LogParser()

        self.generator = FixGenerator()

    def analyze(self, runner_result):

        log = self.reader.from_result(
            runner_result
        )

        issues = self.parser.parse(log)

        fixes = self.generator.generate(
            issues
        )

        return {

            "issues": issues,

            "fixes": fixes,

            "log": log
        }