
## AUC & AP 指标应用即说明

### P-R曲线、平均精度（Average-Precision，AP）  

首先说一下精确率（Precision）与召回率（Recall）  

<img src="https://github.com/QUAFFquaff/gracvity_graph_autoencoders/blob/master/pic_for_md/p_r.jpg?raw=true" width = "550" height = "300" alt="Structure" align=center />  

- True positives : 正样本被正确识别为正样本。
- True negatives: 负样本被正确识别为负样本。 
- False positives: 假的正样本。被错误的识别为正样本。
- False negatives: 假的负样本。被错误识别为负样本。  

Precision是指，在所有识别的测试集中，True positive所占的比率。  

质能方程 $$xyz$$  
$$E=mc^2$$