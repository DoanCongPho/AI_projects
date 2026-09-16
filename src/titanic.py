"""Nạp và xử lý đặc trưng cho bộ dữ liệu Titanic của Kaggle.

Notebook chỉ nên gọi `load()` rồi `add_features()`, không lặp lại logic ở cell.
"""

from __future__ import annotations

import os

import pandas as pd

# Kaggle từng đặt dữ liệu competition ở nhiều vị trí khác nhau, nên dò thay vì
# hard-code một đường dẫn rồi chết khi Kaggle đổi.
_CANDIDATES = (
    "/kaggle/input/competitions/titanic",
    "/kaggle/input/titanic",
)


def find_data_dir(explicit: str | None = None) -> str:
    """Trả về thư mục chứa train.csv. Ưu tiên `explicit` nếu được truyền vào."""
    if explicit:
        return explicit
    for path in _CANDIDATES:
        if os.path.exists(os.path.join(path, "train.csv")):
            return path
    # Dò rộng hơn: quét /kaggle/input tìm train.csv ở bất kỳ độ sâu nào.
    for root, _, files in os.walk("/kaggle/input"):
        if "train.csv" in files:
            return root
    raise FileNotFoundError(
        "Không tìm thấy train.csv. Kiểm tra dataset đã được Add Input vào notebook chưa."
    )


def load(data_dir: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Đọc train.csv và test.csv."""
    d = find_data_dir(data_dir)
    return (
        pd.read_csv(os.path.join(d, "train.csv")),
        pd.read_csv(os.path.join(d, "test.csv")),
    )


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Sinh đặc trưng, trả về bản sao. Không sửa `df` gốc."""
    out = df.copy()

    # Danh xưng trong Name mang thông tin tuổi và giới rõ hơn chính cột Age,
    # vốn thiếu tới 177/891 giá trị.
    out["Title"] = out["Name"].str.extract(r",\s*([^\.]+)\.", expand=False).str.strip()
    rare = ~out["Title"].isin(["Mr", "Mrs", "Miss", "Master"])
    out.loc[rare, "Title"] = "Rare"

    # Điền Age theo trung vị của từng Title thay vì trung vị toàn bộ: trẻ em
    # (Master) và phụ nữ có phân bố tuổi rất khác nhau.
    out["Age"] = out.groupby("Title")["Age"].transform(lambda s: s.fillna(s.median()))
    out["Age"] = out["Age"].fillna(out["Age"].median())  # phòng khi cả nhóm đều rỗng

    out["Fare"] = out["Fare"].fillna(out["Fare"].median())
    out["Embarked"] = out["Embarked"].fillna(out["Embarked"].mode()[0])

    out["FamilySize"] = out["SibSp"] + out["Parch"] + 1
    out["IsAlone"] = (out["FamilySize"] == 1).astype(int)

    # Cabin thiếu 687/891 nên không dùng làm giá trị; chỉ giữ tín hiệu có/không,
    # vì bản thân việc được ghi số cabin đã tương quan với hạng vé.
    out["HasCabin"] = out["Cabin"].notna().astype(int)

    return out


FEATURES = [
    "Pclass", "Sex", "Age", "Fare", "Embarked",
    "Title", "FamilySize", "IsAlone", "HasCabin",
]
CATEGORICAL = ["Sex", "Embarked", "Title"]
NUMERIC = [c for c in FEATURES if c not in CATEGORICAL]
