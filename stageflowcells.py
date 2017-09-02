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

	for root, dirs, files in os.walk(args.basecalled, topdown=False):
		for name in files:
			if name.endswith('.fast5'):
				basecalled_files.add(name)

	# don't copy already staged files
	for root, dirs, files in os.walk(args.staging, topdown=False):
		for name in files:
			if name.endswith('.fast5'):
				basecalled_files.add(name)

	for root, dirs, files in os.walk(args.prebasecalled, topdown=False):
		for name in files:
			if name not in basecalled_files and name.endswith('.fast5'):
				flowcell = ''
				samplename = ''
				f = re.search('_2\d{7}_(F.*?)_', name)
				if f:
					flowcell = f.group(1)
				f = re.search('_(sequencing_run|mux_scan)_(.*)_\d+_read', name)
				if f:
					samplename = f.group(2)

				if args.organiseby == 'flowcell' and flowcell:
					directory_name = flowcell
				elif args.organiseby == 'sample' and name:
					directory_name = samplename
				elif args.organiseby == 'nothing':
					directory_name = ''
				else:
					if flowcell and name:
						directory_name = "%s/%s" % (flowcell, samplename)
					elif name:
						directory_name = samplename
					else:
						print >>sys.stderr, "Skipping %s" % (name,)
						continue

				albacore_root = root[len(args.prebasecalled):]
				# move it
				checkdir = args.staging + '/' + directory_name + '/' + albacore_root
				if not os.path.exists(checkdir):
					os.makedirs(checkdir)
				movefrom = args.prebasecalled + '/' + albacore_root + '/' + name
				moveto = args.staging + '/' + directory_name + '/' + albacore_root + '/' + name
				print("Copy %s to %s" % (movefrom, moveto))

				abspath = os.path.abspath(movefrom)
				os.symlink(abspath, moveto)

parser = argparse.ArgumentParser(description='Stage files for processing.')
parser.add_argument('prebasecalled', 
	    help='directory containing non-basecalled reads')
parser.add_argument('basecalled',
	    help='directory containing basecalled reads')
parser.add_argument('staging',
	    help='staging directory')
parser.add_argument('--organiseby', choices=('wotevs', 'flowcell', 'sample', 'nothing'), default='wotevs',
	    help='organise reads by specific part of read id')

args = parser.parse_args()
run(args)

