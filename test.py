import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# 生成一些示例数据，这里使用随机生成的数据
data = pd.read_csv("nba/SVM.csv")
X = data.drop("diagnose", axis=1)
y = data["diagnose"]

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for model in ['linear', 'poly', 'rbf']:
    # 创建SVM分类器
    clf = svm.SVC(kernel='linear')  # 这里使用线性核

    # 训练SVM模型
    clf.fit(X_train, y_train)

    # 使用模型进行预测
    y_pred = clf.predict(X_test)

    # 计算分类准确率
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # 你给的数据的最后一条PAT2的
    test = np.array([9.65, 46.78, 56.43, 4.03, 5.62, 12.84, 15.62, 10.11, 5.59, 5.99, 4.70, 4.15, 0.63]).reshape(1, -1)
    print(f"使用模型{model},预测结果：", clf.predict(test))
    # 你给的数据的最后一条PAT1的
    test = np.array([11.87, 70.12, 81.99, 4.87, 7.01, 15.31, 17.98, 12.03, 6.54, 7.26, 5.49, 4.83, 0.68]).reshape(1, -1)
    print(f"使用模型{model},预测结果：", clf.predict(test))
