# -*- coding: utf-8 -*-
# standard library
import asyncio
import functools
from contextlib import suppress
from typing import Awaitable, Callable

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class CoroutineScheduler:
    def __init__(
        self,
        timeout: float,
        exponential_back_off_bound: int,
        interval: float,
        max_num_of_timeout: int,
        coroutine: Callable[..., Awaitable],
        *args,
        **kwargs,
    ):

        self._coroutine = coroutine
        self._args = args
        self._kwargs = kwargs
        self._timeout = timeout
        self._max_delay = self._timeout * exponential_back_off_bound
        self._interval = interval

        self._timeout_counter = 0
        self._max_num_of_timeout = max_num_of_timeout
        self._timeout_callback = None

        self._started = False
        self._running = False
        self._event_loop = None
        self._task = None
        self._handler = None

    @property
    def timeout_counter(self) -> int:
        return self._timeout_counter

    @property
    def timeout(self) -> float:
        return self._timeout

    async def start(self):
        if self._started:
            return

        self._event_loop = asyncio.get_running_loop()
        self._started = True
        self._running = False
        self._handler = self._event_loop.call_soon(self._run)

    async def stop(self, wait: float = 0):
        if not self._started:
            return

        self._started = False

        if self._handler:
            self._handler.cancel()
            self._handler = None

        if self._task is None:
            return

        with suppress(asyncio.TimeoutError, asyncio.CancelledError):
            await asyncio.wait_for(self._task, wait)

        self._task = None
        self._running = False

    def _run(self):
        if not self._started:
            return

        self._handler = self._event_loop.call_later(self._interval, self._run)

        # Throttle periodic call
        if self._running:
            return

        if self._timeout_counter >= self._max_num_of_timeout:
            # Break the recursive call to _run()
            self._started = False

            if self._timeout_callback:
                self._timeout_callback()

            return

        self._running = True
        self._task = asyncio.create_task(self._runner())

    async def _runner(self):
        if not self._started:
            return

        try:
            task = asyncio.create_task(self._coroutine(*self._args, **self._kwargs))
            await asyncio.wait_for(task, timeout=self._timeout)

            # Reset timeout counter once a task succeeded
            self._timeout_counter = 0
        except (asyncio.TimeoutError, asyncio.CancelledError):
            self._timeout = min(self._timeout * 2, self._max_delay)
            self._timeout_counter += 1
        finally:
            self._running = False

    def add_timeout_callback(self, func: Callable, *args, **kwargs):
        self._timeout_callback = functools.partial(func, *args, **kwargs)
