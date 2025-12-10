# from django.test import TestCase
import asyncio


# Create your tests here.
async def test():
    await asyncio.sleep(2)
    print(1)


async def test2():
    await asyncio.sleep(2)
    print(2)


async def main():
    await asyncio.gather(test(), test2())


asyncio.run(main())
