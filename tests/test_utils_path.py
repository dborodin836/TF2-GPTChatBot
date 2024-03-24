import pathlib
import sys

from modules.utils.path import resource_path


def test_resource_path():
    # Test case 1: Run the function in source mode
    expected_file = "relative_path"
    expected_path = pathlib.Path(__file__).parent.parent / expected_file

    assert expected_path == pathlib.Path(resource_path(expected_file))

    # Test case 2: Run the function in PyInstaller mode
    sys._MEIPASS = "/path/to/_MEIPASS"
    expected_path = pathlib.Path(sys._MEIPASS) / expected_file

    path = resource_path("relative_path")
    del sys._MEIPASS
    assert pathlib.Path(path) == expected_path
