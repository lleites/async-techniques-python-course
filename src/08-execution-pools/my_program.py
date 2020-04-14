from typing import List

import requests
import bs4
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
from concurrent.futures import Future


def main():
    urls = [
        "https://talkpython.fm",
        "https://pythonbytes.fm",
        "https://google.com",
        "https://realpython.com",
        "https://training.talkpython.fm/",
    ]

    futures: List[Future] = []
    with PoolExecutor() as executor:
        for url in urls:
            f: Future[str] = executor.submit(get_title, url)
            print(
                "Getting title from {}".format(url.replace("https", "")),
                end="... ",
                flush=True,
            )
            futures.append(f)

    for future in futures:
        print(future.result())

    print("Done", flush=True)


def get_title(url: str) -> str:
    import multiprocessing

    p = multiprocessing.current_process()
    print(
        "Getting title from {}, PID: {}, ProcName: {}".format(
            url.replace("https://", ""), p.pid, p.name
        ),
        flush=True,
    )

    resp = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) "
            "Gecko/20100101 Firefox/61.0"
        },
    )
    resp.raise_for_status()

    html = resp.text

    soup = bs4.BeautifulSoup(html, features="html.parser")
    tag: bs4.Tag = soup.select_one("h1")

    if not tag:
        return "NONE"

    if not tag.text:
        a = tag.select_one("a")
        if a and a.text:
            return a.text
        elif a and "title" in a.attrs:
            return a.attrs["title"]
        else:
            return "NONE"

    return tag.get_text(strip=True)


if __name__ == "__main__":
    main()
