"""Local TA workspace. Reads private data at runtime; never copies it into UI assets."""
import argparse
import csv
import json
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WEB = ROOT / 'codebase'
PACK = ROOT / 'data' / 'discord-pack'
if not PACK.exists() and (ROOT / 'data').exists():
    PACK = ROOT / 'data'

try:
    from codebase.mvp_ai import generate_mvp_reply
except ImportError:
    try:
        from mvp_ai import generate_mvp_reply
    except ImportError:
        generate_mvp_reply = None


def timestamp(value):
    return datetime.fromisoformat(value.replace(' ', 'T') + ('+07:00' if len(value) == 16 else ''))


def load_workspace():
    with (PACK / 'k4_messages.csv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    cases = [json.loads(line) for line in (ROOT / 'eval' / 'real_cases.jsonl').read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    questions = []
    drafts = {
        'verify_source': 'Mình đã nhận được câu hỏi. Mình sẽ đối chiếu thông báo và quy định chính thức trước khi xác nhận lại cho bạn nhé.',
        'clarify': 'Bạn gửi thêm thông tin về tình huống đang gặp và thông báo hoặc lỗi liên quan để mình kiểm tra chính xác hơn nhé.',
        'escalate_authority': 'Mình ghi nhận yêu cầu của bạn và sẽ chuyển đến bộ phận phụ trách để xem xét. Hiện chưa có xác nhận thay đổi thời hạn bạn nhé.',
    }
    for case in cases:
        info, label = case['input'], case['expected']
        if not label['is_support_request']:
            continue
        cutoff = timestamp(info['evaluation_time'])
        def lookup(mid):
            matches = [r for r in rows if r['msg_id'] == mid and r['guild'] == info['guild'] and r['channel'] == info['channel']]
            if mid == case['source_msg_id']:
                matches = [r for r in matches if timestamp(r['created_at_vn']) == timestamp(info['sent_at'])]
            if len(matches) != 1:
                raise ValueError(f'{mid}: cần đúng một bản ghi, tìm thấy {len(matches)}')
            if timestamp(matches[0]['created_at_vn']) > cutoff:
                raise ValueError(f'{mid}: ngữ cảnh vượt mốc đánh giá')
            return matches[0]
        source = lookup(case['source_msg_id'])
        context = [lookup(mid) for mid in info['context_message_ids']]
        ctx_str = '\n'.join(f"[{m['author']}]: {m['content']}" for m in context)
        evidence_texts = [m['content'] for m in context if m['msg_id'] in label.get('answer_evidence_ids', [])]
        prev_ans = '\n'.join(evidence_texts) if evidence_texts else None

        ai_out = generate_mvp_reply(
            student_question=source['content'],
            thread_context=ctx_str,
            previous_answer=prev_ans
        ) if generate_mvp_reply else {}
        ai_reply = ai_out.get('suggested_reply', '')
        chosen_draft = ai_reply if ai_reply else drafts.get(label['expected_action'], '')
        questions.append({
            'id': source['msg_id'], 'author': source['author'], 'channel': source['channel'],
            'guild': source['guild'], 'content': source['content'], 'createdAt': source['created_at_vn'],
            'hours': round((cutoff - timestamp(source['created_at_vn'])).total_seconds() / 3600, 2),
            'cutoff': info['evaluation_time'], 'topic': label['topic'],
            'status': 'pending' if label['expected_in_backlog'] == 'yes' else 'answered',
            'answerStatus': label['answer_status'], 'reason': label['reason'],
            'caution': label['must_not'], 'layers': label['difficulty_layers'],
            'draft': chosen_draft,
            'aiSuggestedReply': ai_reply,
            'context': context,
            'evidenceIds': label['answer_evidence_ids'],
        })
    return {'questions': questions, 'meta': {
        'messages': len(rows), 'humans': sum(r['is_bot'].lower() != 'true' for r in rows),
        'bots': sum(r['is_bot'].lower() == 'true' for r in rows),
        'cases': len(cases), 'supportCases': len(questions),
        'source': 'data/discord-pack/k4_messages.csv',
        'annotation': 'Nhãn nháp từ eval/real_cases.jsonl · cần người duyệt',
        'period': '12–14/09/2026',
    }}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0]
        try:
            if path == '/api/workspace':
                body = json.dumps(load_workspace(), ensure_ascii=False).encode('utf-8')
                mime = 'application/json; charset=utf-8'
            elif path == '/api/ai_draft':
                import urllib.parse
                qs = urllib.parse.parse_qs(self.path.split('?', 1)[1] if '?' in self.path else '')
                text = qs.get('text', [''])[0]
                ctx = qs.get('ctx', [''])[0]
                prev = qs.get('prev', [None])[0]
                res = generate_mvp_reply(text, ctx, prev) if generate_mvp_reply else {}
                body = json.dumps(res, ensure_ascii=False).encode('utf-8')
                mime = 'application/json; charset=utf-8'
            elif path == '/api/resolve':
                import urllib.parse
                qs = urllib.parse.parse_qs(self.path.split('?', 1)[1] if '?' in self.path else '')
                msg_id = qs.get('id', [''])[0]
                reply_text = qs.get('reply', [''])[0]
                print(f"[TA COPILOT] 🚀 Gửi phản hồi tin nhắn {msg_id}: {reply_text[:80]}", flush=True)
                body = json.dumps({'status': 'success', 'id': msg_id, 'reply': reply_text}, ensure_ascii=False).encode('utf-8')
                mime = 'application/json; charset=utf-8'
            elif path in ('/', '/index.html', '/styles.css', '/app.js'):
                name = 'index.html' if path == '/' else path[1:]
                body = (WEB / name).read_bytes()
                mime = {'html':'text/html','css':'text/css','js':'text/javascript'}[name.split('.')[-1]] + '; charset=utf-8'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(body)
        except (OSError, ValueError, KeyError) as error:
            body = json.dumps({'error': 'Không đọc được dữ liệu nguồn. Kiểm tra data/discord-pack và eval/real_cases.jsonl.', 'detail': str(error)}, ensure_ascii=False).encode('utf-8')
            self.send_response(503)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8081)
    args = parser.parse_args()
    print(f'TA Copilot: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
