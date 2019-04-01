import os
import sys
from pathlib import Path
from binfilepy import BinFile
from binfilepy import CFWBINARY
from binfilepy import CFWBCHANNEL
from binfilepy import constant


def test_binfilewriter():
    filename = "mytest.bin"
    outfile = Path(filename)
    if outfile.exists():
        outfile.unlink()
    with BinFile(filename, "w") as f:
        header = CFWBINARY()
        header.setValue(1.0 / 240.0, 2019, 1, 28, 8, 30, 0.0, 0.0, 2, 0)
        f.setHeader(header)
        channel1 = CFWBCHANNEL()
        channel1.setValue("I", "mmHg", 1.0, 0.0)
        f.addChannel(channel1)
        channel2 = CFWBCHANNEL("II", "mmHg", 1.0, 0.0)
        f.addChannel(channel2)
        chanData = []
        d1 = [1, 2, 3, 4, 5, 6, 7, 8, 8, 7, 6, 5, 4, 3, 2, 1]
        d2 = [8, 7, 6, 5, 4, 3, 2, 1, 1, 2, 3, 4, 5, 6, 7, 8]
        data1 = []
        data2 = []
        for i in range(500):
            data1 = data1 + d1
            data2 = data2 + d2
        chanData.append(data1)
        chanData.append(data2)
        f.writeHeader()
        f.writeChannelData(chanData)
        f.updateSamplesPerChannel(8000, True)
    with BinFile(filename, "r") as g:
        g.readHeader()
        assert(len(g.channels) == 2)
        assert(g.header.SamplesPerChannel == 8000)
    # remove temporary file created
    try:
        outfile = Path(filename)
        if outfile.exists():
            outfile.unlink()
    except:
        # ignore error
        pass
    return
