
World trade flow analytics

Link Stability

A. To generate set of linear and quadratic fits(one way only) ordered alphabetically:
    1. Run gen_intermediate_data_for_one_way_linear_regression_plot in regression_of_trade_data.py to generate intermediate files:
        - matlab/input-files-percent.txt
        - matlab/output-files-percent.txt
        - matlab/generateplotsloop.m : For each pair of files in input.txt and output.txt, generate linear and quadratic fit. Files are written as specified in output.txt
    2. Run matlab/generateplotsloop.m

B. To generate set of linear and quadratic fits(one way only) ordered by RSquared:
    1. Do A
    2. Update count in compute-stddev.m and run it. It will generate the following:
        - r2-and-slopes-percent.txt : (output_file_path,Rsquared, linear regression slope)
    3. Copy r2-and-slopes-percent.txt into dataset
    4. Remove out/wtf/
       cat r2-and-slopes-percent.txt | sed -f remove-out-wtf.txt | sed -f replace-slash-with-space.txt > r2-and-slopes-percent-sane.txt

    5. Split r2-and-slopes.txt into individual files for each country with graphs sorted
       cat r2-and-slopes-percent-sane.txt| cut -d" " -f 1 | sort | uniq | awk '{print "cat r2-and-slopes-percent-sane.txt | grep \""$1" "$1"\" | sort -k 3 > r2-list/"$1"-r2-list.txt"}'   | sh

    6. The following step is to reorder graph based on fit determined by R squared(Use matlab or shell script to create directory for each country)
       copy in order all the graphs so that high variance ones are in front of the list
       cat r2-list/USA-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh


       cat r2-list/USA-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Afghanistan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Afr_Other_NS-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Africa_N_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Albania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Algeria-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Angola-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Areas_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Argentina-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Armenia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Asia_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Asia_West_NS-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Australia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Austria-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Azerbaijan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bahamas-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bahrain-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bangladesh-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Barbados-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Belarus-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Belgium-Lux-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Belize-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Benin-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bermuda-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bolivia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bosnia_Herzg-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Br_Antr_Terr-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Brazil-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Bulgaria-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Burkina_Faso-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Burundi-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/CACM_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cambodia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cameroon-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Canada-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Carib__NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cent_Afr_Rep-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Chad-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Chile-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/China-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/China_HK_SAR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/China_MC_SAR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/China_SC-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Colombia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Congo-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Costa_Rica-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cote_Divoire-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Croatia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cuba-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Cyprus-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Czech_Rep-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Czechoslovak-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Dem_Rp_Congo-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Denmark-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Djibouti-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Dominican_Rp-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/E_Europe_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/EEC_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Ecuador-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Egypt-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/El_Salvador-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Eq_Guinea-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Estonia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Ethiopia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Eur__EFTA_NS-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Eur_Other_NE-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Falkland_Is-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fiji-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Finland-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_German_DR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_German_FR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_USSR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_Yemen_AR-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_Yemen_Ar-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_Yemen_Dm-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fm_Yugoslav-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fr_Ind_O-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Fr_Guiana-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/France_Monac-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Gabon-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Gambia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Georgia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Germany-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Ghana-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Gibraltar-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Greece-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Greenland-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Guadeloupe-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Guatemala-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Guinea-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/GuineaBissau-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Guyana-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Haiti-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Honduras-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Hungary-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Iceland-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/India-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Indonesia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Int_Org-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Iran-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Iraq-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Ireland-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Israel-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Italy-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Jamaica-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Japan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Jordan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Kazakhstan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Kenya-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Kiribati-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Korea_D_P_Rp-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Korea_Rep_-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Kuwait-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Kyrgyzstan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/LAIA_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Lao_P_Dem_R-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Latvia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Lebanon-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Liberia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Libya-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Lithuania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Madagascar-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Malawi-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Malaysia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mali-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Malta-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mauritania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mauritius-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mexico-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mongolia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Morocco-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Mozambique-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Myanmar-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Nepal-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Neth_Ant_Aru-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Netherlands-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Neutral_Zone-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/New_Calednia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/New_Zealand-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Nicaragua-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Niger-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Nigeria-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Norway-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Occ_Pal_Terr-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Oman-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Oth_Oceania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Pakistan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Panama-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Papua_N_Guin-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Paraguay-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Peru-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Philippines-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Poland-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Portugal-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Qatar-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Rep_Moldova-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Romania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Russian_Fed-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Rwanda-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Samoa-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Saudi_Arabia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Senegal-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Seychelles-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Sierra_Leone-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Singapore-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Slovakia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Slovenia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Somalia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/South_Africa-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Spain-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Sri_Lanka-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/St_Helena-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/St_Kt-Nev-An-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/St_Pierre_Mq-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Sudan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Suriname-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Sweden-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Switz_Liecht-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Syria-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/TFYR_Macedna-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Taiwan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Tajikistan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Tanzania-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Thailand-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Togo-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Trinidad_Tbg-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Tunisia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Turkey-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Turkmenistan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/UK-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/US_NES-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Uganda-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Ukraine-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Untd_Arab_Em-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Uruguay-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Uzbekistan-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Venezuela-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Viet_Nam-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Yemen-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Yugoslavia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Zambia-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/Zimbabwe-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/World-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh
       cat r2-list/China_FTZ-r2-list.txt | awk '{print "cp ../project/temporal_link_stability/matlab/out/wtf/"$1"/"$2".png wtf-ordered/"$1"/"NR"-"$2".png"}' | sh

C. To generate export in 2000 vs slope of linear fits graph:
    1. Do A.1, B.2, B.3, B.4
    2. Run export_in_2000_vs_slope_of_linear_fit.py to generate intermediate files:
        - matlab/out/slope-vs-export-percent/COUNTRY.txt : (Linear regression slope,Export in 2000) pairs for each country
        - matlab/out/slope-vs-export-percent/COUNTRY-world.txt :(Linear regression slope,Export in 2000) pair for World
        - matlab/out/slope-vs-export-percent/all-countries.txt : (COUNTRY.txt,COUNTRY-world.txt) pairs for each country
        - matlab/slope_vs_export_gen.m : Matlab code to generate slope vs export in 2000
    3. Run slope_vs_export_gen.m

D. To generate set of linear and quadratic fits(both ways on same graph) ordered alphabetically
    1. Run gen_intermediate_data_for_both_way_linear_regression_plot in regression_of_trade_data.py to generate intermediate files:
        - matlab/input-files-both-ways-percent.txt
        - matlab/output-files-both-ways-percent.txt
    2. Find the line count of input file generated above and update the matlab code specified as a multi line string at the end of regression_of_trade_data.py
    3. Run regression_of_trade_data.py twice. Once till MATRIX_MAX_DIMENSION then for remaining count.


E. To categorize relationship types as specified in google doc.
    1. Do till D.2