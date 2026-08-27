from dataclasses import dataclass


@dataclass
class Job:
    job_id: str
    owner: str | None = None
    lease_until: int = 0
    state: str = "queued"

    def claim(self, worker: str, now: int, lease_seconds: int = 5) -> bool:
        if self.owner is not None and now < self.lease_until:
            return False
        self.owner = worker
        self.lease_until = now + lease_seconds
        self.state = "running"
        print(f"CLAIM job={self.job_id} worker={worker} lease_until={self.lease_until}")
        return True

    def complete(self, worker: str, now: int) -> bool:
        if worker != self.owner or now > self.lease_until:
            return False
        self.state = "completed"
        print(f"COMPLETE job={self.job_id} worker={worker}")
        return True


if __name__ == "__main__":
    job = Job("job-7")

    assert job.claim("worker-a", now=0)
    assert not job.claim("worker-b", now=3)

    # worker-a disappears; after the lease expires worker-b can recover the job
    assert job.claim("worker-b", now=6)
    assert job.owner == "worker-b"
    assert job.complete("worker-b", now=8)
    assert job.state == "completed"

    print("PASS: stale ownership was recovered without concurrent ownership")
