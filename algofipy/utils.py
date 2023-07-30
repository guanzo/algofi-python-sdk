# IMPORTS
import base64

# external
from algosdk import account, mnemonic
from algosdk.transaction import AssetCreateTxn

# local
from .transaction_utils import get_default_params
# FUNCTIONS

def int_to_bytes(num):
    """Int to convert to bytes.

    :param num: int to convert
    :type num: int
    :return: bytes conversion of int
    :rtype: bytes
    """

    return num.to_bytes(8, 'big')

def base64_to_utf8(b64_str):
    """Convert base64 to utf8.
    :param b64_str: base64 string to convert
    :type b64_str: str
    :return: utf8 string
    :rtype: str
    """

    return base64.b64decode(b64_str).decode("utf-8")


def bytes_to_int(bytes):
    """Bytes to convert to int.

    :param bytes: bytes to convert
    :type bytes: bytes
    :return: int conversion of bytes
    :rtype: int
    """

    return int.from_bytes(bytes, 'big')

def get_new_account():
    """Generate a random Algorand account.

    :return: A newly generated Algorand account (private_key, public_key, passphrase)
    :rtype: (str, str, str)
    """

    key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(key)
    return (key, address, passphrase)

def encode_value(value, type):
    """Encode a value of a given type.

    :param value: value to encode
    :type value: int
    :param type: int or bytes
    :type type: str
    :return: int conversion of bytes
    :rtype: int
    """

    if type == 'int':
        return encode_varint(value)
    raise Exception('Unsupported value type %s!' % type)

def encode_varint(number):
    """Encode an int.

    :param number: number to encode
    :type number: int
    :return: encoded int
    :rtype: bytes
    """

    buf = b''
    while True:
        towrite = number & 0x7f
        number >>= 7
        if number:
            buf += bytes([towrite | 0x80])
        else:
            buf += bytes([towrite])
            break
    return buf

def create_asset_transaction(algod, sender, total, decimals, default_frozen, manager, reserve, freeze, clawback,
                             unit_name, asset_name, url):

    params = get_default_params(algod)

    return AssetCreateTxn(
        sender=sender,
        sp=params,
        total=total,
        decimals=decimals,
        default_frozen=default_frozen,
        manager=manager,
        reserve=reserve,
        freeze=freeze,
        clawback=clawback,
        unit_name=unit_name,
        asset_name=asset_name,
        url=url
    )