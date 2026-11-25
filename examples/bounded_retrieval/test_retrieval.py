from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from retrieval import create_fixture, retrieve, FILES


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)
        self.revision = create_fixture(self.source)

    def test_three_reads_share_one_snapshot(self):
        a, na = retrieve(self.source, self.revision, FILES, batch=False)
        b, nb = retrieve(self.source, self.revision, FILES, batch=True)
        self.assertEqual(a, b)
        self.assertEqual(a, tuple((self.source / name).read_bytes() for name in FILES))
        self.assertEqual((na, nb), (3, 1))

    def test_two_reads_share_one_snapshot(self):
        a, na = retrieve(self.source, self.revision, FILES[:2], batch=False)
        b, nb = retrieve(self.source, self.revision, FILES[:2], batch=True)
        self.assertEqual(a, b)
        self.assertEqual((na, nb), (2, 1))

    def test_wrong_revision_rejected(self):
        with self.assertRaises(ValueError):
            retrieve(self.source, "0" * 40, FILES, batch=True)

    def test_unknown_path_rejected(self):
        with self.assertRaises(ValueError):
            retrieve(self.source, self.revision, ("../other",), batch=True)

    def test_empty_request_rejected(self):
        with self.assertRaises(ValueError):
            retrieve(self.source, self.revision, (), batch=True)

    def test_oversized_batch_rejected(self):
        with self.assertRaises(ValueError):
            retrieve(self.source, self.revision, FILES * 2, batch=True)

    def test_revision_format_rejected(self):
        with self.assertRaises(ValueError):
            retrieve(self.source, "HEAD", FILES, batch=True)
