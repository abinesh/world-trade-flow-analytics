import csv
import os
from project import countries
from project.config import YEAR_COLUMNS, WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL
from project.countries import is_valid_country
from project.traids_vs_degree_plot.export_data.exportdata import ExportData
from project.util import column_to_year, file_safe

rootdir = 'matlab/'

def gen_intermediate_data_for_one_way_linear_regression_plot(data,input_file, f1, f2, f3):
    i = 0
    reader = csv.DictReader(open(input_file, 'rb'), skipinitialspace=True)
    out1 = open(f1, 'w')
    out2 = open(f2, 'w')
    out3 = open(f3, 'w')
    for row in reader:
        importer = row.get('Importer')
        exporter = row.get('Exporter')
        if importer == exporter or exporter == 'World':
            continue
        if not is_valid_country(importer) or not is_valid_country(exporter):
            continue
        subdir = 'in/wtf/' + file_safe(exporter) + '/'
        filepath = subdir + 'exports-to-' + file_safe(importer) + '.txt'

        if not os.path.exists(rootdir + subdir):
            os.makedirs(rootdir + subdir)
        with open(rootdir + filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter='\t')
            for column in YEAR_COLUMNS:
                export_quantity = row.get(column)
                if export_quantity == 'NaN':
                    continue
                year = column_to_year(column)
                print exporter + ' ' + importer + ' ' + str(year) + ' ' + export_quantity + ' ' + str(data.total_exports(
                    exporter, year))
                writer.writerow([year, float(export_quantity) / data.total_exports(exporter, year) * 100])

        out1.write(filepath + "\n")
        out2.write(
            "out/wtf/" + file_safe(exporter) + "/" + file_safe(exporter) + "-export-to-" + file_safe(importer) + "\n")
        print i
        i += 1

    for c in countries.countries:
        out3.write("mkdir('out/wtf/" + file_safe(c) + "')\n")

    out3.write("clear\n")
    out3.write("total = " + str(i) + "\n")
    out3.write("inputfile123=textread('input-files-percent.txt','%s',total)\n")
    out3.write("outputfile123=textread('output-files-percent.txt','%s',total)\n")
    out3.write("\n")
    out3.write("for i=1:total,\n")
    out3.write("    data = load(inputfile123{i})\n")
    out3.write("    datasize = size(data)\n")
    out3.write("    isemptyfile = datasize(1) == 0\n")
    out3.write("    if isemptyfile\n")
    out3.write("        data = [0 0]\n")
    out3.write("    end\n")
    out3.write("    x = data(:,1)\n")
    out3.write("    y = data(:,2)\n")
    out3.write("    ylinearfit = polyval(polyfit(x,y,1),x)\n")
    out3.write("    yquadfit = polyval(polyfit(x,y,2),x)\n")
    out3.write("    plot(x,y,'k-s',x,ylinearfit,x,yquadfit)\n")
    out3.write("    if isemptyfile\n")
    out3.write("        xlabel('No data')\n")
    out3.write("        ylabel('No data')\n")
    out3.write("    else\n")
    out3.write("        xlabel('Year')\n")
    out3.write("        ylabel('Export Quantity')\n")
    out3.write("    end\n")
    out3.write("    saveas(gcf,outputfile123{i},'png')\n")
    out3.write("    i\n")
    out3.write("end\n")


