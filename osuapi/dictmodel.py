from enum import Enum
import logging
import datetime
import warnings

log = logging.getLogger(__name__)


class Attribute:
    def __init__(self, type, *, name=None):
        """
        :type gives a type or function that parses.
        :name overrides the field name in the json response. Defaults to field name in class.
        """

        self.type = type
        self.name = name

    def parse(self, value):
        return self.type(value)


class AttributeModelMeta(type):
    def __new__(cls, name, parents, dct):

        attrmodel = dict()
        for parent in parents:
            attrmodel.update(getattr(parent, "__attributemodel__", dict()))

        for field, value in dct.items():
            if isinstance(value, Attribute):
                value.field_name = field

                attrmodel[value.name or field] = value

        dct['__attributemodel__'] = attrmodel
        return super().__new__(cls, name, parents, dct)


class AttributeModel(object, metaclass=AttributeModelMeta):
    def __init__(self, dct):
        """Generated initializer for creating object from parsed dict.

        dct needs to have every field."""
        for k, v in dct.items():
            try:
                attr = self.__attributemodel__[k]
            except KeyError:
                warnings.warn("Unknown attribute {} in API response for type {}".format(k, type(self)), Warning)
            else:
                setattr(self, attr.field_name, attr.parse(v))

    def _iterator(self):
        for attr in dir(self):
            if attr in self.__attributemodel__:
                yield (attr, getattr(self, attr))

    def __iter__(self):
        return self._iterator()


def JsonList(oftype):
    """Generate a converter that accepts a list of :oftype.

    field = JsonList(int) would expect to be passed a list of things to convert to int"""
    def _(lst):
        return [oftype(entry) for entry in lst]

    return _


def Nullable(oftype):
    """Generate a converter that may be None, or :oftype.

    field = Nullable(DateConverter) would expect either null or something to convert to date"""
    def _(it):
        if it is None:
            return None
        else:
            return oftype(it)

    return _


def PreProcessInt(oftype):
    """Generate a converter that first converts the input to int before passing to :oftype.

    field = PreProcessInt(MyEnum) if field is a string in the json response to be interpteded as int"""
    def _(it):
        return oftype(int(it))
    return _


def DateConverter(val):
    """Converter to convert osu! api's date type into datetime."""
    return datetime.datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
