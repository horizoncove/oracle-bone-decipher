import json,csv
r=json.load(open('raw_results_top5.json'))
N={ # cls: (variant_or_new, glyph_link_notes, phonetic_notes)
'X/1850':("不确定/可能为新字或由·甾类异体：top1 由 p=0.41 与 #2 甾 0.29 差距小；MoCo 由 0.414 vs 吉 0.412 几乎并列",
 "样本为‘凵’形容器内竖一笔（或带短横），与 由/甾/古 共享下部‘凵/口’框形；由 例字内部为菱形/口形，样本多为单竖笔，差异明显",
 "none"),
'X/1264':("可能为 臿 的异体：p=0.57，领先 #2 朕 0.46；MoCo top1 亦为 臿 (0.415 vs 0.296)",
 "样本下部为‘臼’形内含多道斜笔、中贯竖杆，上方两侧有弧笔（似手形）；与 臿 例字共享‘臼+中竖’结构；上部手形 臿 例字中不明显",
 "none"),
'X/1814':("可能为 烄 的异体（也可能为 交/火 组合之新字形）：p=0.64 vs 焚 0.33；MoCo top1 为 赤 (0.481)、烄 第2 (0.464)，两法不完全一致",
 "样本上部为交胫人形‘交’，下部为‘火’；与 烄 例字共享‘交’+‘火’两部件；与 赤（大+火）共享‘火’，区别在上部交胫",
 "烄 从火交声：样本可见的‘交’即候选字声符（据《说文》，未核对卜辞用例）"),
'X/2230':("新字或未定：top1 逆 p=0.20，分数低且两法不一致（MoCo: 遼/𨖹 并列 0.358）",
 "样本左上为倒人形/‘屰’类部件，下为‘止’，部分似从‘彳’；与 逆（屰+止/辵）共享‘止’及倒人形",
 "若上部确为‘屰’，则‘屰’为 逆 之声符（未确认）"),
'X/2213':("倾向新字：top1 飲/㱃 p=0.42，但目视样本为‘酉’+‘彡’三斜笔，不见 飲 的俯身人形与舌形；MoCo top1 配 0.338，分散",
 "与候选共享‘酉’（尊/酒器）部件；右侧三道斜笔似‘彡’，候选 飲/酉/酒 均无此部件（MoCo #5 彭 含‘彡’）",
 "‘酉’在 酒 中为‘酉亦声’（《说文》）；对本字是否表音未知"),
'X/2109':("很可能为 求 的异体：p=0.59 领先 #2 𠦪 0.48；MoCo top1 求 0.445 vs 爻 0.357，两法一致",
 "样本为中贯长竖、两侧对称斜枝、顶部交叉的整体轮廓，与 求 例字几乎同形（整字相似，非偏旁系联）",
 "none"),
'X/2126':("未定/可能新字：top1 貴 p=0.26，分数低；MoCo top1 亦为 貴 0.393（领先 0.15）",
 "样本上部为双手（𦥑/廾形）向下，下部为圆形/‘凵’状物；与 貴（甲骨文作双手捧土/器形）共享双手部件；MoCo #4 廾 亦提示双手",
 "none"),
'X/2173':("很可能为 䧅 的异体（或数据集内重复标注）：p=0.96，几乎全票（32/32），MoCo 䧅 0.54 vs 降 0.42",
 "样本左为‘阜’（梯形竖笔加短横），右为上下叠置部件，与 䧅 例字整体几乎一致；与 降 共享‘阜’",
 "none（未核实）"),
'X/1366':("倾向新字：top1 眢 p=0.43 但目视不像；MoCo 分数低 (0.317) 且分散",
 "样本为‘木/屮’类枝杈，主干中部有方框/束状物（似缚束）；与 析（木）共享‘木’形，与 眢 仅有叉枝相似",
 "none"),
'X/1485':("未定：top1 鬯 p=0.25 低；目视更接近 #2 擒（禽，带柄网形），MoCo 擒 0.334 与 溫 0.336 并列",
 "样本为上部网/器形（交叉网格）+下部带横的长柄，与 擒/禽（毕网有柄）共享‘毕网+柄’部件；与 鬯 共享上部器形",
 "none（禽 从今声，但样本不见‘今’）"),
'X/1370':("未定：classifier 眉 0.22 与 MoCo 省 0.40 不一致",
 "样本下部为‘目’形（三角/菱形眼框），上部为‘丅/屮’形；与 省（屮+目）共享‘目’及上部竖笔结构；与 眉 共享‘目’",
 "none"),
'X/2002':("可能为 嘉 的异体：p=0.76 领先 #2 婦 0.73；但 MoCo 嘉 仅第3 (0.308)，两法部分不一致",
 "样本左为‘女’，右为‘力（耒形）’，与 HUST 嘉(0371) 例字（女+力，即读作嘉之形）同构；与 婦、㚸 共享‘女’",
 "嘉 从加声（《说文》），‘加’含‘力’；样本所见‘力’或与此相关（未核实）"),
'X/2190':("很可能为 途 的异体：p=0.79 领先 0.68；MoCo top1 途 0.543 vs 余 0.36，两法一致",
 "样本上为‘余’（屋顶形+中竖+横），下为‘止’，与 途 例字（余+止）同构；与 余 共享上部",
 "途 从辵余声：样本中的‘余’即候选字声符"),
'X/1401':("倾向新字：top1 妻 p=0.13，极低且分散；MoCo 分数 ≤0.27",
 "样本为上下两个菱形/X 形叠置、下接三角形（似‘大’下肢），与 㚔/幸（刑具形）共享菱形框；与 妻 无明显共享部件",
 "none"),
'X/1270':("可能为 召 的繁形异体：p=0.70 领先 0.64；MoCo top1 召 0.381 vs 0.308",
 "样本上为双手（𦥑形，多指向上）、下为器皿/‘凵’中有物，与 召（繁形：双手+酒器）例字共享‘双手+器’结构",
 "召 从口刀声，但样本中‘刀/匕’不清 → none"),
'Y+H/60003':("未定：classifier 𡈼 0.77 但 MoCo top1 尻 0.631 vs 𡈼 0.595；HWOBC 手写样本彼此高度相似(intra 0.68)",
 "样本为侧立人形（‘人/尸’）下端成圈；与 𡈼（人立于土）、尻（尸下加笔）共享侧身人形，差别在下部圈形",
 "none"),
'Y+H/60004':("可能为 疾 的省体/异体：p=0.49，但 MoCo 丂 0.434 vs 疾 0.433 并列",
 "样本为侧身人形旁加一短竖，疾 例字为人形旁两短竖（‘爿’省形）；共享‘人+床形短竖’",
 "none（《说文》疾 从矢声，样本无矢）"),
'Y+H/6000A':("很可能为 屎 的异体（或与已释类重复）：p=0.90，全票25/25；MoCo 屎 0.603 vs 𡱂 0.536",
 "样本为‘尸’（侧身蹲人形）后下方加数点，与 屎 例字同构；与 尾、𡱂 共享‘尸’",
 "none"),
'Y+H/60012':("未定/可能新字：classifier 身 0.77，但 MoCo top1 家 0.446，两法不一致",
 "样本为人形腹部作菱形/圈（同‘身’之鼓腹）、腹旁加三指‘又’形；与 身 共享鼓腹人形，‘又’为候选所无",
 "none"),
'Y+H/60013':("很可能为 殷 的异体：p=0.64 领先 0.59；MoCo 殷 0.543 vs 㐱 0.393，两法一致",
 "样本左为（鼓腹）人形、右为‘殳’（手持器），与 殷 例字同构，共享‘殳’及人形",
 "none"),
}
SRC_X="无出处信息（来源书：《新甲骨文编》；文件名形如 X_？_{a}…{b}_k，仅含未说明含义的内部流水号，无合集等著录号）"
SRC_YH="无出处信息（24 张为 HWOBC 手写数据集 H_？_{c}_k，1 张来自殷契文渊 Y_？_{c}.jpg；文件名无著录号）"
import os
def src(x):
    s,c=x['cls'].split('/')
    if s=='X':
        nums=sorted({int(f.split('_')[2]) for f in os.listdir(f'data/HUST-OBC/undeciphered/{s}/{c}')})
        return SRC_X.format(a=nums[0],b=nums[-1])
    return SRC_YH.format(c=c)
