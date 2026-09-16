"""Pipeline mô hình cho Titanic.

Gói toàn bộ tiền xử lý và mô hình vào một Pipeline để tránh rò rỉ dữ liệu:
OneHotEncoder chỉ học trên phần train của mỗi fold, không học trên cả tập.
"""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .titanic import CATEGORICAL, FEATURES, NUMERIC


def build_pipeline(n_estimators: int = 300, max_depth: int | None = 6, seed: int = 1) -> Pipeline:
    """Tiền xử lý + RandomForest trong một Pipeline."""
    pre = ColumnTransformer(
        [
            # handle_unknown='ignore' để nhãn chỉ xuất hiện ở test không làm vỡ transform.
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("num", "passthrough", NUMERIC),
        ]
    )
    # Cây quyết định không cần chuẩn hóa thang đo nên passthrough là đủ.
    return Pipeline(
        [
            ("pre", pre),
            ("clf", RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=seed,
                n_jobs=-1,
            )),
        ]
    )


def evaluate(pipe: Pipeline, train: pd.DataFrame, folds: int = 5, seed: int = 1):
    """Cross-validation phân tầng. Trả về mảng accuracy từng fold."""
    # Phân tầng theo nhãn vì tỉ lệ sống sót chỉ khoảng 38%, chia ngẫu nhiên
    # có thể tạo fold lệch làm điểm số dao động mạnh.
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=seed)
    return cross_val_score(pipe, train[FEATURES], train["Survived"], cv=cv, scoring="accuracy")


def make_submission(pipe: Pipeline, train: pd.DataFrame, test: pd.DataFrame,
                    path: str = "submission.csv") -> pd.DataFrame:
    """Huấn luyện trên toàn bộ train rồi ghi file nộp bài."""
    pipe.fit(train[FEATURES], train["Survived"])
    sub = pd.DataFrame({
        "PassengerId": test["PassengerId"],
        "Survived": pipe.predict(test[FEATURES]).astype(int),
    })
    sub.to_csv(path, index=False)
    return sub
