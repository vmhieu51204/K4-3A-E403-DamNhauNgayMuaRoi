import csv
import unittest
from collections import Counter
from server import PACK, load_workspace, timestamp

class WorkspaceTests(unittest.TestCase):
    def test_csv_identity_and_cutoff(self):
        data = load_workspace()
        with (PACK / 'k4_messages.csv').open(encoding='utf-8-sig', newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(data['meta']['messages'], len(rows))
        for q in data['questions']:
            matches = [r for r in rows if (r['msg_id'], r['guild'], r['channel'], r['created_at_vn']) == (q['id'], q['guild'], q['channel'], q['createdAt'])]
            self.assertEqual(len(matches), 1)
            self.assertEqual(q['content'], matches[0]['content'])
            self.assertEqual(q['author'], matches[0]['author'])
            self.assertNotEqual(matches[0]['is_bot'].lower(), 'true')
            for context in q['context']:
                self.assertLessEqual(timestamp(context['created_at_vn']), timestamp(q['cutoff']))
            self.assertTrue(set(q['evidenceIds']).issubset({r['msg_id'] for r in q['context']}))

    def test_backlog_excludes_answered_and_non_questions(self):
        questions = load_workspace()['questions']
        self.assertEqual(Counter(q['status'] for q in questions), {'pending': 7, 'answered': 3})
        by_id = {q['id']: q for q in questions}
        for mid in ('M63574', 'M67317', 'M80655'):
            self.assertEqual(by_id[mid]['status'], 'answered')
        for mid in ('M08376', 'M16680'):
            self.assertNotIn(mid, by_id)
        self.assertTrue(all(q['hours'] == 4.02 for q in questions))

if __name__ == '__main__':
    unittest.main()
