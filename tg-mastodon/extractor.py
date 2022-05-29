from typing import List

from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import requests
from html2text import HTML2Text

markdown_converter = HTML2Text()
markdown_converter.body_width = None
markdown_converter.protect_links = False

text_converter = HTML2Text()
text_converter.body_width = None
text_converter.use_automatic_links = False
text_converter.ignore_emphasis = True
text_converter.hide_strikethrough = True
text_converter.protect_links = False


class Media:
    url: str


class Post:
    __selector: Selector

    rem_id: str

    def __init__(self, sel: Selector):
        self.__selector = sel
        self.rem_id = sel.xpath('@data-post').get()

    def get_media(self) -> List[Media]:
        return []

    def get_message_links(self) -> List[str]:
        return self.__selector.xpath('//*[contains(@class, "js-message_text")]//a/@href').getall()

    def get_message_html(self) -> str:
        return self.__selector.xpath('//*[contains(@class, "js-message_text")]').get()

    def get_message_text(self) -> str:
        return text_converter.handle(self.get_message_html())

    def get_message_markdown(self) -> str:
        return markdown_converter.handle(self.get_message_html())
