import urllib.request
import asyncio

urls = [
    ("21", "https://fastapi.tiangolo.com/tutorial/query-params-str-validations/"),
    ("22", "https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/"),
    ("23", "https://fastapi.tiangolo.com/tutorial/body-multiple-params/"),
    ("24", "https://fastapi.tiangolo.com/tutorial/body-fields/"),
    ("25", "https://fastapi.tiangolo.com/tutorial/body-nested-models/"),
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

async def fetch(url):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")

async def main():
    tasks = [fetch(url) for _, url in urls]
    results = await asyncio.gather(*tasks)
    for i, (num, url) in enumerate(urls):
        with open(f"E:/page_{num}.html", "w", encoding="utf-8") as f:
            f.write(results[i])
        print(f"Page {num} fetched, length={len(results[i])}")

asyncio.run(main())
