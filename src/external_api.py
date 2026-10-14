import asyncio
import httpx

# Обмеження одночасних запитів (Semaphore)
semaphore = asyncio.Semaphore(5)

async def fetch_product_with_retry(client: httpx.AsyncClient, url: str, attempts: int = 3) -> dict:
    async with semaphore:
        for attempt in range(1, attempts + 1):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == attempts:
                    raise
                await asyncio.sleep(attempt)
    raise RuntimeError("Unexpected retry state")

async def fetch_multiple_products(base_url: str, product_ids: list[int]) -> list[dict]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        # Створення задач (Tasks)
        tasks = [
            asyncio.create_task(fetch_product_with_retry(client, f"{base_url}/products/{pid}"))
            for pid in product_ids
        ]
        try:
            # gather + timeout
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
            return list(results)
        except asyncio.TimeoutError:
            return []