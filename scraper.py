# Importing required modules
import sys # for taking url from command line
import requests # sending get request and connect with server
from bs4 import BeautifulSoup # for parsing html 

class WebCrawlerClient:
    def __init__(self, url): 
        self.url = url

    def fetch(self):
        try:
            result = requests.get(self.url, timeout=10, headers={
                    "User-Agent":
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
                }
            )

            result.raise_for_status()
            return result.text
        
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to fetch {self.url}: {e}")

class WebPageParser:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")

    def get_title(self):
        # Not all pages define a title
        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()
        return ""

    def get_visible_text(self):
        if not self.soup.body:
            return ""
        return "\n".join(self.soup.body.stripped_strings)
    
    def get_all_hyperlinks(self):
        return [a['href'] for a in self.soup.find_all('a', href=True)]

class WebCrawlerProject:
    def run(self):
        try:
            if len(sys.argv) <= 1:
                raise ValueError("ERROR: URL Required")
            
            url = sys.argv[1]

            # check if url startswith https://
            if not url.startswith("https://"):
                url = "https://" + url

            html = WebCrawlerClient(url).fetch()
            parser = WebPageParser(html)
            
            print(f"Title of webpage: {parser.get_title()}")
            print()


            print("Body Text of webpage:")
            print(parser.get_visible_text())
            print()

            print("Outlinks: ")
            for link in parser.get_all_hyperlinks():
                print(link)
            print()

        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    WebCrawlerProject().run()