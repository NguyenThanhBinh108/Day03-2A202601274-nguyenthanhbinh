# 🚀 ROLE 4 — HƯỚNG DẪN HOÀN CHỈNH (Copy-Paste Sẵn)
> **Trịnh Hải Đăng** | Role 4: Core Developer / Integrator  
> Nhánh làm việc chính: `haidang2425` → merge vào `main`

---

## ⚡ NGAY BÂY GIỜ — SỬA LỖI TOOLS.PY TRÊN MAIN

> `main` hiện bị lỗi `ImportError: cannot import name 'get_weather'` sau merge `origin/Vũ`.  
> Copy từng dòng vào Terminal:

```powershell
git checkout main
```
```powershell
git checkout haidang2425 -- src/tools.py
```
```powershell
git add src/tools.py
```
```powershell
git commit -m "fix(tools): restore get_weather & search_flights exports after merge conflict with Vu branch"
```
```powershell
git push origin main
```
```powershell
python src/app.py
```

✅ App sẽ chạy thành công!

---

## 🔧 LẦN ĐẦU CÀI ĐẶT MÔI TRƯỜNG (Chỉ làm 1 lần)

```powershell
.venv\Scripts\activate
```
```powershell
pip install -r requirements.txt
```
```powershell
copy .env.example .env
```

> Sau đó mở file `.env`, tìm dòng `LLM_PROVIDER=gemini` và đổi thành:
> ```
> LLM_PROVIDER=mock
> ```
> *(Dùng mock = chạy offline, không cần API key)*

---

## 📍 MỐC 1 — Kiểm tra môi trường

```powershell
git checkout haidang2425
```
```powershell
git fetch --all
```
```powershell
python src/app.py
```
```powershell
git add .
git commit -m "feat(moc1): kiem tra moi truong san sang - Role 4 ready"
git push
```

---

## 📍 MỐC 2 — Baseline Chatbot

```powershell
git checkout main
git fetch --all
```
```powershell
git merge origin/linh
```
```powershell
git merge "origin/Liễu"
```
```powershell
python src/app.py
```
```powershell
git add .
git commit -m "feat(moc2): tich hop Chatbot Baseline - test_cases + prompts hoan chinh"
git push origin main
```

---

## 📍 MỐC 3 — ReAct Agent Loop (Quan trọng nhất)

```powershell
git checkout main
git fetch --all
```
```powershell
git merge origin/Vũ
```
```powershell
git merge "origin/Liễu"
```

> ⚠️ **Nếu bị lỗi import sau khi merge Vũ** → chạy lệnh fix này:
> ```powershell
> git checkout haidang2425 -- src/tools.py
> git add src/tools.py
> git commit -m "fix(tools): restore exports after merge"
> ```

```powershell
python src/app.py
```
```powershell
git add .
git commit -m "feat(moc3): ReAct Agent Loop hoan chinh - tools + prompts + guardrails tich hop"
git push origin main
```

---

## 📍 MỐC 4 — Hoàn chỉnh & Nộp bài

```powershell
git checkout main
git fetch --all
```
```powershell
git merge "origin/Bình"
```
```powershell
python src/app.py
```
```powershell
git add .
git commit -m "feat(moc4): Full Integration hoan thanh - Chatbot + ReAct Agent + Trace Eval"
git push origin main
```

---

## 🚨 XỬ LÝ TÌNH HUỐNG KHẨN (Copy-Paste Sẵn)

### VIM bật lên khi merge
```
Gõ:   :wq    rồi bấm Enter
```

### Merge bị dở dang (MERGE_HEAD exists)
```powershell
git merge --abort
git pull origin main
```

### Conflict sau khi merge
```powershell
git status
```
> Mở file bị conflict → xóa phần `<<<<<<< HEAD`, `=======`, `>>>>>>>` → giữ code đúng
```powershell
git add .
git commit -m "fix: resolve merge conflict - giu lai code chinh xac"
```

### Push bị từ chối (người khác push trước)
```powershell
git pull origin main
git push origin main
```

### Lần đầu push nhánh cá nhân
```powershell
git push --set-upstream origin haidang2425
```

---

## 📋 BẢNG NHÁNH NHÓM

| Nhánh | Người | File đảm nhận | Role |
|-------|-------|--------------|------|
| `origin/linh` | Đỗ Văn Linh | `config/test_cases.json` | Role 1 |
| `origin/Vũ` | Trần Chí Vũ | `src/tools.py` | Role 2 |
| `origin/Liễu` | Đỗ Thu Liễu | `src/prompts.py` | Role 3 |
| `origin/haidang2425` | **Trịnh Hải Đăng** | `src/app.py` | **Role 4** |
| `origin/Bình` | Nguyễn Thanh Bình | `docs/trace_eval.md` | Role 5 |

---

## 📝 CHUẨN COMMIT MESSAGE

| Mốc | Commit Message |
|-----|---------------|
| Fix bug | `fix(tools): mô tả lỗi cụ thể` |
| Mốc 1 | `feat(moc1): kiem tra moi truong san sang` |
| Mốc 2 | `feat(moc2): tich hop Chatbot Baseline hoan chinh` |
| Mốc 3 | `feat(moc3): ReAct Agent Loop hoan chinh` |
| Mốc 4 | `feat(moc4): Full Integration hoan thanh` |
| Merge nhóm | `merge: tich hop code tu [ten-nguoi] branch` |
| Conflict | `fix: resolve merge conflict - [file bi conflict]` |

---

## ✅ KIỂM TRA NHANH MỌI THỨ ĐÃ SẴN SÀNG

```powershell
# Kiểm tra tools.py
python -c "import sys; sys.path.append('src'); from tools import get_weather, search_flights, AVAILABLE_TOOLS; print('tools.py OK')"
```
```powershell
# Kiểm tra prompts.py
python -c "import sys; sys.path.append('src'); from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS; print(f'prompts.py OK - MAX_ITERATIONS={MAX_ITERATIONS}')"
```
```powershell
# Kiểm tra test_cases.json
python -c "import json; d=json.load(open('config/test_cases.json','r',encoding='utf-8')); print(f'test_cases.json OK - {len(d)} cases')"
```
```powershell
# Chạy app hoàn chỉnh
python src/app.py
```

---

## 🎯 OUTPUT CHUẨN KHI APP CHẠY THÀNH CÔNG

```
==================================================
🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT
==================================================
🔌 LLM Provider đang hoạt động: MockProvider (Model: Offline Mock Mode)
✅ Đã tải thành công 5 Test Cases từ config/test_cases.json

--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---
💬 [CHATBOT BASELINE] Câu hỏi: Thời tiết ở Hà Nội hôm nay thế nào...
🤖 Chatbot trả lời: Thought: Cần tra cứu thời tiết Hà Nội...

--- DEMO 2: CHẠY TRÊN REACT AGENT ---
🤖 [REACT AGENT] Câu hỏi: Thời tiết ở Hà Nội hôm nay thế nào...
--- 🔄 Vòng lặp ReAct (Step 1/3) ---
🧠 Thought: Câu hỏi này cần tra cứu thời tiết thời gian thực.
🛠️ Action: get_weather['Hà Nội']
👁️ Observation: Thời tiết Hà Nội: 28°C, Nắng nhẹ, Độ ẩm 65%.
--- 🔄 Vòng lặp ReAct (Step 2/3) ---
🧠 Thought: Tôi đã có thông tin thời tiết Hà Nội...
🏁 Final Answer: Thời tiết Hà Nội hôm nay 28°C, nắng nhẹ. Bạn nên mặc áo phông thoáng mát!
```
