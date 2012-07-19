#!/usr/bin/env python
import cluster
import sys
import csv
import math
import random
import scipy.optimize

# function to minimize
def g(l, returnObject=False):
        minError = sys.maxint
        for i in range(0,iters):
                k1 = cluster.dpmeans(res, l, xVal)
                err, xerr = k1.run()
                if xerr < minError:
                        minError = xerr
			kmin = k1
	if returnObject:
		return minError, k1
        return minError

#parameters
iters = 8        # iterations in search for min
maxClusters = 12 # used for setting minimum lambda
xValFrac = 0.2   # 20% of data for xVal

# Read data from standard in
res = []
for row in csv.reader(sys.stdin):
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
# quick and dirty min scale is average dist if data was along dataspread
dataGrain = dataSpread/maxClusters
# make sure data is in random order
random.shuffle(res)
# set aside for cross-validation
xVal = int(xValFrac*len(res))

optLambda = scipy.optimize.brent(g, 
			brack=(1./dataSpread, 1./dataGrain),
			tol=1e-4, 
			full_output=0,
			maxiter=100)

e,k = g(optLambda, returnObject=True)
wrtr = csv.writer(open("./output/opt_result.csv","wb"))
for x in k.getOutput():
	wrtr.writerow(x)
eWrtr = csv.writer(open("./output/opt_error.csv","wb"))
for x in k.getErrors():
	eWrtr.writerow(x)
print "lambda: %2.5f\n  with error: %2.5f\n"%(optLambda,e)

