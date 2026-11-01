"""Developer-only proposal tests; no model, network or installation calls."""
import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


class CorePremiseProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            'core_premise_eval', ROOT / 'scripts/eval_core_premise_candidate.py')
        cls.proposal = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.proposal)

    def fixture(self):
        import shutil
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        root = pathlib.Path(folder.name).resolve()
        fixture = root / 'tests/fixtures'
        fixture.mkdir(parents=True)
        for name in ('core-premise-candidate.lock.json', 'core-premise-proposal.txt',
                     'core-premise-cases.json', 'core-release-preparation.lock.json'):
            shutil.copy2(ROOT / 'tests/fixtures' / name, fixture / name)
        shutil.copytree(ROOT / 'tests/fixtures/core-release-preparation',
                        fixture / 'core-release-preparation')
        return root

    def observations(self, cases):
        return {'candidate_revision': self.proposal.REVISION,
                'evaluation_protocol': self.proposal.EVALUATION_PROTOCOL,
                'answers': [{'id': case['id'], **case['expected'],
                             'reason': 'Synthetic scorer fixture, not a model observation.'}
                            for case in cases]}

    def test_selected_proposal_reuses_fixed_baseline_without_adoption(self):
        pin, criteria, proposal, cases = self.proposal.inspect()
        self.assertEqual(4, len(criteria))
        self.assertEqual(12, len(cases))
        self.assertFalse(pin['proposal_accepted'])
        self.assertFalse(pin['runtime_qualified'])
        self.assertEqual(382, len(proposal.encode()))
        prompt = self.proposal.prompt(pin, criteria, proposal, cases)
        self.assertEqual(self.proposal.EVALUATION_PROTOCOL, prompt['evaluation_protocol'])
        self.assertEqual(criteria, prompt['baseline_contracts'])
        self.assertTrue(all(set(case) == {'id', 'situation', 'requested_fields'}
                            for case in prompt['cases']))

    def test_corruption_and_unsafe_inputs_fail_before_scoring(self):
        import os
        for failure in ('proposal-byte', 'pin-byte', 'case-byte', 'missing',
                        'symlink', 'hardlink', 'executable', 'baseline-byte',
                        'newline', 'unicode', 'too-large', 'fifo'):
            with self.subTest(failure=failure):
                root = self.fixture()
                path = root / 'tests/fixtures/core-premise-proposal.txt'
                if failure == 'proposal-byte':
                    path.write_bytes(path.read_bytes() + b'Changed.\n')
                elif failure in ('pin-byte', 'case-byte'):
                    name = ('core-premise-candidate.lock.json' if failure == 'pin-byte'
                            else 'core-premise-cases.json')
                    changed = root / 'tests/fixtures' / name
                    changed.write_bytes(changed.read_bytes() + b' ')
                elif failure == 'missing':
                    path.unlink()
                elif failure == 'symlink':
                    path.unlink()
                    path.symlink_to(root / 'tests/fixtures/core-premise-cases.json')
                elif failure == 'hardlink':
                    os.link(path, path.with_suffix('.extra'))
                elif failure == 'executable':
                    path.chmod(0o755)
                elif failure == 'newline':
                    path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
                elif failure == 'unicode':
                    original = path.read_bytes()
                    changed = original.replace('，'.encode(), b',', 1)
                    self.assertNotEqual(original, changed)
                    path.write_bytes(changed)
                elif failure == 'too-large':
                    path.write_bytes(b'x' * (self.proposal.MAX_INPUT_BYTES + 1))
                elif failure == 'fifo':
                    path.unlink()
                    os.mkfifo(path)
                else:
                    path = root / 'tests/fixtures/core-release-preparation/contracts/workflow.md'
                    path.write_bytes(path.read_bytes() + b'Changed.\n')
                with self.assertRaises((self.proposal.EvaluationError,
                                        self.proposal.data.core.SnapshotError, OSError)):
                    self.proposal.inspect(root)

    def test_symlink_ancestor_is_rejected(self):
        root = self.fixture()
        alias = root / 'alias'
        alias.symlink_to(root / 'tests', target_is_directory=True)
        with self.assertRaises(OSError):
            fd = self.proposal.data.core.open_directory(alias / 'fixtures')
            try:
                self.fail('symlink ancestor was followed')
            finally:
                self.proposal.os.close(fd)

    def test_exact_answer_types_order_and_binding_remain_required(self):
        _, _, _, cases = self.proposal.inspect()
        valid = self.observations(cases)
        result = self.proposal.score(valid, cases)
        self.assertTrue(result['passed'])
        for key in ('proposal_accepted', 'runtime_qualified', 'merge_authorized',
                    'observation_provenance_authenticated'):
            self.assertFalse(result[key])
        for failure in ('revision', 'missing', 'repeat', 'reorder', 'extra-root',
                        'missing-protocol', 'legacy-protocol', 'previous-protocol',
                        'unknown-protocol'):
            bad = json.loads(json.dumps(valid))
            if failure == 'revision':
                bad['candidate_revision'] = '0' * 40
            elif failure == 'missing':
                bad['answers'].pop()
            elif failure == 'repeat':
                bad['answers'][1] = bad['answers'][0]
            elif failure == 'reorder':
                bad['answers'].reverse()
            elif failure == 'missing-protocol':
                del bad['evaluation_protocol']
            elif failure in ('legacy-protocol', 'unknown-protocol'):
                bad['evaluation_protocol'] = ('core-premise-failure-cause/v1'
                                              if failure == 'legacy-protocol' else 'unknown')
            elif failure == 'previous-protocol':
                bad['evaluation_protocol'] = 'core-premise-failure-cause/v2'
            else:
                bad['extra'] = True
            with self.subTest(failure=failure):
                with self.assertRaises(self.proposal.EvaluationError):
                    self.proposal.score(bad, cases)
        for value in (1, 'true', False):
            bad = json.loads(json.dumps(valid))
            bad['answers'][0]['reassessment_required'] = value
            self.assertFalse(self.proposal.score(bad, cases)['passed'])
        for reason in ('', ' ', 1, 'x' * 4097):
            bad = json.loads(json.dumps(valid))
            bad['answers'][0]['reason'] = reason
            self.assertFalse(self.proposal.score(bad, cases)['passed'])
        bad = json.loads(json.dumps(valid))
        bad['answers'][0]['unexpected'] = True
        self.assertFalse(self.proposal.score(bad, cases)['passed'])

    def test_observations_remain_strict_json_data(self):
        for raw in (b'{"answers":[],"answers":[]}', b'{"x":NaN}', b'\xff'):
            with self.subTest(raw=raw):
                with self.assertRaises(self.proposal.EvaluationError):
                    self.proposal.data.parse(raw)

    def test_feature_gap_does_not_prove_failure_cause(self):
        _, _, _, cases = self.proposal.inspect()
        answers = self.observations(cases)
        index = next(i for i, case in enumerate(cases)
                     if case['id'] == 'real-requirement-gap')
        answers['answers'][index]['cause'] = 'premise'
        result = self.proposal.score(answers, cases)
        self.assertFalse(result['passed'])
        self.assertEqual(['real-requirement-gap'],
                         [case['id'] for case in result['cases'] if not case['passed']])

    def test_ordinary_vendor_drift_does_not_move_historical_inputs(self):
        root = self.fixture()
        before = self.proposal.inspect(root)
        unrelated = root / 'vendor/engineering-workflow-core/contracts/workflow.md'
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text('A hypothetical later ordinary vendor.\n')
        self.assertEqual(before, self.proposal.inspect(root))


if __name__ == '__main__':
    unittest.main()
