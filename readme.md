# Phân Loại Chủ Đề Và Phân Cụm Bài Báo Dựa Trên  Tiêu Đề Và Nội Dung

Gồm các thành viên:
* Nguyễn An Hưng
* Nguyễn Cửu Nhật Quang
* Nguyễn Đình Anh Tiến
---

**Lý do chọn đề tài**: Trong những năm gần đây, công nghệ 4.0 dần phát triển mạnh ở nước ta (Việt Nam), đơn cử là sự hiện diện của AI, những mô hình tự sinh như chatGPT, mô hình ngôn ngữ lớn,... đã và đang hỗ trợ cho chúng ta trong việc xử lý các bài toán về dữ liệu ngôn ngữ một cách thuận tiện. Tuy nhiên, để phân loại chúng theo các chủ đề vẫn là một bài toán quan trọng bởi đối với những phóng viên báo chí mong muốn tự động hóa quá trình gán chủ đề / nhãn cho bài viết của mình hay đối với đọc giả mong muốn tìm kiếm các bài viết theo chủ đề mong muốn.


**Mục đích đề tài**: Bài toán được xây dựng với mục đích gán chủ đề/ nhãn một cách tự động cho một bài viết đang thực hiện (real-time) bởi tác giả, hoặc xác định các chủ đề, các bài viết liên quan cho các bài báo chưa được gán chủ đề.

Giải pháp đề xuất bao gồm các bước sau: Sau khi trích xuất các trường dữ liệu từ bài báo như tiêu đề, mô tả và nội dung, dữ liệu sẽ được tiền xử lý qua các bước làm sạch, tokenizer và loại bỏ stopwords. Tiếp theo, dữ liệu được chuyển đổi và trích xuất đặc trưng, đánh trọng số cho các trường trước khi gộp lại. Các phương pháp TF-IDF, Feature Hashing và một phương pháp kết hợp do nhóm đề xuất sẽ được sử dụng để biến đổi dữ liệu văn bản thành vector đặc trưng số hóa. Vector này sẽ được sử dụng cho hai bài toán: phân loại chủ đề và mô hình hóa chủ đề. Trong phân loại chủ đề, mô hình sẽ đưa ra xác suất của nhãn cao nhất, còn trong mô hình hóa chủ đề, mô hình sẽ xác định vector đặc trưng gần với chủ đề nào nhất.

