from enum import Enum
import logging

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
                print("help")
                log.warn("Unknown attribute {} in API response for type {}".format(k, type(self)), Warning)
            else:
                setattr(self, attr.field_name, attr.parse(v))
