from project.countries import index_of_country, falklands_war_countries


print index_of_country("USA")
print "\n".join(["%s,%d" % (C, index_of_country(C) + 1) for C in falklands_war_countries])