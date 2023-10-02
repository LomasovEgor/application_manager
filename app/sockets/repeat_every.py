import asyncio
from asyncio import ensure_future
from functools import wraps


def repeat_every(
    *,
    seconds: float,
    max_repetitions: int | None = None,
):
    def decorator(func):
        @wraps(func)
        async def wrapped() -> None:
            repetitions = 0

            async def loop() -> None:
                nonlocal repetitions
                while max_repetitions is None or repetitions < max_repetitions:
                    try:
                        await func()
                        repetitions += 1
                    except Exception as exc:
                        raise exc
                    await asyncio.sleep(seconds)

            ensure_future(loop())

        return wrapped

    return decorator
