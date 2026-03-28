import sys

import requests
from bs4 import BeautifulSoup

def constants() -> dict:
    return {
        "SEARCH_BASE_URL": "https://en.wikipedia.org",
        "HEADERS": {
            "User-Agent": "roads-to-philosophy/1.0 (https://en.wikipedia.org/wiki/Wikipedia:Contact_us)"
        },
        "TIMEOUT": 30
    }

def search_wiki(term: str):
    visited: list[str] = []
    url = constants()["SEARCH_BASE_URL"] + "/wiki/" + term
    while True:
        try:
            response = requests.get(
                url=url,
                headers=constants()["HEADERS"],
                timeout=constants()["TIMEOUT"],
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 404:
                print("It's a dead end !")
                sys.exit(2)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find(id='firstHeading').text
        if title in visited:
            print("It leads to an infinite loop !")
            return
        visited.append(title)
        print(title)
        if title == 'Philosophy':
            print(f"{len(visited)} roads from {visited[0] if visited else 'Philosophy'} to Philosophy")
            return
        content = soup.find(id='mw-content-text')
        if content is None:
            print("It leads to a dead end !")
            return
        all_links = content.select('p > a')
        for link in all_links:
            href = link.get('href')
            if href and href.startswith('/wiki/') and not href.startswith('/wiki/Wikipedia:') and not href.startswith('/wiki/Help:'):
                url = constants()["SEARCH_BASE_URL"] + href
                break
        else:
            print("It leads to a dead end !")
            return
                
    

    



def main():
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        print("Error: please provide exactly one Wikipedia search term.")
        sys.exit(1)
    search_wiki(sys.argv[1].strip())

if __name__ == "__main__":
    main()
