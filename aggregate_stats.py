import pandas as pd
import sys
import glob

first_record = True
master_df = None

for sample in sys.argv[1:]:
	reports = glob.glob("%s/reports/seque*" % (sample,))
	reports.append("%s/sequencing_summary.txt" % (sample,))
	print reports

	for report in reports:
		try:
			df = pd.read_csv(report, sep="\t")
		except ValueError:
			continue

		df['sample'] = sample

		if first_record:
			master_df = df
			first_record = False
		else:
			master_df = master_df.append(df)	

master_df.to_csv('aggregate_stats.txt', sep="\t")

