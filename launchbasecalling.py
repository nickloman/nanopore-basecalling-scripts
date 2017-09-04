#!/bin/bash

import sys
from dask import compute, delayed
import dask.multiprocessing
import os
import os.path
import datetime
import shutil

staging_dir = sys.argv[1]
gridion_basecalls = sys.argv[2]

class MyTask:
	def __init__(self, staging, basecalls, dirname):
		self.staging = staging
		self.basecalls = basecalls
		self.dirname = dirname

def process(t):
	datstr = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

	outdir = "%s/%s" % (t.basecalls, t.dirname)
	for fn in ['configuration.cfg', 'pipeline.log', 'sequencing_summary.txt']:
		if os.path.exists(outdir+'/'+fn):
			if not os.path.exists(outdir+'/reports'):
				os.makedirs(outdir+'/reports')
			shutil.move(outdir+'/'+fn, outdir+'/reports/'+fn+'-'+datstr)

	cmd = ("read_fast5_basecaller.py -c r95_450bps_linear.cfg -i %s/%s -s %s/%s -t 12 -r -o fast5,fastq" % (t.staging, t.dirname, t.basecalls, t.dirname))
	os.system(cmd)

dirs = os.listdir(staging_dir)
#for d in dirs:
#	process(MyTask(staging_dir, gridion_basecalls, d))

values = [delayed(process)(MyTask(staging_dir, gridion_basecalls,x)) for x in dirs]
results = compute(*values, get=dask.multiprocessing.get)


