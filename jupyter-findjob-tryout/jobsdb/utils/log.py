"""
A simple logging utility for printing messages and saving them into a text file.
"""

# import necessary libraries
import os
import sys


def hello_world_log():
    """
    Prints the message 'Hello World'.
    This function doesn't take any arguments or return anything. It simply prints the message 'Hello World'.
    """
    print('Hello World')


def log_to_text_file(log_path, content):
    """
    Writes given content into specified text file path. If an error occurs during writing, prints exception details.

    Args:
        log_path (str): The path where the log file should be created/appended.
        content (list of str): List of strings containing the content to be written into the log file.

    Returns:
        None
    """
    try:
        with open(log_path, 'a') as f:
            # Appends new content instead of clearing existing ones
            f.write(content)
    except Exception as e:
        print("An error occurred while trying to write to the file.")
        print(str(e))

if __name__ == "__main__":
    # Test cases
    hello_world_log()
    log_to_text_file('/tmp/test.txt', ['Test Log Message 1', 'Test Log Message 2'])
