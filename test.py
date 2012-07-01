#!/usr/bin/env python
import cluster
import sys
import csv
import math
import timer

#filename="input/c3_s20_f2.csv"
filename="input/c4_s100_f3.csv"
iters = 50
maxClusters = 12
dataSpread = 10.0

# Read data
res = []
for row in csv.reader(open(filename,"rb")):
	res.append([float(x) for x in row])
nFeatures = len(res[0])

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

for c in range(1,maxClusters):
	k1 = cluster.kmeans(res, c)
	minError = sys.maxint
	with timer.Timer():
		for i in range(0,iters):
			err = k1.run()
			if err < minError:
				minError = err
				writeFile("k-%d-%f1.4"%(c,err), k1)
		print 'k-means,',c,',',minError,',',
				
for l in [(math.sqrt(nFeatures) * dataSpread)/i for i in range(1, 18)]:
	k1 = cluster.dpmeans(res, l)
	minError = sys.maxint
	with timer.Timer():
		for i in range(0,iters):
			err = k1.run()
			if err < minError:
				minError = err
				writeFile("dp-%f1.1-%f1.4"%(l,err), k1)
		print 'dp-means,',dataSpread/l,',',minError,',',
