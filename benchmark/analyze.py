from pathlib import Path
import json,csv,itertools,math,statistics,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
d=json.loads((R/'raw-results.json').read_text());assert d['complete'] and not d.get('error'),'Experiment incomplete'
runs=[r for r in d['runs'] if not r['repeat']];assert len(runs)==24
policies=['FIXED','RANDOM','Q_LEARNING'];labels=['Fixed settings','Random actions','Q-learning'];colors=['#aab9c7','#f7b574','#c8fb75'];seeds=list(range(101,109))
by={(r['seed'],r['policy']):r for r in runs}
for seed in seeds:
 group=[by[seed,p] for p in policies];assert len(set(r['initialHash'] for r in group))==1
 for r in group:
  assert [s['tick'] for s in r['samples']]==list(range(0,1801,30))
  initial=r['samples'][0]['mass'];auc=sum(30*(a['mass']+b['mass'])/2 for a,b in zip(r['samples'],r['samples'][1:]))/1800/initial
  assert math.isclose(auc,r['summary']['meanMassRatio'],rel_tol=1e-12)
repeat=[r for r in d['runs'] if r['repeat']][0];base=by[101,'FIXED'];diff=max(abs(a[k]-b[k]) for a,b in zip(base['samples'],repeat['samples']) for k in ['mass','energy','freeEnergy','occupiedFraction','activity'])
summary={}
for p in policies:
 group=[by[s,p] for s in seeds];vals=[r['summary']['meanMassRatio'] for r in group]
 summary[p]={'n':8,'meanMassRatio':statistics.mean(vals),'medianMassRatio':statistics.median(vals),'meanFinalMassRatio':statistics.mean(r['summary']['finalMassRatio'] for r in group),'meanEnergyRatio':statistics.mean(r['summary']['meanEnergyRatio'] for r in group),'declineCount':sum(r['summary']['declineStep'] is not None for r in group),'declineDetectionSteps':[r['summary']['declineStep'] for r in group],'meanActivity':statistics.mean(r['summary']['meanActivity'] for r in group)}
pairs={}
for p in ['FIXED','RANDOM']:
 differences=np.array([by[s,'Q_LEARNING']['summary']['meanMassRatio']-by[s,p]['summary']['meanMassRatio'] for s in seeds]);obs=abs(differences.mean());null=[abs(np.mean(differences*np.array(signs))) for signs in itertools.product([-1,1],repeat=8)]
 pairs[p]={'meanDifference':float(differences.mean()),'medianDifference':float(np.median(differences)),'wins':int(np.sum(differences>1e-10)),'ties':int(np.sum(abs(differences)<=1e-10)),'losses':int(np.sum(differences< -1e-10)),'relativeDifferenceOfGroupMeans':summary['Q_LEARNING']['meanMassRatio']/summary[p]['meanMassRatio']-1,'exploratorySignFlipP':sum(x>=obs-1e-15 for x in null)/len(null),'differences':differences.tolist()}
results={'summary':summary,'paired':pairs,'repeatMaxAbsoluteDifference':diff,'allInitialHashesMatched':True};(R/'summary.json').write_text(json.dumps(results,indent=2))
with (R/'per-run.csv').open('w') as f:
 fields=['seed','policy','initialHash','initialMass','initialEnergy','meanMassRatio','finalMassRatio','meanEnergyRatio','meanActivity','declineStep','censored','elapsedSeconds'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in runs:w.writerow({k: r.get(k,r['summary'].get(k)) for k in fields})
with (R/'timeseries.csv').open('w') as f:
 fields=['seed','policy','tick','mass','massRatio','energy','energyRatio','freeEnergy','occupiedFraction','activity'];w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in runs:
  for s in r['samples']:w.writerow({'seed':r['seed'],'policy':r['policy'],**s,'massRatio':s['mass']/r['initialMass'],'energyRatio':s['energy']/r['initialEnergy']})
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'figure.facecolor':'#0c1110','axes.facecolor':'#0c1110','axes.edgecolor':'#50604b','axes.labelcolor':'#e9efe2','text.color':'#e9efe2','xtick.color':'#b9c7b0','ytick.color':'#b9c7b0','grid.color':'#364332','savefig.facecolor':'#0c1110'})
fig,axs=plt.subplots(1,2,figsize=(16,8),gridspec_kw={'width_ratios':[1,1.25]});fig.subplots_adjust(left=.075,right=.96,bottom=.20,top=.77,wspace=.27)
fig.text(.075,.925,'ECHO / CONTROLLED PILOT 01',color='#c8fb75',fontsize=15)
fig.text(.075,.861,'Does learned care preserve more simulated mass?',fontsize=23)
for seed in seeds:
 vals=[by[seed,p]['summary']['meanMassRatio'] for p in policies];axs[0].plot(range(3),vals,color='#71826a',alpha=.55,lw=1)
 for x,y,c in zip(range(3),vals,colors):axs[0].scatter(x,y,color=c,s=42,zorder=3)
for i,p in enumerate(policies):
 avg=summary[p]['meanMassRatio'];axs[0].scatter(i,avg,marker='D',s=130,color=colors[i],edgecolor='#0c1110',zorder=5);axs[0].annotate(f'{avg:.3f}',(i,avg),xytext=(12,7),textcoords='offset points',color=colors[i],fontsize=13,fontweight='bold')
