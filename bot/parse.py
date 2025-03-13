import httpx
from lxml import html
from pydantic import HttpUrl

from utils import clean_price


async def get_price(url: HttpUrl, xpath: str) -> float | None | str:
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(str(url), headers=headers,
                                        follow_redirects=True)
            response.raise_for_status()

            tree = html.fromstring(response.content)
            price_obj = tree.xpath(xpath)
            if price_obj:
                price = price_obj[0].text_content().strip()
                return clean_price(price)
            else:
                return None
        except httpx.HTTPStatusError as e:
            return f"HTTP Error {e.response.status_code}"
        except httpx.RequestError:
            return "Ошибка сети"
        except Exception:
            return "Ошибка получения цены"
