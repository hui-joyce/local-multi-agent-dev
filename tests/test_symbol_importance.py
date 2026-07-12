from langgraph_orchestration.graphs.reverse_engineering import _symbol_importance


class TestSymbolImportance:
    def test_security_vocabulary_outranks_neutral(self):
        assert _symbol_importance("-[AuthManager validateCredential:]") > _symbol_importance(
            "-[LayoutView setFrame:]"
        )

    def test_destructors_and_boilerplate_are_penalised(self):
        assert _symbol_importance("-[Foo dealloc]") < 0
        assert _symbol_importance("___copy_helper_block_invoke") < _symbol_importance("_parseToken")

    def test_cxx_destruct_is_penalised(self):
        assert _symbol_importance("-[Foo .cxx_destruct]") < _symbol_importance("-[Foo verify:]")

    def test_trivial_single_arg_setter_is_penalised(self):
        setter = _symbol_importance("-[Foo setName:]")
        richer = _symbol_importance("-[Foo encryptData:withKey:andNonce:]")
        assert richer > setter

    def test_more_arguments_increase_score(self):
        one = _symbol_importance("-[Svc handle:]")
        three = _symbol_importance("-[Svc handle:with:and:]")
        assert three > one
