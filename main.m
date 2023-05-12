clear all; close all; clc
x2=load("data.csv");
x1=load("data.txt");
x=w1;

figure(1);
plot(x(:,1),x(:,2),'.')
hold on;
plot(x(:,1),x(:,2),'ro')
hold off;

