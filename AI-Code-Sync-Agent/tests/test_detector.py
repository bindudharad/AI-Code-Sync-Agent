from project.detector import ProjectDetector


def test_detector():

    detector = ProjectDetector()

    print(
        detector.detect(".")
    )