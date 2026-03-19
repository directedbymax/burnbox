import os

import pytest

from burnbox_cli import BurnBox
from burnbox_cli.common import Common
from burnbox_cli.mode_settings import ModeSettings


class MyOnion:
    def __init__(self):
        self.auth_string = "TestHidServAuth"
        self.private_key = ""
        self.scheduled_key = None

    @staticmethod
    def start_onion_service(
        self, mode, mode_settings_obj, await_publication=True, save_scheduled_key=False
    ):
        return "test_service_id.onion"


@pytest.fixture
def burnbox_obj():
    common = Common()
    return BurnBox(common, MyOnion())


@pytest.fixture
def mode_settings_obj():
    common = Common()
    return ModeSettings(common)


class TestBurnBox:
    def test_init(self, burnbox_obj):
        assert burnbox_obj.hidserv_dir is None
        assert burnbox_obj.onion_host is None
        assert burnbox_obj.local_only is False

    def test_start_onion_service(self, burnbox_obj, mode_settings_obj):
        burnbox_obj.start_onion_service("share", mode_settings_obj)
        assert 17600 <= burnbox_obj.port <= 17650
        assert burnbox_obj.onion_host == "test_service_id.onion"

    def test_start_onion_service_local_only(self, burnbox_obj, mode_settings_obj):
        burnbox_obj.local_only = True
        burnbox_obj.start_onion_service("share", mode_settings_obj)
        assert burnbox_obj.onion_host == "127.0.0.1:{}".format(burnbox_obj.port)
