clear
data = load('in/wtf/USA/exports-to-Afghanistan.txt')
x = data(:,1)
y = data(:,2)
ylinearfit = polyval(polyfit(x,y,1),x)
yquadfit = polyval(polyfit(x,y,2),x)
plot(x,y,'k-s',x,ylinearfit,x,yquadfit)
xlabel('Year')
ylabel('Export Quantity')
saveas(gcf,'out/wtf/USA-Afghanistanaaa','jpg')
