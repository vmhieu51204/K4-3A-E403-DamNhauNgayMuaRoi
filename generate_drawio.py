import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def create_drawio_xml():
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'modified': '2026-09-16T20:45:00.000Z',
        'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'version': '21.6.8',
        'type': 'device'
    })
    
    diagram = ET.SubElement(mxfile, 'diagram', {
        'id': 'CP2_Flowchart_Diagram',
        'name': 'Bản Tin Câu Hỏi Tồn TA - Luồng Hoạt Động'
    })
    
    model = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '1422',
        'dy': '850',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '1650',
        'pageHeight': '1120',
        'math': '0',
        'shadow': '0'
    })
    
    root = ET.SubElement(model, 'root')
    
    # Base cells
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    def add_cell(cell_id, value, style, x, y, w, h, parent='1', is_edge=False, source=None, target=None):
        attribs = {
            'id': cell_id,
            'parent': parent
        }
        if value:
            attribs['value'] = value
        if style:
            attribs['style'] = style
            
        if is_edge:
            attribs['edge'] = '1'
            if source:
                attribs['source'] = source
            if target:
                attribs['target'] = target
            cell = ET.SubElement(root, 'mxCell', attribs)
            geo = ET.SubElement(cell, 'mxGeometry', {'relative': '1', 'as': 'geometry'})
        else:
            attribs['vertex'] = '1'
            cell = ET.SubElement(root, 'mxCell', attribs)
            geo = ET.SubElement(cell, 'mxGeometry', {
                'x': str(x),
                'y': str(y),
                'width': str(w),
                'height': str(h),
                'as': 'geometry'
            })
        return cell

    # Banner Header
    header_val = (
        "<b>MINI HACKATHON AI (BATCH 04 - LỚP 3A - PHÒNG E403) · TRACK B2</b><br>"
        "<span style='font-size: 16px; font-weight: bold;'>SƠ ĐỒ LUỒNG HOẠT ĐỘNG (FLOWCHART CP2): BẢN TIN CÂU HỎI TỒN & ĐIỀU HƯỚNG TRỰC TIẾP CHO TA</span><br>"
        "<span style='font-size: 12px; color: #495057;'>Lát cắt: TA vào ca trực → Xem bản tin AI gom nhóm câu hỏi &gt;4h → Bấm link Jump URL nhảy vào Discord → Trả lời dứt điểm học viên</span>"
    )
    add_cell('header_banner', header_val, 
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#e9ecef;strokeColor=#adb5bd;fontColor=#212529;align=center;verticalAlign=middle;strokeWidth=1;',
             40, 20, 1560, 65)

    # 4 Swimlanes
    # 1. Discord & Học viên
    add_cell('lane_discord', '<b>1. KÊNH DISCORD & HỌC VIÊN</b><br><span style="font-size:11px;font-weight:normal;">Nguồn phát sinh tin nhắn & nơi tiếp nhận phản hồi</span>',
             'swimlane;startSize=35;fillColor=#f8f9fa;strokeColor=#495057;fontStyle=1;fontSize=13;align=center;horizontal=1;container=1;collapsible=0;',
             40, 95, 360, 910)
             
    # 2. Hệ thống Backend & AI Engine
    add_cell('lane_ai', '<b>2. BỘ MÁY AI & XỬ LÝ DỮ LIỆU</b><br><span style="font-size:11px;font-weight:normal;">Quét log, tính SLA, phân cụm chủ đề, sinh Jump URL</span>',
             'swimlane;startSize=35;fillColor=#f3f0ff;strokeColor=#7048e8;fontStyle=1;fontSize=13;align=center;horizontal=1;container=1;collapsible=0;',
             420, 95, 380, 910)
             
    # 3. Giao diện Bản tin TA (Dashboard)
    add_cell('lane_dashboard', '<b>3. BẢN TIN TỔNG HỢP (DASHBOARD CHO TA)</b><br><span style="font-size:11px;font-weight:normal;">Giao diện trực quan phân cụm & cung cấp Jump URL</span>',
             'swimlane;startSize=35;fillColor=#e7f5ff;strokeColor=#1c7ed6;fontStyle=1;fontSize=13;align=center;horizontal=1;container=1;collapsible=0;',
             820, 95, 380, 910)
             
    # 4. Trợ giảng (TA / Moderator)
    add_cell('lane_ta', '<b>4. TRỢ GIẢNG (TA / MODERATOR TRỰC CA)</b><br><span style="font-size:11px;font-weight:normal;">Duyệt thông tin, phản hồi chính thức & đóng ticket</span>',
             'swimlane;startSize=35;fillColor=#e6fcf5;strokeColor=#0ca678;fontStyle=1;fontSize=13;align=center;horizontal=1;container=1;collapsible=0;',
             1220, 95, 380, 910)

    # --- NODES IN LANE 1: DISCORD & HỌC VIÊN ---
    add_cell('node_a1', 
             '<b>BẮT ĐẦU</b><br>Học viên gửi tin nhắn lên kênh Discord<br><i style="font-size:11px;color:#495057;">(Ví dụ: "có điểm danh ws không ạ" M69081)</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#495057;strokeWidth=2;fontColor=#212529;fontSize=12;align=center;',
             70, 150, 300, 60)
             
    add_cell('node_a2',
             '<b>Tin nhắn chưa có reply</b><br>Bị trôi giữa hàng trăm tin chat thảo luận / bot spam trong kênh',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#adb5bd;strokeWidth=1;dashed=1;fontColor=#495057;fontSize=12;align=center;',
             70, 240, 300, 50)
             
    add_cell('node_a3',
             '<b>MỞ DISCORD TẠI VỊ TRÍ GỐC</b><br>Discord App/Web nhảy chính xác tới tin nhắn <i>(Jump URL target: msg_id)</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#edf2ff;strokeColor=#4263eb;strokeWidth=2;fontColor=#1c7ed6;fontSize=12;align=center;',
             70, 620, 300, 60)
             
    add_cell('node_a4',
             '<b>KẾT THÚC THÀNH CÔNG</b><br>Học viên nhận được giải đáp chính thức kịp thời, an tâm nộp bài / tham gia buổi học',
             'ellipse;whiteSpace=wrap;html=1;fillColor=#d3f9d8;strokeColor=#2b8a3e;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             70, 810, 300, 65)

    # --- NODES IN LANE 2: AI & BACKEND ---
    add_cell('node_b1',
             '<b>Cron Job Quét Tin Nhắn Định Kỳ</b><br>Tải dữ liệu tin nhắn mới từ các kênh Discord (mỗi 15–30 phút)',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7048e8;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             460, 150, 300, 55)
             
    add_cell('node_b2',
             '<b>Kiểm Tra SLA Tồn Đọng</b><br>Tin nhắn có chứa câu hỏi VÀ chưa có ai trả lời sau &gt; 4 giờ?',
             'rhombus;whiteSpace=wrap;html=1;fillColor=#f3d9fa;strokeColor=#ae3ec9;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             480, 235, 260, 75)
             
    add_cell('node_b2_no',
             '<b>Bỏ Qua / Giữ Theo Dõi</b><br>Chưa đủ 4h hoặc đã có người trả lời',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#f8f9fa;strokeColor=#ced4da;fontColor=#868e96;fontSize=11;align=center;',
             480, 335, 260, 40)
             
    add_cell('node_b3',
             '<b>AI CORE: Phân Tích & Phân Cụm</b><br>LLM phân loại chủ đề (Workshop, Lab, Phoenix, Logistics) & Đánh giá mức độ rõ ràng',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#d0bfff;strokeColor=#5f3dc4;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             460, 405, 300, 60)
             
    add_cell('node_b4',
             '<b>Phân Nhánh 4 Đường Đi</b><br>Kiểm tra độ rõ &amp; phạm vi câu hỏi<br><i>(4 Lớp Chỗ Khó §5 Spec)</i>',
             'rhombus;whiteSpace=wrap;html=1;fillColor=#fff3bf;strokeColor=#f59f00;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             490, 490, 240, 75)
             
    add_cell('node_b5',
             '<b>TỔNG HỢP BẢN TIN CẤU TRÚC</b><br>1. Trích xuất câu hỏi tóm lược<br>2. Tạo Jump URL trực tiếp tới tin nhắn<br>3. Gợi ý hướng giải quyết/tài liệu liên quan',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7048e8;strokeWidth=2;fontColor=#212529;fontSize=12;align=center;',
             460, 620, 300, 70)
             
    add_cell('node_b6',
             '<b>Ghi Nhận Feedback & Tinh Chỉnh</b><br>Lưu log sửa nhãn / xác nhận của TA để tinh chỉnh prompt & bộ lọc ở lượt sau <i>(HAX G15)</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#f3f0ff;strokeColor=#7048e8;strokeWidth=1;dashed=1;fontColor=#495057;fontSize=11;align=center;',
             460, 890, 300, 50)

    # --- NODES IN LANE 3: DASHBOARD BẢN TIN ---
    add_cell('node_c1',
             '<b>TA MỞ DASHBOARD BẢN TIN</b><br>Đăng nhập vào ca trực, tải dữ liệu tổng hợp mới nhất',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#1c7ed6;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             860, 150, 300, 55)
             
    add_cell('node_c2',
             '<b>Header Thống Kê & Bộ Lọc Ca Trực</b><br>• Tổng tồn: <b>X câu</b> (&gt;4h chưa rep)<br>• Cụm: Workshop (A) | Lab (B) | Phoenix (C)<br>• Bộ lọc theo kênh: <i>channel_01</i> đến <i>12</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#e7f5ff;strokeColor=#1c7ed6;strokeWidth=1.5;fontColor=#1864ab;fontSize=12;align=center;',
             860, 235, 300, 70)
             
    # Cards for different paths in Dashboard
    add_cell('node_c3_happy',
             '<b>[ĐƯỜNG 1 - HAPPY PATH]</b><br>Thẻ câu hỏi rõ ràng &gt;4h<br><b>Nút: [🔗 Nhảy tới Discord]</b> + Gợi ý giải đáp',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#d3f9d8;strokeColor=#2b8a3e;strokeWidth=2;fontColor=#212529;fontSize=12;align=center;',
             860, 405, 300, 60)
             
    add_cell('node_c3_ambiguous',
             '<b>[ĐƯỜNG 2 - LOW-CONFIDENCE]</b><br>Cảnh báo: <b>[⚠️ Cần làm rõ ngữ cảnh]</b><br>Trích xuất kèm 3 tin nhắn liền kề để TA nắm thông tin',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#fff9db;strokeColor=#f59f00;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             860, 485, 300, 65)
             
    add_cell('node_c3_spam',
             '<b>[ĐƯỜNG 3 - OUT-OF-SCOPE]</b><br>Gắn nhãn: <b>[Tán gẫu / Bot spam]</b><br>Tự động ẩn hoặc nút: <i>[Bỏ qua - Không phải câu hỏi]</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe3e3;strokeColor=#e03131;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             860, 565, 300, 50)
             
    add_cell('node_c4',
             '<b>CẬP NHẬT TRẠNG THÁI REALTIME</b><br>Thẻ câu hỏi chuyển trạng thái <b>[Đã giải quyết]</b>, ẩn khỏi hàng đợi ưu tiên',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#d3f9d8;strokeColor=#2b8a3e;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             860, 740, 300, 55)
             
    add_cell('node_c5',
             '<b>BÁO CÁO KẾT THÚC CA TRỰC</b><br>Số câu tồn đã xử lý: 100% · Tự động xuất tóm tắt bàn giao cho TA ca trực kế tiếp',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#d0ebff;strokeColor=#1864ab;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             860, 825, 300, 55)

    # --- NODES IN LANE 4: HÀNH ĐỘNG CỦA TA ---
    add_cell('node_d1',
             '<b>TA Rà Soát Danh Sách Ưu Tiên</b><br>Xem theo thứ tự thời gian chờ lâu nhất hoặc cụm chủ đề khẩn cấp (Workshop/Lab)',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0ca678;strokeWidth=1.5;fontColor=#212529;fontSize=12;align=center;',
             1260, 240, 300, 60)
             
    add_cell('node_d2',
             '<b>TA Click [🔗 Nhảy tới Discord]</b><br>Trình duyệt / Discord Client tự động mở đúng kênh và cuộn tới tin nhắn học viên',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#2b8a3e;strokeWidth=2;fontColor=#2b8a3e;fontSize=12;fontStyle=1;align=center;',
             1260, 405, 300, 60)
             
    add_cell('node_d2_ambiguous',
             '<b>TA Click Xem Ngữ Cảnh Thảo Luận</b><br>Đọc các tin nhắn xung quanh, tag học viên hỏi thêm thông tin lỗi cụ thể <i>(HAX G10)</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#f59f00;strokeWidth=1.5;fontColor=#d9480f;fontSize=12;align=center;',
             1260, 485, 300, 65)
             
    add_cell('node_d3',
             '<b>TA Phản Hồi Trực Tiếp Cho Học Viên</b><br>Soạn câu trả lời giải đáp trên Discord (hoặc chỉnh sửa từ gợi ý của AI)',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0ca678;strokeWidth=2;fontColor=#212529;fontSize=12;align=center;',
             1260, 625, 300, 60)
             
    add_cell('node_d4',
             '<b>TA Click [Xác Nhận Đã Xử Lý]</b><br>Quay lại Dashboard, tích xác nhận để hoàn tất hỗ trợ câu hỏi này',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#c3fae8;strokeColor=#087f5b;strokeWidth=2;fontColor=#212529;fontSize=12;fontStyle=1;align=center;',
             1260, 740, 300, 55)
             
    add_cell('node_d5_correction',
             '<b>[ĐƯỜNG 4 - SỬA ĐỔI / FEEDBACK]</b><br>TA bấm nút: <i>[Sửa chủ đề]</i> hoặc <i>[Đã có bạn học trả lời]</i> để điều chỉnh hệ thống <i>(HAX G9)</i>',
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#7048e8;strokeWidth=1.5;dashed=1;fontColor=#212529;fontSize=12;align=center;',
             1260, 890, 300, 50)

    # --- EDGES / CONNECTIONS ---
    def add_edge(edge_id, source, target, label='', style=''):
        default_style = 'edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#495057;strokeWidth=1.5;fontSize=11;'
        final_style = default_style + style
        add_cell(edge_id, label, final_style, 0, 0, 0, 0, is_edge=True, source=source, target=target)

    # Main flow connections
    add_edge('e1', 'node_a1', 'node_a2', 'Chờ xử lý')
    add_edge('e2', 'node_a2', 'node_b1', 'Quét tin nhắn')
    add_edge('e3', 'node_b1', 'node_b2')
    add_edge('e4', 'node_b2', 'node_b2_no', 'KHÔNG (&lt;4h)', 'strokeColor=#868e96;')
    add_edge('e5', 'node_b2', 'node_b3', 'CÓ (&gt;4h tồn)', 'strokeColor=#ae3ec9;strokeWidth=2;')
    add_edge('e6', 'node_b3', 'node_b4')
    
    # Branching from Node B4
    add_edge('e7_happy', 'node_b4', 'node_b5', 'Rõ ràng &gt;80%', 'strokeColor=#2b8a3e;strokeWidth=2;')
    add_edge('e7_ambig', 'node_b4', 'node_c3_ambiguous', 'Mơ hồ / thiếu context', 'strokeColor=#f59f00;strokeWidth=2;')
    add_edge('e7_spam', 'node_b4', 'node_c3_spam', 'Tán gẫu / Bot', 'strokeColor=#e03131;strokeWidth=1.5;')
    
    add_edge('e8', 'node_b5', 'node_c3_happy', 'Đẩy vào bản tin', 'strokeColor=#2b8a3e;strokeWidth=2;')
    
    # Dashboard to TA interactions
    add_edge('e9', 'node_c1', 'node_c2')
    add_edge('e10', 'node_c2', 'node_d1', 'TA duyệt danh sách')
    add_edge('e11', 'node_d1', 'node_c3_happy', 'Chọn câu hỏi ưu tiên')
    add_edge('e12', 'node_c3_happy', 'node_d2', 'Bấm nút Jump URL', 'strokeColor=#2b8a3e;strokeWidth=2;')
    add_edge('e13', 'node_d2', 'node_a3', 'Mở Discord Client', 'strokeColor=#4263eb;strokeWidth=2;')
    add_edge('e14', 'node_a3', 'node_d3', 'Xem nội dung gốc')
    add_edge('e15', 'node_d3', 'node_a4', 'Gửi lời giải đáp', 'strokeColor=#2b8a3e;strokeWidth=2;')
    add_edge('e16', 'node_d3', 'node_d4', 'Quay lại Dashboard')
    add_edge('e17', 'node_d4', 'node_c4', 'Tích đã xử lý', 'strokeColor=#087f5b;strokeWidth=2;')
    add_edge('e18', 'node_c4', 'node_c5', 'Ca trực hoàn tất')
    
    # Alternative path connections
    add_edge('e19', 'node_c3_ambiguous', 'node_d2_ambiguous', 'TA xử lý case mơ hồ', 'strokeColor=#f59f00;')
    add_edge('e20', 'node_d2_ambiguous', 'node_a3', 'Vào thread hỏi thêm', 'strokeColor=#f59f00;')
    add_edge('e21', 'node_d5_correction', 'node_b6', 'Phản hồi sửa lỗi AI', 'strokeColor=#7048e8;dashed=1;')

    # Legend / Box Ghi chú
    legend_val = (
        "<b>CHÚ GIẢI (LEGEND & NGUYÊN TẮC HAX/PAIR ĐÃ ÁP DỤNG):</b><br>"
        "• <span style='color:#2b8a3e;font-weight:bold;'>Đường 1 (Xanh lá - Happy Path):</span> Câu hỏi rõ ràng &gt;4h → Jump URL Discord → TA reply giải quyết dứt điểm.<br>"
        "• <span style='color:#f59f00;font-weight:bold;'>Đường 2 (Vàng - Low-confidence):</span> Câu hỏi mơ hồ → Gắn cờ cảnh báo & trích xuất ngữ cảnh (HAX G10: Thu hẹp khi nghi ngờ).<br>"
        "• <span style='color:#e03131;font-weight:bold;'>Đường 3 (Đỏ - Out-of-scope):</span> Tán gẫu / Bot spam → Tự động lọc / TA bỏ qua dễ dàng (HAX G8: Gạt bỏ dễ dàng).<br>"
        "• <span style='color:#7048e8;font-weight:bold;'>Đường 4 (Tím nét đứt - Correction):</span> TA sửa nhãn phân cụm hoặc ghi nhận bạn học đã giải đáp (HAX G9 & G15: Sửa & Feedback)."
    )
    add_cell('legend_box', legend_val,
             'rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#495057;strokeWidth=1;fontColor=#212529;fontSize=11;align=left;verticalAlign=middle;spacingLeft=15;',
             40, 1015, 1560, 75)

    return ET.tostring(mxfile, encoding='utf-8', method='xml').decode('utf-8')

xml_content = create_drawio_xml()
reparsed = minidom.parseString(xml_content)
pretty_xml = reparsed.toprettyxml(indent='  ')

with open('cp2_flowchart.drawio.xml', 'w', encoding='utf-8') as f:
    f.write(pretty_xml)

with open('cp2_flowchart.xml', 'w', encoding='utf-8') as f:
    f.write(pretty_xml)

print("Created cp2_flowchart.drawio.xml and cp2_flowchart.xml successfully!")
