clear
total = 5
inputfile123=textread('input-files.txt','%s',total)
outputfile123=textread('output-files.txt','%s',total)

fName = 'stddev.txt';         %# A file name
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
    [a,b,c] = polyfit(x,y,1)
    fprintf(fid,'%s %g\r\n',outputfile123{i},c(2));
    i
end
fclose(fid);                     %# Close the file

