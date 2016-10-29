from collections import OrderedDict


def _is_descriptor(obj):
    """Returns True if obj is a descriptor, False otherwise.
    From cpython Enum"""
    return (
            hasattr(obj, '__get__') or
            hasattr(obj, '__set__') or
            hasattr(obj, '__delete__'))


def _is_dunder(name):
    """Returns True if a __dunder__ name, False otherwise."""
    return (name[:2] == name[-2:] == '__' and
            name[2:3] != '_' and
            name[-3:-2] != '_' and
            len(name) > 4)


def _is_sunder(name):
    """Returns True if a _sunder_ name, False otherwise."""
    return (name[0] == name[-1] == '_' and
            name[1:2] != '_' and
            name[-2:-1] != '_' and
            len(name) > 2)


class FlagsMeta(type):
    """Metaclass for declaring Bitwise flags"""

    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __init__(cls, name, parents, dct):
        cls.__flags_members__ = {}
        for field, value in dct.items():
            if not _is_descriptor(value) and not _is_dunder(field) and not _is_sunder(field):
                if not isinstance(value, tuple):
                    args = (value,)
                else:
                    args = value

                setattr(cls, field, cls(*args))
                setattr(getattr(cls, field), "name", field)

                if (args[0] & (args[0] - 1)) == 0:
                    # Only show pure entries.
                    cls.__flags_members__[args[0]] = (getattr(cls, field))
        return super().__init__(name, parents, dct)


class Flags(metaclass=FlagsMeta):
    """Bitwise flags.

    Supports | operator, repr shows all flags."""
    def __init__(self, value):
        self.value = value

    def __or__(self, other):
        return type(self)(self.value | other.value)

    def __and__(self, other):
        return type(self)(self.value & other.value)

    def __repr__(self):
        return "<%s %s>" % (type(self).__name__, " | ".join((tpl.name for tpl in self.enabled_flags)))

    def __eq__(self, other):
        """Exact value equality."""
        return self.value == other.value

    def __hash__(self):
        return self.value.__hash__()

    @property
    def enabled_flags(self):
        """Return the objects for each individual set flag."""
        if not self.value:
            yield self.__flags_members__[0]
            return

        val = self.value
        while val:
            lowest_bit = val & -val
            val ^= lowest_bit
            yield self.__flags_members__[lowest_bit]

    def contains_any(self, other):
        """Check if any flags are set.

        (OsuMod.Hidden | OsuMod.HardRock) in flags # Check if either hidden or hardrock are enabled.
        OsuMod.keyMod in flags # Check if any keymod is enabled.
        """
        return self.value == other.value or self.value & other.value

    __contains__ = contains_any

    def contains_all(self, other):
        """Checks if all flags are set.

        flags.contains_all(OsuMod.Hidden | OsuMod.HardRock) # Check if both hidden and hardrock are enabled."""
        return (self.value & other.value) == other.value
