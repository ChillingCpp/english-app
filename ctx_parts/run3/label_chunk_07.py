import io, sys, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

INP = r'E:\vibe_coding\english-app\ctx_input\chunk_07.json'
OUT = r'E:\vibe_coding\english-app\ctx_parts\run3\chunk_07.txt'

data = json.load(open(INP, encoding='utf-8'))

def has(t, *phrases):
    for p in phrases:
        if ' ' in p.strip():
            if p.strip() in t:
                return True
        else:
            if re.search(r'(?<![\wÀ-ỹ])' + re.escape(p) + r'(?![\wÀ-ỹ])', t):
                return True
    return False

def label_meaning(word, m):
    t = m.lower()
    L = []
    def add(x):
        if x not in L and len(L) < 4:
            L.append(x)
    # --- religion ---
    if has(t, 'chúa', 'thượng đế', 'cha cố', 'tu viện', 'giáo hoàng', 'tín đồ', 'quây-cơ',
           'thần vận mệnh', 'thần tài', 'ăn chay', 'kính sợ', 'con chiên', 'bầy chiên', 'đàn chiên'):
        add('religion')
    # --- military ---
    if has(t, 'quân đội', 'quân lực', 'trận đánh', 'trận tuyến', 'chiến đấu', 'chiến tranh',
           'vũ lực', 'súng', 'đạn', 'bom', 'pháo đài', 'công sự', 'phòng thủ', 'mặt trận',
           'hành quân', 'phi đội', 'không quân', 'đô đốc', 'gươm', 'lá chắn',
           'phù hiệu', 'huy hiệu', 'tàu chiến', 'xông vào', 'xông lên', 'ngăn chặn',
           'đẩy lui', 'tra tấn', 'tường thành', 'hiếu chiến', 'binh ', 'bộ binh', 'hỏa lực',
           'hoả lực', 'thất thủ'):
        add('military')
    if has(t, 'kiếm') and not has(t, 'đánh kiếm', 'đấu kiếm', 'kiếm được'):
        add('military')
    # --- law / crime ---
    if has(t, 'tòa', 'luật', 'phạt', 'tội', 'kiện', 'tranh chấp', 'tuyên án', 'công bằng',
           'công lý', 'ép buộc', 'cưỡng ép', 'cưỡng đoạt', 'xét xử'):
        add('law')
    if has(t, 'trộm', 'cắp', 'oa trữ', 'ăn cắp', 'băng đảng', 'gian lận', 'lừa', 'hối lộ',
           'trả thù', 'trả đũa', 'dối trá', 'lừa dối', 'giả dối', 'lừa bịp', 'kẻ cắp'):
        add('crime')
    if has(t, 'tiền phạt', 'phạt vạ'):
        add('money')
    # --- government / politics ---
    if has(t, 'nhà nước', 'chính phủ', 'quốc hội', 'nghị viện', 'liên bang', 'quốc khánh',
           'thuế', 'trạm thu thuế'):
        add('government')
    if has(t, 'chính trị', 'bầu cử', 'nghị viện', 'liên bang', 'nước ngoài', 'ngoại quốc',
           'tự do', 'tự quyết', 'tuyên truyền', 'cổ động', 'sủng thần', 'ái thiếp',
           'quý phi', 'lãnh địa', 'thái ấp', 'đặc quyền'):
        add('politics')
    # --- finance / business / money / economy / shopping ---
    if has(t, 'tài chính', 'quỹ', 'vốn', 'lãi', 'cổ phần', 'chứng khoán', 'công trái',
           'thu nhập', 'lợi nhuận', 'đảo nợ', 'đổi nợ', 'cấp vốn', 'tài trợ', 'ngân hàng',
           'nợ', 'của cải', 'tiền của', 'lợi tức', 'lưu hành', 'lưu thông',
           'kiếm được', 'thu được', 'lợi lộc'):
        add('finance')
    if has(t, 'công ty', 'hãng', 'kinh doanh', 'thương nghiệp', 'cửa hàng', 'buôn bán',
           'thành lập', 'hàng hoá', 'hàng hóa', 'hồ sơ'):
        add('business')
    if has(t, 'tiền', 'lương', 'phí', 'hóa đơn', 'thanh toán', 'vé', 'mua', 'bán',
           'thuê', 'xu rượu', 'bảng anh', 'giá cả', 'sụt giá', 'giảm giá', 'thù lao',
           'gia sản', 'ế ẩm') and 'tiền đạo' not in t:
        add('money')
    if has(t, 'sụt giá', 'giảm giá', 'ghi giá', 'báo giá', 'giá cả', 'giá thấp',
           'giá sàn', 'giá thành', 'định giá', 'phá giá', 'giá trị'):
        add('money')
    if has(t, 'kinh tế', 'thị trường'):
        add('economy')
    if has(t, 'siêu thị', 'mua sắm', 'khách hàng'):
        add('shopping')
    # --- work / career / management ---
    if has(t, 'công việc', 'nghề', 'thợ', 'nhân công', 'chức vụ', 'sa thải', 'đuổi việc',
           'thăng chức', 'đồng nghiệp', 'chủ trại', 'tá điền', 'việc làm', 'giúp việc',
           'người hầu', 'làm thuê', 'đồ nghề', 'viện sĩ', 'hội viên', 'giám đốc',
           'sửa chữa', 'thù lao', 'giũa', 'đồng áng'):
        add('work')
        if has(t, 'nghề', 'sự nghiệp', 'thăng chức', 'chức vụ'):
            add('career')
    if has(t, 'quản lý', 'tổ chức', 'sắp xếp', 'bố trí', 'điều hành', 'xúc tiến', 'đẩy mạnh'):
        add('management')
    # --- farming ---
    if has(t, 'ruộng', 'đồng áng', 'trồng trọt', 'cày cấy', 'làm ruộng', 'trang trại',
           'đồn điền', 'nông trường', 'nông dân', 'tá điền', 'đồng cỏ', 'làm vườn',
           'thu hoạch', 'vụ mùa', 'mùa màng', 'màu mỡ', 'quạt thóc', 'quạt lúa',
           'thóc', 'lúa', 'thuốc lá', 'chè', 'hoa màu', 'chủ trại'):
        add('farming')
    # --- education ---
    if (has(t, 'học sinh', 'giáo dục', 'đào tạo', 'kỳ thi', 'tốt nghiệp',
            'học phí', 'đại học', 'thuộc bài', 'phân từ', 'danh động từ', 'nguyên âm',
            'phát âm', 'ngôn ngữ', 'làm tính', 'số học', 'tính toán', 'hàm số', 'tu từ',
            'làm bài', 'bài tập', 'bài kiểm tra', 'bài thi', 'nghiên cứu sinh',
            'am hiểu', 'thông thạo', 'thành thạo')
            and 'màng' not in t):
        add('education')
    if has(t, 'trường') and not has(t, 'chiến trường', 'nông trường') and 'màng' not in t:
        add('education')
    if has(t, 'lớp') and 'màng' not in t:
        add('education')
    # --- science ---
    if has(t, 'khoa học', 'hóa học', 'vật lý', 'thí nghiệm', 'năng lượng',
           'tần số', 'khử trùng', 'chòm sao', 'giả thiết', 'giả thuyết', 'số học', 'tính toán',
           'hàm số'):
        add('science')
    if has(t, 'khí') and not has(t, 'khách khí', 'không khí'):
        add('science')
    # --- technology / internet ---
    if has(t, 'máy tính', 'phần mềm', 'tập tin', 'dữ liệu', 'máy nổ',
           'động cơ', 'guồng', 'ắc quy', 'ròng rọc', 'hoàn ngược',
           'chân vịt', 'cánh quạt'):
        add('technology')
    elif has(t, 'máy') and not has(t, 'máy bay', 'máy ảnh') and 'kiểu cách' not in t:
        add('technology')
    if has(t, 'quạt') and 'hình quạt' not in t:
        add('technology')
    if has(t, 'dữ liệu', 'nguồn cấp', 'mạng internet', 'trực tuyến'):
        add('internet')
    # --- industry / mining / construction / engineering ---
    if has(t, 'khai thác', 'mỏ', 'hầm mỏ', 'đường hầm', 'quặng'):
        add('mining')
    if has(t, 'công nghiệp', 'nhà máy', 'nung', 'luyện kim', 'luyện thép', 'nhiên liệu',
            'chất đốt', 'sấy', 'đốn', 'xẻ gỗ', 'gỗ xẻ', 'than'):
        add('industry')
    if has(t, 'gỗ') and 'bóng gỗ' not in t:
        add('industry')
    if has(t, 'chặt, hạ') and 'chặt chẽ' not in t:
        add('industry')
    if has(t, 'xây', 'xây dựng', 'lát ', 'làm sàn', 'lát sàn', 'đắp', 'khởi công',
           'lấp ', 'nền đường', 'cầu thang', 'dựng khung', 'hàng rào', 'rào lại'):
        add('construction')
    if has(t, 'kỹ thuật', 'cơ khí', 'chế tạo', 'lắp'):
        add('engineering')
    # --- media / communication ---
    if has(t, 'báo', 'tin ngắn', 'bức điện', 'truyền tin', 'phát thanh', 'truyền hình',
           'phát hành', 'bài báo', 'nhà báo', 'tờ báo', 'tin đồn', 'tuyên truyền', 'cổ động'):
        add('media')
    if has(t, 'thư', 'bức thư', 'liên lạc', 'thông tin', 'tuyên bố', 'cam kết',
           'lời hứa', 'bài báo', 'nhà báo', 'tin ngắn', 'bức điện', 'tin đồn', 'báo',
           'nói ra', 'thốt ra', 'lên tiếng', 'tranh luận', 'tầm phào', 'dông dài',
           'ra hiệu', 'phát biểu', 'ngôn ngữ'):
        add('communication')
    # --- food / cooking / restaurant ---
    if has(t, 'thức ăn', 'món ăn', 'đồ ăn', 'dinh dưỡng', 'bữa ăn', 'bữa chén',
           'bữa tiệc', 'quán ăn', 'nhà hàng', 'suất ăn', 'cho ăn', 'ăn cơm', 'ăn uống',
           'sự ăn', 'suất', 'hàng ăn', 'yến mạch', 'lúa mạch', 'thịt', 'trứng', 'sữa',
           'trái cây', 'hoa quả', 'món cá', 'thịt thú', 'thịt rán', 'bột mì', 'thịnh soạn',
           'giấm', 'no nê', 'rượu', 'bia ', 'bơ ', 'thuỷ sản', 'thủy sản', 'hải sản'):
        add('food')
    if has(t, 'nấu', 'nướng', 'rán', 'xào', 'luộc', 'ướp', 'rắc bột',
           'nhà bếp', 'làm bếp'):
        add('cooking')
        if 'food' not in L:
            add('food')
    if has(t, 'chiên') and not has(t, 'con chiên', 'bầy chiên', 'đàn chiên'):
        add('cooking')
        if 'food' not in L:
            add('food')
    if has(t, 'quán ăn', 'nhà hàng', 'bữa tiệc', 'hàng ăn'):
        add('restaurant')
    # --- home / family / friendship / relationships ---
    if has(t, 'gia đình', 'gia quyến', 'cha, bố', 'người cha', 'người đẻ ra', 'tổ tiên',
           'ông tổ', 'con cái', 'dòng dõi', 'gia thế', 'bà con', 'trẻ em', 'trẻ con',
           'anh em'):
        add('family')
    if has(t, 'trong nhà', 'vật dụng trong nhà', 'nội thất', 'căn hộ', 'căn phòng',
           'dãy phòng', 'sàn nhà', 'mái nhà', 'cổng', 'ga ra', 'nhà để ô tô', 'bếp',
           'giường', 'ghế', 'trại trẻ', 'lò sưởi', 'farm-house'):
        add('home')
    if has(t, 'bạn', 'tình bạn', 'thân thiện', 'hòa đồng', 'thân thuộc', 'quen thuộc',
           'người quen'):
        add('friendship')
    elif has(t, 'ủng hộ', 'giúp đỡ'):
        add('social')
    if has(t, 'người yêu', 'người tình', 'tình nhân', 'ăn nằm', 'cầu hôn', 'cô gái',
           'vợ', 'chồng', 'cưới', 'kết hôn', 'sa ngã'):
        if has(t, 'cưới', 'kết hôn', 'vợ', 'chồng'):
            add('marriage')
        add('relationships')
    # --- animals / plants / nature / environment / weather ---
    if has(t, 'con ếch', 'con nhái', 'ngoé', 'câu cá', 'đánh cá', 'chim', 'ngựa', 'cừu',
           'gà', 'gà chọi', 'chó săn', 'chó', 'mèo', 'thú săn', 'súc vật', 'ruồi',
           'giòi', 'cá bột', 'cá hồi', 'thiên nga', 'con mái', 'bò', 'trâu', 'lợn',
           'heo', 'thỏ', 'nhện', 'mạng nhện', 'chồn', 'cáo', 'chọi', 'cá', 'bắt cá', 'món cá',
           'rắn', 'thú săn', 'thú dữ', 'thú hoang', 'thú nuôi', 'lông thú', 'da thú',
           'thịt thú', 'thuỷ sản', 'thủy sản', 'hải sản'):
        if not has(t, 'cá tính'):
            add('animals')
    if has(t, 'cây', 'cây hoa', 'cây irit', 'hoa', 'bông hoa', 'nở hoa', 'ra hoa',
           'khai hoa', 'vườn', 'làm vườn', 'công viên', 'rừng', 'héo'):
        add('plants')
    if has(t, 'lá') and not has(t, 'lá chắn', 'lá số', 'thuốc lá'):
        add('plants')
    if has(t, 'thác', 'sông', 'biển', 'núi', 'đèo', 'đầm lầy', 'băng tuyết', 'nước ngọt',
           'rừng', 'đồng ruộng', 'cánh đồng', 'môi trường', 'thiên nhiên'):
        add('nature')
    if has(t, 'môi trường', 'ô nhiễm'):
        add('environment')
    if has(t, 'thời tiết', 'mưa', 'tuyết', 'lũ', 'lụt', 'bão', 'gió', 'nắng', 'khí hậu',
           'trời đẹp', 'mùa thu', 'mùa đông', 'mùa hè', 'mùa xuân', 'mùa mưa', 'triều',
           'thuỷ triều', 'thủy triều', 'sương', 'đóng băng', 'đông vì lạnh', 'giá lạnh',
           'đông giá', 'thấy lạnh', 'trời lạnh', 'không khí', 'rét'):
        add('weather')
        if has(t, 'lũ', 'lụt', 'bão'):
            add('safety')
    # --- body / health / medicine / appearance / clothing ---
    if has(t, 'ngón tay', 'bàn chân', 'chân', 'mắt', 'tóc', 'da', 'răng',
           'cơ thể', 'thân hình', 'lông', 'đầu gối', 'trán', 'ngực', 'nội tạng',
           'sờ mó', 'sờ soạng'):
        if 'chân vịt' not in t:
            add('body')
    if has(t, 'ruột') and 'anh em' not in t:
        add('body')
    if has(t, 'tay') and 'găng tay' not in t:
        add('body')
    if has(t, 'xinh', 'bảnh', 'vàng hoe', 'trắng (da)', 'ngoại hình', 'trang điểm',
           'đúng mốt', 'hợp thời trang', 'sang trọng', 'tóc giả', 'nét mặt', 'vẻ mặt',
           'trông giống', 'hình dáng', 'sặc sỡ', 'loè loẹt', 'lòe loẹt', 'mốt', 'thời trang'):
        add('appearance')
    elif has(t, 'đẹp') and 'trời đẹp' not in t:
        add('appearance')
    if has(t, 'quần áo', 'ăn mặc', 'giày', 'mũ', 'găng', 'khuy', 'sơ mi', 'váy', 'áo',
           'quần', 'kiểu cắt', 'may mặc', 'y phục', 'trang phục', 'mốt', 'thời trang',
           'vải', 'che mặt', 'mạng che mặt'):
        add('clothing')
    if has(t, 'sức khỏe', 'sung sức', 'khỏe', 'mập', 'béo phì', 'ốm', 'gầy',
           'mệt', 'đau', 'ngất', 'mưng mủ', 'nhọt', 'cúm', 'cơn sốt', 'bệnh sốt',
           'phát sốt', 'lên sốt', 'sốt rét', 'sốt cao', 'bệnh', 'thuốc men', 'thuốc chữa',
           'uống thuốc', 'tiêm thuốc',
           'chữa', 'khám', 'bác sĩ', 'y tế', 'nhịn ăn', 'nhịn đói', 'ăn kiêng',
           'tập thể dục', 'thể dục', 'chạy bộ', 'mất ngủ', 'ngủ', 'bắt mạch',
           'mạch đập', 'bại liệt', 'què', 'thọt', 'tàn tật', 'chảy máu', 'thấy kinh',
           'kinh nguyệt', 'khử trùng'):
        if has(t, 'cúm', 'cơn sốt', 'bệnh sốt', 'phát sốt', 'lên sốt', 'sốt rét',
               'bệnh', 'thuốc men', 'thuốc chữa', 'uống thuốc', 'tiêm thuốc',
               'mưng mủ', 'nhọt', 'bắt mạch', 'chảy máu', 'thấy kinh', 'kinh nguyệt',
               'khử trùng'):
            add('medicine')
        if has(t, 'tập thể dục', 'thể dục', 'chạy bộ'):
            add('exercise')
        if has(t, 'mất ngủ') or (has(t, 'ngủ') and 'ru ngủ' not in t):
            add('sleep')
        add('health')
    if has(t, 'say') and not has(t, 'say mê', 'say đắm'):
        add('health')
    if has(t, 'béo') and not has(t, 'béo bở', 'than'):
        add('health')
    # --- sports / competition / teamwork / leisure / entertainment / hobby ---
    if has(t, 'bóng đá', 'bóng rổ', 'bóng chày', 'bóng chuyền', 'bóng bàn', 'quả bóng',
           'trái bóng', 'đá bóng', 'chơi bóng', 'sân bóng', 'đội bóng', '(bóng',
           'làm bàn', 'sút bóng', 'sút phạt', 'cú sút',
           'bóng gỗ', 'giao bóng', 'quần vợt', 'bi-a', 'crickê', 'quyền anh',
           'võ sĩ', 'cuộc đua', 'thi đấu', 'trận đấu', 'chung kết', 'ván bài', 'ván cờ',
           'cờ vua', 'cờ tướng', 'đánh cờ', 'thể thao', 'vận động viên', 'đấu thủ',
           'ra sân', 'chặn bóng', 'đánh bạc', 'cá cược', 'săn bắn',
           'bắn cung', 'trượt băng', 'điền kinh', 'tiền đạo',
           'tập bắn', 'bắn chim', 'bắn cung', 'bắn (chim', 'đo ván', 'đánh ngã', 'đánh kiếm', 'đấu kiếm',
           'vượt rào', 'nhảy rào', 'chọi', 'keo vật', 'đô vật', 'hâm mộ', 'chèo'):
        add('sports')
    if has(t, 'thi đấu', 'cuộc đua', 'trận đấu', 'chung kết', 'đua', 'đối thủ',
           'vô địch', 'thắng', 'thua'):
        if not (has(t, 'tranh luận', 'đấu tranh')
                and not has(t, 'thi đấu', 'trận đấu', 'cuộc đua', 'vô địch', 'thể thao')):
            add('competition')
    if has(t, 'đồng đội', 'kíp', 'tốp', 'nhóm', 'tập thể', 'đội bóng'):
        add('teamwork')
    if has(t, 'đội') and 'quân đội' not in t:
        add('teamwork')
    if has(t, 'ngày hội', 'lễ hội', 'liên hoan', 'hội diễn', 'diễu hành'):
        add('holiday')
        add('entertainment')
    if has(t, 'trò chơi', 'ván bài', 'ván cờ', 'đánh bạc', 'cá cược', 'khôi hài',
           'hài hước', 'buồn cười', 'diễn viên', 'rạp', 'chiếu bóng', 'quay phim',
           'truyền hình', 'vui đùa', 'vui chơi', 'đùa', 'cợt', 'chơi bóng gỗ'):
        add('entertainment')
    if has(t, 'trò chơi', 'ván bài', 'ván cờ', 'nghỉ mát', 'du lịch', 'đi chơi',
           'nghỉ ngơi', 'chơi ', 'câu cá', 'bóng gỗ'):
        if has(t, 'du lịch'):
            add('tourism')
        add('leisure')
    if has(t, 'sở thích', 'thị hiếu', 'sưu tầm', 'làm cảnh', 'làm vườn', 'câu cá',
           'săn bắn'):
        add('hobby')
    # --- arts / music / literature / photography / design ---
    if has(t, 'tranh biếm', 'tranh khôi hài', 'tranh tượng', 'tranh vẽ',
           'tranh sơn dầu', 'bức tranh', 'tập tranh', 'triển lãm tranh',
           'tượng đài', 'bức tượng', 'pho tượng', 'tạc tượng', 'đúc tượng',
           'trưng bày', 'triển lãm', 'điêu khắc', 'hội họa',
           'nghệ thuật', 'biếm họa', 'phông', 'sân khấu', 'thể loại', 'điệu nhảy',
           'điệu múa', 'nặn'):
        add('arts')
    if has(t, 'nhạc', 'bài hát', 'ca hát', 'âm nhạc', 'quãng', 'nốt', 'nốt gốc',
           'giai điệu', 'đánh đàn', 'búng dây', 'bản nhạc', 'dấu giáng', 'giáng',
           'nhịp điệu'):
        add('music')
    if has(t, 'tiểu thuyết', 'thơ ca', 'thơ ', 'văn ', 'văn học', 'tác phẩm', 'truyện',
           'sách', 'đoạn thơ', 'hư cấu', 'viễn tưởng', 'nhân vật', 'thể loại', 'tu từ'):
        if has(t, 'lá số tử vi'):
            add('culture')
        else:
            add('literature')
    if has(t, 'máy ảnh', 'chụp ảnh', 'phim ảnh', 'giấy ảnh', 'quay phim', 'tiêu điểm'):
        add('photography')
    if has(t, 'chiếu bóng', 'rạp', 'quay phim', 'phim ảnh', 'truyền hình'):
        add('entertainment')
        add('media')
    if has(t, 'thời trang', 'đúng mốt', 'hợp thời trang', 'mốt', 'kiểu cách', 'kiểu ',
           'thiết kế', 'trang trí', 'trang hoàng', 'hình dáng', 'hình vẽ', 'minh họa',
           'sơ đồ', 'bố cục'):
        add('design')
    # --- travel / transportation / tourism ---
    if has(t, 'du lịch', 'nghỉ mát', 'khách sạn', 'hành lý', 'hộ chiếu', 'lữ hành',
           'chuyến bay', 'chuyến đi', 'hành trình', 'máy bay', 'lái máy bay',
           'nước ngoài', 'ngoại quốc'):
        add('travel')
    if has(t, 'du lịch', 'nghỉ mát', 'khách sạn', 'lữ hành'):
        add('tourism')
    if has(t, 'tàu', 'xe', 'ô tô', 'xe lửa', 'đường sắt', 'đường ray', 'đường bộ',
           'đường đi', 'đường phố', 'đường thủy', 'dọc đường', 'đường ghi', 'ngã ba',
           'ngã tư', 'thuyền', 'buồm', 'vận chuyển', 'chở hàng', 'sân bay', 'bến',
           'bến tàu', 'chân vịt', 'cánh quạt', 'toa xe', 'toa tàu', 'lốp', 'xì hơi',
           'xe buýt', 'cây cầu', 'gửi'):
        if not (has(t, 'gửi') and 'cho, gửi, tặng' in t):
            add('transportation')
    # --- feelings / emotions / personality / psychology ---
    if has(t, 'sợ', 'hoảng sợ', 'khiếp', 'kinh khủng', 'khủng khiếp', 'e ngại', 'lo',
           'vui', 'buồn', 'giận', 'xúc động', 'cảm động', 'yêu', 'ghét', 'ghen',
           'xấu hổ', 'hạnh phúc', 'thất vọng', 'hăng hái', 'nhiệt tình', 'sốt sắng',
           'phấn khởi', 'bồn chồn', 'kích động', 'cảm hứng', 'say mê', 'quyến rũ',
           'mê', 'mến', 'nhớ', 'quên', 'tha thứ', 'tự hào', 'hy vọng',
           'thoả mãn', 'thỏa mãn', 'kinh sợ', 'khích động', 'may mắn'):
        add('emotions')
        add('feelings')
    if has(t, 'thích') and 'phóng thích' not in t:
        add('emotions')
        add('feelings')
    if has(t, 'thương') and not has(t, 'thương nghiệp', 'thương mại'):
        if 'emotions' not in L:
            add('emotions')
            add('feelings')
    if has(t, 'hiền', 'dịu dàng', 'hòa nhã', 'dũng cảm', 'gan dạ', 'anh dũng',
           'hào phóng', 'rộng lượng', 'khoan hồng', 'trung thành', 'trung thực',
           'kiên quyết', 'vững vàng', 'xấc', 'láo', 'trơ tráo', 'trơ trẽn', 'suồng sã',
           'sỗ sàng', 'kiêu căng', 'ngạo mạn', 'lập dị', 'kỳ cục', 'đồng bóng',
           'cầu kỳ', 'kiểu cách', 'khó tính', 'lịch sự', 'lễ phép', 'lịch thiệp',
           'cao quý', 'trâm anh', 'quyền quý', 'xảo quyệt', 'quỷ quyệt', 'gian xảo',
           'thật thà', 'ngay thẳng', 'thẳng thắn', 'cá tính', 'dối trá', 'lừa dối',
           'giả dối', 'hiếu chiến'):
        add('personality')
    if has(t, 'tâm lý', 'tính cách', 'cảm giác', 'cảm tưởng', 'cảm xúc', 'tình cảm',
           'trí tưởng tượng', 'óc tưởng tượng', 'hồi tưởng', 'ấn tượng', 'tập trung',
           'suy nghĩ'):
        add('psychology')
    # --- time ---
    if has(t, 'tháng', 'ngày thứ sáu', 'ngày', 'thứ hai', 'thứ ba', 'thứ tư',
           'thứ năm', 'thứ sáu', 'thứ bảy', 'chủ nhật', 'tương lai', 'mãi mãi',
           'vĩnh viễn', 'thường xuyên', 'hằng ngày', 'mỗi ngày',
           'ban đêm', 'ban ngày', 'mùa', 'những năm', 'năm tuổi', 'hằng năm',
           'mỗi năm', 'cả năm', 'thập niên', 'thế kỷ', 'thế hệ', 'thời kỳ', 'thời gian',
           'giờ', 'giây', 'đồng hồ', 'thời vụ', 'đến hạn', 'sớm', 'xưa',
           'giây lát'):
        add('time')
    if has(t, 'buổi') and not has(t, 'chiếu', 'buổi lễ', 'buổi họp'):
        add('time')
    # --- history / geography / culture / philosophy ---
    if has(t, 'lịch sử', 'từ cổ', 'nghĩa cổ', 'thời cổ', 'sụp đổ', 'suy sụp'):
        if has(t, 'lịch sử', 'từ cổ', 'nghĩa cổ', 'thời cổ'):
            add('history')
        if has(t, 'sụp đổ', 'suy sụp'):
            add('politics')
    if has(t, 'địa lý', 'bản đồ', 'lãnh thổ', 'biên giới', 'đất nước', 'đèo'):
        add('geography')
    if has(t, 'văn hóa', 'phong tục', 'tập quán', 'truyền thống', 'dân tộc', 'dân gian',
           'tín ngưỡng', 'di sản', 'chủng tộc'):
        add('culture')
    if has(t, 'triết học', 'luân lý', 'đạo đức'):
        add('philosophy')
    # --- formal / informal ---
    if has(t, 'trang trọng', 'nghi thức', 'nghi lễ', 'chính thức', 'thể thức',
           'thủ tục', 'quy tắc', 'quy định', 'luật lệ'):
        add('formal')
    if has(t, 'thông tục', 'tiếng lóng', 'lóng', 'đùa cợt', 'suồng sã', 'thân mật',
           'con mụ', 'anh chàng', 'gã'):
        add('informal')
    # --- urban / rural ---
    if has(t, 'thành phố', 'đô thị', 'thủ đô', 'khu phố'):
        add('urban')
    if has(t, 'nông thôn', 'làng quê', 'miền quê', 'vùng quê'):
        add('rural')
    # --- success ---
    if has(t, 'thành công', 'thắng lợi', 'vượt qua', 'chiến thắng', 'thành đạt',
           'thịnh vượng', 'giàu có', 'phát đạt', 'có tên tuổi', 'vai vế'):
        add('success')
    # --- safety ---
    if has(t, 'an toàn', 'nguy hiểm', 'cứu đắm', 'cứu hộ', 'cứu nạn', 'bảo vệ',
           'che chở', 'thoát hiểm', 'hoả hoạn', 'cháy nhà', 'cháy rừng'):
        add('safety')
    # --- daily life ---
    if has(t, 'hằng ngày', 'mỗi ngày', 'đời sống', 'sinh hoạt', 'gia dụng'):
        add('daily life')
    if has(t, 'mâu thuẫn', 'họp mặt'):
        add('social')
    # --- glue words (prepositions, numbers, ordinals) ---
    if has(t, 'thay cho', 'thế cho', 'đại diện', 'ủng hộ', 'về phe', 'với mục đích',
           'mặc dù', 'đối với', 'so với', 'trong (thời gian)', 'bởi vì', 'tại vì',
           'rời xa', 'của (ai', 'thứ nhất', 'trước tiên', 'trước hết', 'đầu tiên',
           'thứ năm', 'thứ tư', 'một phần', 'con số', 'cho, gửi, tặng'):
        if not L:
            add('general')
        if len(L) == 1 and L[0] == 'general':
            return L
    if not L:
        add('general')
    return L[:4]

lines = []
for entry in data:
    w = entry['word']
    for i, m in enumerate(entry['meanings'], start=1):
        labs = label_meaning(w, m)
        lines.append(f"{w}\t{i}\t{', '.join(labs)}")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(lines) + '\n')

nw = len(data)
nm = sum(len(e['meanings']) for e in data)
print(f"words={nw} meanings={nm} lines={len(lines)}")
