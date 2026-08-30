import socket
import tempfile
import unittest
from pathlib import Path

from user_bus_doctor import _is_unix_socket, _unix_bus_path, build_report, diagnose_env


class UserBusDoctorTests(unittest.TestCase):
    def test_missing_required_environment_is_error(self):
        checks = diagnose_env({}, exists=lambda _: False)
        self.assertEqual([c["status"] for c in checks], ["error", "error"])

    def test_valid_runtime_and_bus_socket_are_healthy(self):
        env = {
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
        }
        existing = {"/run/user/1000", "/run/user/1000/bus"}
        report = build_report(env, exists=lambda p: p in existing, is_socket=lambda p: p.endswith("/bus"))
        self.assertTrue(report["healthy"])
        self.assertEqual(report["summary"]["errors"], 0)

    def test_missing_bus_socket_is_error(self):
        env = {
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
        }
        report = build_report(env, exists=lambda p: p == "/run/user/1000")
        self.assertFalse(report["healthy"])
        self.assertIn("socket path missing", report["checks"][1]["detail"])

    def test_failed_manager_probe_marks_report_unhealthy(self):
        env = {
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "DBUS_SESSION_BUS_ADDRESS": "unix:abstract=/tmp/dbus-demo",
        }
        probe = {"status": "error", "detail": "Failed to connect to bus", "environment": {}}
        report = build_report(env, probe=probe, exists=lambda _: True)
        self.assertFalse(report["healthy"])
        self.assertEqual(report["checks"][-1]["check"], "systemd_user_manager")

    def test_existing_non_socket_bus_path_is_error(self):
        env = {
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus",
        }
        existing = {"/run/user/1000", "/run/user/1000/bus"}
        report = build_report(env, exists=lambda p: p in existing, is_socket=lambda _: False)
        self.assertFalse(report["healthy"])
        self.assertIn("not a unix socket", report["checks"][1]["detail"])

    def test_real_unix_socket_type_probe(self):
        root = Path(tempfile.mkdtemp())
        regular = root / "regular"
        regular.write_text("x")
        sock_path = root / "bus"
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.bind(str(sock_path))
            self.assertTrue(_is_unix_socket(str(sock_path)))
            self.assertFalse(_is_unix_socket(str(regular)))
        finally:
            sock.close()

    def test_extracts_unix_path(self):
        self.assertEqual(
            _unix_bus_path("unix:path=/run/user/1000/bus,guid=abc"),
            "/run/user/1000/bus",
        )
        self.assertIsNone(_unix_bus_path("tcp:host=127.0.0.1"))


if __name__ == "__main__":
    unittest.main()
