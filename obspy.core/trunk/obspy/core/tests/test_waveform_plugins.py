# -*- coding: utf-8 -*-

from obspy.core import Trace, read
from obspy.core.utcdatetime import UTCDateTime
from obspy.core.util import NamedTemporaryFile, _getPlugins
import numpy as np
import os
import unittest


class WaveformPluginsTestCase(unittest.TestCase):
    """
    Test suite for all installed waveform plug-ins.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_writeFormat(self):
        """
        """
        formats = _getPlugins('obspy.plugin.waveform', 'writeFormat')
        for format in formats:
            for byteorder in ['<', '>', '=']:
                # XXX: SAC and GSE2 fail those test!!!
                if format in ['SAC', 'GSE2']:
                    continue
                # new trace object
                tr = Trace(data=np.arange(0, 2000))
                tr.stats.network = "BW"
                tr.stats.station = "MANZ1"
                tr.stats.location = "00"
                tr.stats.channel = "EHE"
                tr.stats.calib = 0.999999
                tr.stats.starttime = UTCDateTime(2009, 1, 13, 12, 1, 2, 999000)
                #1 - r/w little endian with auto detection
                outfile = NamedTemporaryFile().name
                tr.write(outfile, format=format, byteorder=byteorder)
                if format == 'Q':
                    outfile += '.QHD'
                st = read(outfile)
                self.assertEquals(len(st), 1)
                tr2 = st[0]
                self.assertEquals(tr2.data.dtype.byteorder, '=')
                if format not in ['MSEED', 'WAV']:
                    self.assertAlmostEquals(tr2.stats.calib, 0.999999)
                if format not in ['WAV']:
                    self.assertEquals(tr2.stats.starttime,
                                      UTCDateTime(2009, 1, 13, 12, 1, 2,
                                                  999000))
                if format in ['Q', 'SH_ASC']:
                    self.assertEquals(tr2.id, ".MANZ1..EHE")
                elif format not in ['WAV']:
                    self.assertEquals(tr2.id, "BW.MANZ1.00.EHE")
                os.remove(outfile)
                if format == 'Q':
                    os.remove(outfile[:-4] + '.QBN')
                    os.remove(outfile[:-4])


def suite():
    return unittest.makeSuite(WaveformPluginsTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
