"""Tiện ích dùng trong notebook Kaggle để nạp lại code vừa `git pull` về.

Python cache module sau lần import đầu tiên, nên `git pull` xong mà không
reload thì notebook vẫn chạy code cũ. Gọi `reload_src()` sau mỗi lần pull.
"""

import importlib
import sys


def reload_src(package: str = "src") -> list[str]:
    """Nạp lại `package` và toàn bộ module con đã import. Trả về tên đã reload."""
    # Sau `git pull` có thể có file module mới; xóa cache của import system
    # để Python nhìn thấy chúng thay vì dùng danh sách thư mục đã cache.
    importlib.invalidate_caches()

    targets = [name for name in sys.modules if name == package or name.startswith(package + ".")]
    # Reload module con trước, package cha sau, để cha thấy bản mới của con.
    targets.sort(key=lambda name: name.count("."), reverse=True)
    for name in targets:
        importlib.reload(sys.modules[name])
    return targets
