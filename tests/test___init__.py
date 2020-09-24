from datetime import date
from unittest import TestCase

import bssapi_schemas.odata.InformationRegister as Reg
from bssapi_schemas import exch
from bssapi_schemas import odata


class TestPacketsOfTabData(TestCase):
    Packet: exch.Packet = exch.Packet(
        format='0123456789012345678901234567890123456789', source='0123456789012345678901234567890123456789',
        rows=[{'filed1': 'value', 'filed2': 'value'}, {'filed1': 'value', 'filed2': 'value'}],
        file=exch.Packet.File(
            name='file.dbf', modify=date.today(), hash='0123456789012345678901234567890123456789',
            url=exch.Source(user='ivav', host='santens.ru', port=21, path='/path/to/folder'), hex='0102030405'))

    def test_PacketsOfTabDataMixin(self):
        assert isinstance(odata.PacketsOfTabDataMixin(
            FileName=self.Packet.file.name,
            Source=self.Packet.source,
            Packet=self.Packet), odata.PacketsOfTabDataMixin)

    def test_PacketsOfTabData(self):
        data = Reg.PacketsOfTabData(packet=self.Packet)
        assert isinstance(data, Reg.PacketsOfTabData)


class TestPacketsOfTabDataSources(TestCase):
    FormatPacket: exch.FormatPacket = exch.FormatPacket(
        columns={'digits': exch.ColumnDescription(type='N', length=15, decimal_count=2),
                 'string': exch.ColumnDescription(type='C', length=15, decimal_count=None),
                 'date': exch.ColumnDescription(type='D', length=8, decimal_count=None)},
        url=TestPacketsOfTabData.Packet.file.url,
        hash=exch.Hash(format=TestPacketsOfTabData.Packet.format, source=TestPacketsOfTabData.Packet.source))

    def test_PacketsOfTabDataSourcesMixin(self):
        data = odata.PacketsOfTabDataSourcesMixin(
            Hash=self.FormatPacket.hash.source, Format=self.FormatPacket.hash.format, Packet=self.FormatPacket).dict()
        pass

    def test_PacketsOfTabDataSources(self):
        data = Reg.PacketsOfTabDataSources(format=self.FormatPacket)
        assert isinstance(data, Reg.PacketsOfTabDataSources)
