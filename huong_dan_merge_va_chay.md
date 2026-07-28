# 🚀 HƯỚNG DẪN MERGE CODE & CHẠY APP HOÀN CHỈNH — ROLE 4

> **Bạn là**: Trịnh Hải Đăng (Role 4 - Core Developer/Integrator)  
> **Nhiệm vụ**: Gom toàn bộ code của nhóm, merge, chạy ổn định cho mọi người

---

## 📋 TỔNG QUAN LUỒNG CÔNG VIỆC

```
[Role 1] config/test_cases.json  ┐
[Role 2] src/tools.py            ├──► git push ──► GitHub ──► git pull (bạn) ──► merge ──► python src/app.py ✅
[Role 3] src/prompts.py          ┘
```

---

## 🔧 BƯỚC 1: CÀI ĐẶT MÔI TRƯỜNG (Chỉ làm 1 lần)

### 1.1 Kích hoạt virtual environment
```powershell
# Nếu đã có .venv (như bạn đang dùng)
.venv\Scripts\activate
```

### 1.2 Cài tất cả thư viện
```powershell
pip install -r requirements.txt
```

### 1.3 Tạo file .env từ .env.example
```powershell
copy .env.example .env
```

> ⚠️ **Quan trọng**: Mở file `.env` và điền API key thực. Không để nguyên `your_xxx_key_here`

---

## 🔑 BƯỚC 2: CẤU HÌNH FILE .env

Mở file `.env` và chỉnh sửa theo AI bạn có API key:

```env
# Chọn 1 trong 4 provider: gemini | openai | anthropic | openrouter | mock
LLM_PROVIDER=gemini

# Điền API key tương ứng
GEMINI_API_KEY=AIzaSy...key_thật_của_bạn...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
OPENROUTER_API_KEY=sk-or-...

# Để trống = dùng model mặc định
LLM_MODEL=
```

> 💡 **Không có API key?** Dùng `LLM_PROVIDER=mock` để chạy offline không cần key!

---

## 🔄 BƯỚC 3: KÉO CODE MỚI NHẤT TỪ TẤT CẢ CÁC NHÁNH

### 3.1 Xem tất cả nhánh của nhóm
```powershell
git branch -a
```
Bạn sẽ thấy các nhánh: `Binh`, `Liễu`, `Linh`, `v1`, `main`, `haidang2425`

### 3.2 Pull code từ nhánh main (đã được merge)
```powershell
git checkout main
git pull origin main
```

### 3.3 Xem nhánh nào có code mới cần merge
```powershell
git log --oneline --all --graph
```

---

## 🔀 BƯỚC 4: MERGE CÁC NHÁNH VÀO MAIN

### Cách 1: Merge từng nhánh vào main (Khuyên dùng)
```powershell
# Đảm bảo đang ở nhánh main
git checkout main

# Merge nhánh của từng người
git merge origin/Binh      # Role 1 - Văn Linh (test_cases.json)
git merge origin/Linh      # Role 3 - Thu Liễu (prompts.py)
git merge origin/v1        # Role 2 - Chí Vũ (tools.py)
```

### ⚠️ Nếu có CONFLICT khi merge:
```powershell
# Xem file nào bị conflict
git status

# Mở file đó, tìm dấu hiệu conflict và sửa:
# <<<<<<< HEAD
# code của main
# =======
# code của nhánh kia
# >>>>>>> origin/Binh
# 
# → Giữ lại phần đúng, xóa các dấu <<<, ===, >>>

# Sau khi sửa xong:
git add .
git commit -m "fix: resolve merge conflict"
```

---

## ✅ BƯỚC 5: KIỂM TRA CODE TRƯỚC KHI CHẠY

### 5.1 Kiểm tra file test_cases.json (Role 1)
```powershell
python -c "import json; data=json.load(open('config/test_cases.json','r',encoding='utf-8')); print(f'✅ Có {len(data)} test cases'); print(data[0])"
```

### 5.2 Kiểm tra tools.py (Role 2)
```powershell
python -c "from src.tools import get_weather, search_flights; print('✅ tools.py OK'); print(get_weather('Hà Nội'))"
```

### 5.3 Kiểm tra prompts.py (Role 3)
```powershell
python -c "import sys; sys.path.append('src'); from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS; print(f'✅ prompts.py OK - MAX_ITERATIONS={MAX_ITERATIONS}')"
```

### 5.4 Kiểm tra providers.py
```powershell
python -c "import sys; sys.path.append('src'); from providers import get_llm_provider; p=get_llm_provider(); print(f'✅ Provider: {p.__class__.__name__}')"
```

---

## 🚀 BƯỚC 6: CHẠY APP HOÀN CHỈNH

```powershell
python src/app.py
```

### Output mong đợi khi thành công:
```
==================================================
🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT
==================================================
🔌 LLM Provider đang hoạt động: GeminiProvider (Model: gemini-2.5-flash)
✅ Đã tải thành công 5 Test Cases từ config/test_cases.json

--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---
💬 [CHATBOT BASELINE] Câu hỏi: ...
🤖 Chatbot trả lời: ...

--- DEMO 2: CHẠY TRÊN REACT AGENT ---
🤖 [REACT AGENT] Câu hỏi: ...
--- 🔄 Vòng lặp ReAct (Step 1/3) ---
🧠 Thought: ...
🛠️ Action: get_weather['Hà Nội']
👁️ Observation: Thời tiết Hà Nội: 28°C, Nắng nhẹ...
```

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

| Lỗi | Nguyên nhân | Cách sửa |
|-----|------------|----------|
| `ModuleNotFoundError: No module named 'requests'` | Chưa cài thư viện | `pip install -r requirements.txt` |
| `FileNotFoundError: config/test_cases.json` | Role 1 chưa push | Chờ Role 1 push hoặc tạo file tạm |
| `[Gemini Error]: Chưa cấu hình GEMINI_API_KEY` | Chưa điền .env | Mở `.env`, điền API key thật |
| `CONFLICT` khi merge | 2 người sửa cùng file | Sửa thủ công conflict rồi commit |
| `fatal: no upstream branch` | Nhánh chưa link remote | `git push --set-upstream origin haidang2425` |

---

## 📤 BƯỚC 7: PUSH KẾT QUẢ LÊN GITHUB

Sau khi app chạy ổn:
```powershell
# Đảm bảo ở nhánh main (sau merge)
git checkout main
git add .
git commit -m "Moc 3: ReAct Agent Loop & Safeguards - Full Integration"
git push origin main
```

---

## 🎯 TÓM TẮT QUY TRÌNH NHANH (Cheat Sheet)

```powershell
# 1. Bật venv
.venv\Scripts\activate

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo .env (chỉ lần đầu)
copy .env.example .env   # → rồi mở sửa API key

# 4. Kéo code mới nhất
git checkout main
git pull origin main
git merge origin/Binh
git merge origin/Linh
git merge origin/v1

# 5. Chạy app
python src/app.py

# 6. Push lên GitHub
git add .
git commit -m "done: full integration"
git push
```
