from datetime import date
from unittest import TestCase

import bssapi_schemas.odata.InformationRegister as reg
from bssapi_schemas import exch
from bssapi_schemas.odata import mixin


class TestPacketsOfTabData(TestCase):
    Packet: exch.Packet = exch.Packet(
        format='a123456789012345678901234567890123456789', source='a123456789012345678901234567890123456789',
        rows=[{'filed1': 'value', 'filed2': 'value'}, {'filed1': 'value', 'filed2': 'value'}],
        file=exch.Packet.File(
            name='file.dbf', modify=date.today(), hash='A123456789012345678901234567890123456789',
            url=exch.Source(user='ivav', host='santens.ru', port=21, path='/path/to/folder'), hex='0102030405'))

    def test_mixin_PacketsOfTabData(self):
        data = mixin.PacketsOfTabData(
            Hash=self.Packet.file.hash,
            FileName=self.Packet.file.name,
            Source=self.Packet.source,
            Packet=self.Packet)

    def test_reg_PacketsOfTabData(self):
        data = reg.PacketsOfTabData(packet=self.Packet)



class TestPacketsOfTabDataSources(TestCase):
    FormatPacket: exch.FormatPacket = exch.FormatPacket(
        columns={'digits': exch.ColumnDescription(type='N', length=15, decimal_count=2),
                 'string': exch.ColumnDescription(type='C', length=15, decimal_count=None),
                 'date': exch.ColumnDescription(type='D', length=8, decimal_count=None)},
        url=TestPacketsOfTabData.Packet.file.url,
        hash=exch.Hash(format=TestPacketsOfTabData.Packet.format, source=TestPacketsOfTabData.Packet.source))

    def test_mixin_PacketsOfTabDataSources(self):
        data = mixin.PacketsOfTabDataSources(
            Hash=self.FormatPacket.hash.source, Format=self.FormatPacket.hash.format,
            Packet=self.FormatPacket)


    def test_reg_PacketsOfTabDataSources(self):
        data = reg.PacketsOfTabDataSources(format=self.FormatPacket)

