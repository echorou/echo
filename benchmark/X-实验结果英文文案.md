# 实验结果英文串文

建议替换原预热计划的研究结果时段。第1条附 ECHO-pilot-results.png，后两条回复前一条。以下均为本轮实际结果；下一轮仅为研究方向，尚未完成。原始数据包上传到公开可访问位置后，可另附真实链接。

## 1/3

ECHO research log 01: Does learned care help? We tested fixed settings, random actions and a Q-learning caretaker across 8 matched worlds, 1,800 steps each. Same initial states. 24 runs. Here's what happened.

## 2/3

Mean time-averaged mass / initial mass: fixed 3.269, random 3.293, Q-learning 3.282. Q-learning was +0.41% vs fixed and -0.32% vs random. Two expanding worlds dominate these means; all three policies reached sustained decline in 6/8 worlds.

## 3/3

This cold-start pilot shows no consistent advantage for learned care. Each Q-learning run had only 8 feedback updates. Next question: does longer training help on unseen worlds? We'll need better measures of structure and stability, too. Mass alone is not intelligence.
