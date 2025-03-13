from lxml import etree

from pydantic import BaseModel, HttpUrl, validator, field_validator


class BaseSchema(BaseModel):
    title: str
    url: HttpUrl


class UsersDataSchema(BaseSchema):
    xpath: str

    @field_validator('xpath')
    def validate_xpath(cls, value):
        try:
            etree.XPath(value)
        except etree.XPathSyntaxError:
            raise ValueError('Некорректный XPath')
        return value


class ProductDataSchema(BaseSchema):
    price: float
