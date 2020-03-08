import pytest
from sepicker.elster.elster_frame import ElsterFrame


class TestElsterFrame:
    def setup(self):
        self.elster_frame = ElsterFrame(
            'OUTSIDE_TEMPERATURE',
            '180.000c',
            'dec_val'
        )

    def test_message(self):
        assert self.elster_frame.message() == [49, 0, 250, 0, 12]

    @pytest.mark.parametrize('value', [245])
    def test_formatter_with_dec_value(self, value):
        assert self.elster_frame.formatter(value) == '24.5'

    @pytest.mark.parametrize('value', [256])
    def test_formatter_with_little_endian(self, value):
        elster_frame = ElsterFrame('STATUS', '180.fdad', 'little_endian')
        assert elster_frame.formatter(value) == '1'

    @pytest.mark.parametrize('value', [1])
    def test_formatter_without_format(self, value):
        elster_frame = ElsterFrame('ERROR', '180.0001')
        assert elster_frame.formatter(value) == 1
