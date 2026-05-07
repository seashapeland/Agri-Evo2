# dataset/utils.py
import gzip
from pathlib import Path

def open_genome_file(path: Path):
    """
    自动识别 .gz / 普通文本
    """
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="ignore")
    return open(path, "r", encoding="utf-8", errors="ignore")


# dataset/utils.py
def read_fasta_first_record(path: Path, max_lines=10_000):
    """
    只读取 FASTA 第一条序列
    - 不加载整个文件
    - 支持超大文件
    """
    header = None
    seq_lines = []

    with open_genome_file(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is None:
                    header = line[1:]
                else:
                    break  # 第二条记录，结束
            else:
                if header is not None:
                    seq_lines.append(line)

            if len(seq_lines) >= max_lines:
                break

    return {
        "header": header,
        "sequence": "".join(seq_lines)
    }


