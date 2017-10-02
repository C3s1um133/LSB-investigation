#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re

from urllib2 import quote as urlquote
from urllib2 import unquote as urlunquote
from urllib import _is_unicode
from urllib import _asciire
from urllib import _hextochr
from xml.sax.saxutils import escape as entityquote
from xml.sax.saxutils import unescape as entityunquote
from codecs import register, CodecInfo

from struct import pack, unpack

MORSE = (
    ('A', ".-"),            # A, a
    ('B', "-..."),          # B, b
    ('C', "-.-."),          # C, c
    ('D', "-.."),           # D, d
    ('E', "."),             # E, e
    ('F', "..-."),          # F, f
    ('G', "--."),           # G, g
    ('H', "...."),          # H, h
    ('I', ".."),            # I, i
    ('J', ".---"),          # J, j
    ('K', "-.-"),           # K, k; 
                            # also used to indicate "Invitation to Transmit"
    ('L', ".-.."),          # L, l
    ('M', "--"),            # M, m
    ('N', "-."),            # N, n
    ('O', "---"),           # O, o
    ('P', ".--."),          # P, p
    ('Q', "--.-"),          # Q, q
    ('R', ".-."),           # R, r
    ('S', "..."),           # S, s
    ('T', "-"),             # T, t
    ('U', "..-"),           # U, u
    ('V', "...-"),          # V, v
    ('W', ".--"),           # W, w
    ('X', "-..-"),          # X, x
    ('Y', "-.--"),          # Y, y
    ('Z', "--.."),          # Z, z
    ('0', "-----"),         # 0
    ('1', ".----"),         # 1
    ('2', "..---"),         # 2
    ('3', "...--"),         # 3
    ('4', "....-"),         # 4
    ('5', "....."),         # 5
    ('6', "-...."),         # 6
    ('7', "--..."),         # 7
    ('8', "---.."),         # 8
    ('9', "----."),         # 9
    (' ', "/"),             # Currently used to indicate character boundaries
    ('.', ".-.-.-"),        # Period
    (',', "--..--"),        # Comma
    ('?', "..--.."),        # Question Mark
    ('\'', ".----."),       # Apostrophe
    ('!', "-.-.--"),        # Exclamation Point, Digraph: KW (Not standardized, ---. also used)
    ('/', "-..-."),         # Slash or Fraction Bar
    ('(', "-.--."),         # Open Parenthesis
    (')', "-.--.-"),        # Close Parenthesis
    ('&', ".-..."),         # Ampersand, Digraph: AS, Prosign: Wait (Not in ITU-R recommendation)
    (':', "---..."),        # Colon
    (';', "-.-.-."),        # Semicolon
    ('=', "-...-"),         # Double Dash (Equal Sign)
    ('+', ".-.-."),         # Plus Sign
    ('-', "-....-"),        # Hyphen or Minus Sign
    ('_', "..--.-"),        # Underscore (Not in ITU-R recommendation)
    ('"', ".-..-."),        # Quotation Mark
    ('$', "...-..-"),       # Dollar Sign, Digraph: SX (Not in ITU-R recommendation)
    ('@', ".--.-."),        # At Sign, Digraph: AC (Formally added to ITU-R recommendation in 2004)
    ('', '')
    )


###############################################################################
# ascii85 defs
###############################################################################


ascii85_charset = re.compile('([!-u]*)')


###############################################################################
# yenc defs
###############################################################################


yenc_escape = [0x00, 0x0a, 0x0d, ord('='), ord('.')]


###############################################################################
# BCD
###############################################################################

# soon....

###############################################################################
# helper functions
###############################################################################


def blocks(data, size):
    assert (len(data) % size) == 0, \
           "Cannot divide into blocks of size %s" % size
    for i in xrange(0, len(data), size):
        yield data[i:i + size]


def parity(bit_array, odd=False):
    out = sum(bit_array) % 2
    if odd:
        out = ~out % 2
    return out


def rotx(data, rotval):
    output = []
    for d in data:
        if not d.isalpha():
            output.append(d)
            continue
        off = 65
        if d.islower():
            off += 32
        output.append(chr((((ord(d) - off) + rotval) % 26) + off))
    return unicode(''.join(output))


