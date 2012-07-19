#!/usr/bin/env Rscript

library(ggplot2)
library(gridExtra)
library(reshape2)

X <- read.delim("./output/opt_result.csv", sep=",", header=FALSE)
X$cluster <- as.factor(X$V3)
summary(X)
p <-ggplot(data=X) + 
	geom_point(aes(V1, V2, shape = cluster, color = cluster)) + 
	facet_wrap( ~ V4) +
ggsave(file="./img/opt_iters.png", width=8, height=8, dpi=100)

Y <- read.delim("./output/opt_error.csv", sep=",", header=FALSE)
#summary(Y)
colnames(Y) <- c("Iteration","TrainErr","XValidErr")
YY <- melt(Y, id=("Iteration"))
summary(YY)
p1 <-ggplot(data=YY) +
	geom_point(aes(Iteration,value, color=variable)) +
	geom_line(aes(Iteration, value, color=variable)) +
	scale_y_log10() +
	ylab("Normalized Error") 
ggsave(file="./img/opt_error.png", width=4, height=4, dpi=100)
