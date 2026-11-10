import sys
from pathlib import Path

# 让 tests/ 下的用例能直接 `import backend.*`（pytest 从项目根目录运行）
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest


class CheckItem:
    """轻量替身：真实 CheckItemResult 是 Pydantic 模型，这里只需要三个属性。"""

    def __init__(self, item_text: str, confirmed_text: str | None = None, matched_text: str | None = None):
        self.item_text = item_text
        self.confirmed_text = confirmed_text
        self.matched_text = matched_text


@pytest.fixture
def make_item():
    def _make(item_text: str, confirmed_text: str | None = None, matched_text: str | None = None) -> CheckItem:
        return CheckItem(item_text, confirmed_text, matched_text)

    return _make
