from pathlib import Path


class ProjectDetector:

    PROJECT_FILES = {
        "node": "package.json",
        "python": "requirements.txt",
        "java": "pom.xml",
        "dotnet": "*.csproj",
        "flutter": "pubspec.yaml",
        "rust": "Cargo.toml",
        "go": "go.mod"
    }

    def detect(self, project_path):

        root = Path(project_path)

        for project_type, file in self.PROJECT_FILES.items():

            if "*" in file:

                if list(root.glob(file)):
                    return project_type

            else:

                if (root / file).exists():
                    return project_type

        return "unknown"