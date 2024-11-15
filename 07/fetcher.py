import asyncio
import argparse
import re
from collections import Counter
import aiohttp


class UrlFetcher:
    def __init__(self, max_count_requests):
        self.semaphore = asyncio.Semaphore(max_count_requests)
        self.total_processed = 0
        self.failed_urls = []
        self.success_urls = []

    async def fetch_url(self, session: aiohttp.ClientSession, url) -> str:
        try:
            async with self.semaphore:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            self.failed_urls.append(url)
            print(f"Ошибка при загрузке {url}: {e}")
            return ""

    def get_top_words(self, text, top_k=10):
        # Удаляем HTML-теги
        clean_text = re.sub(r"<[^>]+>", " ", text)
        # Находим слова
        words = re.findall(r"\w+", clean_text.lower())
        word_counts = Counter(words)
        return dict(word_counts.most_common(top_k))

    async def process_urls(self, urls, top_k):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_and_analyze(session, url, top_k)
                for url in urls
            ]
            await asyncio.gather(*tasks)

    async def fetch_and_analyze(
            self, session: aiohttp.ClientSession,
            url: str, top_k: int):
        content = await self.fetch_url(session, url)
        if content:
            analysis = self.get_top_words(content, top_k)
            self.success_urls.append(url)
            print(f"URL: {url}\nТоп {top_k} частых слов: {analysis}")
        self.total_processed += 1
        print(f"Обработано URL адресов: {self.total_processed}")


def load_urls(url_file):
    with open(url_file, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file]
    return urls


async def main(url_file, count_requests):
    urls = load_urls(url_file)
    if not urls:
        print("Файл URL-ов пуст.")
        return

    fetcher = UrlFetcher(max_count_requests=int(count_requests))
    print(f"Обработка {len(urls)} URL-ов с {count_requests}" +
          " одновременными запросами: ")
    await fetcher.process_urls(urls, top_k=10)
    print("Обработка завершина")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("count_requests")
    parser.add_argument("url_file")
    args = parser.parse_args()

    # Запуск основного цикла
    asyncio.run(main(args.url_file, args.count_requests))
