from utils.WDPair import WDPair


def test_wdpair():
    assert WDPair(10, 10) < WDPair(10, 11)
    assert WDPair(9, 20) < WDPair(10, 11)
    assert WDPair(11, 10) > WDPair(10, 11)
    assert WDPair(11, 10) > WDPair(4, 11)
    assert WDPair(11, 11) == WDPair(11, 11)
    assert (WDPair(10, 10) + WDPair(11, 11)).x == 21
    assert (WDPair(10, 34) + WDPair(11, 5)).y == 39