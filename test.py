#!/usr/bin/env python
import cluster
import sys
import csv
import math
import timer
import random
from optparse import OptionParser
parser = OptionParser()

parser.add_option("-f", "--file", dest="file", default="./input/c4_s300_f2.csv",
                 help="Input file name")
parser.add_option("-i", "--iterations", dest="iter", default=20,
                 help="Iterations to use in searching for min error. Default 20.")
(options, args) = parser.parse_args()

filename = options.file
iters = int(options.iter)

maxClusters = 10

# Read data
res = []
for row in csv.reader(open(filename,"rb")):
	res.append([float(x) for x in row])
nFeatures = len(res[0])
minx, maxx = [sys.maxint for i in range(0,nFeatures)], [-sys.maxint for i in range(0,nFeatures)]
for r in res:
	idx = 0
	for i in minx:
		if r[idx] < i:
			minx[idx] = r[idx]
		idx += 1
	idx = 0
	for i in maxx:
	        if r[idx] > i:
	                maxx[idx] = r[idx]
	        idx += 1
dataSpread = max([abs(x - y) for x, y in zip(maxx, minx)])

# write results
def writeFile( postfix, k):
	fn = filename.split('/')[-1]
	fn += "_" + str(postfix)
	wrtr = csv.writer(open("./output/"+fn+"_result.csv","wb"))
	for x in k.getOutput():
		wrtr.writerow(x)
	eWrtr = csv.writer(open("./output/"+fn+"_error.csv","wb"))
	for x in k.getErrors():
		eWrtr.writerow(x)

# make sure data is in random order
random.shuffle(res)
# 20 percent set aside for cross-validation
xval = int(0.20*len(res))

for c in range(1,maxClusters+1):
	minError = sys.maxint
	with timer.Timer():
		for i in range(0,iters):
			k1 = cluster.kmeans(res, c, xval)
			err, xerr = k1.run()
			if xerr < minError:
				minError = xerr
				writeFile("k-%d-%f1.4"%(c,err), k1)
			print 'k-means,',i,',',c,',',minError,',Inter'
			sys.stderr.write("kmeans clusters: %d iter: %d \n"%(c,i))
		print 'k-means,',c,',',minError,',',

minl = math.log(0.9)
maxl = math.log(math.sqrt(2.0) * dataSpread)
dl = (maxl-minl)/float(maxClusters)
for l in [math.exp(minl + i*dl) for i in range(0, 2*maxClusters)]:
	minError = sys.maxint
	with timer.Timer():
		for i in range(0,iters):
			k1 = cluster.dpmeans(res, l, xval)
			err, xerr = k1.run()
			if xerr < minError:
				minError = xerr
				writeFile("k-%d-%f1.4"%(c,err), k1)
			print 'dp-means,',i,',',l,',',minError,',Inter'
			sys.stderr.write("dpmeans lambda: %2.5f iter: %d \n"%(c,i))
		print 'dp-means,',l,',',minError,',',
