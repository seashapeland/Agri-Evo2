import gzip
from pathlib import Path

def compute_fasta_stats(file_path: Path):
    """
    统计 FASTA 文件中的：
    - record_count
    - avg_length

    支持 .fa / .fa.gz
    """
    record_count = 0
    total_length = 0
    current_seq_len = 0

    # 自动判断是否 gzip
    open_func = gzip.open if file_path.suffix == ".gz" else open

    with open_func(file_path, "rt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if current_seq_len > 0:
                    total_length += current_seq_len
                    current_seq_len = 0
                record_count += 1
            else:
                current_seq_len += len(line)

        # 最后一条序列
        if current_seq_len > 0:
            total_length += current_seq_len

    if record_count == 0:
        return 0, 0

    avg_length = total_length // record_count
    return record_count, avg_length
