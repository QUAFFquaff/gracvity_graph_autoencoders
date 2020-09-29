
## AUC & AP 指标应用即说明

### P-R曲线  

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

P-R曲线：
选取不同阈值时对应的精度和召回画出来 

<img src="https://github.com/QUAFFquaff/gracvity_graph_autoencoders/blob/master/pic_for_md/p-r-curve.jpg?raw=true" width = "550" height = "300" alt="Structure" align=center /> 
总体趋势，精度越高，召回越低，当召回达到1时，对应概率分数最低的正样本，这个时候正样本数量除以所有大于等于该阈值的样本数量就是最低的精度值。

### **平均精度（Average-Precision，AP）**  
P-R曲线围起来的面积，通常来说一个越好的分类器，AP值越高。

### **ROC曲线**  

- 横坐标：假正率(False positive rate， FPR)，FPR = FP / [ FP + TN] ，代表所有负样本中错误预测为正样本的概率，假警报率；
- 纵坐标：真正率(True positive rate， TPR)，TPR  = TP / [ TP + FN] ，代表所有正样本中预测正确的概率，命中率。

<img src="https://github.com/QUAFFquaff/gracvity_graph_autoencoders/blob/master/pic_for_md/ROC.jpg?raw=true" width = "300" height = "300" alt="Structure" align=center />    
曲线越接近(0,1)，分类效果越好。
曲线绘制的时候会选取不同的threshold，每个threshold对应曲线中的一个点。有时候会画成阶梯形曲线。


### **AUC曲线**  
AUC: Area Under Curve, 是 ROC曲线下的面积。