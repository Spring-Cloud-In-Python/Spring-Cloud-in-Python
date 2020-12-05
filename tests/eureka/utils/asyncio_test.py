# -*- coding: utf-8 -*-

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import asyncio

# scip plugin
from eureka.utils import CoroutineSupervisor


class TestCoroutineSupervisor:
    def setup_method(self):
        self.event_loop = asyncio.get_event_loop()

    @staticmethod
    async def run_coroutine_supervisor(coroutine_supervisor, wait: float):
        await coroutine_supervisor.start()
        await asyncio.sleep(wait)
        await coroutine_supervisor.stop()

    def test_run(self):
        store = dict(value="was not running")

        async def func():
            store["value"] = "already run"

        coroutine_supervisor = CoroutineSupervisor(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_tasks=5, coroutine=func
        )
        self.event_loop.run_until_complete(self.run_coroutine_supervisor(coroutine_supervisor, wait=0.1))

        assert "already run" == store["value"], "After run value should be set."

    def test_throttling_without_timeout(self):
        store = dict(count=0)

        async def func():
            previous_count = store["count"]
            store["count"] += 1
            await asyncio.sleep(0.1)

            # The difference is 1 only if only one coroutine accesses func() at the same time
            assert previous_count + 1 == store["count"]

        coroutine_supervisor = CoroutineSupervisor(
            timeout=5, exponential_back_off_bound=100, interval=0.01, max_num_of_tasks=5, coroutine=func
        )
        self.event_loop.run_until_complete(self.run_coroutine_supervisor(coroutine_supervisor, wait=1))

    def test_args(self):
        store = dict(arg=None)

        async def func(arg):
            store["arg"] = arg

        coroutine_supervisor = CoroutineSupervisor(5, 100, 0.01, 5, func, "expected")
        self.event_loop.run_until_complete(self.run_coroutine_supervisor(coroutine_supervisor, wait=0.1))

        assert "expected" == store["arg"], "After run arg should be 'expected'."

    def test_kwargs(self):
        store = dict(value=None)

        async def func(value=None):
            store["value"] = value

        coroutine_supervisor = CoroutineSupervisor(5, 100, 0.01, 5, func, value="expected")
        self.event_loop.run_until_complete(self.run_coroutine_supervisor(coroutine_supervisor, wait=0.1))

        assert "expected" == store["value"], "After run arg should be 'expected'."

    def test_args_kwargs(self):
        store = dict(arg=None, value=None)

        async def func(arg, value=None):
            store["arg"] = arg
            store["value"] = value

        coroutine_supervisor = CoroutineSupervisor(5, 100, 0.01, 5, func, "expected_arg", value="expected_kwarg")
        self.event_loop.run_until_complete(self.run_coroutine_supervisor(coroutine_supervisor, wait=0.1))

        assert "expected_arg" == store["arg"], "After run arg should be 'expected'."
        assert "expected_kwarg" == store["value"], "After run arg should be 'expected'."

    def test_timeout(self):
        async def func():
            await asyncio.sleep(0.3)

        coroutine_supervisor = CoroutineSupervisor(
            timeout=0.01, exponential_back_off_bound=100, interval=0.01, max_num_of_tasks=5, coroutine=func
        )

        async def run():
            await coroutine_supervisor.start()
            await asyncio.sleep(0.3)
            assert coroutine_supervisor.current_num_of_tasks > 1
            await coroutine_supervisor.stop()

        self.event_loop.run_until_complete(run())

    def test_max_number_of_running_tasks(self):
        async def func():
            await asyncio.sleep(0.3)

        max_num_of_tasks = 5

        coroutine_supervisor = CoroutineSupervisor(
            timeout=0.01,
            exponential_back_off_bound=100,
            interval=0.01,
            max_num_of_tasks=max_num_of_tasks,
            coroutine=func,
        )

        async def run():
            await coroutine_supervisor.start()
            await asyncio.sleep(0.3)
            assert coroutine_supervisor.current_num_of_tasks == max_num_of_tasks
            await coroutine_supervisor.stop()

        self.event_loop.run_until_complete(run())

    def tear_down(self):
        self.event_loop.close()
