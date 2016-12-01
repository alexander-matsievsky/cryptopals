# -*- coding: utf-8 -*-
import re

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ChallengesSpider(CrawlSpider):
    name = 'challenges'
    allowed_domains = ['cryptopals.com']
    start_urls = ['https://cryptopals.com/']

    rules = [
        Rule(LinkExtractor(allow=r'challenges'), callback='parse_challenge'),
        Rule(LinkExtractor(allow=r'sets')),
    ]

    def parse_challenge(self, response):
        self.logger.info(response.url)
        (challenge_set, challenge) = re.search(r'/sets/(\d+)/challenges/(\d+)', response.url).groups()
        html = BeautifulSoup(response.body, 'html.parser')
        list(html.find(class_='container').children)
        return {
            'set': int(challenge_set),
            'challenge': int(challenge),
            'url': response.url,
            'title': response.css('.container > :nth-child(3) h3::text').extract_first(),
            'html': response.css('.container > :nth-child(3)').extract_first()
        }
