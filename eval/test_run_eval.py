"""Offline regression tests; never call the live API."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import run_eval as runner


class EvalTests(unittest.TestCase):
    def test_pacer_spaces_requests_and_retries(self):
        pacer = runner.RequestPacer(5)
        with patch.object(runner.time, 'monotonic', side_effect=[100, 100, 102, 105, 111, 111]), \
                patch.object(runner.time, 'sleep') as sleep:
            pacer.wait()
            pacer.wait()
            pacer.wait()
        sleep.assert_called_once_with(3)

    def test_context_cutoff_and_duplicate_rejected(self):
        case = {'source_msg_id': 'M1', 'input': {
            'load_message_text_from_source': True, 'guild': 'G', 'channel': 'C',
            'sent_at': '2026-09-17T10:00:00+07:00',
            'evaluation_time': '2026-09-17T14:01:00+07:00',
            'context_message_ids': ['M2'], 'official_sources': []}}
        target = dict(msg_id='M1', guild='G', channel='C', created_at_vn='2026-09-17 10:00',
                      content='question', is_bot='False', reply_to='')
        context = dict(target, msg_id='M2', created_at_vn='2026-09-17 14:02')
        with self.assertRaisesRegex(ValueError, 'evaluation_time'):
            runner.prepare_input(case, [target, context])
        context['created_at_vn'] = '2026-09-17 11:00'
        with self.assertRaisesRegex(ValueError, 'tìm thấy 2'):
            runner.prepare_input(case, [target, context, context])
        data = runner.prepare_input(case, [target, context])
        self.assertEqual(data['context_messages'][0]['msg_id'], 'M2')
        self.assertIs(data['is_bot'], False)

    def test_backlog_metrics_and_skips(self):
        rows = []
        for gold, predicted in [('yes', 'yes'), ('yes', 'no'), ('no', 'yes')]:
            rows.append({'status': 'fail', 'expected': {'expected_in_backlog': gold},
                         'prediction': {'expected_in_backlog': predicted},
                         'checks': dict.fromkeys(runner.FIELDS, False)})
        rows.append({'status': 'skipped'})
        stats = runner.summarize(rows)
        self.assertEqual(stats['evaluated'], 3)
        self.assertEqual(stats['backlog']['precision'], 0.5)
        self.assertEqual(stats['backlog']['recall'], 0.5)
        self.assertIsNone(runner.summarize([])['backlog']['recall'])

    def test_end_to_end_mocked_api_and_no_label_leak(self):
        case = runner.load_cases('synthetic')[0]
        prediction = {f: case['expected'][f] for f in runner.FIELDS}
        prediction.update(reason='Test only', draft_reply='Test only')
        seen = []

        def fake_urlopen(req, timeout):
            payload = json.loads(req.data)
            data = json.loads(payload['input'])
            self.assertNotIn('expected', data)
            self.assertNotIn('annotation', data)
            self.assertNotIn('scenario_summary', data)
            self.assertEqual(data, case['input'])
            self.assertTrue(payload['text']['format']['strict'])
            seen.append(payload)
            return io.StringIO(json.dumps({'status': 'completed', 'output': [
                {'content': [{'type': 'output_text', 'text': json.dumps(prediction)}]}],
                'usage': {'total_tokens': 10}}))

        with tempfile.TemporaryDirectory() as folder:
            argv = ['run_eval.py', '--provider', 'openai', '--dataset', 'synthetic', '--limit', '1', '--output-dir', folder]
            with patch.object(runner.sys, 'argv', argv), patch.object(runner, 'load_env'), \
                    patch.dict(runner.os.environ, {'OPENAI_API_KEY': 'offline-test'}), \
                    patch.object(runner.request, 'urlopen', fake_urlopen), \
                    contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(), 0)
            report = json.loads(next(Path(folder).glob('*.json')).read_text(encoding='utf-8'))
            self.assertEqual(report['summary']['all']['passed'], 1)
            self.assertEqual(len(seen), 1)

    def test_gemini_request_and_response(self):
        case = runner.load_cases('synthetic')[0]
        prediction = {f: case['expected'][f] for f in runner.FIELDS}
        prediction.update(reason='Test', draft_reply='Test')

        def fake_urlopen(req, timeout):
            self.assertEqual(req.full_url,
                'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions')
            self.assertEqual(req.get_header('Authorization'), 'Bearer gemini-test')
            payload = json.loads(req.data)
            self.assertNotIn('provider', payload)
            self.assertEqual(payload['model'], 'gemini-3.5-flash-lite')
            self.assertEqual(json.loads(payload['messages'][1]['content']), case['input'])
            self.assertTrue(payload['response_format']['json_schema']['strict'])
            return io.StringIO(json.dumps({'choices': [{'finish_reason': 'stop',
                'message': {'content': json.dumps(prediction)}}]}))

        with patch.object(runner.request, 'urlopen', fake_urlopen):
            actual, _ = runner.predict(case['input'], 'gemini-test',
                'gemini-3.5-flash-lite', runner.PROMPT, 90, 'gemini')
        self.assertEqual(actual, prediction)

    def test_openrouter_request_and_response(self):
        case = runner.load_cases('synthetic')[0]
        prediction = {f: case['expected'][f] for f in runner.FIELDS}
        prediction.update(reason='Test', draft_reply='Test')

        def fake_urlopen(req, timeout):
            self.assertEqual(req.full_url, 'https://openrouter.ai/api/v1/chat/completions')
            self.assertEqual(req.get_header('Authorization'), 'Bearer router-test')
            payload = json.loads(req.data)
            self.assertEqual(payload['model'], 'openai/gpt-4.1-mini')
            self.assertEqual(json.loads(payload['messages'][1]['content']), case['input'])
            self.assertTrue(payload['response_format']['json_schema']['strict'])
            self.assertTrue(payload['provider']['require_parameters'])
            return io.StringIO(json.dumps({'choices': [{'finish_reason': 'stop',
                'message': {'content': json.dumps(prediction)}}], 'usage': {'total_tokens': 10}}))

        with patch.object(runner.request, 'urlopen', fake_urlopen):
            actual, usage = runner.predict(case['input'], 'router-test',
                'openai/gpt-4.1-mini', runner.PROMPT, 90, 'openrouter')
        self.assertEqual(actual, prediction)
        self.assertEqual(usage['total_tokens'], 10)


if __name__ == '__main__':
    unittest.main()
