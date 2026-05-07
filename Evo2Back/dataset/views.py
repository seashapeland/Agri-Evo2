from django.http import JsonResponse, Http404, HttpResponse, FileResponse
from .models import Dataset, GenomeFile
from .services import sync_genome_data
from .utils.utils import read_fasta_first_record, open_genome_file
from pathlib import Path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def dataset_list(request):
    """
    GET /api/datasets/
    """
    # sync_genome_data()

    data = []

    for ds in Dataset.objects.prefetch_related("files").all():
        data.append({
            "id": ds.id,
            "species": ds.species,
            "version": ds.version,
            "folder": ds.folder_name,
            "files": [
                {
                    "id": f.id,
                    "name": f.name,
                    "type": f.file_type,
                    "size": f.file_size,
                    "updated": f.updated_at.strftime("%Y-%m-%d"),
                    "recordCount": f.record_count,
                    "avgLength": f.avg_length,
                }
                for f in ds.files.all()
            ],
            "fileCount": ds.files.count(),
        })

    return JsonResponse(data, safe=False)


@csrf_exempt
def dataset_update(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    sync_genome_data()
    return JsonResponse({"status": "success"})


def file_preview(request, file_id):
    """
    GET /api/files/<id>/preview/
    """
    try:
        gf = GenomeFile.objects.get(id=file_id)
    except GenomeFile.DoesNotExist:
        raise Http404("File not found")

    file_path = Path(settings.GENOME_DATA_ROOT) / gf.file_path
    if not file_path.exists():
        raise Http404("File missing on disk")

    # 只允许 FASTA / PEP / CDS / cDNA
    if gf.file_type == "GFF3":
        return JsonResponse({
            "error": "GFF3 does not support FASTA preview"
        }, status=400)

    data = read_fasta_first_record(file_path)

    return JsonResponse({
        "id": gf.id,
        "name": gf.name,
        "type": gf.file_type,
        "preview": data
    })


def file_download(request, file_id):
    """
    GET /api/files/<id>/download/
    """
    try:
        gf = GenomeFile.objects.get(id=file_id)
    except GenomeFile.DoesNotExist:
        raise Http404("File not found")

    file_path = Path(settings.GENOME_DATA_ROOT) / gf.file_path
    if not file_path.exists():
        raise Http404("File missing")

    response = FileResponse(
        open(file_path, "rb"),
        as_attachment=True,
        filename=gf.name
    )
    return response
