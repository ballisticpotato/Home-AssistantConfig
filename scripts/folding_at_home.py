#!/usr/bin/python3

from telnetlib import Telnet
import argparse
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--action', choices=['pause','unpause'])
parser.add_argument('--power', choices=['light', 'medium', 'full'])
args = parser.parse_args()

with Telnet('192.168.1.71', 36330) as tn:
    tn.read_until(b'Folding@home')
    tn.write(b'auth jerry\n')
    tn.expect([b'OK'])
    if args.action:
        tn.write(args.action.encode('ascii') + b'\n')

    if args.power:
        tn.write(b'option power ' + args.power.encode('ascii') + b'\n')

    tn.close()