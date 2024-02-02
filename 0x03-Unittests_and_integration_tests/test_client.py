#!/usr/bin/env python3
"""Unittests for class GithubOrgClient in client."""
import unittest
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from unittest.mock import patch, PropertyMock, Mock
from requests import HTTPError
from parameterized import parameterized, parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """Represents test cases for GithubOrgClient."""

    @parameterized.expand([
        # ("google", {"login": "google"}),
        # ("abc", {"login": "abc"})
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, input, mock):
        # mock.return_value = MagicMock(return_value=expected)
        test_class = GithubOrgClient(input)
        # self.assertEqual(test_class.org(), expected)
        test_class.org()
        mock.called_once_with(f"https://api.github.com/orgs/{input}")

    def test_public_repos_url(self):
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        test_payload = {
            "name": "dagger",
            "owner":
            {
                "login": "google",
                "id": 1342004
            }
        }
        mock_get_json.return_value = test_payload["name"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["name"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "other"}}, "apache-2.0", False)
    ])
    def test_has_license(self, repo, key, expected) -> None:
        goclient = GithubOrgClient("dagger")
        client_has_licence = goclient.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3]
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Represents integration tests for GithubOrgClient class."""

    @classmethod
    def SetUpClass(cls):
        """Set-up for tests."""
        route_payload = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self):
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        test_class = GithubOrgClient("google")
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Tears down the tests."""
        cls.get_patcher.stop()
