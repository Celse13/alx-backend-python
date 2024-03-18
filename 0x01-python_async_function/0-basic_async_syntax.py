#!/usr/bin/env python3
""" Async function """
import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """Async function"""
    wait = random.uniform(0, max_delay)
    await asyncio.sleep(wait)
    return wait
