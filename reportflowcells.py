#Written by Nick Loman @pathogenomenick

import sys
from collections import defaultdict
import re

stats = defaultdict(int)

for name in sys.stdin:
	flowcell = ''
	samplename = ''
	f = re.search('_2\d{7}_(F.*?)_', name)
	if f:
		flowcell = f.group(1)
	f = re.search('_(sequencing_run|mux_scan)_(.*)_\d+_read', name)
	if f:
		samplename = f.group(2)

	if flowcell:
		directory_name = flowcell
	elif name:
		directory_name = samplename
	stats[directory_name] += 1

for k, v in stats.iteritems():
	print "%s\t%s" % (k, v)

