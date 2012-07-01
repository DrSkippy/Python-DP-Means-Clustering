#!/usr/bin/env python

import random
import csv
import sys

def createTestData(nSample, nFeatures, nClusters):
	scaleMu = 10.
	scaleSig = 0.5 + float(options.overlap) * scaleMu * nFeatures/nClusters
	for i in range(0, nClusters):
		mu = [random.random() * scaleMu - scaleMu/2 for j in range(0,nFeatures)]
		sig = [(0.75 * random.random() + 0.25) * scaleSig for j in range(0,nFeatures)]
		#
		res = [[random.gauss(mu[i], sig[i]) for x in range(0, nSample)] for i in range(0, nFeatures)]
		for i in range(0,nSample):
			yield [res[j][i] for j in range(0, nFeatures)]

if __name__ == '__main__':
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-s", "--sample-size", dest="sample", default=10,
			help="Sample size per cluster")
	parser.add_option("-f", "--features", dest="features", default=2,
			help="Number of features")
	parser.add_option("-c", "--clusters", dest="clusters", default=2,
			help="Sample size")
	parser.add_option("-o", "--overlap", dest="overlap", default=0.0,
			help="0 - distinct, 1 - scale = sig")
	(options, args) = parser.parse_args()
	wtr = csv.writer(sys.stdout)
	for x in createTestData(int(options.sample), int(options.features), int(options.clusters)):
		wtr.writerow(x)
