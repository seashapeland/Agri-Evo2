import tempfile
from pathlib import Path

from django.test import TestCase, override_settings
from django.utils import timezone

from dataset.models import Dataset, GenomeFile
from dataset.services import sync_genome_data


class SyncGenomeDataTestCase(TestCase):
    def setUp(self):
        """
        每个 test 之前都会执行
        """
        # 创建一个临时目录，模拟 GENOME_DATA_ROOT
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        # 构造一个物种目录
        self.species_dir = self.root / "oryza_sativa"
        self.species_dir.mkdir()

        # 构造一个合法的 FA 文件
        self.fa_file = self.species_dir / "oryza_sativa.v1.cds.fa"
        self.fa_file.write_text(
            ">gene1\nATGC\n>gene2\nATGC\n"
        )

        # 构造一个非法文件（应被忽略）
        self.bad_file = self.species_dir / "README.txt"
        self.bad_file.write_text("ignore me")

    def tearDown(self):
        """
        每个 test 之后执行
        """
        self.temp_dir.cleanup()

    @override_settings(GENOME_DATA_ROOT=None)
    def test_sync_genome_data_creates_dataset_and_genomefile(self):
        """
        测试：合法 FA 文件是否被正确导入
        """
        with override_settings(GENOME_DATA_ROOT=self.root):
            sync_genome_data()

        # Dataset 是否创建
        self.assertEqual(Dataset.objects.count(), 1)

        dataset = Dataset.objects.first()
        self.assertEqual(dataset.species, "oryza sativa")
        self.assertEqual(dataset.version, "v1")
        self.assertEqual(dataset.folder_name, "oryza_sativa")

        # GenomeFile 是否创建
        self.assertEqual(GenomeFile.objects.count(), 1)

        genome_file = GenomeFile.objects.first()
        self.assertEqual(genome_file.name, "oryza_sativa.v1.cds.fa")
        self.assertEqual(genome_file.file_type, "CDS")
        self.assertIsNotNone(genome_file.record_count)
        self.assertIsNotNone(genome_file.avg_length)

    @override_settings(GENOME_DATA_ROOT=None)
    def test_sync_genome_data_ignores_invalid_files(self):
        """
        测试：非法文件不会生成 GenomeFile
        """
        with override_settings(GENOME_DATA_ROOT=self.root):
            sync_genome_data()

        # README.txt 不应被导入
        self.assertEqual(GenomeFile.objects.count(), 1)

