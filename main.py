import scrapy
import json
import urllib.request
from urllib.parse import urlparse, quote


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.promiedos.com.ar/historialpartidos.php']

    def parse(self, response):
        # team_link = response.css('.datosequipo2b::attr(href)').extract()[0]
        # yield scrapy.Request(team_link, callback=self.parse_team)
        for team_link in response.css('.datosequipo2b::attr(href)').extract():
            team_link = urllib.request.unquote(team_link)
            yield scrapy.Request(team_link, callback=self.parse_team)

    def parse_team(self, response):
        # match_link = response.css('td a::attr(href)').extract()[0]
        # yield scrapy.Request(match_link, callback=self.parse_matches)

        for match_link in response.css('td a::attr(href)').extract():
            yield scrapy.Request(safe_url(match_link), callback=self.parse_matches)

    def parse_matches(self, response):
        matches = []
        matches_elements = response.css('tr[style="background: #e5e5e5"]')
        dates_elements = response.css('.diadelpart::text').extract()
        for i in range(len(matches_elements)):
            match_el = matches_elements[i]
            teams = [
                ''.join(el.css('::text').extract()).strip()
                for el in match_el.css('td[width="140"]')
            ]
            score = match_el.css('.datoequipo::text').extract()
            matches.append([
                teams[0],
                score[0].strip(),
                score[1].strip(),
                teams[1],
                dates_elements[i].strip()
            ])

        file_path = self.file_path_for(response.url)
        print('got %d matches for %s to save at %s' % (len(matches), response.url, file_path))
        with open(file_path, 'w') as json_file:
            json.dump(matches, json_file, ensure_ascii=False, indent=2)

    @staticmethod
    def file_path_for(url):
        if 'versus' in url:
            first_team = 'Argentina'
            second_team = url.split('=')[-1]
        else:
            base_url, first_team, second_team = url.split('=')
            first_team = first_team.split('&')[0]
        first_team = urllib.request.unquote(first_team, encoding='latin1')
        second_team = urllib.request.unquote(second_team, encoding='latin1')
        return 'data/%s-%s.json' % (first_team, second_team)


def safe_url(url):
    url = urlparse(url)
    return url.scheme + '://' + url.netloc + url.path + '?' + safe_params(url.query)


def safe_params(s):
    safe = []
    for tuple in s.split('&'):
        k, v = tuple.split('=')
        safe.append(k + '=' + quote(v, encoding='latin1'))
    return '&'.join(safe)