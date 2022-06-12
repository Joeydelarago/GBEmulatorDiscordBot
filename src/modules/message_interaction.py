import asyncio
import logging
from typing import List


async def read_emoji_options(client, message, options: List[str]) -> str:
    for option in options:
        await message.add_reaction(option)

    try:
        reaction, user = await client.wait_for("reaction_add",
                                                    check=lambda reaction, user: reaction.message.id == message.id,
                                                    timeout=60)
        return reaction.emoji
    except asyncio.TimeoutError:
        logging.info("Timed out selecting a game")