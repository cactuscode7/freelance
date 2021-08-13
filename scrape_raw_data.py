import json
from pathlib import Path
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
class universities(scrapy.Spider):
    name = "univ"
    start_urls = ["https://www.ugc.ac.in/"]
    project_dir = Path(__file__).resolve().parents[0]
    BASE = "https://www.ugc.ac.in/"
    raw_data_folder = project_dir.joinpath("raw")
    raw_data_folder.mkdir(parents=True, exist_ok=True)


    def start_request(self):
        univ_types = [
            'centraluniversity.aspx',
            'privatuniversity.aspx',
            'deemeduniversity.aspx',
            'stateuniversity.aspx'
            ]
        for univ_type in univ_types:
            # url = urljoin(BASE,univ_type)
            yield Request(
                url = urljoin(BASE,univ_type),
                callback=self.parse,
                headers=headers,
                # meta= {"url":url}
            )
            

    def parse(self,response):
        state_urls = response.xpath('//td/li/a/@href').getall()
        for state in state_urls:
            yield Request(
                url = urljoin(BASE,state),
                callback = self.parse_state
                
            )

        
    def parse_state(self,response):
        dict_ = {}
        # details_dict = {}
        for selector in response.xpath('//tr/td/div[@class="panel panel-default"]/div[@class="panel-body"]'):
            dict_["university_name"] = selector.css('b::text').get().strip()
            self.logger.info(f"{dict_['university_name']}")
            self.logger.debug(self.raw_data_folder)

            # with open(str(self.raw_data_folder) + "/data.json", "a+") as f:
            #     f.write(json.dumps(dict_) + "\n")
    

def main():
    process = CrawlerProcess()
    process.crawl(universities)
    process.start()


if __name__ == "__main__":
    main()