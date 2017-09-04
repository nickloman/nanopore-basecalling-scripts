#Written by Nick Loman @pathogenomenick

from __future__ import print_function

import os
import os.path
import sys
import shutil
import re
import argparse

def run(args):
	basecalled_files = set()

	for root, dirs, files in os.walk(args.dir, topdown=False):
		for name in files:
			if name.endswith('.fast5'):
				if name in basecalled_files:
					fn = args.dir + '/' + root + '/' + name
					print(fn)
					os.unlink(fn)
				basecalled_files.add(name)

parser = argparse.ArgumentParser(description='Stage files for processing.')
parser.add_argument('dir', help='Directory to remove duplicates from')

args = parser.parse_args()
run(args)

