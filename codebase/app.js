// TA Copilot MVP — Bước 4: Giao diện TA Dashboard tối giản
let questions = [], scanning = false, toastTimer;
const drafts = new Map(), $ = id => document.getElementById(id);
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function toast(message) {
  clearTimeout(toastTimer);
  $('toast').textContent = message;
  $('toast').hidden = false;
  toastTimer = setTimeout(() => $('toast').hidden = true, 3000);
}

function currentDraft(q) {
  return drafts.get(q.id) ?? q.aiSuggestedReply ?? q.draft ?? '';
}

function render() {
  const pending = questions.filter(q => q.status === 'pending');

  // Hiển thị tổng số card đang có trong Backlog dưới dạng text đơn giản
  if ($('backlog-counter')) {
    $('backlog-counter').textContent = `${pending.length} câu hỏi đang chờ`;
  }

  const query = $('search')?.value.trim().toLocaleLowerCase('vi') || '';
  const sortVal = $('sort')?.value || 'longest';
  const filtered = pending.filter(q => `${q.content} ${q.author} ${q.id} ${q.channel} ${q.guild}`.toLocaleLowerCase('vi').includes(query))
                          .sort((a, b) => sortVal === 'longest' ? b.hours - a.hours || a.createdAt.localeCompare(b.createdAt) : b.createdAt.localeCompare(a.createdAt));

  $('result-count').textContent = `Hiển thị ${filtered.length} / ${pending.length} câu hỏi trong Backlog`;
  $('questions-container').innerHTML = filtered.length
    ? filtered.map(renderCard).join('')
    : '<div class="empty"><span>✓</span><h3>Không còn câu hỏi nào trong Backlog</h3><p>Tất cả câu hỏi đã được giải đáp và đóng case thành công.</p></div>';
}

function renderCard(q) {
  // Màu viền card theo urgency: đỏ nếu ≥24h (critical), cam nếu 4h-24h (warning)
  const urgencyClass = q.hours >= 24 ? 'critical' : 'warning';
  const urgencyBadge = q.hours >= 24 ? 'urgent' : '';

  return `
    <article class="question-card ${urgencyClass}">
      <div class="question-meta">
        <span class="status-dot"></span>
        <strong>${esc(q.author)}</strong>
        <span class="channel">#${esc(q.channel)}</span>
        <span class="question-id">(${esc(q.id)})</span>
        <span class="wait-badge ${urgencyBadge}">◷ Chờ ${q.hours}h</span>
        <button class="button" data-action="open-thread" data-id="${esc(q.id)}" style="margin-left: auto; padding: 4px 10px; font-size: 11px;">
          💬 Xem Thread
        </button>
      </div>

      <p class="question-text" style="font-size: 14px; margin: 12px 0 14px; line-height: 1.5; color: #f8fafc;">
        “${esc(q.content)}”
      </p>

      <label class="draft-label" for="draft-${esc(q.id)}" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 12px; color: #94a3b8; font-weight: 500;">
        <span>💬 Câu trả lời đề xuất (AI Draft):</span>
        <span style="font-size: 11px; color: #64748b;">TA có thể gõ sửa trực tiếp</span>
      </label>

      <textarea id="draft-${esc(q.id)}" data-draft="${esc(q.id)}" rows="3" class="draft-textarea" placeholder="Nhập hoặc chỉnh sửa câu trả lời cho học viên..." style="width: 100%; border-radius: 10px; padding: 10px 12px; font-size: 13px; font-family: inherit; line-height: 1.5; box-sizing: border-box;">${esc(currentDraft(q))}</textarea>

      <div class="question-bottom" style="display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 14px; padding-top: 10px; border-top: 1px solid rgba(148, 163, 184, 0.08);">
        <button class="button" data-action="open-discord" data-id="${esc(q.id)}">
          ↗️ Mở Discord
        </button>
        <button class="button primary" data-action="send" data-id="${esc(q.id)}">
          🚀 Gửi &amp; Đóng Case
        </button>
      </div>
    </article>
  `;
}

