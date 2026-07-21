from writer.file_writer import FileWriter


def test_writer():

    writer = FileWriter()

    writer.write(
        "test/main.py",
        "print('Hello')"
    )

    print("Writer Test Passed")