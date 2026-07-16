from pathlib import Path


# todo add proper error handling and tests
def read_file(file_path: str) -> str:
    """Returns the string contents of a given file.

    Args:
      file_path The abs path of the file

    Returns:
      Contents of the file as string
    """
    try:
        data_file = Path(__file__).parent / file_path
        with open(data_file, "r", encoding="utf-8") as f:
            content = f.read()
            print(content)
            return content
    except Exception as e:
        raise e
