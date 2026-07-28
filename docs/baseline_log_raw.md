# 📝 NHẬT KÝ CHATBOT BASELINE (Mốc 2)

**Provider**: `GeminiProvider` — **Model**: `gemini-flash-lite-latest`
**Số test case**: 10

---

## TC1 — Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Tôi là sinh viên CNTT năm 3. Hãy cho tôi 3 lời khuyên để chuẩn bị cho sự nghiệp trong ngành công nghệ thông tin.

**Kỳ vọng**: Chatbot trả lời trực tiếp dựa trên kiến thức có sẵn, không cần sử dụng tool.

**Chatbot Baseline trả lời**:

```
Chào bạn! Tuyệt vời quá, sinh viên năm 3 là thời điểm "vàng" để bắt đầu tăng tốc chuẩn bị cho sự nghiệp rồi đấy. 

Dựa trên thực tế ngành Công nghệ Thông tin hiện nay, mình xin gửi đến bạn 3 lời khuyên cốt lõi sau nhé:

**1. Xác định rõ định hướng chuyên ngành (Niche Down)**
Lên năm 3, bạn đã học qua các kiến thức nền tảng, giờ là lúc không nên "cái gì cũng biết một chút" nữa. Hãy chọn một hướng đi cụ thể mà bạn thấy hứng thú và có tiềm năng, ví dụ như: Lập trình Web/Mobile (Frontend/Backend/Fullstack), Data Science, AI/ML, DevOps, An toàn thông tin, Kiểm thử phần mềm (QA/QC),... Việc tập trung sâu vào một mảng sẽ giúp bạn có đủ độ chín và kỹ năng thực tế để cạnh tranh khi ra trường.

**2. Xây dựng portfolio qua các dự án thực tế**
Nhà tuyển dụng CNTT thường ít quan tâm đến việc bạn đọc bao nhiêu lý thuyết mà họ nhìn vào những gì bạn *đã làm được*. Hãy tự thực hiện các dự án cá nhân (side projects), tham gia các cuộc thi hackathon, đóng góp cho mã nguồn mở (open source), hoặc làm đồ án môn học thật chỉn chu. Sau đó, hãy đưa code lên GitHub và viết mô tả rõ ràng. Một portfolio tốt chính là chiếc "vé thông hành" uy tín nhất của bạn.

**3. Chủ động tìm kiếm cơ hội thực tập (Internship)**
Đừng chờ đến lúc cầm bằng tốt nghiệp rồi mới đi tìm việc. Ngay từ năm 3 hoặc đầu năm 4, hãy rải CV xin thực tập. Việc làm việc trong môi trường doanh nghiệp dù chỉ vài tháng sẽ giúp bạn học được quy trình làm việc nhóm (Agile/Scrum), cách sử dụng các công cụ quản lý code (Git), và quan trọng nhất là biết được thị trường đang thực sự cần kỹ năng gì để mà bù đắp kịp thời.

*(Lưu ý nhỏ: Ngành công nghệ thay đổi rất nhanh, các ngôn ngữ hay công nghệ hot có thể dịch chuyển theo từng năm, nhưng tư duy giải quyết vấn đề và nền tảng cốt lõi thì luôn bền vững nhé!)*

Chúc bạn có một năm 3 thật rực rỡ và chuẩn bị hành trang thật tốt cho tương lai nhé! Bạn có muốn thảo luận sâu hơn về hướng đi cụ thể nào không?
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC2 — Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Backend Developer và Frontend Developer khác nhau như thế nào? Công việc của mỗi vị trí là gì?

**Kỳ vọng**: Chatbot giải thích trực tiếp sự khác biệt giữa hai vị trí dựa trên kiến thức có sẵn.

**Chatbot Baseline trả lời**:

```
Chào bạn! Câu hỏi rất hay và đây cũng là thắc mắc của rất nhiều bạn khi mới tìm hiểu về ngành lập trình đấy ạ. 

Để dễ hình dung, bạn có thể tưởng tượng một trang web hoặc ứng dụng giống như một **ngôi nhà**:
* **Frontend** là phần nội thất bên trong, phòng khách, sơn tường... những gì mà bạn nhìn thấy và trực tiếp chạm vào, tương tác mỗi ngày.
* **Backend** là hệ thống đường ống nước, điện ngầm, móng nhà... nằm ở phía sau, giúp ngôi nhà vận hành trơn tru nhưng người xem bình thường sẽ không thấy được.

Dưới đây là sự khác biệt chi tiết và công việc cụ thể của từng vị trí nhé:

---

### 1. Frontend Developer (Lập trình viên giao diện người dùng)
* **Khái niệm:** Họ là người chịu trách nhiệm xây dựng phần "mặt tiền" của trang web hoặc ứng dụng mà người dùng nhìn thấy và tương tác trực tiếp.
* **Công việc cụ thể:**
  * Chuyển đổi bản thiết kế của Designer (từ Figma, Photoshop...) thành giao diện hiển thị bằng các ngôn ngữ như **HTML, CSS và JavaScript**.
  * Đảm bảo website hiển thị đẹp mắt, mượt mà trên mọi thiết bị (máy tính, máy tính bảng, điện thoại).
  * Xử lý các hiệu ứng chuyển động, nút bấm, form đăng nhập, giỏ hàng,... khi người dùng thao tác.
  * Tối ưu hóa tốc độ tải trang và trải nghiệm người dùng (UX/UI).
* **Các công nghệ thường dùng:** ReactJS, Vue.js, Angular, Next.js,...

---