## Cấu trúc thư mục
- `cleaned_data`: nơi chưa các dữ liệu đã làm sạch - bao gồm 2 files là tệp tin lấy `600` mẫu từng chủ đề (`new_data_train.csv`) sử dụng cho huấn luyện và xác thực mô hình  và (`new_data_test.csv`) sử dụng cho kiểm thử mô hình.
- `raw_data`: nơi chứa dữ liệu thô, bao gồm 2 files đã được tổng hợp từ 2 nguồn dữ liệu [báo Dân Trí](https://dantri.com.vn) và [báo VNExpress](https://vnexpress.net)
- `requirement_files`: Bao gồm các tệp tin cần thiết cho quá trình chạy của hệ thống, trong folder này bao gồm các tệp tin và thư mục như:
    *  `data`: Chứa các dữ liệu sử dụng cho việc huấn luyện mô hình
        *  `class_names.txt`: Chứa các nhãn chủ đề, mỗi chủ đề nằm trên 1 dòng tương ứng vị trí tại dòng đó là chỉ số của chủ đề
        * `X_train.txt`: Sử dụng làm dữ liệu đầu vào huấn luyện của mô hình
        * `y_train.txt`: là tệp tin chứa các nhãn tương ứng với các dòng dữ liệu từ tệp `X_train.txt`
        * `X_valid.txt`: là tệp tin sử dụng cho việc xác thực và dựa vào đó để tinh chỉnh tham số của mô hình
        * `y_train.txt`: là tệp tin chứa các nhãn tương ứng với các dòng dữ liệu từ tệp `X_valid.txt`
    * `abbreviations.txt`: chứa các từ viết tắt.
    * `vietnamese-stopwords.txt`: chứa các từ stopwords.
    * `requirements.txt`: là file chứa các thông tin về thư viện yêu cầu sử dụng các tệp tin chương trình (.py) hoặc các tệp tin jupyter notebook

- `craw_data.py`: là tệp tin chương trình crawl dữ liệu từ trang dantri.com.vn, có thể sử dụng cú pháp bên dưới để crawl dữ liệu:
```bash
$ python craw_data.py --url "https://dantri.com.vn" --out_dir "dantri_test" --page 10
```

- `Crawl_and_TrucQuanHoaDuLieu_KHDL_21TDT_Team21.ipynb`: là file notebook dùng để chạy chương trình crawl dữ liệu, phân tích dữ liệu và trực quan hóa dữ liệu.
- `KhaoSatThamSo.ipynb`: là file notebook chứa các chương trình khảo sát các tham số như: 
    * Trọng số của các trường đặc trưng: tiêu đề, mô tả, nội dụng
    * Khảo sát tham số trong TF-IDF
    * Khảo sát tham số của hai mô hình Multinomial Naive Bayes và RandomForest
- `TF-IDF_FeatureHashing_Team21_KHDL_Feature_extraction_and_Modeling.ipynb`: là file notebook dùng để chạy các chương trình trích xuất đặc trưng, vector hóa dữ liệu và kiểm nghiệm chúng thông qua việc huấn luyện mô hình với bộ dữ liệu huấn luyện, kiểm thử chúng trên bộ dữ liệu kiểm thử. Trong tệp tin này thực hiện hai phương pháp TF-IDF và Feature Hashing (custom).
- `PP_KetHop_FeatureHashing_Team21_KHDL_Feature_extraction_and_Modeling.ipynb`: là file notebook dùng để chạy các chương trình trích xuất đặc trưng, vector hóa dữ liệu và kiểm nghiệm chúng thông qua việc huấn luyện mô hình với bộ dữ liệu huấn luyện, kiểm thử chúng trên bộ dữ liệu kiểm thử. Trong tệp tin này thực hiện phương pháp nhóm tác giả đề xuất kết hợp TF-IDF với cố định chiều vector đặc trưng.
- `TopicModeling.ipynb`: là tệp tin chứa các chương trình thực thi việc mô hình hóa chủ đề (có thể xem là phân cụm dữ liệu nhưng thực tế Topic Modeling tương tự nhưng không được gọi là phân cụm dữ liệu)
- `TieuLuanKHDL_Team21_21TDT.pdf`: là tệp tin Tiểu luận khoa học tổng hợp lại những điều mà nhóm đã nghiên cứu để giải quyết bài toán đã đề ra.
- `Team21_KHDL_Presentation_Final.pdf`: là slides nhóm sử dụng cho việc trình bày các điều mà nhóm đã cải tiến giúp độ chính xác của mô hình tăng lên, ngoài ra nhóm còn thuyết trình về bài toán mới là topic modeling.
- `readme.md`: là file hướng dẫn.

## Hướng dẫn chạy chương trình
Trước khi chạy các mã nguồn, mọi người cần cài đặt các thư viện cần thiết bằng 
```bash
pip install -r requirement_files/requirements.txt
```
Sau khi cài đặt thư viện, mọi người có thể cài đặt thêm jupyter notebook hoặc jupyter lab để thực hiện việc chạy chương trình. Ngoài ra, có thể sử dụng VS Code để chạy chương trình trên file notebook.

### Đối với crawl dữ liệu ở trang dantri.com.vn
Khi thực hiện crawl tại trang này, khi chạy code chương trình sẽ tự tạo một thư mục `dantri`, sau đó sẽ lưu các đường dẫn tới các chủ đề của các bài báo cụ thể `url_****.txt`, từ những file này code sẽ thực hiện việc lấy dữ liệu trên từng chủ đề và ghi thành các file có định dạng `<chu_de>.csv` và đồng thời ghi chúng vào file `dantri.csv`.


### Đối với crawl dữ liệu ở trang vnexpress.net
Dữ liệu được crawl theo từng chủ đề nên cần có bước tổng hợp các chủ đề lại thành một file `vne.csv` duy nhất. (có thể sử dụng thư viện pandas và câu lệnh `pandas.concat`) 

## References
* [https://viblo.asia/p/tien-xu-li-du-lieu-van-ban-voi-nltk-Az45b0LgZxY](https://viblo.asia/p/tien-xu-li-du-lieu-van-ban-voi-nltk-Az45b0LgZxY)
* [https://towardsdatascience.com/website-data-cleaning-in-python-for-nlp-dda282a7a871](https://towardsdatascience.com/website-data-cleaning-in-python-for-nlp-dda282a7a871)
* [https://viblo.asia/p/text-processing-in-nlp-projects-bWrZnwQwlxw](https://viblo.asia/p/text-processing-in-nlp-projects-bWrZnwQwlxw)
* [https://viblo.asia/p/cai-dat-mo-hinh-phan-loai-cam-xuc-tieng-viet-018J2vdRJYK](https://viblo.asia/p/cai-dat-mo-hinh-phan-loai-cam-xuc-tieng-viet-018J2vdRJYK)
* [https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud](https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html#wordcloud.WordCloud)
* [https://www.datacamp.com/tutorial/wordcloud-python](https://www.datacamp.com/tutorial/wordcloud-python)
* [https://www.analyticsvidhya.com/blog/2021/12/text-classification-of-news-articles/](https://www.analyticsvidhya.com/blog/2021/12/text-classification-of-news-articles/)
* [https://viblo.asia/p/text-processing-in-nlp-projects-bWrZnwQwlxw](https://viblo.asia/p/text-processing-in-nlp-projects-bWrZnwQwlxw)