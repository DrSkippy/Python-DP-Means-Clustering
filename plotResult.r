#!/usr/bin/env Rscript

library(ggplot2)
library(gridExtra)


X <- read.delim("./result.csv", sep=",", header=FALSE)
X$cluster <- as.factor(X$V3)
summary(X)

p <-ggplot(aes(V1,V2), data=X) + 
	geom_point(aes(shape = cluster, color = cluster)) + 
	facet_wrap( ~ V4) +
ggsave(file="./img/iters.png", width=6, height=8, dpi=100)


Y <- read.delim("./error.csv", sep=",", header=FALSE)
summary(Y)
p1 <-ggplot(aes(V1, V2), data=Y) +
	geom_point(color = "blue") +
	geom_line(color = "blue") +
	xlab("Iteration") +
	ylab("Norm Error")
ggsave(file="./img/error.png", width=4, height=4, dpi=100)
