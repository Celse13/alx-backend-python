#!/usr/bin/env python3
""" a module of unittests for client.py"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """ test for GithubOrgClient class"""

    @parameterized.expand(
        [
            ("google"),
            ("abc"),
        ]
    )
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name: str, mock_get: Mock) -> None:
        """test for org method of GithubOrgClient class"""
        client_for_github_org = GithubOrgClient(org_name)
        self.assertEqual(client_for_github_org.org, {"payload": True})
        url = f"https://api.github.com/orgs/{org_name}"
        mock_get.assert_called_once_with(url)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org) -> None:
        """a test for _public_repos_url method of GithubOrgClient class"""
        pay_load = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_org.return_value = pay_load
        client_for_github_org = GithubOrgClient("google")
        self.assertEqual(client_for_github_org._public_repos_url,
                         pay_load["repos_url"])

    @patch("client.get_json",
           return_value=[
               {"name": "repo1"},
               {"name": "repo2"}
           ]
           )
    def test_public_repos(self, mock_get_json) -> None:
        """a test for public_repos method of GithubOrgClient class"""
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock
        ) as repo:
            repo.return_value = (
                "https://api.github.com/orgs/google/repos"
            )
            client_for_github_org = GithubOrgClient("google")
            self.assertEqual(client_for_github_org.public_repos(),
                             ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            repo.assert_called_once()

    @parameterized.expand(
        [
            ({"license": {"key": "my_license"}}, "my_license", True),
            ({"license": {"key": "other_license"}}, "my_license", False),
        ]
    )
    def test_has_license(self, repo, license_key, expected_result) -> None:
        """a test for has_license method of GithubOrgClient class"""
        client_for_github_org = GithubOrgClient("google")
        self.assertEqual(
            client_for_github_org.has_license(
                repo, license_key), expected_result)


@parameterized_class(('org_payload', 'repos_payload',
                      'expected_repos', 'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """a class for integration tests for GithubOrgClient class"""
    @classmethod
    def setUpClass(cls):
        """a method that sets up the class"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """a method that returns the side effect of the mock get"""
            class MockResponse:
                def __init__(self, json_data):
                    self.json_data = json_data

                def json(self):
                    return self.json_data

            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            else:
                return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """a method that deconstructs the class"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """a test for public_repos method of GithubOrgClient class"""
        client_for_github_org = GithubOrgClient("google")
        self.assertEqual(
            client_for_github_org.public_repos(),
            self.expected_repos)

    def test_public_repos_with_license(self):
        """a test for public_repos of GithubOrgClient class with license"""
        client_for_github_org = GithubOrgClient("google")
        self.assertEqual(
            client_for_github_org.public_repos(
                license="apache-2.0"),
            self.apache2_repos)
