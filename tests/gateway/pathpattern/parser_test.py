# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.gateway.pathpattern import LiteralPathElement, PathElement, PathPatternParser, SeparatorPathElement

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

parser = PathPatternParser()


class TestParser:
    def given_pattern(self, path_pattern: str):
        self.path_pattern = parser.parse(path_pattern)

    def should_match(self, path: str):
        assert self.path_pattern.matches(path=path), f"{self.path_pattern} should match {path}"

    def should_not_match(self, path: str):
        assert not self.path_pattern.matches(path=path), f"{self.path_pattern} should not match {path}"

    def test_path_pattern_linked_list_parsed(self):
        self.given_pattern("/api/users")

        element: PathElement = self.path_pattern.head
        assert isinstance(element, SeparatorPathElement)
        element = element.next
        assert isinstance(element, LiteralPathElement)
        assert element.text == "api"
        element = element.next
        assert isinstance(element, SeparatorPathElement)
        element = element.next
        assert isinstance(element, LiteralPathElement)
        assert element.text == "users"

    def test_normal_path(self):
        self.given_pattern("/api/users")
        self.should_match("/api/users")
        self.should_not_match("/users")
        self.should_not_match("/api/users/")  # trailing separator case, consider to optionally enable it
        self.should_not_match("users")
        self.should_not_match("/api/user")
        self.should_not_match("/api/messages")
        self.should_not_match("/aqi/messages")