def rotx_codec_generator(rotval):
    name = "rot%d"  % rotval
    rx_enc = lambda data: (rotx(data, rotval), len(data))
    rx_dec = lambda data: (rotx(data, -rotval), len(data))
    return CodecInfo(name=name, encode=rx_enc, decode=rx_dec)


def get_codecs_list():
    """In case you're wondering what's in this package, you can find out.
    """
    for codec in  CODECS_IN_FILE.iterkeys():
        print codec


###############################################################################
# actual encoders and encoding wrappers
###############################################################################


def morse_encode(input, errors='strict'):
    morse_map = dict(MORSE)
    input = input.upper()
    for c in input:
        assert c in morse_map, "Unencodable character '%s' found. Failing" % c
    output = ' '.join(morse_map[c] for c in input)
    return (output, len(input))


def morse_decode(input, errors='strict'):
    morse_map = dict((c, m) for m, c in MORSE)
    input = input.replace('  ', '/').replace('/', ' / ')
    splinput = input.split()
    for c in splinput:
        assert c in morse_map, "Could not decode '%s' to ascii. Failing" % c
    output = ''.join(morse_map[c] for c in splinput)
    return (output, len(input))


def bin_encode(input, errors='strict'):
    """print 8 bits of whatever int goes in"""
    output = ""
    for c in input:
        l = '{0:0>8b}'.format(ord(c))
        output += ''.join(l)
    return (output, len(input))


def bin_decode(input, errors='strict'):
    """print 8 bits of whatever int goes in"""
    output = ""
    assert (len(input) % 8) == 0, \
           "Wrong number of bits, %s is not divisible by 8" % len(input)
    output = ''.join(chr(int(c, 2)) for c in blocks(input, 8))
    return (output, len(input))


def url_decode(input, errors='strict'):
    output = urlunquote(input)
    return (output, len(input))


def url_encode(input, errors='strict'):
    output = urlquote(input)
    return (output, len(input))


def entity_decode(input, errors='strict'):
    output = entityunquote(input)
    return (output, len(input))


def entity_encode(input, errors='strict'):
    output = entityquote(input)
    return (output, len(input))

def entity_encode_hex(input, errors='strict'):
    """
    Encode &, <, and > in a string of data.
    as their hex HTML entity representation.
    """
    output = ''
    for character in input:
        if character in ('&', '<', '>'):
            output += "&#x%s;" % character.encode('hex')
        else:
            output += character

    return (output, len(input))

def entity_decode_hex(input, errors='strict'):
    """
    Decode hex HTML entity data in a string.
    """
    if _is_unicode(input):
        if '%' not in input:
            return s
        bits = _asciire.split(input)
        res = [bits[0]]
        append = res.append
        for i in range(1, len(bits), 2):
            append(unquote(str(bits[i])).decode('latin1'))
            append(bits[i + 1])
        return (''.join(res), len(input))

    preamble_regex = re.compile(r"&#x", flags=re.I)
    bits = preamble_regex.split(input)
    # fastpath
    if len(bits) == 1:
        return input
    res = [bits[0]]
    append = res.append
    for item in bits[1:]:
        try:
            append(_hextochr[item[:2]])
            append(item[3:])
        except KeyError:
            append('&#x')
            append(item)
            append(';')

    return (''.join(res), len(input))


def ascii85_encode(input, errors='strict'):
    #encoding is adobe not btoa
    bs = 4
    padding = bs - ((len(input) % bs) or bs)
    input += '\0' * padding
    output = ""
    for block in blocks(input, bs):
        start = unpack(">I", block)[0]
        if not start:
            output += "z"
            continue
        quot, rem = divmod(start, 85)
        chr_block = chr(rem + 33)
        for i in xrange(bs):
            quot, rem = divmod(quot, 85)
            chr_block += chr(rem + 33)
        output += ''.join(reversed(chr_block))
    if padding:
        output = output[:-padding]
    return output, len(input)


