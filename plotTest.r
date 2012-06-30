#!/usr/bin/env Rscript

library(ggplot2)
library(gridExtra)

X <- read.delim("./output/test.csv", sep=",", header=FALSE)
X$method <- as.factor(X$V1)
summary(X)

p <-ggplot(data=X, aes(V2,V3)) + 
	geom_point(aes(color = method)) +
	geom_line(aes(color= method)) +
	scale_y_log10() + 
	xlab("Parameter") +
	ylab("Error") 
ggsave(file="./img/test_errors.png", width=5, height=4, dpi=100)


p1 <-ggplot(data=X, aes(V2, V4)) + 
	geom_point(aes(color = method)) +
	geom_line(aes(color = method)) +  
	xlab("Parameter") +
	ylab("Time") 
ggsave(file="./img/test_times.png", width=5, height=4, dpi=100)
