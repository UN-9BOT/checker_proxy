import asyncio
from datetime import datetime as dt

import aiofiles  # type: ignore
from httpx import AsyncClient
from termcolor import cprint

from config import DATETIME_FORMAT_FN, SETTINGS


async def load_proxy_file() -> list[str]:
    async with aiofiles.open(SETTINGS.input_file) as f:
        proxies = await f.readlines()
    return proxies


async def save_good_proxy(good_proxy: list[str]) -> None:
    file_name = f"{SETTINGS.input_file}_{dt.now().strftime(DATETIME_FORMAT_FN)}.txt"
    async with aiofiles.open(file_name, "a") as f:
        await f.write("\n".join(good_proxy))
    cprint(f"Write good_proxy to file -> {file_name}", color="cyan")


async def process_proxy(proxy: str) -> str:
    try:
        async with AsyncClient(proxy=proxy) as cli:
            response = await cli.get(SETTINGS.used_site)
            response.raise_for_status()
    except Exception as exc:
        cprint(f"{exc=} for -> {proxy}", color="dark_grey")
        raise
    return proxy


async def main() -> None:
    proxies = await load_proxy_file()

    finished_tasks = await asyncio.gather(*[process_proxy(p.strip()) for p in proxies], return_exceptions=True)
    good_proxy: list[str] = [res for res in finished_tasks if not isinstance(res, BaseException)]

    cprint(f"Count good_proxy = {len(good_proxy)}", color="green")
    if good_proxy:
        await save_good_proxy(good_proxy)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