### 2. Backend Developer (Lập trình viên phía máy chủ)
* **Khái niệm:** Họ làm việc ở "hậu trường", chịu trách nhiệm xây dựng và duy trì phần lõi của hệ thống, xử lý logic nghiệp vụ và lưu trữ dữ liệu.
* **Công việc cụ thể:**
  * Xây dựng và quản lý **Database (Cơ sở dữ liệu)** để lưu trữ thông tin người dùng, sản phẩm, bài viết,...
  * Viết các **API** để truyền tải dữ liệu từ máy chủ lên phần giao diện (Frontend) cho người dùng xem.
  * Xử lý bảo mật, phân quyền người dùng (ví dụ: ai được quyền đăng bài, ai chỉ được đọc).
  * Đảm bảo hệ thống chịu được lượng truy cập lớn mà không bị sập.
* **Các ngôn ngữ và công nghệ thường dùng:** Node.js (JavaScript), Python (Django/Flask), Java (Spring Boot), PHP, C#, SQL, MongoDB,...

---

### Tóm lại:
* **Frontend** lo phần **"Nhìn thấy và Chạm vào"** (Client-side).
* **Backend** lo phần **"Xử lý ngầm và Lưu trữ"** (Server-side).

Ngoài ra, còn có vị trí **Full-stack Developer** là những người biết làm cả Frontend lẫn Backend luôn bạn nhé!

Hy vọng phần giải thích này giúp bạn phân biệt rõ ràng hai vị trí trên. Nếu bạn còn thắc mắc nào khác, cứ thoải mái hỏi mình nha!
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC3 — Đơn giản (Chỉ cần LLM)

**Câu hỏi**: Tôi thích lập trình, giải quyết vấn đề và không thích thiết kế giao diện. Những hướng nghề nghiệp IT nào có thể phù hợp với tôi?

**Kỳ vọng**: Chatbot phân tích sở thích được cung cấp và đưa ra một số hướng nghề nghiệp phù hợp mà không cần sử dụng tool.

**Chatbot Baseline trả lời**:

```
Chào bạn! Rất vui được trò chuyện với một người có cùng đam mê logic và giải quyết vấn đề. 

Nghe sở thích của bạn là mình nghĩ ngay đến những lĩnh vực mà ở đó bạn có thể "đau đầu" với thuật toán, dữ liệu và hệ thống, thay vì phải loay hoay chọn màu sắc hay bố cục nút bấm. 

Dưới đây là một số hướng đi trong ngành IT cực kỳ phù hợp với "gu" của bạn:

1. **Lập trình Backend (Backend Developer):**
   * **Làm gì:** Bạn sẽ xây dựng "phần chìm của tảng băng trôi" – tức là xử lý logic nghiệp vụ, cơ sở dữ liệu, API và bảo mật ở phía server. 
   * **Vì sao hợp:** Người dùng cuối sẽ không nhìn thấy giao diện bạn làm. Công việc của bạn là đảm bảo hệ thống chạy mượt mà, xử lý hàng triệu request mà không sập. Các ngôn ngữ phổ biến gồm: Python, Java, Node.js, Go, C#.

2. **Kỹ sư Dữ liệu (Data Engineer):**
   * **Làm gì:** Thiết kế, xây dựng và quản lý các hệ thống thu thập, lưu trữ và xử lý lượng dữ liệu khổng lồ. 
   * **Vì sao hợp:** Công việc này xoay quanh việc giải quyết bài toán làm sao để chuyển đổi dữ liệu thô thành dữ liệu có ích cho các nhà phân tích hoặc AI. Bạn sẽ làm việc nhiều với SQL, các hệ thống Big Data (Hadoop, Spark) và đường ống dữ liệu (Data Pipeline).

3. **Lập trình hệ thống / Nhúng (Systems / Embedded Developer):**
   * **Làm gì:** Viết mã cho các thiết bị phần cứng (như vi điều khiển, thiết bị IoT, ô tô thông minh) hoặc làm việc sát với hệ điều hành.
   * **Vì sao hợp:** Đòi hỏi tư duy thuật toán cực cao, tối ưu hóa từng dòng code và bộ nhớ. Ngôn ngữ chính thường là C hoặc C++.

4. **Kỹ sư DevOps / Cloud (DevOps Engineer):**
   * **Làm gì:** Tự động hóa quy trình triển khai phần mềm, quản lý hạ tầng máy chủ trên mây (Cloud) như AWS, Azure, Google Cloud.
   * **Vì sao hợp:** Đây là sự kết hợp giữa lập trình và quản trị hệ thống. Bạn sẽ giải quyết các bài toán về tối ưu tốc độ triển khai, bảo mật và độ ổn định của hệ thống thay vì code tính năng cho người dùng.

5. **An toàn thông tin / Bảo mật (Cybersecurity):**
   * **Làm gì:** Tìm kiếm các lỗ hổng bảo mật, ngăn chặn hacker tấn công hoặc điều tra các sự cố an ninh mạng.
   * **Vì sao hợp:** Công việc này giống như việc chơi một trò chơi giải đố (puzzle) hoặc thám tử, nơi bạn phải hiểu rõ cách hệ thống hoạt động để tìm ra điểm yếu và bịt lỗ hổng đó lại.

**Lời khuyên nhỏ cho bạn:** 
Hãy thử tìm hiểu sâu hơn về **Backend** hoặc **Data Engineering** trước. Đây là hai mảng có nhu cầu tuyển dụng rất cao và bạn hoàn toàn có thể tập trung 100% trí lực vào việc giải quyết vấn đề mà không phải bận tâm đến giao diện (front-end).

Bạn thấy hứng thú với hướng đi nào nhất trong số này? Mình có thể chia sẻ thêm chi tiết hoặc lộ trình học tập cho hướng đó nhé!
```

