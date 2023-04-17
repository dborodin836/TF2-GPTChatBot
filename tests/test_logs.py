import os
import tempfile

from utils.logs import log_message, log_to_file, get_time_stamp

# Define test data
test_username = "test_user"
test_prompt = "test_prompt"
test_message = "test_message"


def test_log_message(capfd):
    # Call the log_message function
    log_message('CHAT', 'John', 'Hello, how are you?')

    # Capture the output that would normally be printed to the console
    out, err = capfd.readouterr()

    # Check that the output matches the expected format
    expected_output = f"[{get_time_stamp()}] (CHAT) User: 'John' --- 'Hello, how are you?'\n"
    assert out == expected_output


def test_log_to_file():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Set the log file path to be inside the temporary directory
        log_file_path = os.path.join(tmpdir, 'output.log')

        # Call the function that writes to the log file
        log_to_file('test message', log_file_path)

        # Check that the log file exists and contains the expected message
        with open(log_file_path, 'r') as f:
            assert 'test message' in f.read()
