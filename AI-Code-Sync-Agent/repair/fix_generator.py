class FixGenerator:

    FIXES = {

        "module_not_found":
            "Install the missing dependency and verify import paths.",

        "syntax_error":
            "Check the reported line for invalid syntax.",

        "import_error":
            "Verify the module exists and the import statement is correct.",

        "type_error":
            "Check argument types and function signatures.",

        "reference_error":
            "Ensure the referenced variable is defined before use.",

        "file_not_found":
            "Verify the file path exists.",

        "permission":
            "Check file or folder permissions."
    }

    def generate(self, issues):

        suggestions = []

        for issue in issues:

            if issue in self.FIXES:

                suggestions.append({

                    "issue": issue,

                    "suggestion": self.FIXES[issue]

                })

        return suggestions