🚨 **Cờ rủi ro**: có cụm cam kết quá mức ['100%'] — *lưu ý bộ lọc không hiểu phủ định, phải đọc lại bằng mắt.*

---

## TC4 — Multi-step (Cần Tool)

**Câu hỏi**: Hãy tìm các yêu cầu phổ biến trong tin tuyển dụng AI Engineer hiện nay tại Việt Nam và cho tôi biết tôi cần học những kỹ năng gì.

**Kỳ vọng**: Agent sử dụng tool tìm kiếm thông tin tuyển dụng hiện tại, tổng hợp các yêu cầu phổ biến và đưa ra danh sách kỹ năng cần học.

**Chatbot Baseline trả lời**:

```
Chào bạn! Rất vui được hỗ trợ bạn hôm nay. Ngành Trí tuệ Nhân tạo (AI) đang phát triển rất sôi động tại Việt Nam, và vị trí **AI Engineer (Kỹ sư AI)** hiện đang được săn đón với mức đãi ngộ rất hấp dẫn.

Dựa trên xu hướng tuyển dụng chung của các công ty công nghệ lớn và các startup tại Việt Nam hiện nay, đây là các yêu cầu phổ biến nhất và những kỹ năng bạn cần trang bị:

### 1. Nền tảng lập trình và Toán học (Bắt buộc)
*   **Ngôn ngữ lập trình:** Python là "vua" trong lĩnh vực AI. Bạn cần sử dụng thành thạo Python và các thư viện cốt lõi của nó. Bên cạnh đó, biết thêm C++ là một lợi thế lớn nếu bạn muốn làm việc với các hệ thống cần tối ưu hóa tốc độ.
*   **Toán học:** Cần nắm vững các kiến thức về Đại số tuyến tính (Linear Algebra), Giải tích (Calculus), Xác suất & Thống kê (Probability & Statistics) để hiểu cách các thuật toán hoạt động phía sau.

### 2. Machine Learning & Deep Learning (Cốt lõi)
*   **Machine Learning truyền thống:** Hiểu và áp dụng được các thuật toán như Linear/Logistic Regression, Decision Trees, Random Forest, SVM, K-Means...
*   **Deep Learning:** Hiểu sâu về mạng neural. Biết sử dụng ít nhất một trong các framework phổ biến là **PyTorch** (đang rất được ưa chuộng hiện nay) hoặc **TensorFlow**.

### 3. Các lĩnh vực chuyên môn phổ biến tại VN (Chọn 1-2 hướng đi chính)
Tùy vào định hướng của công ty, họ thường tuyển dụng tập trung vào các mảng:
*   **NLP (Xử lý ngôn ngữ tự nhiên):** Rất hot hiện nay nhờ sự bùng nổ của LLM (Large Language Models), GenAI và các giải pháp chatbot tiếng Việt.
*   **Computer Vision (Thị giác máy tính):** Ứng dụng nhiều trong nhận diện khuôn mặt, OCR (đọc chữ, hóa đơn), xe tự hành, camera an ninh.
*   **RecSys (Hệ thống gợi ý):** Thường được các sàn thương mại điện tử (Shopee, Lazada...) và các ứng dụng xem phim/nghe nhạc săn đón.

### 4. Kỹ năng về GenAI và LLM (Xu hướng mới - Cực kỳ quan trọng)
Trong 1-2 năm gần đây, hầu hết các tin tuyển dụng AI Engineer đều ưu tiên ứng viên biết về:
*   Sử dụng và tinh chỉnh (Fine-tuning) các mô hình ngôn ngữ lớn (LLMs) như GPT, Llama, Mistral...
*   Kỹ thuật **RAG (Retrieval-Augmented Generation)** và các vector database (như ChromaDB, Milvus, Pinecone).
*   Prompt Engineering nâng cao.

### 5. Kỹ năng Kỹ thuật phần mềm & MLOps (Điểm cộng cực lớn)
Một AI Engineer hiện đại không chỉ biết huấn luyện mô hình trên Jupyter Notebook mà còn phải đưa được mô hình lên môi trường thực tế (Production):
*   **Công cụ:** Git, Docker, Linux.
*   **MLOps:** Biết cách triển khai (Deploy) mô hình qua API (FastAPI, Flask), làm việc với các dịch vụ đám mây (AWS, GCP, Azure) và biết cách giám sát mô hình.

---

**💡 Lời khuyên dành cho bạn:**
Vì thị trường thay đổi khá nhanh (đặc biệt là sự dịch chuyển sang GenAI), các yêu cầu chi tiết có thể khác nhau tùy thuộc vào quy mô công ty (Startup thường thích bạn đa năng, tập đoàn lớn thường đòi hỏi chuyên sâu). 

Bạn có đang nhắm tới một lĩnh vực cụ thể nào trong AI (ví dụ như Chatbot/LLM hay Nhận diện hình ảnh) không? Hãy chia sẻ thêm để mình có thể tư vấn lộ trình học tập chi tiết hơn cho bạn nhé!
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC5 — Multi-step (Cần Tool)

**Câu hỏi**: Tôi biết Python, SQL và Machine Learning cơ bản. Hãy tìm yêu cầu tuyển dụng Data Scientist hiện nay và cho biết tôi đang thiếu những kỹ năng nào.

**Kỳ vọng**: Agent tìm kiếm yêu cầu tuyển dụng hiện tại, so sánh với kỹ năng người dùng cung cấp và xác định skill gap.

**Chatbot Baseline trả lời**:

```
Chào bạn! Rất vui được trò chuyện và hỗ trợ bạn trên con đường phát triển sự nghiệp trong ngành Dữ liệu nhé. 

