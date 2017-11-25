#Written by Nick Loman @pathogenomenick

from __future__ import print_function


import os
import os.path
import sys
import shutil
import re
import argparse
import time

try:
    from os import scandir
except ImportError:
    from scandir import scandir

# Modified version of scandir.walk that doesn't stat() symlinks to check if they are directories

def walk(top, topdown=True, onerror=None, followlinks=False):
    """Like Python 3.5's implementation of os.walk() -- faster than
    the pre-Python 3.5 version as it uses scandir() internally.
    """
    dirs = []
    nondirs = []

    # We may not have read permission for top, in which case we can't
    # get a list of the files the directory contains.  os.walk
    # always suppressed the exception then, rather than blow up for a
    # minor reason when (say) a thousand readable directories are still
    # left to visit.  That logic is copied here.
    try:
        scandir_it = scandir(top)
    except OSError as error:
        if onerror is not None:
            onerror(error)
        return

    while True:
        try:
            try:
                entry = next(scandir_it)
            except StopIteration:
                break
        except OSError as error:
            if onerror is not None:
                onerror(error)
            return

        try:
            is_dir = entry.is_dir(follow_symlinks=False)
        except OSError:
            # If is_dir() raises an OSError, consider that the entry is not
            # a directory, same behaviour than os.path.isdir().
            is_dir = False

        if is_dir:
            dirs.append(entry.name)
        else:
            nondirs.append(entry.name)

        if not topdown and is_dir:
            # Bottom-up: recurse into sub-directory, but exclude symlinks to
            # directories if followlinks is False
            if followlinks:
                walk_into = True
            else:
                try:
                    is_symlink = entry.is_symlink()
                except OSError:
                    # If is_symlink() raises an OSError, consider that the
                    # entry is not a symbolic link, same behaviour than
                    # os.path.islink().
                    is_symlink = False
                walk_into = not is_symlink

            if walk_into:
                for entry in walk(entry.path, topdown, onerror, followlinks):
                    yield entry

    # Yield before recursion if going top down
    if topdown:
        yield top, dirs, nondirs

        # Recurse into sub-directories
        for name in dirs:
            new_path = join(top, name)
            # Issue #23605: os.path.islink() is used instead of caching
            # entry.is_symlink() result during the loop on os.scandir() because
            # the caller can replace the directory entry during the "yield"
            # above.
            if followlinks or not islink(new_path):
                for entry in walk(new_path, topdown, onerror, followlinks):
                    yield entry
    else:
        # Yield after recursion if going bottom up
        yield top, dirs, nondirs

def run(args):
	basecalled_files = set()

	print ("Walk basecalls\n")
	for root, dirs, files in walk(args.basecalled, topdown=False):
		for name in files:
			if name.endswith('.fast5'):
				basecalled_files.add(name)

	print ("Walk staging\n")
	# don't copy already staged files
	for root, dirs, files in walk(args.staging, topdown=False):
		for name in files:
			if name.endswith('.fast5'):
				basecalled_files.add(name)

	already_processed = set()
	print (len(already_processed))

	print ("Walk prebasecalled\n")

	for root, dirs, files in walk(args.prebasecalled, topdown=False):
		for filename in files:
			if filename.endswith('.tmp'):
				name = filename[0:len(filename)-4]
			else:
				name = filename
			
			if name not in basecalled_files and \
                           name.endswith('.fast5') and \
                           name not in already_processed:
				print ("Processing %s" % (name))

				#delta = time.time() - os.stat(root+'/'+filename).st_mtime
				#if delta < (30*60):
				#	print ("Skipping as too new: %s" % (delta,))
				#	continue

				flowcell = ''
				samplename = ''

				f = re.search('_2\d{7}_(F.*?)_', name)
				if f:
					flowcell = f.group(1)
				f = re.search('_(sequencing_run|mux_scan)_(.*_\d+)_read', name)
				if f:
					samplename = f.group(2)
				else:
					f = re.search('_(sequencing_run|mux_scan)_(.*)_ch(\d+)_read(\d+)', name)
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
				movefrom = args.prebasecalled + '/' + albacore_root + '/' + filename
				moveto = args.staging + '/' + directory_name + '/' + albacore_root + '/' + name

				print("Copy %s to %s" % (movefrom, moveto))

				abspath = os.path.abspath(movefrom)
				os.symlink(abspath, moveto)

				already_processed.add(name)

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

