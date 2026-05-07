import re
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from .models import Dataset, GenomeFile
from .utils.fasta_stats import compute_fasta_stats

FA_PATTERN = re.compile(
    r"""
    (?P<species>[^.]+)
    \.
    (?P<version>[A-Za-z0-9._-]+)
    \.
    (?P<seqtype>cds|cdna|pep|ncrna|gff3)
    (\.all)?
    \.
    fa(sta)?(\.gz)?
    $
    """,
    re.IGNORECASE | re.VERBOSE
)


SEQTYPE_MAP = {
    "cds": "CDS",
    "cdna": "cDNA",
    "pep": "PEP",
    "ncrna": "ncRNA",
    "gff3": "GFF3",
}

def sync_genome_data():
    root = Path(settings.GENOME_DATA_ROOT)

    for species_dir in root.iterdir():
        if not species_dir.is_dir():
            continue

        folder_name = species_dir.name
        species_name = folder_name.replace("_", " ")

        for file_path in species_dir.iterdir():
            if not file_path.is_file():
                continue

            match = FA_PATTERN.match(file_path.name)
            if not match:
                continue

            version = match.group("version")
            seqtype_raw = match.group("seqtype").lower()
            file_type = SEQTYPE_MAP.get(seqtype_raw)
            if not file_type:
                continue

            dataset, _ = Dataset.objects.get_or_create(
                species=species_name,
                version=version,
                folder_name=folder_name,
            )

            stat = file_path.stat()
            relative_path = file_path.relative_to(root).as_posix()

            record_count = None
            avg_length = None

            # 只对 FASTA 类文件做统计
            if file_type in {"CDS", "cDNA", "PEP", "ncRNA"}:
                record_count, avg_length = compute_fasta_stats(file_path)

            GenomeFile.objects.update_or_create(
                dataset=dataset,
                name=file_path.name,
                defaults={
                    "file_type": file_type,
                    "file_path": relative_path,
                    "file_size": stat.st_size,
                    "updated_at": timezone.datetime.fromtimestamp(
                        stat.st_mtime
                    ).date(),
                    "record_count": record_count,
                    "avg_length": avg_length,
                },
            )

