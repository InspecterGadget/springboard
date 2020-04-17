import pandas as pd

def write_xls(df, name):
    writer = pd.ExcelWriter(name)
    df.to_excel(writer)
    writer.save()

def implement_manual_edits(orig, replace, full_list):
    for i in range (0,len(orig)-1):
        full_list = [x.replace(orig[i], replace[i]) for x in full_list]
    return full_list

ss_2011 = pd.read_excel('NCAA Schools 11-12.xlsx', header=1)
o_2011 = pd.read_excel('NCAA Odds 11-12.xlsx', header=0)

write_xls(ss_2011, 'Season stats header adjusted.xlsx')
ss_team_set= ss_2011['School'].to_list()
o_team_set= set(o_2011['Team'].to_list())
print(ss_team_set)
ss_team_set = list(map(str,ss_team_set))
team_ids = [i for i in range (1, len(ss_team_set)+1)]
#ss_team_set = list(zip(team_ids, ss_team_set))
print(ss_team_set)
new_set = [x.replace('\xa0NCAA', '').replace(' ','').replace('CalStatery','CS').replace('-','') for x in ss_team_set]

ss_team_set = new_set
print(new_set)
manual_update = pd.read_excel('team matcher manual.xlsx', header=0)
replaced_list = list(manual_update.ss_replace)
orig_list = list(manual_update.ss)
print(ss_team_set)
ss_team_set = implement_manual_edits(orig_list,replaced_list,ss_team_set)
print(ss_team_set)

man_update2 = pd.read_excel('team matcher manual2.xlsx')
replaced_list2 = list(man_update2.ss_replace)
orig_list2 = list(man_update2.ss)
print("OL2 = ", orig_list2)
print("R2 = ",replaced_list2)
ss_team_set = implement_manual_edits(orig_list2,replaced_list2,ss_team_set)
id_data = [ss_2011['Rk'],ss_2011['School'],ss_team_set]
print([ss_2011['Rk'],ss_2011['School'],ss_team_set])
#team_id_set = pd.DataFrame([ss_2011['Rk'],ss_2011['School'],ss_team_set])
ss_2011['School'] = ss_team_set
#ss_team_set = [x.lower() for x in ss_team_set]
#o_team_set = [x.lower() for x in o_team_set]
#print(team_id_set)
#write_xls(team_id_set,'id_master.xlsx')
#print(team_id_set)
'''
name_match = [team for team in o_team_set if (team in ss_team_set)]

o_unmatched = [team for team in o_team_set if (team not in ss_team_set)]
ss_unmatched = [team for team in ss_team_set if (team not in name_match)]
#print ("Matched = ",len(name_match))
ss_unmatched.sort()
o_unmatched.sort()
print(o_unmatched)
print(ss_unmatched)
print(len(o_unmatched))
print(len(ss_unmatched))
team_match = pd.DataFrame([o_unmatched,ss_unmatched])
team_match = team_match.transpose()
write_xls(team_match,'team matcher.xlsx')

write_xls(ss_2011, 'schools post name match.xlsx')
'''