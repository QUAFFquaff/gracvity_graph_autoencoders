
## AUC & AP 指标应用即说明

### P-R曲线、平均精度（Average-Precision，AP）  

首先说一下精确率（Precision）与召回率（Recall）  

<img src="https://github.com/QUAFFquaff/gracvity_graph_autoencoders/blob/master/pic_for_md/p_r.jpg?raw=true" width = "550" height = "300" alt="Structure" align=center />  

- True positives : 正样本被正确识别为正样本。
- True negatives: 负样本被正确识别为负样本。 
- False positives: 假的正样本。被错误的识别为正样本。
- False negatives: 假的负样本。被错误识别为负样本。  

Precision是指，在所有识别的测试集中，True positive所占的比率。  

$$Precision=\frac{TP}{TP+FP}$$  
Recall 是测试集中所有正样本样例中，被正确识别为正样本的比例。  

$$Recall=\frac{TP}{TP+FN}$$  

下图是P/R曲线画到一起的图。

<img src="https://github.com/QUAFFquaff/gracvity_graph_autoencoders/blob/master/pic_for_md/pr_graph.jpg?raw=true" width = "550" height = "300" alt="Structure" align=center /> 

在二分类时选取阈值有时候会参考P-R曲线，选取两个曲线的交点。