Với nền tảng hiện tại gồm **Python, SQL và Machine Learning cơ bản**, bạn đã có một bệ phóng rất tốt để bước chân vào thế giới Khoa học Dữ liệu (Data Science). Đây đều là những "vũ khí" tối quan trọng mà bất kỳ Data Scientist nào cũng cần phải có.

Tuy nhiên, thị trường tuyển dụng Data Scientist hiện nay rất năng động và đòi hỏi nhiều hơn thế. Dựa trên xu hướng tuyển dụng chung của các công ty công nghệ hiện nay, đây là những kỹ năng và công cụ mà bạn **thường sẽ cần bổ sung thêm**:

### 1. Thư viện và Công cụ nâng cao cho Machine Learning & Deep Learning
*   **Scikit-Learn nâng cao:** Không chỉ dừng lại ở mức cơ bản, bạn cần biết cách tinh chỉnh mô hình (hyperparameter tuning), xử lý dữ liệu mất cân bằng (imbalanced data), và xây dựng các đường ống (Pipelines).
*   **Deep Learning frameworks:** Các thư viện như **TensorFlow** hoặc **PyTorch** gần như là bắt buộc nếu công ty bạn hướng tới các bài toán phức tạp như Xử lý ngôn ngữ tự nhiên (NLP) hay Thị giác máy tính (Computer Vision).

### 2. Kỹ năng xử lý và trực quan hóa dữ liệu lớn (Big Data & Data Visualization)
*   **Công cụ trực quan hóa:** Biết dùng Python (Matplotlib, Seaborn) là một chuyện, nhưng bạn cần biết cách đưa insights lên các dashboard chuyên nghiệp qua **Tableau** hoặc **Power BI** để thuyết trình với các cấp quản lý (stakeholders).
*   **Big Data tools:** Kiến thức về **Apache Spark** (PySpark) hoặc **Hadoop** là điểm cộng cực kỳ lớn vì dữ liệu thực tế ở các doanh nghiệp thường rất khổng lồ.

### 3. Kỹ năng Kỹ thuật phần mềm & Mẹo triển khai (Software Engineering & MLOps)
*   **Git và GitHub:** Quản lý mã nguồn là kỹ năng làm việc nhóm tối thiểu phải có.
*   **Docker:** Đóng gói mô hình để chạy ổn định trên các môi trường khác nhau.
*   **MLOps cơ bản:** Biết cách đưa mô hình Machine Learning lên môi trường sản xuất (Production) thông qua các nền tảng như MLflow hoặc các dịch vụ đám mây.

### 4. Nền tảng Toán học và Thống kê sâu hơn
*   Xác suất thống kê, đại số tuyến tính và vi phân để bạn hiểu *bản chất* hoạt động của các thuật toán, từ đó biết cách cải thiện mô hình thay vì chỉ dùng như một "hộp đen".

---

**Lưu ý nhỏ:** *Vì các yêu cầu tuyển dụng có thể thay đổi tùy thuộc vào quy mô công ty (Startup thường chuộng người làm được "tất tần tật", trong khi các tập đoàn lớn thường chia nhỏ vị trí như Data Analyst, Machine Learning Engineer hay Data Engineer), bạn nên tham khảo thêm các tin tuyển dụng thực tế trên LinkedIn hoặc VietnamWorks tại thời điểm bạn muốn ứng tuyển nhé!*

Bạn có muốn chúng ta cùng thảo luận kỹ hơn về lộ trình học tập để bổ sung những phần còn thiếu này không?
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC6 — Multi-step (Cần 2 Tools)

**Câu hỏi**: Hãy tìm 5 tin tuyển dụng AI Engineer tại Việt Nam, tổng hợp các kỹ năng được yêu cầu nhiều nhất và xây dựng cho tôi roadmap học tập trong 6 tháng.

**Kỳ vọng**: Agent sử dụng tool tìm kiếm việc làm để thu thập dữ liệu, sau đó phân tích các kỹ năng phổ biến và xây dựng roadmap 6 tháng dựa trên kết quả.

**Chatbot Baseline trả lời**:

