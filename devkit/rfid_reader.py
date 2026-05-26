from mfrc522 import MFRC522

rdr = MFRC522(
    sck=18,
    mosi=23,
    miso=19,
    rst=27,
    cs=5
)

def read_card():

    rdr.init()

    stat, tag_type = rdr.request(
        rdr.REQIDL
    )

    if stat == rdr.OK:

        stat, uid = rdr.SelectTagSN()

        if stat == rdr.OK:

            card = int.from_bytes(
                bytes(uid),
                "little",
                False
            )

            return card

    return None