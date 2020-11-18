# -*- coding: utf-8 -*-

# pypi/conda library
from wrapt.decorators import synchronized

__author__ = "Haribo (haribo1558599@gmail.com)"
__license__ = "Apache 2.0"

# standard library
import threading

sum_ = 0
num_of_threads = 100
target_sum = 10000000


@synchronized
def increment(num):
    global sum_
    for i in range(num):
        sum_ += 1


class IncrementThread(threading.Thread):
    def __init__(self, num, name):
        super(self.__class__, self).__init__(name=name)
        self._num = num

    def run(self):
        increment(self._num)


def test_synchronization():
    """
    We use the simple scenario in which multiple threads will try to increment a
    shared variable concurrently, and assert that the result will still be
    equal to our target.
    """

    # The tasks must dispatch to threads evenly
    assert target_sum % num_of_threads == 0

    increment_num_per_thread = target_sum // num_of_threads

    threads = [IncrementThread(increment_num_per_thread, "Thread_%d" % i) for i in range(num_of_threads)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    assert sum_ == target_sum
