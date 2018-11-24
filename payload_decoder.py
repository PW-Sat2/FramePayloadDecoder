import imp
import os
import sys
import socket
import re
import struct
import json
import pprint


sys.path.append(os.path.join(os.path.dirname(
    __file__), '../PWSat2OBC/integration_tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import timedelta, datetime, date, time

from struct import pack

import response_frames

from bitarray import bitarray
from devices import comm_beacon
from telecommand import *

from emulator.beacon_parser.full_beacon_parser import FullBeaconParser
from emulator.beacon_parser.parser import BitReader, BeaconStorage


from utils import ensure_string, ensure_byte_list
import response_frames


class InvalidFrame:
    def __init__(self, raw, error):
        self._raw = raw
        self._error = error


class FallbackResponseDecorator:
    def __init__(self, frame_decoder):
        self._frame_decoder = frame_decoder

    def decode(self, frame):
        try:
            return self._frame_decoder.decode(frame)
        except Exception as e:
            return InvalidFrame(frame, e)


class ParseBeacon:
    @staticmethod
    def parse(frame):
        print type(frame)
        if isinstance(frame, comm_beacon.BeaconFrame):
            all_bits = bitarray(endian='little')
            all_bits.frombytes(''.join(map(lambda x: pack('B', x), frame.payload())))
            
            reader = BitReader(all_bits)
            store = BeaconStorage()

            parsers = FullBeaconParser().GetParsers(reader, store)
            parsers.reverse()

            while len(parsers) > 0:
                parser = parsers.pop()
                parser.parse()

            result = store.storage
        else:
            result = frame

        return result

    @staticmethod
    def convert_values(o):
        if isinstance(o, timedelta):
            return o.total_seconds()
        
        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, time):
            return o.strftime("%H:%M:%S")

        try:
            return {
                'raw': o.raw,
                'converted': o.converted,
                'unit': getattr(o, 'unit') if hasattr(o, 'unit') else None
            }
        except AttributeError:
            return o


    @staticmethod
    def convert(beacon):
        for k, v in beacon.items():
            for k2, v2 in beacon[k].items():
                beacon[k][k2] = ParseBeacon.convert_values(v2)

        return beacon

    @staticmethod
    def convert_json(beacon):
        return json.dumps(beacon, default=ParseBeacon.convert_values, sort_keys=True, indent=4)



class PayloadDecoder:
    @staticmethod
    def decode(raw_frame_payload):
        frame_decoder = FallbackResponseDecorator(response_frames.FrameDecoder(response_frames.frame_factories))
        frame_object = frame_decoder.decode(ensure_byte_list(raw_frame_payload))

        return ParseBeacon.parse(frame_object)