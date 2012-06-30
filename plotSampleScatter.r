#!/usr/bin/env Rscript

library(ggplot2)
library(gridExtra)

X <- read.delim("./input/c4_s100_f3.csv", sep=",", header=FALSE)
summary(X)

p1 <-ggplot(data=X, aes(V1,V2)) + 
	geom_point() +
	xlab("feature 1") +
	ylab("feature 2") 

p2 <-ggplot(data=X, aes(V3,V2)) + 
	geom_point() +
	xlab("feature 3") +
	ylab("feature 2")

p3 <-ggplot(data=X, aes(V1,V3)) + 
	geom_point() +
	xlab("feature 1") + 
	ylab("feature 3")

png(filename = "./img/3d-sample-data.png", width=600, height=600, unit="px")
print(
	grid.arrange(p1, p2, p3, ncol = 2)
	 )
dev.off()

#
X <- read.delim("./input/c3_s20_f2.csv", sep=",", header=FALSE)
summary(X)
p <-ggplot(data=X, aes(V1,V2)) + 
	geom_point() +
ggsave(file="./img/2d-sample-data.png", width=5, height=4, dpi=100)