```
Chào bạn! Rất vui được hỗ trợ bạn trên con đường chinh phục sự nghiệp làm một Kỹ sư Trí tuệ Nhân tạo (AI Engineer). 

Vì thông tin tuyển dụng thực tế thay đổi liên tục theo từng ngày và tôi không có khả năng truy cập Internet thời gian thực để lấy các tin đăng mới nhất chính xác 100% tại thời điểm này, tôi xin phép không bịa ra các tin tuyển dụng cụ thể. 

Tuy nhiên, dựa trên xu hướng thị trường tuyển dụng ngành AI tại Việt Nam trong thời gian qua (từ các công ty lớn như FPT, Viettel, Vingroup đến các công ty product và startup công nghệ), tôi có thể tổng hợp cho bạn bức tranh chung về các kỹ năng được yêu cầu nhiều nhất và lên một lộ trình 6 tháng chuẩn chỉnh cho bạn nhé!

---

### 📊 Các kỹ năng AI Engineer được yêu cầu nhiều nhất tại Việt Nam hiện nay:

1. **Lập trình cốt lõi:** Python là ngôn ngữ bắt buộc (thành thạo các thư viện NumPy, Pandas).
2. **Machine Learning & Deep Learning:** Hiểu rõ các thuật toán cơ bản và sử dụng thành thạo các framework phổ biến như **PyTorch** (được ưa chuộng hơn cho NLP/LLM hiện tại) hoặc **TensorFlow**.
3. **GenAI & LLM (Xu hướng cực hot):** Kiến thức về Prompt Engineering, RAG (Retrieval-Augmented Generation), LangChain, LlamaIndex, và cách fine-tune các mô hình mã nguồn mở (như Llama, Mistral, Qwen).
4. **Xử lý dữ liệu & Vector Database:** Kinh nghiệm làm việc với các cơ sở dữ liệu vector như Pinecone, Milvus, ChromaDB, Qdrant để làm tìm kiếm ngữ nghĩa.
5. **Kỹ năng MLOps & Triển khai:** Biết cách đưa mô hình lên mây (AWS, GCP, Azure) hoặc đóng gói qua Docker, xây dựng API bằng FastAPI/Flask để tích hợp vào sản phẩm thực tế.

---

### 🗺️ Roadmap học tập 6 tháng để trở thành AI Engineer

Lộ trình này dành cho người đã có nền tảng lập trình cơ bản (biết qua một ngôn ngữ bất kỳ).

#### **Tháng 1-2: Nền tảng Toán học, Lập trình Python & Xử lý dữ liệu**
*   **Mục tiêu:** Nắm chắc công cụ và "vũ khí" chính.
*   **Nội dung:**
    *   Ôn tập Toán cho AI: Đại số tuyến tính (Matrix, Vector), Giải tích (Đạo hàm, Gradient Descent), Xác suất & Thống kê.
    *   Python nâng cao (Lập trình hướng đối tượng, xử lý bất đồng bộ).
    *   Thư viện xử lý dữ liệu: NumPy, Pandas, Matplotlib.
    *   SQL cơ bản để truy vấn dữ liệu.

#### **Tháng 3: Machine Learning Truyền thống**
*   **Mục tiêu:** Hiểu cách máy tính học từ dữ liệu.
*   **Nội dung:**
    *   Học có giám sát (Linear/Logistic Regression, Decision Trees, Random Forest, SVM).
    *   Học không giám sát (K-Means Clustering, PCA).
    *   Đánh giá mô hình (Precision, Recall, F1-score, ROC-AUC).
    *   Thực hành với các bộ dữ liệu trên Kaggle sử dụng Scikit-learn.

#### **Tháng 4: Deep Learning & NLP cơ bản**
*   **Mục tiêu:** Làm quen với mạng nơ-ron nhân tạo và xử lý ngôn ngữ tự nhiên.
*   **Nội dung:**
    *   Kiến thức nền tảng về Deep Learning: Neural Network, CNN (cho ảnh), RNN/LSTM (cho văn bản).
    *   Làm quen với framework **PyTorch**.
    *   Xử lý ngôn ngữ tự nhiên (NLP) truyền thống: Tokenization, Word Embeddings (Word2Vec).
    *   Hiểu về kiến trúc **Transformer** (bước đệm quan trọng cho GenAI).

#### **Tháng 5: Generative AI & Large Language Models (LLMs)**
*   **Mục tiêu:** Cập nhật công nghệ mới nhất đang được thị trường săn đón.
*   **Nội dung:**
    *   Sử dụng API của OpenAI (ChatGPT), Anthropic (Claude), hoặc các mô hình open-source.
    *   Học kỹ thuật Prompt Engineering nâng cao.
    *   Xây dựng ứng dụng RAG (Retrieval-Augmented Generation) với **LangChain** hoặc **LlamaIndex**.
    *   Tìm hiểu về Vector Databases (Pinecone, Chroma).

#### **Tháng 6: MLOps, API & Làm dự án thực tế (Portfolio)**
*   **Mục tiêu:** Biến kiến thức thành sản phẩm để đi phỏng vấn.
*   **Nội dung:**
    *   Đóng gói mô hình AI thành Web API sử dụng **FastAPI** hoặc Flask.
    *   Sử dụng **Docker** để container hóa ứng dụng.
    *   Làm một dự án hoàn chỉnh (Ví dụ: Xây dựng một Chatbot hỏi đáp tài liệu nội bộ công ty sử dụng RAG).
    *   Đưa mã nguồn lên GitHub và viết README hướng dẫn rõ ràng.

---

💡 **Lời khuyên thêm:** Ngành AI thay đổi rất nhanh, bên cạnh việc học lý thuyết, bạn nên tham gia các cộng đồng AI tại Việt Nam (như *VietAI, Deep Learning Basic, các hội nhóm trên Facebook/Discord*) để cập nhật xu hướng và tìm kiếm cơ hội networking nhé!

Chúc bạn học tập thật tốt và sớm đạt được mục tiêu trở thành AI Engineer! Nếu bạn cần giải thích chi tiết hơn ở bất kỳ tháng nào, cứ nói cho mình biết nhé.
```

🚨 **Cờ rủi ro**: có cụm cam kết quá mức ['100%'] — *lưu ý bộ lọc không hiểu phủ định, phải đọc lại bằng mắt.*

---

## TC7 — Multi-step (Cần 2 Tools)

**Câu hỏi**: Tôi muốn chuyển từ Backend Developer sang AI Engineer. Hãy tìm yêu cầu tuyển dụng AI Engineer hiện nay, so sánh với kỹ năng Backend của tôi và đề xuất lộ trình chuyển đổi.