def gen_intermediate_data_for_both_way_linear_regression_plot(data,f1, f2, f3):
    out1 = open(f1, 'w')
    out2 = open(f2, 'w')
    i = 0
    for exporter in countries.countries:
        subdir = 'in/wtf/' + file_safe(exporter) + '/'
        for importer in countries.countries:
            if importer == exporter:
                continue
            filepath = subdir + 'exports-to-' + file_safe(importer) + '.txt'
            if not os.path.exists(rootdir + subdir):
                os.makedirs(rootdir + subdir)
            file_non_empty = False
            with open(rootdir + filepath, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                for y in YEAR_COLUMNS:
                    year = column_to_year(y)
                    a1 = float(data.export_data(year, exporter, importer))
                    a2 = data.total_exports(exporter, year)
                    a3 = float(data.export_data(year, importer, exporter))
                    a4 = data.total_exports(importer, year)
                    print "In %d, %s to %s: %f/%f, %s to %s : %f/%f" % (
                        year, exporter, importer, a1, a2, importer, exporter, a3, a4)
                    if a1 == 0.0 and a3 == 0.0:
                        continue
                    file_non_empty = True
                    export_percentage = 0 if a2 == 0 else a1 / a2 * 100
                    import_percentage = 0 if a4 == 0 else a3 / a4 * 100
                    writer.writerow([year, export_percentage, import_percentage])
            if file_non_empty:
                out1.write(filepath + "\n")
                out2.write(
                    "out/wtf/" + file_safe(exporter) + "/" + file_safe(exporter) + "-export-to-" + file_safe(
                        importer) + "\n")
                print i
                i += 1
            else:
                os.remove(rootdir + '/' + filepath)
                pass

    pass


data = ExportData()
data.load_export_data(WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, should_include_world=True)

#gen_intermediate_data_for_one_way_linear_regression_plot(data,WORLD_TRADE_FLOW_DATA_FILE_ORIGINAL, 'matlab/input-files-percent.txt',
#    'matlab/output-files-percent.txt', 'matlab/generateplotsloop.m')
gen_intermediate_data_for_both_way_linear_regression_plot(data,'matlab/input-files-both-ways-percent.txt',
    'matlab/output-files-both-ways-percent.txt', 'matlab/generateplotsloop.m')

'''
mkdir('out/wtf/USA')
mkdir('out/wtf/Afghanistan')
mkdir('out/wtf/Afr_Other_NS')
mkdir('out/wtf/Africa_N_NES')
mkdir('out/wtf/Albania')
mkdir('out/wtf/Algeria')
mkdir('out/wtf/Angola')
mkdir('out/wtf/Areas_NES')
mkdir('out/wtf/Argentina')
mkdir('out/wtf/Armenia')
mkdir('out/wtf/Asia_NES')
mkdir('out/wtf/Asia_West_NS')
mkdir('out/wtf/Australia')
mkdir('out/wtf/Austria')
mkdir('out/wtf/Azerbaijan')
mkdir('out/wtf/Bahamas')
mkdir('out/wtf/Bahrain')
mkdir('out/wtf/Bangladesh')
mkdir('out/wtf/Barbados')
mkdir('out/wtf/Belarus')
mkdir('out/wtf/Belgium-Lux')
mkdir('out/wtf/Belize')
mkdir('out/wtf/Benin')
mkdir('out/wtf/Bermuda')
mkdir('out/wtf/Bolivia')
mkdir('out/wtf/Bosnia_Herzg')
mkdir('out/wtf/Br_Antr_Terr')
mkdir('out/wtf/Brazil')
mkdir('out/wtf/Bulgaria')
mkdir('out/wtf/Burkina_Faso')
mkdir('out/wtf/Burundi')
mkdir('out/wtf/CACM_NES')
mkdir('out/wtf/Cambodia')
mkdir('out/wtf/Cameroon')
mkdir('out/wtf/Canada')
mkdir('out/wtf/Carib__NES')
mkdir('out/wtf/Cent_Afr_Rep')
mkdir('out/wtf/Chad')
mkdir('out/wtf/Chile')
mkdir('out/wtf/China')
mkdir('out/wtf/China_HK_SAR')
mkdir('out/wtf/China_MC_SAR')
mkdir('out/wtf/China_SC')
mkdir('out/wtf/Colombia')
mkdir('out/wtf/Congo')
mkdir('out/wtf/Costa_Rica')
mkdir('out/wtf/Cote_Divoire')
mkdir('out/wtf/Croatia')
mkdir('out/wtf/Cuba')
mkdir('out/wtf/Cyprus')
mkdir('out/wtf/Czech_Rep')
mkdir('out/wtf/Czechoslovak')
mkdir('out/wtf/Dem_Rp_Congo')
mkdir('out/wtf/Denmark')
mkdir('out/wtf/Djibouti')
mkdir('out/wtf/Dominican_Rp')
mkdir('out/wtf/E_Europe_NES')
mkdir('out/wtf/EEC_NES')
mkdir('out/wtf/Ecuador')
mkdir('out/wtf/Egypt')
mkdir('out/wtf/El_Salvador')
mkdir('out/wtf/Eq_Guinea')
mkdir('out/wtf/Estonia')
mkdir('out/wtf/Ethiopia')
mkdir('out/wtf/Eur__EFTA_NS')
mkdir('out/wtf/Eur_Other_NE')
mkdir('out/wtf/Falkland_Is')
mkdir('out/wtf/Fiji')
mkdir('out/wtf/Finland')
mkdir('out/wtf/Fm_German_DR')
mkdir('out/wtf/Fm_German_FR')
mkdir('out/wtf/Fm_USSR')
mkdir('out/wtf/Fm_Yemen_AR')
mkdir('out/wtf/Fm_Yemen_Ar')
mkdir('out/wtf/Fm_Yemen_Dm')
mkdir('out/wtf/Fm_Yugoslav')
mkdir('out/wtf/Fr_Ind_O')
mkdir('out/wtf/Fr_Guiana')
mkdir('out/wtf/France_Monac')
mkdir('out/wtf/Gabon')
mkdir('out/wtf/Gambia')
mkdir('out/wtf/Georgia')
mkdir('out/wtf/Germany')
mkdir('out/wtf/Ghana')
mkdir('out/wtf/Gibraltar')
mkdir('out/wtf/Greece')
mkdir('out/wtf/Greenland')
mkdir('out/wtf/Guadeloupe')
mkdir('out/wtf/Guatemala')
mkdir('out/wtf/Guinea')
mkdir('out/wtf/GuineaBissau')
mkdir('out/wtf/Guyana')
mkdir('out/wtf/Haiti')
mkdir('out/wtf/Honduras')
mkdir('out/wtf/Hungary')
mkdir('out/wtf/Iceland')
mkdir('out/wtf/India')
mkdir('out/wtf/Indonesia')
mkdir('out/wtf/Int_Org')
mkdir('out/wtf/Iran')
mkdir('out/wtf/Iraq')
mkdir('out/wtf/Ireland')
mkdir('out/wtf/Israel')
mkdir('out/wtf/Italy')
mkdir('out/wtf/Jamaica')
mkdir('out/wtf/Japan')
mkdir('out/wtf/Jordan')
mkdir('out/wtf/Kazakhstan')
mkdir('out/wtf/Kenya')
mkdir('out/wtf/Kiribati')
mkdir('out/wtf/Korea_D_P_Rp')
mkdir('out/wtf/Korea_Rep_')
mkdir('out/wtf/Kuwait')
mkdir('out/wtf/Kyrgyzstan')
mkdir('out/wtf/LAIA_NES')
mkdir('out/wtf/Lao_P_Dem_R')
mkdir('out/wtf/Latvia')
mkdir('out/wtf/Lebanon')
mkdir('out/wtf/Liberia')
mkdir('out/wtf/Libya')
mkdir('out/wtf/Lithuania')
mkdir('out/wtf/Madagascar')
mkdir('out/wtf/Malawi')
mkdir('out/wtf/Malaysia')
mkdir('out/wtf/Mali')
mkdir('out/wtf/Malta')
mkdir('out/wtf/Mauritania')
mkdir('out/wtf/Mauritius')
mkdir('out/wtf/Mexico')
mkdir('out/wtf/Mongolia')
mkdir('out/wtf/Morocco')
mkdir('out/wtf/Mozambique')
mkdir('out/wtf/Myanmar')
mkdir('out/wtf/Nepal')
mkdir('out/wtf/Neth_Ant_Aru')
mkdir('out/wtf/Netherlands')
mkdir('out/wtf/Neutral_Zone')
mkdir('out/wtf/New_Calednia')
mkdir('out/wtf/New_Zealand')
mkdir('out/wtf/Nicaragua')
mkdir('out/wtf/Niger')
mkdir('out/wtf/Nigeria')
mkdir('out/wtf/Norway')
mkdir('out/wtf/Occ_Pal_Terr')
mkdir('out/wtf/Oman')
mkdir('out/wtf/Oth_Oceania')
mkdir('out/wtf/Pakistan')
mkdir('out/wtf/Panama')
mkdir('out/wtf/Papua_N_Guin')
mkdir('out/wtf/Paraguay')
mkdir('out/wtf/Peru')
mkdir('out/wtf/Philippines')
mkdir('out/wtf/Poland')
mkdir('out/wtf/Portugal')
mkdir('out/wtf/Qatar')
mkdir('out/wtf/Rep_Moldova')
mkdir('out/wtf/Romania')
mkdir('out/wtf/Russian_Fed')
mkdir('out/wtf/Rwanda')
mkdir('out/wtf/Samoa')
mkdir('out/wtf/Saudi_Arabia')
mkdir('out/wtf/Senegal')
mkdir('out/wtf/Seychelles')
mkdir('out/wtf/Sierra_Leone')
mkdir('out/wtf/Singapore')
mkdir('out/wtf/Slovakia')
mkdir('out/wtf/Slovenia')
mkdir('out/wtf/Somalia')
mkdir('out/wtf/South_Africa')
mkdir('out/wtf/Spain')
mkdir('out/wtf/Sri_Lanka')
mkdir('out/wtf/St_Helena')
mkdir('out/wtf/St_Kt-Nev-An')
mkdir('out/wtf/St_Pierre_Mq')
mkdir('out/wtf/Sudan')
mkdir('out/wtf/Suriname')
mkdir('out/wtf/Sweden')
mkdir('out/wtf/Switz_Liecht')
mkdir('out/wtf/Syria')
mkdir('out/wtf/TFYR_Macedna')
mkdir('out/wtf/Taiwan')
mkdir('out/wtf/Tajikistan')
mkdir('out/wtf/Tanzania')
mkdir('out/wtf/Thailand')
mkdir('out/wtf/Togo')
mkdir('out/wtf/Trinidad_Tbg')
mkdir('out/wtf/Tunisia')
mkdir('out/wtf/Turkey')
mkdir('out/wtf/Turkmenistan')
mkdir('out/wtf/UK')
mkdir('out/wtf/US_NES')
mkdir('out/wtf/Uganda')
mkdir('out/wtf/Ukraine')
mkdir('out/wtf/Untd_Arab_Em')
mkdir('out/wtf/Uruguay')
mkdir('out/wtf/Uzbekistan')
mkdir('out/wtf/Venezuela')
mkdir('out/wtf/Viet_Nam')
mkdir('out/wtf/Yemen')
mkdir('out/wtf/Yugoslavia')
mkdir('out/wtf/Zambia')
mkdir('out/wtf/Zimbabwe')
mkdir('out/wtf/World')
mkdir('out/wtf/China_FTZ')
clear
total = 26245
inputfile123=textread('input-files-both-ways-percent-no-yemen.txt','%s',total)
outputfile123=textread('output-files-both-ways-percent-no-yemen.txt','%s',total)

for i=1:total,
    data = load(inputfile123{i})
    datasize = size(data)
    isemptyfile = datasize(1) == 0
    if isemptyfile
        data = [0 0]
    end
    x = data(:,1)
    export = data(:,2)
    exportLinearFit = polyval(polyfit(x,export,1),x)
    exportMovingAvg = moving(export,5)

    exportOtherWay = data(:,3)
    exportOtherWayLinearFit = polyval(polyfit(x,exportOtherWay,1),x)
    exportOtherWayMovingAvg = moving(exportOtherWay,5)

    plot(x,export,'-or',x,exportLinearFit,'-.r',x,exportMovingAvg,'-.r',x,exportOtherWay,'-ob',x,exportOtherWayLinearFit,'-.b',x,exportOtherWayMovingAvg,'-.b')
    if isemptyfile
        xlabel('No data')
        ylabel('No data')
    else
        xlabel('Year, Legend: Export direction: Red:A->B, Blue:B->A')
        ylabel('Export Quantity')
    end
    saveas(gcf,outputfile123{i},'png')
    i
end
'''