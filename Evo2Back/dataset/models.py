from django.db import models

class Dataset(models.Model):
    """
    基因数据集（一个物种 + 一个版本）
    对应 genome_data 下的一个文件夹
    """
    species = models.CharField(
        max_length=100,
        help_text="物种学名，例如 Oryza sativa"
    )

    version = models.CharField(
        max_length=50,
        help_text="注释版本，例如 IRGSP-1.0 / TAIR10"
    )

    folder_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="文件夹名，例如 Oryza_sativa"
    )

    description = models.TextField(
        blank=True,
        help_text="可选说明信息"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('species', 'version')
        ordering = ['species']

    def __str__(self):
        return f"{self.species} ({self.version})"


class GenomeFile(models.Model):
    """
    基因文件（FASTA / GFF3）
    """
    FILE_TYPE_CHOICES = [
        ('CDS', 'CDS'),
        ('cDNA', 'cDNA'),
        ('PEP', 'Protein'),
        ('ncRNA', 'ncRNA'),
        ('GFF3', 'GFF3'),
    ]

    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        related_name='files'
    )

    name = models.CharField(
        max_length=200,
        help_text="文件名"
    )

    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPE_CHOICES
    )

    file_path = models.CharField(
        max_length=300,
        help_text="相对 GENOME_DATA_ROOT 的路径"
    )

    file_size = models.BigIntegerField(
        help_text="文件大小（字节）"
    )

    updated_at = models.DateField(
        help_text="文件最后更新时间"
    )

    record_count = models.IntegerField(
        null=True,
        blank=True,
        help_text="FASTA 条目数量（可选）"
    )

    avg_length = models.IntegerField(
        null=True,
        blank=True,
        help_text="平均序列长度（可选）"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_type']

    def __str__(self):
        return f"{self.name} [{self.file_type}]"