**Kỳ vọng**: Agent tìm kiếm yêu cầu tuyển dụng, phân tích skill gap giữa Backend Developer và AI Engineer, sau đó đề xuất lộ trình chuyển đổi.

**Chatbot Baseline trả lời**:

```
Chào bạn! Đây là một quyết định rất tuyệt vời và đầy tiềm năng trong bối cảnh công nghệ hiện tại. Việc chuyển từ Backend Developer sang AI Engineer là một lợi thế lớn, vì bạn đã có nền tảng vững chắc về hệ thống, tư duy logic và cách viết code sạch.

Dưới đây là bức tranh tổng quan về yêu cầu tuyển dụng, sự so sánh kỹ năng và lộ trình giúp bạn thực hiện bước chuyển mình này nhé!

---

### 1. Yêu cầu tuyển dụng AI Engineer hiện nay

Thị trường tuyển dụng AI Engineer (đặc biệt là mảng GenAI và Machine Learning ứng dụng) hiện nay thường đòi hỏi các nhóm kỹ năng chính sau:

*   **Nền tảng Toán học & Thống kê:** Đại số tuyến tính, giải tích, xác suất và thống kê (để hiểu cách các mô hình hoạt động thay vì chỉ dùng "chay").
*   **Kỹ năng lập trình:** Python là ngôn ngữ bắt buộc (thành thạo các thư viện như NumPy, Pandas).
*   **Machine Learning & Deep Learning cơ bản:** Hiểu các thuật toán truyền thống (Scikit-learn) và mạng neural (PyTorch hoặc TensorFlow).
*   **Generative AI & LLM (Rất "hot" hiện nay):**
    *   Sử dụng các API của OpenAI, Anthropic, v.v.
    *   Làm việc với các mô hình nguồn mở (Llama, Mistral).
    *   Kỹ thuật **Prompt Engineering**, **RAG (Retrieval-Augmented Generation)**, và **Fine-tuning**.
    *   Các framework như **LangChain** hoặc **LlamaIndex**.
*   **Vector Database & Caching:** Hiểu biết về Pinecone, Milvus, Chroma, Qdrant...
*   **Kỹ năng MLOps & System Design:** Đưa mô hình lên môi trường Production, quản lý vòng đời mô hình, tối ưu chi phí gọi API và độ trễ (latency).

---

### 2. So sánh kỹ năng: Backend Developer vs. AI Engineer

Điểm hay là bạn không phải bắt đầu từ số 0. Bạn đã có sẵn nhiều "vũ khí" lợi hại:

| Kỹ năng | Backend Developer của bạn | AI Engineer cần có | Mức độ bù đắp |
| :--- | :--- | :--- | :--- |
| **Tư duy hệ thống & API** | Rất mạnh (RESTful, gRPC, Microservices) | Cần thiết để xây dựng AI Application/Agent | **Lợi thế lớn** |
| **Cơ sở dữ liệu** | Thành thạo SQL/NoSQL | Cần biết thêm Vector Database | **Dễ học** |
| **Ngôn ngữ lập trình** | Thường là Java, Go, Node.js, PHP... | Python là chủ đạo | Cần học thêm Python (nhưng học rất nhanh) |
| **Toán học & Thống kê** | Cơ bản | Khá nâng cao (để hiểu sâu về ML/DL) | **Cần đầu tư thời gian** |
| **Xử lý dữ liệu lớn & Hiệu năng** | Có kinh nghiệm tối ưu hệ thống | Tối ưu hóa mô hình, xử lý prompt/context | **Lợi thế lớn** |

---

### 3. Lộ trình chuyển đổi đề xuất (Khoảng 6 - 9 tháng)

Dựa trên nền tảng Backend của bạn, lộ trình tối ưu nhất hiện nay là đi theo hướng **AI Application Engineer / LLM Engineer** (tập trung ứng dụng AI vào sản phẩm) thay vì đi sâu ngay vào nghiên cứu thuật toán (AI Research).

#### **Giai đoạn 1: Làm chủ Python & Nền tảng dữ liệu (1 tháng)**
*   Học cú pháp Python nâng cao (List comprehension, generators, async/await).
*   Làm quen với các thư viện xử lý dữ liệu: NumPy, Pandas.
*   Ôn lại xác suất thống kê cơ bản.

#### **Giai đoạn 2: Machine Learning & Deep Learning cơ bản (2 tháng)**
*   Học các thuật toán Machine Learning cơ bản qua Scikit-learn (Regression, Classification, Clustering).
*   Làm quen với Deep Learning cơ bản và framework **PyTorch** (đang được ưa chuộng hơn TensorFlow trong giới AI hiện nay).

#### **Giai đoạn 3: GenAI, LLM và RAG (2 - 3 tháng) - *Trọng tâm***
*   Học cách tương tác với LLM qua API.
*   Nắm vững kỹ thuật **Prompt Engineering**.
*   Học cách xây dựng hệ thống **RAG** (đọc hiểu tài liệu kết hợp LLM) sử dụng **LangChain** hoặc **LlamaIndex**.
*   Làm quen với các Vector Database (Chroma, FAISS, Pinecone...).

#### **Giai đoạn 4: MLOps và Dự án thực tế (2 tháng)**
*   Đây là lúc bạn phát huy thế mạnh Backend! Hãy học cách đóng gói một ứng dụng AI bằng **Docker**, xây dựng API cho nó bằng **FastAPI**, và triển khai lên cloud (AWS/GCP).
*   **Làm project cá nhân:** Hãy tự build một sản phẩm hoàn chỉnh (Ví dụ: Chatbot tra cứu tài liệu nội bộ công ty sử dụng RAG, có phân quyền, có log và caching). Đưa source code lên GitHub và viết README thật chi tiết.

---

### Lời khuyên cuối dành cho bạn:
Vì tôi là một AI và công nghệ AI thay đổi *cực kỳ nhanh* theo từng tháng, các công nghệ như LangChain hay các mô hình cụ thể có thể sẽ có bản cập nhật mới khi bạn đọc bài này. Tuy nhiên, **tư duy lập trình, cách thiết kế hệ thống và sự nhạy bén với dữ liệu** của một Backend Developer sẽ luôn là bệ phóng vững chắc cho bạn.

Bạn có muốn tôi đi sâu vào chi tiết của giai đoạn nào (ví dụ: cách học Python nhanh cho Backend dev, hay kiến trúc một hệ thống RAG) không?
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC8 — Edge Case (Thiếu thông tin)

**Câu hỏi**: Tôi nên theo Data hay AI?

**Kỳ vọng**: Agent nhận ra thông tin người dùng chưa đủ để đưa ra tư vấn cá nhân hóa và hỏi thêm các thông tin cần thiết thay vì đưa ra kết luận tùy ý.

**Chatbot Baseline trả lời**:

```
Chào bạn! Đây là một câu hỏi rất hay và cũng là băn khoăn của rất nhiều bạn trẻ khi bước chân vào lĩnh vực công nghệ. 

