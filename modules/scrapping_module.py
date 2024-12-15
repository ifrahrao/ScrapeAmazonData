import requests
from bs4 import BeautifulSoup
import json

base_url = "https://www.amazon.com/"


class ScrapeAmazonData:
    def __init__(self, url):
        self.url = url
        self.result = []

    def get_pagination_url(self, soup):
        next_page_url = ""
        pagination = soup.findAll("a", {"class": "s-pagination-item"})
        if pagination:
            next_page_url = pagination[0].get('href')
        return next_page_url

    def get_product_data(self, page_content):
        result = []

        products = page_content.findAll("div", {"class": "puisg-row"})
        for product in products:
            product_detail = {}
            image_div = product.find("div", {"class": "s-product-image-container"})
            if image_div:
                product_detail["image_url"] = image_div.select(".s-image")[0].get("src")
            # title
            title_div = product.find("div", {"data-cy": "title-recipe"})

            if title_div:
                product_detail["title"] = title_div.select("h2")[0].text
            else:
                product_detail["title"] = ""
            # review
            review_div = product.find("div", {"data-cy": "reviews-block"})
            if review_div:
                review_data = review_div.find("span", {"data-component-type": "s-client-side-analytics"})
                if review_data:
                    product_detail["reviews"] = review_data.select("span")[0].text
                else:
                    product_detail["reviews"] = ""
            else:
                product_detail["reviews"] = ""

            # price
            price_div = product.find("span", {"class": "a-price"})
            if price_div:
                product_detail["price"] = price_div.select("span")[0].text
            else:
                product_detail["price"] = ""

            # delivery info
            delivery_div = product.find("div", {"data-cy": "delivery-recipe"})
            if delivery_div:
                delivery_info = delivery_div.select("span")
                if delivery_info:
                    product_detail["delivery_info"] = delivery_info[0].text
                else:
                    product_detail["delivery_info"] = ""
            else:
                product_detail["delivery_info"] = ""

            if "image_url" in product_detail:
                result.append(product_detail)

        return result

    def scrape_data(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                   "Accept-Encoding": "gzip, deflate",
                   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                   "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        page = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        result = self.get_product_data(soup)
        self.result = self.result + result
        next_url_format = base_url + self.get_pagination_url(soup)

        for i in range(2, 21):
            next_url = next_url_format.replace("page=2", "page=" + str(i)).replace("pg_2", "pg_" + str(i))
            print(next_url)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                       "Accept-Encoding": "gzip, deflate",
                       "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
                       "Connection": "close", "Upgrade-Insecure-Requests": "1"}

            page = requests.get(next_url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            result = self.get_product_data(soup)
            print(len(result))
            self.result = self.result + result

        return self.result
