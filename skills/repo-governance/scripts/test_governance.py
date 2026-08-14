"""Run the governance test domains through the historical unittest entrypoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("governance.py")
sys.path.insert(0, str(SCRIPT.parent))

from test_governance_documents import GovernanceDocumentTests
from test_governance_legacy import GovernanceLegacyTests
from test_governance_locales import GovernanceLocaleTests
from test_governance_support import governance
from test_governance_transactions import GovernanceTransactionTests
from test_governance_validation import GovernanceValidationTests

# Keep the original class name and direct ``python3 test_governance.py`` behavior
# while storing each cohesive domain in its own reviewable module.
GovernanceTests = type(
    "GovernanceTests",
    (
        GovernanceDocumentTests,
        GovernanceLocaleTests,
        GovernanceTransactionTests,
        GovernanceLegacyTests,
        GovernanceValidationTests,
    ),
    {},
)
del GovernanceDocumentTests
del GovernanceLegacyTests
del GovernanceLocaleTests
del GovernanceTransactionTests
del GovernanceValidationTests


__all__ = ["SCRIPT", "GovernanceTests", "governance"]


if __name__ == "__main__":
    unittest.main()
