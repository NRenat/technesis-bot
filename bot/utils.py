import re

from pydantic import ValidationError

from schemas import UsersDataSchema


def validate_dataframe(data):
    valid_data = []
    invalid_data = []
    for index, row in data.iterrows():
        title, url, xpath = row.get('title'), row.get('url'), row.get('xpath')
        try:
            validated_row = UsersDataSchema(
                title=title,
                url=url,
                xpath=xpath,
            )
            valid_data.append({
                'title': validated_row.title,
                'url': validated_row.url,
                'xpath': validated_row.xpath,
            })
        except ValidationError as e:
            invalid_data.append({
                'validation_error': str(e),
                'title': title,
                'url': url,
                'xpath': xpath,
            })
    return valid_data, invalid_data


def clean_price(price_str: str) -> float:
    if ',' in price_str and '.' not in price_str:
        price_str = price_str.replace(',', '.')

    cleaned_price = re.sub(r'[^\d.]', '', price_str)

    return float(cleaned_price)
