import json
import os
import time
from urllib import error, request as urllib_request

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


INFERENCE_BASE_URL = os.getenv("EVO2_INFERENCE_BASE_URL", "http://localhost:18002").rstrip("/")
GENERATE_ENDPOINT = f"{INFERENCE_BASE_URL}/generate"
RESULT_ENDPOINT_TEMPLATE = f"{INFERENCE_BASE_URL}/result/{{job_id}}"
MODELS_ENDPOINT = f"{INFERENCE_BASE_URL}/models"
REQUEST_TIMEOUT_SECONDS = 60
POLL_INTERVAL_SECONDS = float(os.getenv("EVO2_POLL_INTERVAL_SECONDS", "1.0"))
POLL_TIMEOUT_SECONDS = int(os.getenv("EVO2_POLL_TIMEOUT_SECONDS", "600"))


def _json_response(payload, status=200):
    return JsonResponse(payload, status=status, json_dumps_params={"ensure_ascii": False})


def _read_json_body(request):
    try:
        body = request.body.decode("utf-8") if request.body else "{}"
        data = json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, _json_response({"detail": "Request body must be valid JSON."}, status=400)

    if not isinstance(data, dict):
        return None, _json_response({"detail": "Request JSON must be an object."}, status=400)
    return data, None


def _http_post_json(url, payload):
    req = urllib_request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib_request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8") or "{}"
        return json.loads(raw)


def _http_get_json(url):
    req = urllib_request.Request(
        url=url,
        headers={"Accept": "application/json"},
        method="GET",
    )
    with urllib_request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8") or "{}"
        return json.loads(raw)


def _proxy_inference_and_wait(inference_payload):
    try:
        submit_data = _http_post_json(GENERATE_ENDPOINT, inference_payload)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return _json_response({"detail": "Inference submit failed.", "error": detail}, status=502)
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _json_response({"detail": "Inference submit failed.", "error": str(exc)}, status=502)

    job_id = submit_data.get("job_id")
    if not job_id:
        return _json_response(
            {"detail": "Inference service did not return job_id.", "response": submit_data},
            status=502,
        )

    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    result_url = RESULT_ENDPOINT_TEMPLATE.format(job_id=job_id)

    while time.monotonic() < deadline:
        try:
            task_data = _http_get_json(result_url)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            return _json_response({"detail": "Inference polling failed.", "error": detail}, status=502)
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return _json_response({"detail": "Inference polling failed.", "error": str(exc)}, status=502)

        status_value = task_data.get("status")
        if status_value == "finished":
            return _json_response(
                {
                    "status": "finished",
                    "job_id": job_id,
                    "result": task_data.get("result"),
                }
            )
        if status_value == "failed":
            return _json_response(
                {
                    "status": "failed",
                    "job_id": job_id,
                    "error": task_data.get("error", "Inference task failed."),
                },
                status=500,
            )

        time.sleep(POLL_INTERVAL_SECONDS)

    return _json_response(
        {
            "status": "timeout",
            "job_id": job_id,
            "detail": f"Inference polling timed out after {POLL_TIMEOUT_SECONDS} seconds.",
        },
        status=504,
    )


def models(request):
    if request.method != "GET":
        return _json_response({"detail": "Method not allowed. Use GET."}, status=405)

    try:
        data = _http_get_json(MODELS_ENDPOINT)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return _json_response({"detail": "Fetch models failed.", "error": detail}, status=502)
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _json_response({"detail": "Fetch models failed.", "error": str(exc)}, status=502)

    return _json_response(data)


@csrf_exempt
def cds_completion(request):
    if request.method != "POST":
        return _json_response({"detail": "Method not allowed. Use POST."}, status=405)

    data, err = _read_json_body(request)
    if err:
        return err

    prompt = data.get("prompt") or data.get("sequence")
    if not prompt:
        return _json_response({"detail": "Field 'prompt' is required."}, status=400)

    inference_payload = {
        "model": data.get("model", "evo2-1b"),
        "prompt": prompt,
        "tokens": data.get("tokens", 200),
        "temperature": data.get("temperature", 1.0),
        "topk": data.get("topk", data.get("topK", 40)),
    }

    return _proxy_inference_and_wait(inference_payload)


@csrf_exempt
def promoter_extension(request):
    return _json_response({"detail": "promoter-extension endpoint is not implemented yet."}, status=501)


@csrf_exempt
def intron_generation(request):
    return _json_response({"detail": "intron-generation endpoint is not implemented yet."}, status=501)
