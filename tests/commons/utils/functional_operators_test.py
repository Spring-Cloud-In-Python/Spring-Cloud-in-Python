# scip plugin
from spring_cloud.commons.utils.functional_operators import filter_get_first, flat_map

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"


def test_flat_map():
    the_list = ["a,b,c", "1,2,3", ""]
    results = flat_map(lambda e: e.split(","), the_list)
    assert ["a", "b", "c", "1", "2", "3", ""] == results


def test_filter_get_first_Given_numbers():
    the_list = [1, 2, 3, 4, 5, 6, 7, 8]
    result = filter_get_first(lambda e: e > 4, the_list)
    assert 5 == result


def test_filter_get_first_Given_empty_list():
    the_list = []
    result = filter_get_first(lambda e: e > 4, the_list)
    assert result is None
