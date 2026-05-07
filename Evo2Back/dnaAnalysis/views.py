import json
import os
from urllib import error, request as urllib_request

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


ANALYSIS_BASE_URL = os.getenv("EVO2_ANALYSIS_BASE_URL", "http://localhost:18002").rstrip("/")
COMPARE_ENDPOINT = f"{ANALYSIS_BASE_URL}/compare"
LIKELIHOOD_ENDPOINT = f"{ANALYSIS_BASE_URL}/likelihood"
REQUEST_TIMEOUT_SECONDS = int(os.getenv("EVO2_ANALYSIS_TIMEOUT_SECONDS", "120"))


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

@csrf_exempt
def compare(request):
    if request.method != "POST":
        return _json_response({"detail": "Method not allowed. Use POST."}, status=405)

    data, err = _read_json_body(request)
    if err:
        return err

    reference = data.get("reference")
    generated = data.get("generated")
    if not reference or not generated:
        return _json_response({"detail": "Fields 'reference' and 'generated' are required."}, status=400)

    try:
        result = _http_post_json(COMPARE_ENDPOINT, {"reference": reference, "generated": generated})
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return _json_response({"detail": "DNA analysis request failed.", "error": detail}, status=502)
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _json_response({"detail": "DNA analysis request failed.", "error": str(exc)}, status=502)

    return _json_response(result)


@csrf_exempt
def likelihood(request):
    if request.method != "POST":
        return _json_response({"detail": "Method not allowed. Use POST."}, status=405)

    data, err = _read_json_body(request)
    if err:
        return err

    sequence = data.get("sequence") or data.get("prompt")
    if not sequence:
        return _json_response({"detail": "Field 'sequence' is required."}, status=400)

    payload = {
        "model": data.get("model", "evo2_1b"),
        "sequence": sequence,
    }
    if data.get("model_size") is not None:
        payload["model_size"] = data.get("model_size")
    if data.get("timeout_seconds") is not None:
        payload["timeout_seconds"] = data.get("timeout_seconds")

    try:
        result = _http_post_json(LIKELIHOOD_ENDPOINT, payload)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return _json_response({"detail": "DNA likelihood request failed.", "error": detail}, status=502)
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return _json_response({"detail": "DNA likelihood request failed.", "error": str(exc)}, status=502)

    return _json_response(result)
