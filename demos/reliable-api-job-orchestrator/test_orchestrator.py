import unittest
from orchestrator import ReliableJobOrchestrator

class Clock:
    def __init__(self): self.t = 1000.0
    def now(self): return self.t
    def advance(self, seconds): self.t += seconds

class Tests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.o = ReliableJobOrchestrator(now=self.clock.now)

    def test_idempotent_submit_returns_same_job(self):
        a = self.o.submit({'task':'x'}, 'key-1')
        b = self.o.submit({'task':'x'}, 'key-1')
        self.assertEqual(a['job_id'], b['job_id'])

    def test_active_lease_blocks_second_worker(self):
        j = self.o.submit({}, 'k')['job_id']
        self.o.claim(j, 'w1', 10)
        with self.assertRaises(RuntimeError): self.o.claim(j, 'w2', 10)

    def test_expired_lease_allows_recovery(self):
        j = self.o.submit({}, 'k')['job_id']
        self.o.claim(j, 'w1', 10)
        self.clock.advance(11)
        state = self.o.claim(j, 'w2', 10)
        self.assertEqual(state['owner'], 'w2')

    def test_completion_requires_valid_lease(self):
        j = self.o.submit({}, 'k')['job_id']
        self.o.claim(j, 'w1', 10)
        with self.assertRaises(RuntimeError): self.o.complete(j, 'w2', {'ok':True})

    def test_completion_receipt_is_stable(self):
        j = self.o.submit({}, 'k')['job_id']
        self.o.claim(j, 'w1', 10)
        a = self.o.complete(j, 'w1', {'ok':True})
        b = self.o.complete(j, 'w1', {'ok':True})
        self.assertEqual(a['receipt'], b['receipt'])
        self.assertEqual(a['status'], 'completed')

if __name__ == '__main__': unittest.main()