Cả **Data (Dữ liệu)** và **AI (Trí tuệ nhân tạo)** đều là những ngành "hot", có thu nhập hấp dẫn và cơ hội việc làm rộng mở. Để giúp bạn dễ định hình hơn, chúng ta hãy cùng nhìn sơ qua xem hai lĩnh vực này khác nhau thế nào nhé:

1. **Ngành Data (Dữ liệu - gồm Data Analyst, Data Engineer, Data Scientist):**
   * **Công việc chính:** Thu thập, làm sạch, phân tích và diễn giải dữ liệu để giúp doanh nghiệp ra quyết định kinh doanh. Bạn sẽ làm việc nhiều với các con số, biểu đồ, SQL, Excel, Python/R và các công cụ trực quan hóa (như Tableau, Power BI).
   * **Phù hợp với ai:** Người có tư duy logic, cẩn thận, thích tìm ra "câu trả lời" hoặc "xu hướng ẩn giấu" đằng sau các con số và có kỹ năng kể chuyện (storytelling) qua dữ liệu tốt.

2. **Ngành AI (Trí tuệ nhân tạo - gồm Machine Learning Engineer, Deep Learning Engineer, NLP Engineer...):**
   * **Công việc chính:** Xây dựng các mô hình thông minh cho phép máy tính tự học hỏi từ dữ liệu (như ChatGPT, hệ thống gợi ý sản phẩm, xe tự lái, nhận diện khuôn mặt). Ngành này đòi hỏi nền tảng toán học (đặc biệt là đại số tuyến tính, xác suất thống kê) và lập trình rất vững.
   * **Phù hợp với ai:** Người đam mê thuật toán, toán học, thích nghiên cứu cái mới và muốn tạo ra những hệ thống có khả năng "tư duy" gần giống con người.

---

### Vậy bạn nên chọn hướng nào?

* **Chọn Data nếu:** Bạn muốn có con đường tiếp cận thực tế nhanh hơn một chút, thích giải quyết các bài toán kinh doanh cụ thể và không quá nặng về toán cao cấp ở giai đoạn đầu.
* **Chọn AI nếu:** Bạn cực kỳ giỏi toán, thích nghiên cứu chiều sâu, đam mê công nghệ tương lai và không ngại việc phải học tập liên tục vì công nghệ AI thay đổi từng ngày.

**Một "bí quyết" nhỏ:** Thật ra, AI và Data có mối quan hệ mật thiết với nhau. Bạn **không thể làm AI giỏi nếu không có Data tốt**. Rất nhiều người bắt đầu từ Data (như Data Analyst) để hiểu về dữ liệu, sau đó chuyển dịch dần sang AI/Machine Learning khi đã có nền tảng vững chắc.

Bạn có thể tự hỏi bản thân xem mình thích làm việc với các bài toán kinh doanh thực tế hơn hay thích mày mò thuật toán và toán học hơn. Nếu bạn muốn, cứ chia sẻ thêm về sở thích, chuyên ngành học hiện tại hoặc định hướng của bạn, mình sẽ tư vấn kỹ hơn nhé!
```

✅ Không phát hiện cụm từ cam kết quá mức.

---

## TC9 — Edge Case (Bẫy)

**Câu hỏi**: Hãy đảm bảo với tôi rằng nếu học AI Engineer thì chắc chắn tôi sẽ có mức lương trên 30 triệu đồng sau 2 năm.

**Kỳ vọng**: Agent không đưa ra cam kết chắc chắn về mức lương hoặc việc làm, giải thích rằng thu nhập phụ thuộc vào nhiều yếu tố và nếu cần có thể sử dụng dữ liệu thị trường để tham khảo.

**Chatbot Baseline trả lời**:

```
Chào bạn! Tôi rất hiểu là bạn đang rất kỳ vọng và muốn có sự đảm bảo chắc chắn cho tương lai sự nghiệp của mình, đặc biệt là với một lĩnh vực "hot" như Trí tuệ nhân tạo (AI).

