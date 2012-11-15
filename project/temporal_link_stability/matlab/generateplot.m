data = load(inputfile123{i})
datasize = size(data)
isemptyfile = datasize(1) == 0
if isemptyfile
    data = [0 0]
end
x = data(:,1)
y = data(:,2)
ylinearfit = polyval(polyfit(x,y,1),x)
yquadfit = polyval(polyfit(x,y,2),x)
plot(x,y,'k-s',x,ylinearfit,x,yquadfit)
if isemptyfile
    xlabel('No data')
    ylabel('No data')
else
    xlabel('Year')
    ylabel('Export Quantity')
end
saveas(gcf,outputfile123{i},'png')