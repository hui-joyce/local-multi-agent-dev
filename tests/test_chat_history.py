import json

from langgraph_orchestration import chat_history


def _point_at(tmp_path, monkeypatch):
    target = tmp_path / "chat_history.json"
    monkeypatch.setenv("CHAT_HISTORY_FILE", str(target))
    monkeypatch.delenv("CHAT_HISTORY_DIR", raising=False)
    return target

def test_load_missing_returns_empty(tmp_path, monkeypatch):
    _point_at(tmp_path, monkeypatch)
    assert chat_history.load_history() == []

def test_round_trip(tmp_path, monkeypatch):
    _point_at(tmp_path, monkeypatch)
    history = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
    ]
    chat_history.save_history(history)
    assert chat_history.load_history() == history

def test_save_creates_parent_dir(tmp_path, monkeypatch):
    target = tmp_path / "nested" / "deep" / "history.json"
    monkeypatch.setenv("CHAT_HISTORY_FILE", str(target))
    chat_history.save_history([{"role": "user", "content": "x"}])
    assert target.exists()

def test_malformed_entries_filtered(tmp_path, monkeypatch):
    target = _point_at(tmp_path, monkeypatch)
    # missing 'content', not a dict, and a valid one
    target.write_text(json.dumps([
        {"role": "user"},
        "not-a-dict",
        {"role": "assistant", "content": "ok"},
    ]), encoding="utf-8")
    assert chat_history.load_history() == [{"role": "assistant", "content": "ok"}]

def test_corrupt_file_returns_empty(tmp_path, monkeypatch):
    target = _point_at(tmp_path, monkeypatch)
    target.write_text("{not valid json", encoding="utf-8")
    assert chat_history.load_history() == []

def test_save_caps_length(tmp_path, monkeypatch):
    _point_at(tmp_path, monkeypatch)
    big = [{"role": "user", "content": str(i)} for i in range(chat_history.MAX_MESSAGES + 50)]
    chat_history.save_history(big)
    loaded = chat_history.load_history()
    assert len(loaded) == chat_history.MAX_MESSAGES
    # keeps the most recent messages
    assert loaded[-1]["content"] == str(chat_history.MAX_MESSAGES + 49)

def test_history_path_prefers_file_over_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("CHAT_HISTORY_FILE", str(tmp_path / "explicit.json"))
    monkeypatch.setenv("CHAT_HISTORY_DIR", str(tmp_path / "somedir"))
    assert chat_history.history_path() == tmp_path / "explicit.json"

def test_history_path_uses_dir(tmp_path, monkeypatch):
    monkeypatch.delenv("CHAT_HISTORY_FILE", raising=False)
    monkeypatch.setenv("CHAT_HISTORY_DIR", str(tmp_path / "somedir"))
    assert chat_history.history_path() == tmp_path / "somedir" / "chat_history.json"