function openThreadModal(id) {
  const q = questions.find(q => q.id === id);
  if (!q) return;

  const thread = [
    { msg_id: q.id, author: q.author, content: q.content, created_at_vn: q.createdAt },
    ...(q.context || [])
  ].sort((a, b) => a.created_at_vn.localeCompare(b.created_at_vn));

  $('dialog-header-title').textContent = `THREAD: #${esc(q.channel)} · ${esc(q.author)}`;
  $('dialog-content').innerHTML = `
    <div style="margin-bottom: 12px; padding: 10px 12px; background: rgba(15, 23, 42, 0.6); border-radius: 10px; border-left: 3px solid #3b82f6;">
      <strong style="color: #60a5fa; font-size: 12px;">Câu hỏi mục tiêu:</strong>
      <p style="margin: 4px 0 0; color: #f8fafc; font-size: 13px;">${esc(q.content)}</p>
    </div>

    <details class="source-thread" open style="margin-top: 10px;">
      <summary style="font-size: 12px; font-weight: 600; color: #cbd5e1; cursor: pointer; padding: 6px 0;">
        Ngữ cảnh hội thoại liên quan (${thread.length} tin nhắn)
      </summary>
      <div style="max-height: 360px; overflow-y: auto; margin-top: 8px; display: flex; flex-direction: column; gap: 8px;">
        ${thread.map(m => `
          <article class="thread-message ${m.msg_id === q.id ? 'target-message' : ''}" style="padding: 8px 12px; border-radius: 8px; background: ${m.msg_id === q.id ? 'rgba(59, 130, 246, 0.12)' : 'rgba(30, 41, 59, 0.5)'}; border: 1px solid ${m.msg_id === q.id ? 'rgba(59, 130, 246, 0.3)' : 'rgba(148, 163, 184, 0.08)'};">
            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #94a3b8; margin-bottom: 4px;">
              <strong style="color: ${m.msg_id === q.id ? '#93c5fd' : '#e2e8f0'};">${esc(m.author)}</strong>
              <span>${esc(m.created_at_vn)}</span>
            </div>
            <p style="margin: 0; font-size: 13px; color: #cbd5e1; line-height: 1.4;">${esc(m.content)}</p>
          </article>
        `).join('')}
      </div>
    </details>
  `;

  $('thread-dialog').showModal();
}

function handleSendAndClose(id) {
  const q = questions.find(q => q.id === id);
  const input = $(`draft-${id}`);
  if (!q || !input) return;

  const text = input.value.trim();
  if (!text) {
    input.setCustomValidity('Vui lòng nhập câu trả lời trước khi gửi.');
    input.reportValidity();
    input.focus();
    return;
  }

  q.reply = text;
  drafts.set(id, text);
  q.status = 'resolved'; // Đóng case, xóa ngay khỏi Backlog hiển thị

  // Lưu lại phản hồi đã chỉnh sửa vào server log / state
  fetch(`/api/resolve?id=${encodeURIComponent(id)}&reply=${encodeURIComponent(text)}`).catch(() => {});

  render();
  toast(`Đã gửi phản hồi cho @${q.author} & Đóng case thành công!`);
}

// Sự kiện click trên danh sách card
$('questions-container').onclick = e => {
  const b = e.target.closest('[data-action]');
  if (!b) return;

  const id = b.dataset.id;
  const action = b.dataset.action;

  if (action === 'open-thread') {
    openThreadModal(id);
  } else if (action === 'open-discord') {
    const q = questions.find(q => q.id === id);
    const url = q ? `https://discord.com/channels/${encodeURIComponent(q.guild)}/${encodeURIComponent(q.channel)}/${encodeURIComponent(q.id)}` : 'https://discord.com';
    window.open(url, '_blank', 'noopener,noreferrer');
    toast(`Đang chuyển đến Discord channel #${q?.channel || ''}...`);
  } else if (action === 'send') {
    handleSendAndClose(id);
  }
};

// Cập nhật giá trị nháp khi TA gõ phím
$('questions-container').oninput = e => {
  const id = e.target.dataset.draft;
  if (id) {
    e.target.setCustomValidity('');
    drafts.set(id, e.target.value);
  }
};

$('search').oninput = render;
if ($('sort')) $('sort').onchange = render;
$('close-dialog').onclick = () => $('thread-dialog').close();
$('dialog-close-btn').onclick = () => $('thread-dialog').close();
$('thread-dialog').onclick = e => {
  if (e.target === $('thread-dialog')) {
    $('thread-dialog').close();
  }
};
$('scan-button').onclick = () => loadWorkspace(true);

document.addEventListener('keydown', e => {
  if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !$('thread-dialog').open) {
    e.preventDefault();
    $('search').focus();
  }
});

async function loadWorkspace(refresh = false) {
  if (scanning) return;
  scanning = true;
  $('scan-button').disabled = true;
  $('scan-button').textContent = 'Đang đọc CSV...';
  $('scan-progress').hidden = false;

  try {
    const response = await fetch('/api/workspace', { cache: 'no-store' });
    if (!response.ok) throw new Error('Không đọc được nguồn');
    const payload = await response.json();
    if (!Array.isArray(payload.questions) || !payload.meta) throw new Error('Sai định dạng');

    const previous = new Map(questions.map(q => [q.id, q]));
    questions = payload.questions.map(q => {
      const old = previous.get(q.id);
      return old ? { ...q, status: old.status, reply: old.reply } : q;
    });

    render();
    if (refresh) toast('Đã cập nhật lại danh sách câu hỏi.');
  } catch (error) {
    if (!questions.length) {
      $('questions-container').innerHTML = '<div class="empty"><h3>Chưa tải được câu hỏi</h3><p>Kiểm tra kết nối server local.</p></div>';
    }
    toast('Không tải được dữ liệu nguồn.');
  } finally {
    scanning = false;
    $('scan-button').disabled = false;
    $('scan-button').innerHTML = '⚡ Đọc lại dữ liệu';
    $('scan-progress').hidden = true;
  }
}

render();
loadWorkspace();
