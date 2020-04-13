import aiohttp
import bs4
from colorama import Fore
import asyncio


async def get_html(episode_number: int) -> str:
    print(
        Fore.YELLOW + f"Getting HTML for episode {episode_number}", flush=True
    )

    url = f"https://talkpython.fm/{episode_number}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.text()


def get_title(episode_number: int, html: str) -> str:

    print(Fore.CYAN + f"Getting TITLE for episode {episode_number}", flush=True)
    soup = bs4.BeautifulSoup(html, "html.parser")
    header = soup.select_one("h1")
    if not header:
        return "MISSING"

    return header.text.strip()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title_range())

    print("Done.")


async def get_title_range():
    # Please keep this range pretty small to not DDoS my site. ;)
    tasks = []
    for n in range(150, 160):
        tasks.append(asyncio.create_task(process_page(n)))

    await asyncio.wait(tasks)


async def process_page(episode_number: int):
    html = await get_html(episode_number)
    title = get_title(episode_number, html)
    print(Fore.WHITE + f"Title found: {title}", flush=True)


if __name__ == "__main__":
    main()
