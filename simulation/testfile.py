import math


def payload_size_to_time(payload, sf):
    BW = 125
    PL = payload
    CR = 4
    CRC = 1
    H = 1
    DE = 0
    SF = sf
    npreamble = 8
    if sf >= 11:
        DE = 0

    Rs = BW / (math.pow(2, SF))
    Ts = 1 / Rs
    symbol = 8 + max(math.ceil((8.0 * PL - 4.0 * SF + 28 + 16 * CRC - 20.0 * H) /
                               (4.0 * (SF - 2.0 * DE))) * (CR + 4), 0)
    Tpreamble = (npreamble + 4.25) * Ts
    Tpayload = symbol * Ts
    ToA = Tpreamble + Tpayload
    return ToA


def main():
    print(payload_size_to_time(51, 7))


if __name__ == "__main__":
    main()
