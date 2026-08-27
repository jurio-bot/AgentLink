from dataclasses import dataclass
from enum import Enum


class ReceiptState(str, Enum):
    NOT_STARTED = "not_started"
    COMPLETED = "completed"
    UNCERTAIN = "uncertain"


class RecoveryDecision(str, Enum):
    RETRY = "retry"
    SKIP_ALREADY_COMPLETED = "skip_already_completed"
    RECONCILE_MANUALLY = "reconcile_manually"


@dataclass(frozen=True)
class ActionReceipt:
    action_id: str
    state: ReceiptState


def decide_recovery(receipt: ActionReceipt) -> RecoveryDecision:
    if receipt.state is ReceiptState.COMPLETED:
        return RecoveryDecision.SKIP_ALREADY_COMPLETED

    if receipt.state is ReceiptState.NOT_STARTED:
        return RecoveryDecision.RETRY

    return RecoveryDecision.RECONCILE_MANUALLY


def main() -> None:
    examples = [
        ActionReceipt("send-summary", ReceiptState.COMPLETED),
        ActionReceipt("write-report", ReceiptState.NOT_STARTED),
        ActionReceipt("external-update", ReceiptState.UNCERTAIN),
    ]

    print("AgentLink receipt replay simulator\n")

    for receipt in examples:
        decision = decide_recovery(receipt)
        print(
            f"action={receipt.action_id:<16} "
            f"receipt={receipt.state.value:<12} "
            f"decision={decision.value}"
        )


if __name__ == "__main__":
    main()
