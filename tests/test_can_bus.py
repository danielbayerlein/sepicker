import can
from freezegun import freeze_time
import pytest

from sepicker.elster.elster import Elster
from sepicker.interface.can_bus import CanBus


class TestCanBus:
    @pytest.fixture
    def can_bus(self):
        return CanBus(interface='can0', sender=680)

    @pytest.fixture
    def mock_can_interface_bus(self, mocker):
        return mocker.patch('can.interface.Bus')

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

    def test_init(self, can_bus):
        assert can_bus.interface == 'can0'
        assert can_bus.sender == int('680', 16)

    def test_enter_success(self, mock_can_interface_bus, can_bus, elster):
        with can_bus:
            can_bus.set_notifier(elster.listener)
            assert can_bus.bus is not None
            mock_can_interface_bus.assert_called_once_with(
                channel='can0',
                interface='socketcan'
            )

    def test_enter_failure(self, mocker, can_bus):
        mock_exit = mocker.patch('sys.exit', side_effect=SystemExit)
        with pytest.raises(SystemExit):
            with can_bus:
                pass
        mock_exit.assert_called_once_with(1)

    def test_exit(self, mock_can_interface_bus, mocker, can_bus):
        can_bus.notifier = mocker.Mock()
        with can_bus:
            pass
        can_bus.notifier.stop.assert_called_once()
        mock_can_interface_bus.return_value.shutdown.assert_called_once()

    def test_send(self, mock_can_interface_bus, mocker, can_bus, elster):
        with can_bus:
            can_bus.set_notifier(elster.listener)
            can_bus.send(bytearray([0xd2, 0x00, 0x0c, 0x01, 0x80]))
            mock_can_interface_bus.return_value.send.assert_called_once()
            sent_msg = mock_can_interface_bus.return_value.send.call_args[0][0]
            assert sent_msg.arbitration_id == int('680', 16)
            assert sent_msg.data == bytearray([0xd2, 0x00, 0x0c, 0x01, 0x80])
            assert sent_msg.is_extended_id is False

    def test_set_notifier(self, mock_can_interface_bus, mocker, can_bus):
        listener = mocker.Mock()
        with can_bus:
            can_bus.set_notifier(listener)
            assert isinstance(can_bus.notifier, can.Notifier)
            assert listener in can_bus.notifier.listeners
