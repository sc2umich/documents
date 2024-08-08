import os
import re
import pandas as pd
dir_struct =  list(os.walk("."))

re_title = re.compile("Title: (.*?)$",re.MULTILINE)
re_author = re.compile("Author: (.*?)$",re.MULTILINE)
re_date = re.compile("Date: (.*?)$",re.MULTILINE)

def link_format(id,file):
    if id=="Not Published":
        return "Not Published"
    return f"[{id}]({file})"

memos = []
memo_result = [(d,files) for d,ds,files in dir_struct if "memorandums" in d][0]
memo_files = memo_result[1]
d = memo_result[0]

agenda_result = [(d,files) for d,ds,files in dir_struct if "meetings" in d[-8:]][0]
agenda_files = agenda_result[1]
d_agenda = agenda_result[0]



for filename in memo_files:
    memo = {}
    if filename=="memos.md" or filename=="test.md":
        continue
    else:
        memo["id"] = filename[0:7]
        memo["filename"]=filename
        with open(os.path.join(d,filename),"r") as f:
            txt = f.read()
        # print(txt)
        memo["title"] = re_title.search(txt)[1]
        try:
            memo["author"] = re_author.search(txt)[1]
        except Exception:
            memo["author"] = ""
        try:
            memo["date"] = re_date.search(txt)[1]
        except Exception:
            memo["date"] = ""

        memo["semester"] = filename[0:3]

        for agenda_f in agenda_files:
            with open(os.path.join(d_agenda,agenda_f),"r") as f:
                a_txt = f.read()
            if memo["id"] in a_txt:
                memo["a_id"] = agenda_f[0:-3]
                memo["a_filename"] = "../meetings/"+agenda_f
    memos.append(memo)

df_memo = pd.DataFrame(memos)
# print(df_memo)
df_memo["a_id"] = df_memo["a_id"].fillna("Not Published")
df_memo["Document"] = df_memo.apply(lambda row: link_format(row["id"],row["filename"]),axis=1)
df_memo["Associated Agenda"] = df_memo.apply(lambda row: link_format(row["a_id"],row["a_filename"]),axis=1)
df_memo = df_memo.rename({"title":"Title","author":"Author","date":"Date","semester":"Semester"},axis=1)
df_memo = df_memo.drop(["id","a_id","a_filename","filename"],axis=1)
df_memo = df_memo[["Document","Title","Author","Date","Semester","Associated Agenda"]]
semesters = df_memo.groupby("Semester").count().index

with open("memorandums/test.md","w") as f:
    for s in semesters:
        f.write(f"# {s}\n\n")
        df_memo[df_memo["Semester"]==s].sort_values("Document").to_markdown(f,index=False)
        f.write(f"\n\n")


# Legislation
re_sponsor = re.compile("Sponsor(s): (.*?)$",re.MULTILINE)


leg_result = [(d,files) for d,ds,files in dir_struct if "legislation" in d][0]
leg_files = leg_result[1]
d_leg = leg_result[0]

legs = []
for filename in leg_files:
    leg = {}
    if filename=="legislation.md" or filename=="test.md":
        continue
    else:
        leg["id"] = filename[0:7]
        leg["filename"]=filename
        with open(os.path.join(d_leg,filename),"r") as f:
            txt = f.read()
        # print(txt)
        leg["title"] = re_title.search(txt)[1]
        try:
            leg["sponsor"] = re_sponsor.search(txt)[1]
        except Exception:
            leg["sponsor"] = ""
        try:
            leg["date"] = re_date.search(txt)[1]
        except Exception:
            leg["date"] = ""

        leg["semester"] = filename[0:3]
        leg["approved"] = ""
        leg["minutes"] = ""

        for agenda_f in agenda_files:
            with open(os.path.join(d_agenda,agenda_f),"r") as f:
                a_txt = f.read()
            if leg["id"] in a_txt:
                leg["a_id"] = agenda_f[0:-3]
                leg["a_filename"] = "../meetings/"+agenda_f
    legs.append(leg)

df_memo = pd.DataFrame(legs)
# print(df_memo)
df_memo["a_id"] = df_memo["a_id"].fillna("Not Published")
df_memo["Document"] = df_memo.apply(lambda row: link_format(row["id"],row["filename"]),axis=1)
df_memo["First Reading"] = df_memo.apply(lambda row: link_format(row["a_id"],row["a_filename"]),axis=1)
df_memo = df_memo.rename({"title":"Title","sponsor":"Sponsor(s)","date":"Date","semester":"Semester","approved":"Approved","minutes":"Minutes"},axis=1)
df_memo = df_memo.drop(["id","a_id","a_filename","filename"],axis=1)
df_memo = df_memo[["Document","Title","Sponsor(s)","Date","Semester","First Reading","Approved","Minutes"]]

semesters = df_memo.groupby("Semester").count().index



with open("legislation/legislation.md","w") as f:
    for s in semesters:
        f.write(f"# {s}\n\n")
        df_memo[df_memo["Semester"]==s].sort_values("Document").to_markdown(f,index=False)
        f.write(f"\n\n")