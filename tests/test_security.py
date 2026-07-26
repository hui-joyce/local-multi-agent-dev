import pytest

from langgraph_orchestration.security import (
    enforce_bind_policy,
    is_loopback_host,
)


@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1", ""])
def test_is_loopback_host_true(host):
    assert is_loopback_host(host) is True

@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.10", "example.com"])
def test_is_loopback_host_false(host):
    assert is_loopback_host(host) is False

def test_enforce_bind_policy_refuses_non_loopback():
    with pytest.raises(RuntimeError):
        enforce_bind_policy("0.0.0.0", surface="test")

@pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1", ""])
def test_enforce_bind_policy_allows_loopback(host):
    enforce_bind_policy(host, surface="test")
