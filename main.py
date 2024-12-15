import requests
from bs4 import BeautifulSoup
import json
from modules import input_module, scrapping_module, output_module

base_url = "https://www.amazon.com/s?k="


def scrape_data(json_file):
    input = input_module.InputModule()
    output = output_module.OutputModule()
    q = input.read_queries(json_file)
    print(q)
    for i in q:
        url = base_url + i
        print("--- Scrapping :" + url)
        scrape_amazon_data = scrapping_module.ScrapeAmazonData(url=url)
        data = scrape_amazon_data.scrape_data()
        output.save_data(data, "result/", i + ".json")
        print("---- End -----")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape_data("user_queries.json")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