axs[0].set_xticks(range(3),labels);axs[0].set_xlim(-.3,2.7);axs[0].set_ylim(bottom=0);axs[0].set_ylabel('Time-averaged mass / initial mass');axs[0].set_title('All 8 matched worlds · diamonds = means',loc='left',fontsize=12);axs[0].grid(axis='y',alpha=.5)
for p,c,label in zip(policies,colors,labels):
 arr=np.array([[s['mass']/r['initialMass'] for s in r['samples']] for r in [by[seed,p] for seed in seeds]])
 for v in arr:axs[1].plot(range(0,1801,30),v,color=c,lw=.65,alpha=.13)
 axs[1].plot(range(0,1801,30),arr.mean(0),color=c,lw=2.5,label=label)
axs[1].axhline(.1,color='#f0ece0',ls=':',lw=1,alpha=.65);axs[1].set_xlabel('Simulation step');axs[1].set_ylabel('Mass / initial mass');axs[1].set_title('Mass trajectories · bold = mean across worlds',loc='left',fontsize=12);axs[1].set_xlim(0,1800);axs[1].set_ylim(bottom=0);axs[1].grid(alpha=.4);axs[1].legend(facecolor='#18221a',edgecolor='#364332',fontsize=11)
for ax in axs:ax.spines[['top','right']].set_visible(False)
fig.text(.075,.095,'8 seeds × 3 policies · garden world · 128² cells · 1,800 steps/run · fresh Q-table per run',fontsize=12,color='#b9c7b0')
fig.text(.075,.055,'Mass is a simulator proxy, not lifespan or intelligence. Small cold-start pilot; no general efficacy claim.',fontsize=12,color='#c8fb75')
fig.savefig(R/'ECHO-pilot-results.png',dpi=150);fig.savefig(R/'ECHO-pilot-results.svg');plt.close(fig)
rows='\n'.join(f"| {label} | {summary[p]['meanMassRatio']:.4f} | {summary[p]['medianMassRatio']:.4f} | {summary[p]['meanFinalMassRatio']:.4f} | {summary[p]['declineCount']}/8 |" for p,label in zip(policies,['固定环境','随机干预','Q-learning']))
comparison='\n'.join(f"- Q-learning 相对 {p}：主指标的配对均值差 {pairs[p]['meanDifference']:+.6f}；均值相对差 {pairs[p]['relativeDifferenceOfGroupMeans']:+.2%}；{pairs[p]['wins']} 胜 / {pairs[p]['ties']} 平 / {pairs[p]['losses']} 负。探索性双侧符号翻转 p={pairs[p]['exploratorySignFlipP']:.4f}。" for p in ['FIXED','RANDOM'])
report=f'''# ECHO 小规模配对对照实验结果

执行日期：2026-09-25。完成 24 次主要运行和 1 次重复校验。此报告只描述给定模拟器、设定、种子和时间窗口的结果。

## 主要结果

主指标为「时间平均质量 / 初始质量」：对质量比曲线做梯形积分，再除以 1,800 步。1.0 表示平均维持初始质量，不代表100%个体存活。质量是模拟器的连续场量，静止或密集图案也可能得分高。

| 策略 | 主指标均值 | 主指标中位数 | 终点质量比均值 | 检出持续衰退 |
|---|---:|---:|---:|---:|
{rows}

{comparison}

符号翻转检验是探索性描述，依赖配对差在零假设下可交换符号的假设；样本仅8组，两次比较未进行多重检验校正，不作为确认性优越性证据。这里没有把模拟质量的差异解释成寿命、真实生命或代币价值的提高。

## 衰退事件

规则在运行前写入 PROTOCOL.md：每30步观测，连续10次质量低于初始值10%时，记录该次检测步数。此检测时间不是实际寿命。未检测到则右删失于1800步，运行不因衰退而提前终止。

'''+'\n'.join(f"- {p}（种子101–108顺序）：{summary[p]['declineDetectionSteps']}" for p in policies)+f'''

## 一致性与执行环境

- 所有同种子三组初始数组哈希完全相同。
- FIXED / seed 101 的重复运行，全部观测指标最大绝对差为 {diff:.12g}。
- 浏览器：{d['metadata']['userAgent']}
- GPU：{d['metadata']['renderer']}
- 开始：{d['startedAt']}；结束：{d['finishedAt']}。
- 源码与协议SHA-256在运行前保存于 source-hashes.json；分析程序随数据交付。

## 实验限制

1. 只有 garden 场景、8个种子，每个策略/种子运行一次；没有估计多个探索随机种子的内部波动。
2. Q-learning 从空表开始，每次仅有8次已完成反馈更新。结果不代表充分训练后的策略，也不代表算法普遍优劣。
3. 固定组仅选 action 0（光照.35、变异.002）；没有对所有固定设置做最优基线搜索。所有组均从该配置启动，与网站初始变异.003不同。
4. 当前奖励偏向总质量增长。质量扩张可能对应无趣的空间填满，不能等同于复杂性、适应性或更高级生命。
5. 随机和学习组共享相同初始PRNG seed，但随机数调用数不同，因此不具有相同动作序列。
6. 本轮是在同一浏览器/GPU复测，不能证明跨设备逐位重现。
7. 没有实验操控代币、价格或持币权利，结果不构成这些方面的证据。

## 交付文件

- PROTOCOL.md：运行前协议。
- raw-results.json：完整元信息、每次观测、动作历史和Q表，含重复校验。
- per-run.csv、timeseries.csv：可直接分析的数据。
- summary.json：汇总及探索性配对比较。
- ECHO-pilot-results.png / .svg：真实数据图。
- source/：实验网页和锁定的模拟源码；保留上游MIT许可。
- analyze.py：图表及报告生成脚本（需要numpy、matplotlib）。
'''
(R/'实验结果报告.md').write_text(report)
print(json.dumps(results,indent=2));print('Validated dataset and generated plots/report.')
