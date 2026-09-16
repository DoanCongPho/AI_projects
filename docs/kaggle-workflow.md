# Quy trình: code ở local, chạy trên Kaggle

Mục tiêu: sửa code ở máy rồi `git push`, notebook Kaggle `git pull` là có bản mới.
Không phải upload tay. Dataset vẫn nằm nguyên trên Kaggle, không tải về.

Repo: https://github.com/DoanCongPho/AI_projects

## Nguyên tắc

Logic nặng đặt trong `src/*.py`, không viết thẳng vào cell.
Notebook chỉ còn việc: pull code, gọi hàm, vẽ biểu đồ, khám phá dữ liệu.

Lý do: cell notebook không diff được tử tế và không tái sử dụng được.
File `.py` thì tôi sửa ở local dễ, bạn review trên GitHub cũng dễ.

## Thiết lập một lần trên Kaggle

1. Mở notebook, vào **Settings** ở cột phải
2. Bật **Internet** (bắt buộc, không có thì `git clone` chết)
3. Dán cell dưới vào đầu notebook

```python
REPO = "https://github.com/DoanCongPho/AI_projects.git"
CODE = "/kaggle/working/code"

import os, sys, subprocess

if not os.path.exists(CODE):
    subprocess.run(["git", "clone", "--depth", "1", REPO, CODE], check=True)
else:
    subprocess.run(["git", "-C", CODE, "pull", "--ff-only"], check=True)

if CODE not in sys.path:
    sys.path.insert(0, CODE)
```

`--depth 1` chỉ lấy commit mới nhất, clone nhanh hơn nhiều so với lấy cả lịch sử.

## Mỗi lần tôi sửa code

Chạy lại cell trên để pull, rồi nạp lại module:

```python
from src.bootstrap import reload_src
reload_src()
```

Bỏ qua bước `reload_src()` là notebook chạy code cũ mà không báo lỗi gì.
Đây là lỗi hay gặp nhất khi làm theo cách này.

## Đọc dữ liệu

Dataset Kaggle luôn nằm ở `/kaggle/input/<tên-dataset>/`, chỉ đọc, không ghi được.
Muốn ghi thì ghi vào `/kaggle/working/`.

```python
import os
for root, dirs, files in os.walk("/kaggle/input"):
    print(root, files[:5])
```

## Nếu repo là private

Đừng viết token thẳng vào notebook, vì notebook public là lộ.
Dùng **Add-ons → Secrets**, tạo secret tên `GITHUB_TOKEN`, rồi:

```python
from kaggle_secrets import UserSecretsClient

token = UserSecretsClient().get_secret("GITHUB_TOKEN")
REPO = f"https://{token}@github.com/DoanCongPho/AI_projects.git"
```

## Giới hạn cần biết

- Sửa code trên web Kaggle sẽ **không** quay về GitHub. Nguồn duy nhất là repo.
  Muốn lưu ngược lại thì dùng File → Link to GitHub, nhưng đừng trộn hai chiều.
- Kaggle chỉ chạy cả notebook từ đầu khi Save Version. Chạy interactive thì
  vẫn phải tự bấm từng cell như bình thường.
