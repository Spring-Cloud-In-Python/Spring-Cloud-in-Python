# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio

# scip plugin
from eureka.utils import CoroutineScheduler


class TestCoroutineScheduler:
    def setup_method(self):
        self.event_loop = asyncio.get_event_loop()

    @staticmethod
    async def run_coroutine_scheduler(coroutine_scheduler, wait: float):
        await coroutine_scheduler.start()
        await asyncio.sleep(wait)
        await coroutine_scheduler.stop()

    def test_run(self):
        store = dict(value="was not running")

        async def func():
            store["value"] = "already run"

        coroutine_scheduler = CoroutineScheduler(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_timeout=5, coroutine=func
        )
        self.event_loop.run_until_complete(self.run_coroutine_scheduler(coroutine_scheduler, wait=0.1))

        assert "already run" == store["value"], "After run value should be set."

    def test_throttling_without_timeout(self):
        store = dict(count=0)

        async def func():
            previous_count = store["count"]
            store["count"] += 1
            await asyncio.sleep(0.1)

            # The difference is 1 only if only one coroutine accesses func() at the same time
            assert previous_count + 1 == store["count"]

        coroutine_scheduler = CoroutineScheduler(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_timeout=5, coroutine=func
        )
        self.event_loop.run_until_complete(self.run_coroutine_scheduler(coroutine_scheduler, wait=1))

    def test_args(self):
        store = dict(arg=None)

        async def func(arg):
            store["arg"] = arg

        coroutine_scheduler = CoroutineScheduler(5, 100, 0.01, 5, func, "expected")
        self.event_loop.run_until_complete(self.run_coroutine_scheduler(coroutine_scheduler, wait=0.1))

        assert "expected" == store["arg"], "After run arg should be 'expected'."

    def test_kwargs(self):
        store = dict(value=None)

        async def func(value=None):
            store["value"] = value

        coroutine_scheduler = CoroutineScheduler(5, 100, 0.01, 5, func, value="expected")
        self.event_loop.run_until_complete(self.run_coroutine_scheduler(coroutine_scheduler, wait=0.1))

        assert "expected" == store["value"], "After run arg should be 'expected'."

    def test_args_kwargs(self):
        store = dict(arg=None, value=None)

        async def func(arg, value=None):
            store["arg"] = arg
            store["value"] = value

        coroutine_scheduler = CoroutineScheduler(5, 100, 0.01, 5, func, "expected_arg", value="expected_kwarg")
        self.event_loop.run_until_complete(self.run_coroutine_scheduler(coroutine_scheduler, wait=0.1))

        assert "expected_arg" == store["arg"], "After run arg should be 'expected'."
        assert "expected_kwarg" == store["value"], "After run arg should be 'expected'."

    def test_timeout(self):
        store = dict(timeout=False)
        max_num_of_timeout = 3

        def logger(msg: str):
            store["timeout"] = True
            print(msg)

        async def func():
            await asyncio.sleep(0.3)

        coroutine_scheduler = CoroutineScheduler(
            timeout=0.01,
            exponential_back_off_bound=100,
            interval=0.01,
            max_num_of_timeout=max_num_of_timeout,
            coroutine=func,
        )
        coroutine_scheduler.add_timeout_callback(logger, "Exceed maximum num of timeout")

        async def run():
            await coroutine_scheduler.start()
            await asyncio.sleep(2)

        self.event_loop.run_until_complete(run())
        assert store["timeout"]


class TestMultipleCoroutineScheduler:
    def setup_method(self):
        self.event_loop = asyncio.get_event_loop()

    @staticmethod
    async def run_coroutine_scheduler(coroutine_scheduler_1, coroutine_scheduler_2, wait: float):
        await asyncio.gather(coroutine_scheduler_1.start(), coroutine_scheduler_2.start())
        await asyncio.sleep(wait)
        await asyncio.gather(coroutine_scheduler_1.stop(), coroutine_scheduler_2.stop())

    def test_throttling_without_timeout(self):
        store = dict(count_1=0, count_2=0)

        async def func_1():
            previous_count = store["count_1"]
            store["count_1"] += 1
            await asyncio.sleep(0.1)

            # The difference is 1 only if only one coroutine accesses func() at the same time
            assert previous_count + 1 == store["count_1"]

        async def func_2():
            previous_count = store["count_2"]
            store["count_2"] += 1
            await asyncio.sleep(0.1)

            # The difference is 1 only if only one coroutine accesses func() at the same time
            assert previous_count + 1 == store["count_2"]

        coroutine_scheduler_1 = CoroutineScheduler(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_timeout=5, coroutine=func_1
        )
        coroutine_scheduler_2 = CoroutineScheduler(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_timeout=5, coroutine=func_2
        )
        self.event_loop.run_until_complete(
            self.run_coroutine_scheduler(coroutine_scheduler_1, coroutine_scheduler_2, wait=1)
        )

    def test_timeout(self):
        store = dict(timeout_1=False, timeout_2=False)
        max_num_of_timeout = 3

        def logger_1(msg: str):
            store["timeout_1"] = True
            print(msg)

        def logger_2(msg: str):
            store["timeout_2"] = True
            print(msg)

        async def func():
            await asyncio.sleep(0.3)

        coroutine_scheduler_1 = CoroutineScheduler(
            timeout=0.01,
            exponential_back_off_bound=100,
            interval=0.01,
            max_num_of_timeout=max_num_of_timeout,
            coroutine=func,
        )
        coroutine_scheduler_1.add_timeout_callback(logger_1, "Exceed maximum num of timeout")

        coroutine_scheduler_2 = CoroutineScheduler(
            timeout=0.01,
            exponential_back_off_bound=100,
            interval=0.01,
            max_num_of_timeout=max_num_of_timeout,
            coroutine=func,
        )
        coroutine_scheduler_2.add_timeout_callback(logger_2, "Exceed maximum num of timeout")

        async def run():
            await asyncio.gather(coroutine_scheduler_1.start(), coroutine_scheduler_2.start())
            await asyncio.sleep(2)

        self.event_loop.run_until_complete(run())
        assert store["timeout_1"] and store["timeout_2"]
