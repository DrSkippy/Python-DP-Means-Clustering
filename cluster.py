#!/usr/bin/env python
from pprint import pprint
import sys
import random
import math
import timer

class kmeans(object):

	def __init__(self, _X, _k):
		# X is sample size lists of dim length
		self.nFeatures = len(_X[0])
		self.size = len(_X)
		self.X = _X
		self.k = _k
		self.dataClusterId = [-1 for i in range(0, self.size)] # index of group for each data pair
		self.clusters = {}
		idx = 0
		# initialize to k random data points
		for i in random.sample(range(0, self.size), self.k):
			self.clusters[idx] = self.X[i]
			idx += 1
		# output records
		self.record = []
		self.errorRecord = []
		
	def dSquared(self, x, y):
		dist2 = 0.0
		for j,k in zip(x,y):
			dist2 += (j - k)**2
		return dist2

	def error(self):
		res = 0.0
		for i in range(0, self.size):
			res += self.dSquared(self.X[i], self.clusters[self.dataClusterId[i]])
		return res/self.size

	def nearestCluster(self, x):
		cmin = sys.maxint
		cidx = -sys.maxint
		for j in self.clusters:
			dist = math.sqrt(self.dSquared(x, self.clusters[j]))
			if dist < cmin:  # record closest centroid
				cmin = dist
				cidx = j
		return cidx, cmin

	def assign(self):
		for i in range(0, self.size):
			self.dataClusterId[i], dmin = self.nearestCluster(self.X[i])

	def updateClusters(self):
		ctemp = {} # dim sums by cluster
		for j in range(0, self.k):
			ctemp[j] = []
			for k in range(0, self.nFeatures):
				ctemp[j].append(0.0) # init sums
			ctemp[j].append(0) # init counter
		for i in range(0,self.size):
			for j in range(0, self.nFeatures):
				ctemp[self.dataClusterId[i]][j] += self.X[i][j]
			ctemp[self.dataClusterId[i]][self.nFeatures] += 1 # count
		for c in self.clusters:
			if ctemp[c][self.nFeatures] <> 0:
				self.clusters[c] = [ ctemp[c][k]/ctemp[c][self.nFeatures] for k in range(0,self.nFeatures)]
			else:
				# no members in this cluster!
				pass
		return

	def run(self, nmax = 100, eps = 1e-7):
		prev = 0.0
		for iter in range(0,nmax):
			self.assign()
			err = self.error()
			self.errorRecord.append((iter, err))
			self.output(str(iter))
			if abs(err-prev) < eps:
				sys.stderr.write("Tolerance reached at step %d\n"%iter)
				break
			prev = err
			self.updateClusters()
		sys.stderr.write("Iterations completed: %d\n"%iter)
		sys.stderr.write("Final error: %f\n"%err)
		self.output("Final")
		return err

	def output(self, iter):
		for i in range(0,self.size):
			self.record.append([str(y) for y in self.X[i]]        + [str(self.dataClusterId[i])] + ["Iter-%s"%iter])
		for k in self.clusters:
			self.record.append([str(y) for y in self.clusters[k]] + [str(k)]                     + ["Iter-%s"%iter])

	def getOutput(self):
		for x in self.record:
			yield x

	def getErrors(self):
		for x in self.errorRecord:
			yield x
			

class dpmeans(kmeans):
	def __init__(self, _X, _lam = 1):
		# init kmean with 1 cluster
		kmeans.__init__(self, _X, 1)
		self.lam = _lam

	def assign(self):
		for i in range(0, self.size):
			cidx, dmin = self.nearestCluster(self.X[i])
			if dmin > self.lam:
				self.k += 1
				self.clusters[self.k-1] = self.X[i]
				self.dataClusterId[i] = self.k-1
			else:
				self.dataClusterId[i] = cidx

if __name__ == '__main__':
	import csv
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option("-k", "--kmeans-clusters", dest="clusters", default=None,
			help="If present, use kmeans with number of clusters specified")
	parser.add_option("-l", "--lamda", dest="lam", default=None,
			help="If preset, use dpmeans with lambda parameters specified")
	(options, args) = parser.parse_args()

	res = []
	for row in csv.reader(sys.stdin):
		res.append([float(x) for x in row])
	if options.clusters is not None:
		k1 = kmeans(res, int(options.clusters))
	elif options.lam is not None:
		k1 = dpmeans(res, float(options.lam))
	else:
		sys.stderr.write("Use -h for help.\n")
		sys.exit()

	#
	with timer.Timer(verbose=True):
		k1.run()
	#
	wrtr = csv.writer(open("./output/result.csv","wb"))
	for x in k1.getOutput():
		wrtr.writerow(x)
	eWrtr = csv.writer(open("./output/error.csv","wb"))
	for x in k1.getErrors():
		eWrtr.writerow(x)
