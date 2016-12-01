import requests
from requests.auth import HTTPBasicAuth
from scrapy import signals
from scrapy.crawler import CrawlerProcess

from spiders.challenges import ChallengesSpider


def collect_challenges():
    def challenge_scraped(**kwargs):
        challenge = kwargs['item']
        challenges.append(challenge)

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ChallengesSpider)
    (crawler,) = process.crawlers

    challenges = []
    crawler.signals.connect(challenge_scraped, signal=signals.item_scraped)
    process.start()
    return sorted(challenges, key=lambda challenge: (challenge['set'], challenge['challenge']))


def create_github_issue_descriptor(token, challenge):
    return {
        'auth': HTTPBasicAuth('alexander-matsievsky', token),
        'headers': {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'
        },
        'json': {
            'title': '{set}.{challenge}. {title}'.format(
                set=challenge['set'],
                challenge=challenge['challenge'],
                title=challenge['title']
            ),
            'body': '[{title}]({url})\n\n{html}'.format(
                title=challenge['title'],
                url=challenge['url'],
                html=challenge['html']
            ),
            'labels': ['set: {set}'.format(set=challenge['set'])]
        }
    }


def send_github_issue(github_issue_descriptor):
    url = 'https://api.github.com/repos/alexander-matsievsky/cryptopals/issues'
    requests.request('post', url, **github_issue_descriptor)


for challenge in collect_challenges():
    print(str(create_github_issue_descriptor('', challenge)))
    # send_github_issue(create_github_issue_descriptor('', challenge))
