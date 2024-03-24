from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class SetOnceDictionary(Generic[K, V], dict):
    def __setitem__(self, key: K, value: V):
        if self.get(key, None) is not None:
            raise ModificationOfSetKey("You cannot modify value after setting it.")
        super().__setitem__(key, value)

    def __delitem__(self, key: K):
        raise DeletionOfSetKey("You cannot delete value after setting it.")


class ModificationOfSetKey(Exception):
    pass


class DeletionOfSetKey(Exception):
    pass
