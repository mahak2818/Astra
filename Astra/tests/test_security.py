"""
Unit tests for Security Gate enforcement of Level 0, 1, and 2 clearances.
"""

import unittest
from astra.security.gate import SecurityGate
from astra.models.schemas import SecurityLevel, Task


class TestSecurity(unittest.TestCase):
    def test_security_level_0_1_auto_approved(self):
        gate = SecurityGate()

        task_lvl0 = Task(capability_name="browser", action_name="open", security_level=SecurityLevel.LEVEL_0)
        self.assertTrue(gate.check_clearance(task_lvl0))

        task_lvl1 = Task(capability_name="files", action_name="write_file", security_level=SecurityLevel.LEVEL_1)
        self.assertTrue(gate.check_clearance(task_lvl1))

    def test_security_level_2_requires_confirmation(self):
        # Without callback -> rejected
        gate_no_cb = SecurityGate()
        task_lvl2 = Task(capability_name="git", action_name="push", security_level=SecurityLevel.LEVEL_2)
        self.assertFalse(gate_no_cb.check_clearance(task_lvl2))

        # With callback approving -> approved
        gate_approved = SecurityGate(confirmation_callback=lambda req: True)
        self.assertTrue(gate_approved.check_clearance(task_lvl2))

        # With callback rejecting -> rejected
        gate_rejected = SecurityGate(confirmation_callback=lambda req: False)
        self.assertFalse(gate_rejected.check_clearance(task_lvl2))


if __name__ == "__main__":
    unittest.main()
