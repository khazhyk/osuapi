class FlagsMeta(type):
    """Metaclass for declaring Bitwise flags"""
    def __init__(cls, name, parents, dct):
        cls.__flags_members__ = []
        for field, value in dct.items():
            if not callable(value) and not (field.startswith("__") and field.endswith("__")):
                setattr(cls, field, cls(value))

                if (value & (value - 1)) == 0:
                    # Only show pure entries.
                    cls.__flags_members__.append((getattr(cls, field), field))
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
        return "<{} {}>".format(type(self).__name__, " | ".join([tpl[1] for tpl in self.__flags_members__ if tpl[0] in self]))

    def __eq__(self, other):
        """Exact value equality."""
        return self.value == other.value

    def __contains__(self, other):
        """Check if any flags are set.

        (OsuMod.Hidden | OsuMod.HardRock) in flags # Check if either hidden or hardrock are enabled.
        OsuMod.keyMod in flags # Check if any keymod is enabled.
        """
        return self.value & other.value or self.value == other.value

    def all_set(self, other):
        """Checks if all flags are set.

        flags.all_set(OsuMod.Hidden | OsuMod.HardRock) # Check if both hidden and hardrock are enabled."""
        return (self.value & other.value) == other.value
