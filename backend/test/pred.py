import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    confusion_matrix, ConfusionMatrixDisplay,
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc, roc_auc_score
)

class PredictAnalyzer:
    def __init__(self, task_type, y, y_pred, y_prob=None, class_names=None):
        """
        Parameters
        ----------
        task_type : str
            "regression" or "classifier"
        y : array-like
            실제 값
        y_pred : array-like
            예측 값
        y_prob : array-like, optional
            분류일 경우 확률 (predict_proba 결과)
        class_names : list, optional
            분류일 경우 클래스 이름 리스트
        """
        self.task_type = task_type
        self.y = np.array(y)
        self.y_pred = np.array(y_pred)
        self.y_prob = y_prob
        self.class_names = class_names

    def analyze(self):
        if self.task_type == "regression":
            self._analyze_regression()
        elif self.task_type == "classifier":
            self._analyze_classification()
        else:
            raise ValueError("task_type must be 'regression' or 'classifier'")

    def _analyze_regression(self):
        # --- 성과 지표 ---
        r2 = r2_score(self.y, self.y_pred)
        mse = mean_squared_error(self.y, self.y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(self.y, self.y_pred)

        print("📊 Regression Metrics")
        print(f"R² Score : {r2:.3f}")
        print(f"MSE      : {mse:.3f}")
        print(f"RMSE     : {rmse:.3f}")
        print(f"MAE      : {mae:.3f}")

        # --- y vs y_pred 산점도 ---
        plt.figure(figsize=(6,6))
        plt.scatter(self.y, self.y_pred, alpha=0.6)
        plt.plot([self.y.min(), self.y.max()], [self.y.min(), self.y.max()], "r--")
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.title("y vs y_pred")
        plt.show()

    def _analyze_classification(self):
        # --- 성과 지표 ---
        acc = accuracy_score(self.y, self.y_pred)
        prec = precision_score(self.y, self.y_pred, average="weighted", zero_division=0)
        rec = recall_score(self.y, self.y_pred, average="weighted", zero_division=0)
        f1 = f1_score(self.y, self.y_pred, average="weighted", zero_division=0)

        print("📊 Classification Metrics")
        print(f"Accuracy  : {acc:.3f}")
        print(f"Precision : {prec:.3f}")
        print(f"Recall    : {rec:.3f}")
        print(f"F1 Score  : {f1:.3f}")

        # --- Confusion Matrix ---
        cm = confusion_matrix(self.y, self.y_pred)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.class_names)
        disp.plot(cmap="Blues")
        plt.title("Confusion Matrix")
        plt.show()

        # --- ROC Curve (이진 or 다중) ---
        if self.y_prob is not None:
            try:
                if self.y_prob.ndim == 1 or self.y_prob.shape[1] == 2:  # 이진 분류
                    y_prob_binary = self.y_prob[:,1] if self.y_prob.ndim > 1 else self.y_prob
                    fpr, tpr, _ = roc_curve(self.y, y_prob_binary)
                    roc_auc = auc(fpr, tpr)

                    plt.figure()
                    plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
                    plt.plot([0,1],[0,1], "k--")
                    plt.xlabel("False Positive Rate")
                    plt.ylabel("True Positive Rate")
                    plt.title("ROC Curve")
                    plt.legend(loc="lower right")
                    plt.show()
                else:  # 다중 분류 → micro-average
                    from sklearn.preprocessing import label_binarize
                    y_bin = label_binarize(self.y, classes=np.arange(self.y_prob.shape[1]))
                    fpr, tpr, _ = roc_curve(y_bin.ravel(), self.y_prob.ravel())
                    roc_auc = auc(fpr, tpr)

                    plt.figure()
                    plt.plot(fpr, tpr, label=f"micro-average ROC (AUC = {roc_auc:.2f})", color="blue")
                    plt.plot([0,1],[0,1], "k--")
                    plt.xlabel("False Positive Rate")
                    plt.ylabel("True Positive Rate")
                    plt.title("Multiclass ROC Curve (micro-average)")
                    plt.legend(loc="lower right")
                    plt.show()
            except Exception as e:
                print("ROC Curve 계산 불가:", e)
