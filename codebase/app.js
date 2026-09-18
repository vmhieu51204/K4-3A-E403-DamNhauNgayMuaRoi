// Reads anonymized CSV via local server. Replies are session-only; no Discord API calls.
const topics={all:'Tất cả',attendance:'Điểm danh & Workshop',technical:'Lỗi kỹ thuật',team:'Ghép đội',policy:'Quy chế'};
const names={awaiting:'Chờ làm rõ',pending:'Hộp thư câu hỏi',resolved:'Đã xử lý',answered:'Đã có phản hồi',dismissed:'Đã bỏ qua',feed:'Bản tin Discord'};
let questions=[],view='pending',topic='all',scanning=false,toastTimer;
const drafts=new Map(), $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function toast(message){clearTimeout(toastTimer);$('toast').textContent=message;$('toast').hidden=false;toastTimer=setTimeout(()=>$('toast').hidden=true,3500);}
function needsClarification(q){return q.layers?.includes(2)&&q.answerStatus!=='answered';}
function clarificationDraft(q){
 if(!needsClarification(q))return null;
 return q.id==='M33885'?'Bạn đang bị out khỏi Zoom, Phoenix hay ứng dụng nào khác? Bạn dùng máy tính hay điện thoại? Có thông báo lỗi nào xuất hiện không?':'Bạn đang hỏi về thủ tục nào và mục nào trong sổ tay? Bạn gửi thêm đoạn hướng dẫn hoặc thông báo liên quan để mình kiểm tra chính xác nhé.';
}
function haxDetails(q){
 const topicReasons={attendance:'Nội dung liên quan lịch workshop, điểm danh hoặc chuyên cần.',technical:'Tin nhắn mô tả lỗi sử dụng; chưa đủ thông tin để xác định ứng dụng hoặc nguyên nhân.',team:'Nội dung liên quan ghép đội hoặc thời hạn lập đội.',policy:'Nội dung liên quan quy trình, sổ tay hoặc xác nhận hành chính.'};
 const clarify=needsClarification(q);
 return `<div class="hax-signals"><span class="confidence-badge" title="CSV và nhãn hiện tại không có điểm tin cậy AI. Không quy đổi nhãn thành phần trăm.">HAX G2 · Độ tin cậy: chưa có điểm AI</span>${clarify?'<span class="clarify-badge">HAX G10 · Mơ hồ — cần hỏi lại</span>':''}</div>${clarify?'<div class="clarify-notice"><strong>Hỏi lại trước khi đưa giải pháp.</strong> Chỉ lưu câu hỏi làm rõ; câu này chuyển sang Chờ làm rõ, không tính là đã xử lý.</div>':''}<details class="hax-reasoning"><summary>HAX G11 · AI Reasoning <span>Giải thích từ nhãn đối chiếu</span></summary><p><strong>Vì sao chọn ${esc(topics[q.topic]||q.topic)}:</strong> ${esc(topicReasons[q.topic]||'Theo nhãn đối chiếu của case.')}</p><p><strong>Vì sao ${q.answerStatus==='answered'?'không đưa vào tồn':'cần xem xét'}:</strong> ${esc(q.reason)}</p><p><strong>Bằng chứng:</strong> ${q.evidenceIds.length?esc(q.evidenceIds.join(', ')):'Chưa có bằng chứng phản hồi trong ngữ cảnh đã chọn.'} · Mốc ${esc(q.cutoff)}.</p><small>Nguồn: nhãn nháp eval/real_cases.jsonl, cần TA duyệt; không phải suy luận do AI vừa tạo.</small></details>`;
}
function render(){
 const pending=questions.filter(q=>q.status==='pending');
 const count=status=>questions.filter(q=>q.status===status).length;
 $('stat-total').textContent=pending.length;$('nav-count').textContent=pending.length;
 $('stat-critical').textContent=pending.filter(q=>q.hours>=24).length;
 $('stat-warning').textContent=pending.filter(q=>q.hours>=4&&q.hours<24).length;
 $('stat-resolved').textContent=count('resolved');$('resolved-nav').textContent=count('resolved');
 $('awaiting-nav').textContent=count('awaiting');$('answered-nav').textContent=count('answered');$('dismissed-nav').textContent=count('dismissed');
 $('breadcrumb').textContent=names[view];
 document.querySelectorAll('[data-view]').forEach(b=>{b.classList.toggle('active',b.dataset.view===view);b.setAttribute('aria-current',b.dataset.view===view?'page':'false');});
 $('inbox').hidden=view==='feed';$('feed-panel').hidden=view!=='feed';
 $('feed-text').textContent=`# BẢN TIN CÂU HỎI TỒN KHÓA 4\n${pending.length} câu hỏi cần xem xét theo mốc đánh giá riêng từng case.\nNhãn nháp đối chiếu, chưa phải kết quả AI.\n\n`+Object.entries(topics).filter(([key])=>key!=='all').map(([key,name])=>{const group=pending.filter(q=>q.topic===key);return group.length?`## ${name}\n`+group.map(q=>`• [${q.id}] ${q.author} · ${q.guild} · #${q.channel}\n  Chờ ${q.hours}h tại ${q.cutoff}\n  ${q.content}`).join('\n\n'):'';}).filter(Boolean).join('\n\n');
 const pool=questions.filter(q=>q.status===view);
 $('list-title').innerHTML=`${names[view]} <span>${pool.length}</span>`;
 $('list-description').textContent={pending:'Câu hỏi cần xem xét tại mốc đánh giá của từng case.',resolved:'Phản hồi bạn đã lưu trong phiên này.',awaiting:'Đã lưu câu hỏi làm rõ; chưa giải quyết xong và chưa gửi Discord.',answered:'Đã có phản hồi trong nguồn; không tính vào số bạn xử lý trong ca.',dismissed:'Có thể đưa câu hỏi trở lại hộp thư.'}[view]||'';
 $('topic-filters').innerHTML=Object.entries(topics).map(([key,label])=>`<button class="topic-button ${topic===key?'active':''}" data-topic="${key}" aria-pressed="${topic===key}">${label}<span>${pool.filter(q=>key==='all'||q.topic===key).length}</span></button>`).join('');
 const query=$('search').value.trim().toLocaleLowerCase('vi');
 const filtered=pool.filter(q=>(topic==='all'||q.topic===topic)&&`${q.content} ${q.author} ${q.id} ${q.channel} ${q.guild}`.toLocaleLowerCase('vi').includes(query)).sort((a,b)=>$('sort').value==='longest'?b.hours-a.hours||a.createdAt.localeCompare(b.createdAt):b.createdAt.localeCompare(a.createdAt));
 $('result-count').textContent=`Hiển thị ${filtered.length} / ${pool.length} câu hỏi`;
 $('questions-container').innerHTML=filtered.length?filtered.map(renderCard).join(''):'<div class="empty"><span>✓</span><h3>Không có câu hỏi trong mục này</h3><p>Thử từ khóa khác hoặc chọn tất cả chủ đề.</p></div>';
}
function currentDraft(q){return drafts.get(q.id)??clarificationDraft(q)??q.draft;}
function renderCard(q){
 const editable=['pending','awaiting'].includes(q.status);
 return `<article class="question-card ${q.hours>=24?'critical':''}"><div class="question-meta"><span class="status-dot"></span><strong>${esc(q.author)}</strong><button class="channel" data-action="open" data-id="${esc(q.id)}" title="Xem ngữ cảnh tin nhắn">#${esc(q.channel)} ↗</button><span class="question-id">(${esc(q.id)})</span><span class="wait-badge ${q.hours>=24?'urgent':''}">${view==='pending'?`◷ Chờ ${q.hours}h`:esc(names[view])}</span><span class="topic-tag">${esc(topics[q.topic]||q.topic)}</span></div><p class="question-text">“${esc(q.content)}”</p>${haxDetails(q)}${editable?`<label class="draft-label" for="draft-${esc(q.id)}">💬 Soạn câu trả lời · #${esc(q.channel)}<span>HAX G9 · TA chỉnh sửa trước khi lưu</span></label><textarea id="draft-${esc(q.id)}" data-draft="${esc(q.id)}" rows="2" placeholder="Nhập câu trả lời...">${esc(currentDraft(q))}</textarea>`:''}<div class="question-bottom">${view==='pending'?`<button class="text-button" data-action="dismiss" data-id="${esc(q.id)}" title="HAX G8 · Bỏ qua một click, có thể khôi phục">✕ Bỏ qua</button>`:`<button class="text-button" data-action="restore" data-id="${esc(q.id)}">↶ Đưa về hộp thư</button>`}<div class="card-actions"><button class="button" data-action="open" data-id="${esc(q.id)}" title="Pack đã ẩn danh: xem ngữ cảnh local, không mở Discord thật">🔗 Xem ngữ cảnh Discord</button>${editable?`<button class="button primary" data-action="save" data-id="${esc(q.id)}">${needsClarification(q)?'💬 Lưu câu hỏi làm rõ':'✓ Lưu Reply & Đóng Case'}</button>`:''}</div></div></article>`;
}
function saveReply(id,input){
 const q=questions.find(q=>q.id===id);if(!q||!input)return;
 const text=input.value.trim();
 if(!text){input.setCustomValidity('Nhập câu trả lời trước khi lưu.');input.reportValidity();return;}
 q.reply=text;drafts.set(id,text);q.status=needsClarification(q)?'awaiting':'resolved';
 if($('reply-dialog').open)$('reply-dialog').close();
 render();toast(q.status==='awaiting'?'Đã lưu câu hỏi làm rõ · Chưa giải quyết xong, chưa gửi Discord.':'Đã lưu phản hồi trong phiên · Chưa gửi Discord.');
}
function openQuestion(id){
 const q=questions.find(q=>q.id===id);if(!q)return;
 const done=['resolved','answered'].includes(q.status);
 const thread=[{msg_id:q.id,author:q.author,content:q.content,created_at_vn:q.createdAt},...q.context].sort((a,b)=>a.created_at_vn.localeCompare(b.created_at_vn));
 const clarify=needsClarification(q);
 const reply=q.status==='answered'?q.context.filter(m=>q.evidenceIds.includes(m.msg_id)).map(m=>m.content).join('\n\n'):done?q.reply:(drafts.get(id)??clarificationDraft(q)??q.draft);
 $('dialog-content').innerHTML=`<h2 id="dialog-title">${esc(q.author)} <span># ${esc(q.channel)}</span></h2><div class="dialog-question">${esc(q.content)}</div>${haxDetails(q)}<div class="context-note">${esc(q.reason)}<br><strong>Mốc đánh giá:</strong> ${esc(q.cutoff)}<br><strong>Lưu ý:</strong> ${esc(q.caution)}</div><details class="source-thread" open><summary>Ngữ cảnh từ CSV · ${thread.length} tin nhắn</summary>${thread.map(m=>`<article class="thread-message ${m.msg_id===q.id?'target-message':''}"><div><strong>${esc(m.author)}</strong><span>${esc(m.msg_id)} · ${esc(m.created_at_vn)}${q.evidenceIds.includes(m.msg_id)?' · Bằng chứng phản hồi':''}</span></div><p>${esc(m.content)}</p></article>`).join('')}</details><label class="draft-label" for="reply-input">${done?'Phản hồi đã lưu / có trong nguồn':'HAX G9 · Chỉnh sửa bản nháp'}<span>${done?'Xem ngữ cảnh trước khi kết luận':'Mẫu soạn sẵn · chưa dùng AI'}</span></label><textarea id="reply-input" ${done?'readonly':''}>${esc(reply)}</textarea><p class="dialog-note">Pack đã ẩn danh và không có Jump URL thật. Phản hồi chỉ lưu trong phiên, chưa gửi Discord. Tải lại trang sẽ đặt lại thao tác.</p><div class="dialog-actions"><button class="button" id="cancel-reply">Đóng</button>${done?'':`<button class="button primary" id="send-reply">${clarify?'Lưu câu hỏi làm rõ':'✓ Lưu phản hồi & đóng câu hỏi'}</button>`}</div>`;
 $('cancel-reply').onclick=()=>$('reply-dialog').close();
 if(!done){$('reply-input').oninput=e=>{e.target.setCustomValidity('');drafts.set(id,e.target.value);};$('send-reply').onclick=()=>saveReply(id,$('reply-input'));}
 $('reply-dialog').showModal();
}
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view;topic='all';$('search').value='';render();});
$('topic-filters').onclick=e=>{const b=e.target.closest('[data-topic]');if(b){topic=b.dataset.topic;render();}};
$('questions-container').oninput=e=>{const id=e.target.dataset.draft;if(id){e.target.setCustomValidity('');drafts.set(id,e.target.value);}};
$('questions-container').onclick=e=>{const b=e.target.closest('[data-action]');if(!b)return;const q=questions.find(q=>q.id===b.dataset.id);if(!q)return;if(b.dataset.action==='open')openQuestion(q.id);else if(b.dataset.action==='save')saveReply(q.id,$(`draft-${q.id}`));else{q.status=b.dataset.action==='dismiss'?'dismissed':'pending';render();toast(b.dataset.action==='dismiss'?'Đã chuyển sang mục Đã bỏ qua.':'Đã đưa về hộp thư để xem xét lại.');}};
$('search').oninput=render;$('sort').onchange=render;$('close-dialog').onclick=()=>$('reply-dialog').close();
$('reply-dialog').onclick=e=>{if(e.target===$('reply-dialog')){const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close();}};
$('scan-button').onclick=()=>loadWorkspace(true);
$('copy-feed').onclick=async()=>{try{await navigator.clipboard.writeText($('feed-text').textContent);toast('Đã sao chép bản tin.');}catch{const range=document.createRange();range.selectNodeContents($('feed-text'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Đã chọn bản tin. Nhấn Ctrl+C để sao chép.');}};
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!$('reply-dialog').open&&view!=='feed'){e.preventDefault();$('search').focus();}});
async function loadWorkspace(refresh=false){
 if(scanning)return;scanning=true;$('scan-button').disabled=true;$('scan-button').textContent='Đang đọc CSV...';$('scan-progress').hidden=false;
 try{
  const response=await fetch('/api/workspace',{cache:'no-store'});if(!response.ok)throw new Error('Không đọc được nguồn');
  const payload=await response.json();if(!Array.isArray(payload.questions)||!payload.meta)throw new Error('Sai định dạng');
  const previous=new Map(questions.map(q=>[q.id,q]));
  questions=payload.questions.map(q=>{const old=previous.get(q.id);return old?{...q,status:old.status,reply:old.reply}:q;});
  const m=payload.meta;
  $('source-summary').textContent=`${m.messages.toLocaleString('vi')} tin nhắn · ${m.supportCases} câu hỏi đối chiếu · ${m.period}`;
  $('source-detail').textContent=`${m.humans} tin người · ${m.bots} tin bot. Danh sách dùng nhãn nháp của ${m.cases} case, không phải kết quả AI quét toàn bộ CSV. Thời gian chờ tính tại mốc đánh giá riêng từng câu.`;
  $('data-error').hidden=true;render();if(refresh)toast('Đã đọc lại CSV; giữ các thao tác trong phiên.');
 }catch(error){$('data-error').hidden=false;$('data-error').textContent='Không tải được dữ liệu. Chạy python codebase/server.py rồi mở http://127.0.0.1:8081. Kiểm tra data/discord-pack và thử Đọc lại dữ liệu.';if(!questions.length)$('questions-container').innerHTML='<div class="empty"><h3>Chưa tải được câu hỏi</h3><p>Cần máy chủ local để đọc thư mục data.</p></div>';toast('Không tải được dữ liệu nguồn.');}
 finally{scanning=false;$('scan-button').disabled=false;$('scan-button').innerHTML='<span>↻</span> Đọc lại dữ liệu';$('scan-progress').hidden=true;}
}
$('show-reports').onclick=async()=>{const panel=$('original-report');panel.hidden=!panel.hidden;$('show-reports').setAttribute('aria-expanded',String(!panel.hidden));if(panel.hidden)return;panel.textContent='Đang tải bản tin gốc...';try{const response=await fetch('/api/reports');if(!response.ok)throw new Error();panel.textContent=(await response.json()).text;}catch{panel.textContent='Không đọc được k4_daily_reports.md. Đóng và mở lại để thử lại.';}};
render();loadWorkspace();
