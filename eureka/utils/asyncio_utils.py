# -*- coding: utf-8 -*-
# standard library
import asyncio
from contextlib import suppress
from typing import Awaitable, Callable

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"


class CoroutineSupervisor:
    def __init__(
        self,
        timeout: float,
        exponential_back_off_bound: int,
        interval: float,
        max_num_of_tasks: int,
        coroutine: Callable[..., Awaitable],
        *args,
        **kwargs
    ):

        self._coroutine = coroutine
        self._args = args
        self._kwargs = kwargs
        self._timeout = timeout
        self._max_delay = self._timeout * exponential_back_off_bound
        self._interval = interval

        self._current_num_of_tasks = 0
        self._max_num_of_tasks = max_num_of_tasks

        self._started = False
        self._running = False
        self._event_loop = None
        self._task = None
        self._handler = None

    @property
    def current_num_of_tasks(self) -> int:
        return self._current_num_of_tasks

    @property
    def timeout(self):
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
        if self._running or self._current_num_of_tasks >= self._max_num_of_tasks:
            return

        self._running = True
        self._current_num_of_tasks += 1
        self._task = asyncio.create_task(self._runner())

    async def _runner(self):
        if not self._started:
            return

        try:
            task = asyncio.create_task(self._coroutine(*self._args, **self._kwargs))

            # Since it'll cause unknown error if the running coroutine was interrupted,
            # we shield the coroutine to prevent it from cancellation after timeout;
            # therefore, there are more than one coroutine running concurrently
            # when timeout occurs.
            await asyncio.wait_for(
                asyncio.shield(self._decrement_current_num_of_tasks_after_done(task)), timeout=self._timeout
            )
        except (asyncio.TimeoutError, asyncio.CancelledError):
            self._timeout = min(self._timeout * 2, self._max_delay)
        finally:
            self._running = False

    async def _decrement_current_num_of_tasks_after_done(self, task):
        await task
        self._current_num_of_tasks -= 1
