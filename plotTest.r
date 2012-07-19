#!/usr/bin/env Rscript

library(ggplot2)
library(gridExtra)
library(reshape2)

X <- read.delim("./output/test.csv", sep=",", header=FALSE)
colnames(X) <- c("mthd","parameter","error","time")
X$method <- as.factor(X$mthd)

summary(X)

p <-ggplot(data=X, aes(parameter, error)) + 
	geom_point(aes(color=method)) +
	geom_line(aes(color=method)) +
	scale_y_log10() + 
	xlab("Parameter") +
	ylab("Normalized Error") 
ggsave(file="./img/test_errors.png", width=5, height=4, dpi=100)

p1 <-ggplot(data=X, aes(parameter, time)) + 
	geom_point(aes(color = method)) +
	geom_line(aes(color = method)) +  
	xlab("Parameter") +
	ylab("Time") 
ggsave(file="./img/test_times.png", width=5, height=4, dpi=100)

p2 <-ggplot(data=X, aes(error, time)) + 
	geom_point(aes(color = method)) +
	#geom_line(aes(color = method)) +  
	geom_smooth(aes(color=method), method = "lm") + 
	scale_y_log10() + 
	scale_x_log10() + 
	xlab("Error") +
	ylab("Time") 
ggsave(file="./img/test_times-error.png", width=5, height=4, dpi=100)