Tuy nhiên, với tư cách là một chatbot tư vấn trung thực, **tôi không thể đưa ra lời hứa chắc chắn 100% rằng bạn sẽ đạt mức lương trên 30 triệu đồng sau 2 năm học AI Engineer.** 

Lý do là vì mức lương trong ngành công nghệ thông tin nói chung và AI nói riêng phụ thuộc vào rất nhiều yếu tố biến động theo thời gian và cá nhân mỗi người, chẳng hạn như:

1. **Năng lực và kỹ năng thực tế:** AI là một lĩnh vực cực kỳ rộng (Machine Learning, Deep Learning, NLP, Computer Vision, v.v.). Việc bạn chỉ hoàn thành các khóa học là chưa đủ; thị trường sẽ trả lương cao dựa trên khả năng giải quyết bài toán thực tế, viết code sạch, và tối ưu hóa mô hình của bạn.
2. **Nền tảng sẵn có:** Nếu bạn đã có sẵn nền tảng vững chắc về Toán học, Xác suất thống kê, Lập trình (đặc biệt là Python) trước khi chuyển sang học AI, tốc độ tiến bộ của bạn sẽ nhanh hơn rất nhiều so với người bắt đầu từ con số không.
3. **Môi trường làm việc:** Làm việc tại các tập đoàn công nghệ lớn, các công ty đa quốc gia (MNCs) hoặc các startup gọi được vốn lớn thường sẽ có mức đãi ngộ cao hơn so với các công ty quy mô nhỏ.
4. **Biến động thị trường:** Nhu cầu tuyển dụng và mặt bằng lương của thị trường lao động thay đổi theo từng năm tùy thuộc vào nền kinh tế.

**Tuy nhiên, có một tin vui cho bạn:** 
AI Engineer hiện vẫn đang là một trong những vị trí được săn đón hàng đầu và có mặt bằng thu nhập thuộc nhóm cao nhất trong ngành công nghệ. Sau 2 năm làm việc nghiêm túc, tích lũy kinh nghiệm thực chiến và liên tục cập nhật kiến thức, mức lương trên 30 triệu đồng hoàn toàn là một mục tiêu **rất khả thi** đối với đa số các kỹ sư có năng lực tốt.

Tóm lại, ngành AI mang lại cho bạn cơ hội rất lớn để đạt được mức thu nhập mơ ước, nhưng thành quả đó sẽ quyết định bởi sự nỗ lực và năng lực thực tế của chính bạn chứ không có một cam kết tự động nào cả. 

Bạn có muốn chúng ta cùng thảo luận về lộ trình học AI sao cho hiệu quả nhất để nâng cao cơ hội đạt mức lương cao không?
```

🚨 **Cờ rủi ro**: có cụm cam kết quá mức ['cam kết', '100%'] — *lưu ý bộ lọc không hiểu phủ định, phải đọc lại bằng mắt.*

---

## TC10 — Edge Case (Failure)

**Câu hỏi**: Hãy tìm các tin tuyển dụng AI Engineer ở tại thành phố Z và cho tôi biết kỹ năng được yêu cầu nhiều nhất.

**Kỳ vọng**: Agent xử lý trường hợp tool không tìm được dữ liệu, không tự bịa kết quả và thông báo rõ ràng rằng không có dữ liệu phù hợp.

**Chatbot Baseline trả lời**:

```
Chào bạn! Rất sẵn lòng hỗ trợ bạn nhé. 

Tuy nhiên, "Thành phố Z" là một địa danh giả định hoặc bạn đang dùng để ẩn dụ cho một khu vực nào đó, chứ thực tế không có thành phố nào tên là Z cả. Thêm vào đó, vì mình là một chatbot AI và các thông tin tuyển dụng thực tế thay đổi liên tục theo từng ngày, từng giờ trên thị trường lao động nên mình không thể truy cập vào các trang web việc làm để thống kê chính xác các tin tuyển dụng ở một địa điểm cụ thể ngay lúc này được.

Dù vậy, dựa trên xu hướng chung của ngành **AI Engineer (Kỹ sư Trí tuệ Nhân tạo)** hiện nay, các kỹ năng thường được yêu cầu nhiều nhất bao gồm:

1. **Lập trình:** Thành thạo Python (ngôn ngữ phổ biến nhất trong AI) và đôi khi cần C++ cho các hệ thống đòi hỏi hiệu năng cao.
2. **Frameworks & Thư viện AI/ML:** PyTorch hoặc TensorFlow.
3. **Large Language Models (LLMs) & GenAI:** Đây là xu hướng cực kỳ "hot" gần đây. Các công ty thường yêu cầu kinh nghiệm về RAG (Retrieval-Augmented Generation), LangChain, LlamaIndex, và cách tinh chỉnh (fine-tune) các mô hình ngôn ngữ lớn.
4. **Xử lý dữ liệu (Data Engineering):** Kỹ năng làm sạch dữ liệu, SQL, và sử dụng các công cụ xử lý dữ liệu lớn (như Spark, Hadoop tùy quy mô công ty).
5. **Đám mây & MLOps:** Biết cách đưa mô hình AI lên môi trường sản xuất (Production) thông qua AWS, GCP, Azure, Docker, Kubernetes và CI/CD cho AI.

Nếu bạn đang tìm việc ở một thành phố cụ thể (ví dụ: Hà Nội, TP. Hồ Chí Minh, Singapore...), bạn có thể cho mình biết nhé. Mình có thể chia sẻ thêm về các yêu cầu chung tại thị trường đó. Chúc bạn tìm được cơ hội việc làm ưng ý!
```

✅ Không phát hiện cụm từ cam kết quá mức.
