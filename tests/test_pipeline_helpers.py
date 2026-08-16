import importlib
import os
import sys
from pathlib import Path

import pytest

from ipsw_service.ipsw_api import _version_tuple

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"


@pytest.fixture(scope="module")
def automation():
    # importing the module chdirs to the project root, so restore the cwd afterwards
    original_cwd = os.getcwd()
    sys.path.insert(0, str(_SCRIPTS_DIR))
    try:
        yield importlib.import_module("automation")
    finally:
        sys.path.remove(str(_SCRIPTS_DIR))
        os.chdir(original_cwd)


class TestPinnedDevices:
    def test_unset_means_auto_detect(self, automation, monkeypatch):
        monkeypatch.delenv("PIPELINE_DEVICES", raising=False)
        assert automation.pinned_devices() == []

    @pytest.mark.parametrize("raw", ["iPhone18,1 iPhone17,1", "iPhone18,1;iPhone17,1"])
    def test_space_and_semicolon_are_the_separators(self, automation, monkeypatch, raw):
        monkeypatch.setenv("PIPELINE_DEVICES", raw)
        assert automation.pinned_devices() == ["iPhone18,1", "iPhone17,1"]

    def test_commas_are_part_of_the_identifier_not_a_separator(self, automation, monkeypatch):
        monkeypatch.setenv("PIPELINE_DEVICES", "iPhone18,1")
        assert automation.pinned_devices() == ["iPhone18,1"]

    def test_blank_value_is_auto_detect(self, automation, monkeypatch):
        monkeypatch.setenv("PIPELINE_DEVICES", "   ")
        assert automation.pinned_devices() == []


class TestKeepPerDevice:
    def test_defaults_to_one(self, automation, monkeypatch):
        monkeypatch.delenv("PIPELINE_KEEP_PER_DEVICE", raising=False)
        assert automation.keep_per_device() == 1

    @pytest.mark.parametrize("raw,expected", [("3", 3), ("0", 1), ("-2", 1), ("junk", 1)])
    def test_never_drops_below_one(self, automation, monkeypatch, raw, expected):
        # keeping zero would delete the baseline the next diff needs
        monkeypatch.setenv("PIPELINE_KEEP_PER_DEVICE", raw)
        assert automation.keep_per_device() == expected


class TestStalePartialDays:
    def test_defaults_to_a_week(self, automation, monkeypatch):
        monkeypatch.delenv("PIPELINE_STALE_PARTIAL_DAYS", raising=False)
        assert automation.stale_partial_days() == 7

    @pytest.mark.parametrize("raw,expected", [("0", 0), ("30", 30), ("-1", 0), ("junk", 7)])
    def test_parses_and_clamps(self, automation, monkeypatch, raw, expected):
        monkeypatch.setenv("PIPELINE_STALE_PARTIAL_DAYS", raw)
        assert automation.stale_partial_days() == expected


class TestVersionTuple:
    # the ordering `local_ipsws` sorts by; lives in ipsw_api since release_key subsumed it
    def test_double_digit_minor_beats_single_digit(self):
        assert _version_tuple("26.10") > _version_tuple("26.9")

    def test_patch_release_beats_its_base(self):
        assert _version_tuple("26.5.2") > _version_tuple("26.5")

    def test_non_numeric_parts_are_dropped(self):
        assert _version_tuple("26.7 beta") == (26,)


class TestParseIpswName:
    def test_parses_device_version_and_build(self, automation):
        parsed = automation.parse_ipsw_name("iPhone18,1_26.4.2_23E261_Restore.ipsw")
        assert parsed == {"device": "iPhone18,1", "version": "26.4.2", "build": "23E261"}

    @pytest.mark.parametrize(
        "name",
        [
            "checksums.txt.sha1",
            "iPhone18,1_26.4.2_23E261_Restore.ipsw.download",
            "iPhone18,1_26.4.2_Restore.ipsw",
            "random.ipsw",
        ],
    )
    def test_rejects_anything_that_is_not_a_complete_ipsw(self, automation, name):
        assert automation.parse_ipsw_name(name) is None

    def test_round_trips_with_ipsw_filename(self, automation):
        name = automation.ipsw_filename("iPhone18,1", "26.6", "23G71")
        assert automation.parse_ipsw_name(name)["build"] == "23G71"


class TestLocalIpsws:
    @staticmethod
    def _populate(directory, names):
        for name in names:
            (directory / name).write_bytes(b"x")

    def test_orders_newest_version_first_and_filters_by_device(
        self, automation, tmp_path, monkeypatch
    ):
        self._populate(
            tmp_path,
            [
                "iPhone18,1_26.4.1_23E254_Restore.ipsw",
                "iPhone18,1_26.6_23G71_Restore.ipsw",
                "iPhone17,1_26.0_23A341_Restore.ipsw",
                "checksums.txt.sha1",
            ],
        )
        monkeypatch.setattr(automation, "DOWNLOAD_DIR", tmp_path)
        assert [e["version"] for e in automation.local_ipsws("iPhone18,1")] == ["26.6", "26.4.1"]
        assert len(automation.local_ipsws()) == 3

    def test_missing_directory_is_empty(self, automation, tmp_path, monkeypatch):
        monkeypatch.setattr(automation, "DOWNLOAD_DIR", tmp_path / "absent")
        assert automation.local_ipsws() == []


class TestManagedDevices:
    def test_combines_pinned_selection_with_previously_handled_devices(
        self, automation, tmp_path, monkeypatch
    ):
        state = tmp_path / "known.json"
        automation.write_json(state, {"iPhone17,1": {"version": "26.0", "build": "23A341"}})
        monkeypatch.setattr(automation, "KNOWN_BUILDS_FILE", state)
        monkeypatch.setenv("PIPELINE_DEVICES", "iPhone18,1")
        assert automation.managed_devices() == ["iPhone18,1", "iPhone17,1"]

    def test_no_duplicates_when_selection_is_already_recorded(
        self, automation, tmp_path, monkeypatch
    ):
        state = tmp_path / "known.json"
        automation.write_json(state, {"iPhone18,1": {"version": "26.6", "build": "23G71"}})
        monkeypatch.setattr(automation, "KNOWN_BUILDS_FILE", state)
        monkeypatch.setenv("PIPELINE_DEVICES", "iPhone18,1")
        assert automation.managed_devices() == ["iPhone18,1"]

    def test_empty_when_nothing_pinned_or_recorded(self, automation, tmp_path, monkeypatch):
        monkeypatch.setattr(automation, "KNOWN_BUILDS_FILE", tmp_path / "absent.json")
        monkeypatch.delenv("PIPELINE_DEVICES", raising=False)
        assert automation.managed_devices() == []


class TestReadJson:
    def test_missing_file_returns_the_default(self, automation, tmp_path):
        assert automation.read_json(tmp_path / "absent.json", {"fallback": True}) == {
            "fallback": True
        }

    def test_corrupt_file_returns_the_default(self, automation, tmp_path):
        target = tmp_path / "bad.json"
        target.write_text("{not json", encoding="utf-8")
        assert automation.read_json(target, []) == []

    def test_write_creates_parent_directories(self, automation, tmp_path):
        target = tmp_path / "nested" / "deep" / "state.json"
        automation.write_json(target, {"a": 1})
        assert automation.read_json(target, None) == {"a": 1}