def ascii85_decode(input, errors='strict'):
    bs = 5
    for i in ('y', 'z'):
        for block in input.split(i)[:-1]:
            assert not len(block) % bs, "'%s' found within a block" % i
            #this will handle the error but it will not give a good
            #error message
    # supports decoding as adobe or btoa 4.2
    input = input.replace('z', '!!!!!')  # adobe & btoa 4.2
    input = input.replace('y', '+<VdL')  # btoa replace block of ' '
    input = ''.join(re.findall(ascii85_charset, input))
    # silently drop all non-ascii85 chars....
    padding = bs - ((len(input) % bs) or bs)
    input += 'u' * padding
    output = ""
    for block in blocks(input, bs):
        data = 0
        for idx in xrange(len(block)):
            place = (bs - 1) - idx
            place_val = ord(block[idx]) - 33
            if place:
                place_val = place_val * (85 ** place)
            data += place_val
        assert 0 <= data <= 4294967295, "invalid block '%s'" % block
        output += pack(">I", data)
    if padding:
        output = output[:-padding]
    return output, len(input)


def y_encode(input, errors='strict'):
    output = ''
    for c in input:
        o = (ord(c) + 42) % 256
        if o in yenc_escape:
            output += '='
            o = (o + 64) % 256
        output += chr(o)
    return output, len(input)


def y_decode(input, errors='strict'):
    output = ''
    #this is more C than python
    len_in = len(input)
    i = 0
    while True:
        if i == len_in:
            break
        c = ord(input[i])
        if input[i] == '=':
            assert len_in > (i + 1), "last character cannot be an escape"
            i += 1
            c = (ord(input[i]) - 64) % 256
        c = (c - 42) % 256
        i += 1
        output += chr(c)
    return output, len(input)


def aba_track_2_encode(input, errors='strict'):
    #this is in progress
    output = ''
    assert all(map(lambda x: 0x3f >= ord(x) >= 0x30, input)), \
               "Characters found out of range 0x30 - 0x3f"
    len_in = len(input)
    assert len_in <= 37, ("No room for sentinel and LRC. "
                          "Input must be 37 characters or under")
    input = ";" + input + "?"
    out = []
    for c in input:
        c = ord(c) - 48
        l = list('{0:0>4b}'.format(c))
        l = [int(i) for i in reversed(l)]
        l.append(sum(l) % 2)
        out.append(l)
    lrc = [parity(int(l[i]) for l in out) for i in xrange(4)]
    lrc.append(parity(lrc))
    out.append(lrc)
    output = ""
    for l in out:
        output += ''.join(str(i) for i in l)
    return output, len(input)


def aba_track_2_decode(input, errors='strict'):
    #this is in progress
    len_in = len(input)
    assert not len_in % 5, "Input must be divisible by 5"
    assert not len_in > (5 * 40), "String too long: cannot be ABA Track 2"
    #we're going to ignore parity for now
    print [chr(int(c[:0:-1], 2)+48) for c in blocks(input, 5)]
    output = ''.join(chr(int(c[:0:-1], 2)+48) for c in blocks(input, 5))
    output = output[-1:]
    return output, len(input)





###############################################################################
# Codec Registration
###############################################################################

CODECS_IN_FILE = {"morse": CodecInfo(name='morse',
                                     encode=morse_encode,
                                     decode=morse_decode),
                  "bin": CodecInfo(name='bin',
                                   encode=bin_encode,
                                   decode=bin_decode),
                  "url": CodecInfo(name='url',
                                   encode=url_encode,
                                   decode=url_decode),
                  "entity": CodecInfo(name='entity',
                                   encode=entity_encode,
                                   decode=entity_decode),
                  "entityhex": CodecInfo(name='entityhex',
                                   encode=entity_encode_hex,
                                   decode=entity_decode_hex),
                  "ascii85": CodecInfo(name='ascii85',
                                       encode=ascii85_encode,
                                       decode=ascii85_decode),
                  "yenc": CodecInfo(name='yenc',
                                       encode=y_encode,
                                       decode=y_decode),
                }


for r in xrange(1, 26):
    CODECS_IN_FILE["rot%d" % r] = rotx_codec_generator(r)


#this is bad, I need to do something different
register(lambda name: CODECS_IN_FILE[name])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
