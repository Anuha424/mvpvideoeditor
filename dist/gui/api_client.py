"""
HTTP Client for Go Video Editor Engine with QThread support.
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from PySide6.QtCore import QThread, Signal


@dataclass
class JobStatus:
    """Represents the status of a rendering job."""
    job_id: str
    status: str
    progress: float
    type: str
    output: str
    error: Optional[str] = None


class EngineClient:
    """HTTP client for the Go Video Editor Engine REST API."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._timeout = 10

    def health_check(self) -> Dict[str, Any]:
        """Check if the engine is running."""
        try:
            r = self.session.get(f"{self.base_url}/api/health", timeout=5)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "error": "cannot connect"}
        except requests.exceptions.Timeout:
            return {"status": "timeout", "error": "connection timed out"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def trim_video(
        self,
        input_path: str,
        start_time: float,
        end_time: float,
        output_path: str = ""
    ) -> Dict[str, Any]:
        """Submit a trim job."""
        payload: Dict[str, Any] = {
            "inputPath": input_path,
            "startTime": start_time,
            "endTime": end_time,
        }
        if output_path:
            payload["outputPath"] = output_path
        return self._post("/api/trim", payload)

    def merge_videos(
        self,
        input_paths: List[str],
        output_path: str = ""
    ) -> Dict[str, Any]:
        """Submit a merge job."""
        payload: Dict[str, Any] = {"inputPaths": input_paths}
        if output_path:
            payload["outputPath"] = output_path
        return self._post("/api/merge", payload)

    def blur_watermark(
        self,
        input_path: str,
        x: int,
        y: int,
        w: int,
        h: int,
        blur_strength: int = 10,
        output_path: str = ""
    ) -> Dict[str, Any]:
        """Submit a watermark blur job."""
        payload: Dict[str, Any] = {
            "inputPath": input_path,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "blurStrength": blur_strength,
        }
        if output_path:
            payload["outputPath"] = output_path
        return self._post("/api/watermark-blur", payload)

    def get_job_status(self, job_id: str) -> JobStatus:
        """Get job status."""
        try:
            r = self.session.get(f"{self.base_url}/api/status/{job_id}", timeout=5)
            r.raise_for_status()
            d = r.json()
            return JobStatus(
                job_id=d.get("job_id", job_id),
                status=d.get("status", "unknown"),
                progress=float(d.get("progress", 0)),
                type=d.get("type", ""),
                output=d.get("output", ""),
                error=d.get("error"),
            )
        except Exception as e:
            return JobStatus(
                job_id=job_id,
                status="error",
                progress=0,
                type="",
                output="",
                error=str(e),
            )

    def is_connected(self) -> bool:
        """Check if engine is reachable."""
        return self.health_check().get("status") == "running"

    def _post(self, endpoint: str, payload: Dict) -> Dict:
        """POST request with error handling."""
        try:
            r = self.session.post(
                f"{self.base_url}{endpoint}",
                json=payload,
                timeout=self._timeout,
            )
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ConnectionError:
            return {"error": "cannot connect to engine"}
        except requests.exceptions.HTTPError as e:
            try:
                return e.response.json()
            except Exception:
                return {"error": f"HTTP {e.response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


# ─── QThread Classes for Non-blocking Operations ─────────────────────────────

class HealthCheckThread(QThread):
    """Background thread for health checks."""
    finished = Signal(dict)

    def __init__(self, client: EngineClient):
        super().__init__()
        self.client = client

    def run(self):
        result = self.client.health_check()
        self.finished.emit(result)


class SubmitJobThread(QThread):
    """Background thread for submitting jobs."""
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, client: EngineClient, endpoint: str, payload: Dict):
        super().__init__()
        self.client = client
        self.endpoint = endpoint
        self.payload = payload

    def run(self):
        try:
            result = self.client._post(self.endpoint, self.payload)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class PollJobThread(QThread):
    """Background thread for polling job status."""
    finished = Signal(object)  # JobStatus

    def __init__(self, client: EngineClient, job_id: str):
        super().__init__()
        self.client = client
        self.job_id = job_id

    def run(self):
        status = self.client.get_job_status(self.job_id)
        self.finished.emit(status)
