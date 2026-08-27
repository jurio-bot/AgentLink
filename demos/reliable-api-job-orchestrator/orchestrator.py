from dataclasses import dataclass, asdict
from typing import Dict, Optional
import hashlib, json, time

@dataclass
class Job:
    job_id: str
    payload: dict
    status: str = 'queued'
    owner: Optional[str] = None
    lease_until: float = 0.0
    result: Optional[dict] = None
    receipt: Optional[str] = None

class ReliableJobOrchestrator:
    def __init__(self, now=time.time):
        self._jobs: Dict[str, Job] = {}
        self._idem: Dict[str, str] = {}
        self._now = now

    @staticmethod
    def _job_id(idempotency_key: str) -> str:
        return 'job_' + hashlib.sha256(idempotency_key.encode()).hexdigest()[:16]

    def submit(self, payload: dict, idempotency_key: str) -> dict:
        if idempotency_key in self._idem:
            return self.get(self._idem[idempotency_key])
        jid = self._job_id(idempotency_key)
        self._jobs[jid] = Job(job_id=jid, payload=payload)
        self._idem[idempotency_key] = jid
        return self.get(jid)

    def claim(self, job_id: str, worker: str, lease_seconds: int = 30) -> dict:
        job = self._jobs[job_id]
        now = self._now()
        if job.status == 'completed':
            return self.get(job_id)
        if job.owner and job.lease_until > now and job.owner != worker:
            raise RuntimeError('job_already_leased')
        job.owner = worker
        job.lease_until = now + lease_seconds
        job.status = 'running'
        return self.get(job_id)

    def complete(self, job_id: str, worker: str, result: dict) -> dict:
        job = self._jobs[job_id]
        if job.status == 'completed':
            return self.get(job_id)
        if job.owner != worker or job.lease_until <= self._now():
            raise RuntimeError('invalid_or_expired_lease')
        job.result = result
        job.status = 'completed'
        job.receipt = hashlib.sha256(json.dumps({
            'job_id': job.job_id, 'result': result
        }, sort_keys=True).encode()).hexdigest()
        return self.get(job_id)

    def get(self, job_id: str) -> dict:
        return asdict(self._jobs[job_id])
