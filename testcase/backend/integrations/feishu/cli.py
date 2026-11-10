import argparse
import sys
from pathlib import Path

from backend.integrations.feishu.service import FeishuConfigError, feishu_url_to_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="将飞书文档/知识库链接解析为 Markdown")
    parser.add_argument("url", help="飞书文档或知识库 URL")
    parser.add_argument("-o", "--output", help="输出 Markdown 文件路径", default=None)
    args = parser.parse_args()

    try:
        markdown = feishu_url_to_markdown(args.url)
    except FeishuConfigError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print("已写入:", output_path)
        return

    print(markdown)


if __name__ == "__main__":
    main()
