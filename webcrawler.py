import requests
from bs4 import BeautifulSoup
import argparse
import time


def crawl_web(url, word, depth):
    visited = set()
    queue = [(url, 0)]
    total_count = 0

    while queue:
        url, level = queue.pop(0)
        if level > depth:
            break

        if url in visited:
            continue

        visited.add(url)
        print(f"Crawling: {url}")

        # Set a User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                body_text = soup.get_text()

                # Count the occurrences of the word
                word_count = body_text.lower().count(word.lower())
                total_count += word_count
                print(f"Occurrences of '{word}' on {url}: {word_count}")

                # Extract links from the webpage
                links = soup.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and href.startswith("http"):
                        queue.append((href, level + 1))

                # Delay between requests to mimic human-like behavior
                time.sleep(2)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while accessing {url}: {e}")

    print(f"\nTotal occurrences of '{word}' across all pages: {total_count}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('url', type=str, help='URL to crawl')
    parser.add_argument('word', type=str, default='kayako', nargs='?', help='Word to search for')
    parser.add_argument('depth', type=int, default=2, nargs='?', help='Scan depth level')
    args = parser.parse_args()

    crawl_web(args.url, args.word, args.depth)
