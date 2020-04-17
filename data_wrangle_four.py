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
reordered_2011 = pd.read_excel('schools post name match.xlsx')
ranks = ss_2011['Rk'].to_list()
odds_names_ordered = reordered_2011['School']
ss_team_set= ss_2011['School'].to_list()
o_team_set= set(o_2011['Team'].to_list())
team_id_set = pd.DataFrame([ranks,ss_team_set,odds_names_ordered])
team_id_set = team_id_set.transpose()
team_id_set.columns = ['ID', 'Stats name', 'Odds name']
write_xls(team_id_set,'id_master.xlsx')