METH="ResNet50 闭集分类器（HUST-OBC 官方 Validation 权重，1588 已释类；对该类全部样本 softmax 取均值）；另附 MoCo-ResNet18 嵌入检索（每已释类 12 张图库，类得分=各样本最大余弦相似度之均值）。OBSD 未运行（未找到已发布的扩散模型 checkpoint）"
rows=[]
for x in r:
    c=x['cls']; v,g,p=N[c]
    A='; '.join(f"{a[0]} ({a[2]:.3f}, {a[3]}/{x['n']}票)" for a in x['A'])
    B='; '.join(f"{b[0]} ({b[2]:.3f})" for b in x['B'])
    rows.append(dict(obc_class_id=c,n_samples=x['n'],top5_candidates_classifier=A,top5_candidates_moco_knn=B,method=METH,
      source_rubbings=src(x),variant_or_new=v,excluded_miscarve='unchecked — needs original rubbing review',glyph_link_notes=g,phonetic_notes=p,
      intra_class_sim=round(x['intra_sim'],3)))
with open('results.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump(rows,open('results_rows.json','w'),ensure_ascii=False,indent=1)
LIM="""## 方法与局限 (Methods & limits)

- **性质**：以下均为 **AI 候选，未经人工验证**，不构成释读结论；需结合原拓、辞例与字形演变由研究者复核。
- **选类**：HUST-OBC 未释字（undeciphered）中样本最多的 20 类。X 子集（《新甲骨文编》）前 15 类样本数 61–26；其后有上百个 Y+H 类并列为 25 张，按类编号排序取前 5 个（60003/60004/6000A/60012/60013）——这是平局截断，不代表这 5 类比其余 25 张类更“重要”。
- **方法 A（主排序）**：ResNet50 闭集分类器，HUST-OBS 官方 Validation 权重（val_max_val_acc.pth），1588 个已释类；对该类全部样本求 softmax 均值，列出 top-5（括号内：均值概率，以及该候选为 argmax 的样本票数）。闭集模型**必然**输出某个已释字，即使该字确为新字。
- **方法 B（交叉检验）**：HUST-OBS MoCo-ResNet18 自监督嵌入，与每个已释类 12 张样本（共 18,015 张）做余弦检索；类得分=每个样本对该类的最大相似度再取均值。
- **OBSD（扩散模型释读）未运行**：OBSD 仓库已克隆，但其 README 只提供 refine 步骤用的 FontDiffuser 权重，未找到已发布的 OBSD 扩散模型 checkpoint（需自行在 HUST-OBC 上训练，本轮未做），故本版仅用图像检索/分类。
- **异体/新字判断**：依据 top1 概率、与 #2 的分差、两种方法是否一致及目视比对；属启发式。
- **字形系联/音义**：字形系联为在本 box 上逐类目视样本与候选例字图像所得；音义仅在候选字的已知声符（据《说文》）确实在样本中可见时注明，未核卜辞用例。
- **误刻排除**：全部为 unchecked — needs original rubbing review。
- **出处**：HUST-OBC 未释字文件名不含合集等著录号，故 source_rubbings 均为“无出处信息”；未做任何推测。
- **数据偏差**：Y+H 类主要为 HWOBC 手写摹本（类内相似度 0.59–0.70，远高于 X 类 0.09–0.40），且多个类与已释例字几乎同形（如 6000A→屎、X/2173→䧅），可能是不同来源间的标注不一致/重复，而非真正“新释”。
- **许可**：HUST-OBC 采用 **CC BY-NC 4.0**——仅限非商业使用、须署名；**不要公开再分发图像**（contact_sheet.png 仅供团队内部使用）。
"""
md=["# 未释字候选样例 v0.1（20 字）\n","HUST-OBC 未释字 Top-20 类的 AI 候选释读。附图：contact_sheet.png（左：3 个未释样本；右：分类器 top-3 候选的已释例字）。\n",
"| obc_class_id | n | top-5（分类器 p, 票数） | top-5（MoCo kNN 余弦） | variant_or_new | glyph_link_notes | phonetic_notes | source_rubbings | excluded_miscarve |","|---|---|---|---|---|---|---|---|---|"]
for x in rows:
    md.append('| '+' | '.join(str(x[k]).replace('|','/') for k in ['obc_class_id','n_samples','top5_candidates_classifier','top5_candidates_moco_knn','variant_or_new','glyph_link_notes','phonetic_notes','source_rubbings','excluded_miscarve'])+' |')
md.append('\n**method（所有行相同）**：'+METH+'\n')
md.append(LIM)
open('results.md','w').write('\n'.join(md)); open('limits.md','w').write(LIM)
