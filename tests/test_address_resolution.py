from langgraph_orchestration.tooling.decompiler_tools import (
    _resolve_func_and_segment,
    _resolve_objc_method_impl,
)


class _Root:
    def __init__(self, boundaries=None, segment="", objc=None, objc_raises=False):
        self._boundaries = boundaries or {}
        self._segment = segment
        self._objc = objc or []
        self._objc_raises = objc_raises

    def exposed_get_function_boundaries(self, addr):
        return self._boundaries.get(addr, (0, 0))

    def exposed_get_segment_name(self, addr):
        return self._segment

    def exposed_find_objc_method_impl(self, selector):
        if self._objc_raises:
            raise RuntimeError("older server has no exposed_find_objc_method_impl")
        return self._objc

class _Conn:
    def __init__(self, root):
        self.root = root

class TestResolveFuncAndSegment:
    def test_classifies_a_real_function(self):
        conn = _Conn(_Root(boundaries={0x1100: (0x1000, 0x1200)}, segment="__text"))
        is_func, func_start, seg = _resolve_func_and_segment(conn, 0x1100)
        assert is_func is True
        assert func_start == 0x1000
        assert seg == "__text"

    def test_falls_back_when_no_boundaries(self):
        conn = _Conn(_Root(boundaries={0x1100: (0, 0)}, segment=""))
        is_func, func_start, seg = _resolve_func_and_segment(conn, 0x1100)
        assert is_func is False
        assert func_start == 0x1100  # falls back to the queried address
        assert seg == ""

class TestResolveObjcMethodImpl:
    def test_resolves_selector_to_real_implementation(self):
        root = _Root(
            boundaries={0x2200: (0x2200, 0x2300)},
            segment="__text",
            objc=[{"address": 0x2200, "name": "-[AuthManager verify:]"}],
        )
        out = _resolve_objc_method_impl(_Conn(root), "verify:", "verify:")
        assert out is not None
        assert out["type"] == "symbol"
        assert out["query"] == "-[AuthManager verify:]"
        assert out["address"] == hex(0x2200)

    def test_skips_objc_msgsend_stub_segments(self):
        root = _Root(
            boundaries={0x3300: (0x3300, 0x3300)},
            segment="__auth_stubs",
            objc=[{"address": 0x3300, "name": "-[X verify:]"}],
        )
        assert _resolve_objc_method_impl(_Conn(root), "verify:", "verify:") is None

    def test_no_match_returns_none(self):
        assert _resolve_objc_method_impl(_Conn(_Root(objc=[])), "verify:", "verify:") is None

    def test_returns_none_when_server_lacks_objc_lookup(self):
        root = _Root(objc_raises=True)
        assert _resolve_objc_method_impl(_Conn(root), "verify:", "verify:") is None
