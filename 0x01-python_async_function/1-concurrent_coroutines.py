#!/usr/bin/env python3
"""Script for async routine, wait_n."""
from typing import List
import asyncio

wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """
    Spawns/Generates wait_random n times with the specified max_delay.
    Returns the list of all the delays (float values)
    in ascending order without using sort() because of concurrency.
    """
    tasks = [asyncio.create_task(wait_random(max_delay)) for _ in range(n)]
    return [await task for task in asyncio.as_completed(tasks)]
