clear
total = 23705
inputfile123=textread('input-files-percent.txt','%s',total)
outputfile123=textread('output-files-percent.txt','%s',total)

fName = 'r2-and-slopes-percent.txt';         %# A file name
fid = fopen(fName,'w');            %# Open the file


for i=1:total,
    data = load(inputfile123{i})
    datasize = size(data)
    isemptyfile = datasize(1) == 0
    if isemptyfile
        data = [0 0]
    end
    x = data(:,1)
    y = data(:,2)
    a=0
    b=0
    c=0
    [p,s] = polyfit(x,y,1)
    r2=1 - s.normr^2 / norm(y-mean(y))^2
    fprintf(fid,'%s %g %f\r\n',outputfile123{i},r2,p(1));
    i
end
fclose(fid);                     %# Close the file
