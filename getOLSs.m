#test
file = csvread("archived/output-buys-2.csv");

file = file(2:end,2:end);

percentOver = file(:,1)./file(:,3);

epg = ols(percentOver, [ones(size(percentOver,1),1) file(:,21:36)]);

out = ols(file(:,37:53).*((file(:,5)./file(:,4)).**4), [ones(size(file,1),1) file(:,2) file(:,6:19) percentOver])';


# out = ols(file(:,37:53), [ones(size(file,1),1) file(:,2) file(:,6:19) percentOver])';

save estimateOver.csv epg;

save extimateBuy.txt out;
