#!/usr/bin/env python3
"""Unittests for utils module."""
import unittest
from unittest.mock import Mock, patch
import requests
from utils import access_nested_map, get_json, memoize
from typing import Any
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Represent test cases for access_nested_map()."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    # Test return type:
    # self.assertEqual(access_nested_map.__annotations__['return'], Any)
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


class TestGetJson(unittest.TestCase):
    """Represents test cases for get_json()."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        config = {"return_value.json.return_value": test_payload}
        mock = patch('requests.get', **config).start()
        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patch('requests.get', **config).start()


class TestMemoize(unittest.TestCase):
    """Represent test cases for memoize()."""

    def test_memoize(self):

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock_method.assert_called_once()
