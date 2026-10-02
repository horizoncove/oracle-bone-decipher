import json,csv
r=json.load(open('appendix_raw.json')); m=json.load(open('appendix_map.json'))
rows={x['obc_class_id']:x for x in csv.DictReader(open('appendix_all_classes.csv'))}
# add k column to all-classes csv
with open('appendix_all_classes.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['obc_class_id','n_samples','serial_min','serial_max','n_serials','hust_appendix_k(≈附录号,书号约在k..k+20)'])
    for cid,x in sorted(rows.items(),key=lambda t:m[t[0]]): w.writerow([cid,x['n_samples'],x['serial_min'],x['serial_max'],x['n_serials'],m[cid]])
win={'X/1212':'992,1007','X/113':'17,22','X/773':'606','X/800':'631','X/833':'646','X/1054':'857','X/264':'139','X/1153':'934,939','X/1195':'980,992','X/39':'1038,1039','X/365':'243','X/1190':'980'}
notes={
'X/1190':'TOP8｜宀/丵状尖顶+王(玉)+下部臼/凵框，构件与“璞(𤰇)”全同→疑为璞异体（当释而未释？）',
'X/839':'TOP8｜燕形鸟+旁加点/小画→燕之繁体或从燕之字（地名？）',
'X/365':'TOP8｜眉(目+眉毛)+下叠框格状构件→从眉之合体；分类器眉.82，需辨是否即眉异体',
'X/462':'TOP8｜户形+又/攴→启/肇系（肇.78）；与X/461(k310 户+又→取?)相邻同族',
'X/956':'TOP8｜口(或二)覆于丙(冂内八)→丙声字？商省/冋/尚之讹待考',
'X/276':'TOP8｜跪人头上Y/V形→光之异体（两法均光）',
'X/297':'TOP8｜跪女+8字形糸/幺贯身→女+糸会意（妟/妾仅形近）；X/299(k165)同族',
'X/849':'TOP8｜示(丅)+卩/巳形曲笔→祀或𥘅(示+卩)异体',
'X/299':'跪女+糸缠绕，与X/297同族（妍.45）',
'X/1195':'冊中贯丨→冊/毌系变体',
'X/39':'酉上加X/叉形→从酉之字（祼/瓚类祭名？）',
'X/358':'长方器形+殳→从殳击器（𣪕.46）',
'X/82':'彳/亻+乎形加点→乎系？',
'X/391':'凵上两高长方→㠭族（与395、48同族）','X/395':'凵上两工形→㠭族','X/48':'凵+两竖环→㠭族/幽?',
'X/461':'空长方+又/卩→取/启系，与462相邻','X/113':'人形Y角+胸带→免？',
'X/1008':'梯形双格内有点→宜/俎或㐭','X/278':'跪人三叉头饰→每/茍系',
'X/773':'脊干单侧多枝+卷首','X/800':'凡/冂框+它/己形','X/833':'X星形+又','X/857':'大人身交叉画→爽/奭?','X/1054':'菱/六角形+人或刀(刜.29)',
'X/1212':'旗杆飘游自凵/口/田升起，两法均分散','X/690':'木/屮植于凵/皿','X/1148':'混杂类（火/屮于冂 + 朿?）','X/264':'卩/跪人+口→次/御?','X/473':'叟/爇系','X/1153':'兽形(狐/犬)'}
top8=['X/1190','X/839','X/365','X/462','X/956','X/276','X/297','X/849']
def f5(s): return '; '.join(f'{a[0]} {a[2]:.2f}' for a in s[:5])
out=[]
for e in r:
    c=e['cls']; x=rows[c]
    out.append(dict(rank=(top8.index(c)+1 if c in top8 else ''),obc_class_id=c,serial_range=f"{x['serial_min']}-{x['serial_max']}",n=e['n'],hust_k=m[c],
      clf_top5=f5(e['A']),moco_top5=f5(e['B']),yuan_window_hits=win.get(c,''),notes=notes.get(c,'')))
out.sort(key=lambda d:(d['rank']=='',d['rank'] or 0,-int(d['n'])))
with open('appendix_pool.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
