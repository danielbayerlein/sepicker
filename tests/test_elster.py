from datetime import datetime
from freezegun import freeze_time
import pytest

from sepicker.elster.elster import Elster


class TestElster:
    @pytest.fixture
    @freeze_time("2024-11-10")
    def elster(self):
        return Elster(
            sender=680,
            items=[
                {
                    "name": 'OUTSIDE_TEMPERATURE',
                    "index": '180.000c',
                    "format": 'dec_val'
                }
            ]
        )

    def test_init(self, elster):
        assert elster.frames[0].name == 'OUTSIDE_TEMPERATURE'
        assert elster.frames[0].receiver == int('180', 16)
        assert elster.frames[0].register == int('000c', 16)
        assert elster.frames[0].format == 'dec_val'
        assert elster.values == []
        assert elster.datetime == datetime(2024, 11, 10)
        assert elster.sender == int(str(680), 16)

    @pytest.mark.parametrize("msg_data, arbitration_id", [
        ([0xd2, 0x00, 0x0c, 0x01, 0x80], int('180', 16)),
        ([0xd2, 0x00, 0xfa, 0x00, 0x0c, 0x01, 0x80], int('180', 16)),
    ])
    def test_listener(self, msg_data, arbitration_id, mocker, elster):
        msg_mock = mocker.Mock(
            spec="can.Message",
            data=bytearray(msg_data),
            arbitration_id=arbitration_id
        )
        elster.listener(msg_mock)

        assert len(elster.values) == 1
        assert elster.values[0][0] == datetime(2024, 11, 10)
        assert elster.values[0][1] == 'OUTSIDE_TEMPERATURE'
        assert elster.values[0][2] == '38.4'

    def test_listener_invalid(self, mocker, elster):
        msg_mock = mocker.Mock(
            spec="can.Message",
            data=bytearray([0xd2, 0x00, 0x0c, 0x01, 0x80]),
            arbitration_id=int('601', 16)
        )
        elster.listener(msg_mock)

        assert len(elster.values) == 0

    def test_is_done(self, elster):
        elster.values = [
            (datetime.now(), 'OUTSIDE_TEMPERATURE', int('180', 16))
        ]
        assert elster.is_done()

        elster.values = [
            (datetime.now(), 'OUTSIDE_TEMPERATURE', int('180', 16)),
            (datetime.now(), 'ISTTEMPERATUR_HK_2', int('601', 16))
        ]
        assert not elster.is_done()

    def test__exist_receiver(self, elster):
        assert elster._exist_receiver(int('180', 16))
        assert not elster._exist_receiver(int('601', 16))

    def test__get_frame(self, elster):
        frame = elster._get_frame(int('180', 16), 0x0c)
        assert frame.name == 'OUTSIDE_TEMPERATURE'

        frame = elster._get_frame(int('601', 16), 0x0c)
        assert frame is None
