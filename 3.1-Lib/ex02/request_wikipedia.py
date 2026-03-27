import sys
import json
import dewiki
import requests

def adapt_term(term: str) -> str:
    return term.replace(" ", "_")

def wiki_search(term):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "parse",
        "page": term,
        "format": "json",
        "prop": "wikitext",
        "redirects": "true",

    }

    headers = {
        # Pon algo descriptivo + forma de contacto (URL a repo, página de usuario, etc.)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0",
        "Accept-Encoding": "gzip",
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        sys.exit(1)
    try:
        data: dict = json.loads(r.text)
    except json.decoder.JSONDecodeError as e:
        raise e
    if data.get("error") is not None:
        raise Exception(data["error"]["info"])
    output = dewiki.from_string(data.get("parse", {}).get("wikitext", {}).get("*", ""))
    with open(f"{adapt_term(term)}.wiki", "w", encoding="utf-8") as f:
        f.write(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python request_wikipedia.py <search_term>")
        sys.exit(1)
    term = sys.argv[1]
    try:
        wiki_search(term)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
