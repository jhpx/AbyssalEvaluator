# mvenum.py

from enum import Enum


class MVEnum(Enum):
    """允许多值定位的枚举类"""

    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values
        return obj

    def mv_value(self, index):
        return self._all_values[index]

    # def __repr__(self):
    #     return '<%s.%s: %s>' % (
    #         self.__class__.__name__,
    #         self._name_,
    #         ', '.join([repr(v) for v in self._all_values]),
    #     )
