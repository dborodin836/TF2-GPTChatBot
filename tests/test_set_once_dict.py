import pytest

from modules.set_once_dict import SetOnceDictionary, DeletionOfSetKey, ModificationOfSetKey


def test_read():
    expected = "test"
    d = SetOnceDictionary()
    d["test"] = expected
    assert expected == d["test"]


def test_overwrite():
    d = SetOnceDictionary()
    d["test"] = "test"
    with pytest.raises(ModificationOfSetKey):
        d["test"] = "test_overwrite"


def test_delete():
    d = SetOnceDictionary()
    d["test"] = "test"
    with pytest.raises(DeletionOfSetKey):
        del d["test"]
