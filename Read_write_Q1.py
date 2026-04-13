def read_file(file_name: str) -> str:
    """Reads and returns the content of a text file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()


def write_file(file_name: str, content: str) -> None:
    """Writes content to a text file."""
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)
