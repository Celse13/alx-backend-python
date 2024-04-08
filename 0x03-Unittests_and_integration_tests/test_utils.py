#!/usr/bin/env python3
""" module for testing utils.py"""
import unittest
from unittest.mock import patch, Mock
from typing import Any, Tuple, Dict
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """test_access_nested_map"""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str], expected: Any
    ) -> None:
        """test_access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b"))
        ]
    )
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str]
    ) -> None:
        """test_access_nested_map_exception"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """test_get_json"""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    @patch("requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        """test get_json"""
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """test memoize"""

    def test_memoize(self) -> None:
        """test memoize"""

        class TestClass:
            """test class"""

            def a_method(self) -> int:
                """a_ method """
                return 42

            @memoize
            def a_property(self) -> int:
                """ aproperty """
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mocked.assert_called_once()
