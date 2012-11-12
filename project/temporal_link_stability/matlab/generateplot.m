clear
data = load('in/wtf/USA/exports-to-Afghanistan.dat')
x = data(:,1)
y = data(:,2)
yfit = polyval(polyfit(x,y,1),x)
plot(x,y,'o',x,yfit)
xlabel('Year')
ylabel('Export Quantity')
saveas(gcf,'out/wtf/USA-Afghanistan','jpg')