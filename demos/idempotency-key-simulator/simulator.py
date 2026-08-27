from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Receipt:
    idempotency_key: str
    result: str


class Executor:
    def __init__(self) -> None:
        self._receipts: Dict[str, Receipt] = {}

    def execute(self, idempotency_key: str, payload: str) -> Receipt:
        existing = self._receipts.get(idempotency_key)
        if existing:
            print(f"REPLAY  key={idempotency_key} -> returning original receipt")
            return existing

        print(f"EXECUTE key={idempotency_key} payload={payload}")
        receipt = Receipt(idempotency_key=idempotency_key, result=f"done:{payload}")
        self._receipts[idempotency_key] = receipt
        return receipt


if __name__ == "__main__":
    executor = Executor()
    key = "job-42:send-summary"

    first = executor.execute(key, "summary-v1")
    second = executor.execute(key, "summary-v1")
    third = executor.execute(key, "summary-v1")

    assert first == second == third
    print("PASS: duplicate retries did not repeat the side effect")
