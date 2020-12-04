# -*- coding: utf-8 -*-
# scip plugin
from spring_cloud.gateway.pathpattern import PathPatternParser

__author__ = "Waterball (johnny850807@gmail.com)"
__license__ = "Apache 2.0"

parser = PathPatternParser()


class TestParser:
    def given_pattern(self, path_pattern: str):
        self.path_pattern = parser.parse(path_pattern)

    def should_match(self, path: str):
        assert self.path_pattern.matches(path), f"{self.path_pattern} should match {path}"

    def should_not_match(self, path: str):
        assert not self.path_pattern.matches(path), f"{self.path_pattern} should not match {path}"

    def test_normal_path(self):
        self.given_pattern("/api/users")
        self.should_match("/api/users")
        self.should_not_match("/users")
        self.should_not_match("users")
        self.should_not_match("/api/user")
        self.should_not_match("/api/messages")
