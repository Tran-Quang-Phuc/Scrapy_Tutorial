# Scrapy_tutorial
Scrapy là một framework được viết bằng Python, nó cung cấp một cấu trúc tương đối đầy đủ cho việc thu thập thông tin và trích xuất dữ liệu từ các trang Web một cách nhanh chóng và dễ dàng.

![Scrapy](https://raw.githubusercontent.com/tuantmtb/int3507-2017/master/group3/img/Scrapy-Logo.png)

# 1. Scrapy Architecture
## 1.1. Thành phần
Scrapy được thiết kế bao gồm 7 thành phần chính sau:

**Scrapy Engine**

Engine chịu trách nhiệm điều khiển luồng giữa các thành phần của hệ thống.

**Scheduler**

Scheduler nhận các requests từ Engine và lập lịch thứ tự cho các URLs cần tải.

**Downloader**

Downloader chịu trách nhiệm cho việc tìm tải các trang Web và cung cấp chúng cho Engine.

**Spider**

Spiders là class do người dùng viết, dùng để bóc tách dữ liệu cần thiết và tạo các URLs mới để nạp lại cho Scheduler qua Engine.

**Item Pipeline**

Item Pipeline chịu trách nhiệm xử lý các dữ liệu đã được bóc tách bởi Spiders và lưu trữ chúng vào cơ sở dữ liệu.

**Downloader middlewares**

Downloader middlewares nằm giữa Engine và Downloader, xử lý các response được đẩy vào từ Engine và các response được tạo từ Downloader.

**Spider middlewares**

Spider middlewares nằm giữa Engine và Spiders, xử lý các response đầu vào của Spiders và đầu ra (item và các URLs mới).
## 1.2. Data flow
![Data flow image](https://doc.scrapy.org/en/latest/_images/scrapy_architecture_02.png)


  1. Engine lấy các request được khởi tạo ban đầu từ Spider.
  2. Engine lập lịch các request trong Scheduler và yêu cầu request tiếp theo để crawl.
  3. Scheduler gửi request tiếp theo đến Engine.
  4. Engine gửi request tới Downloader, đi qua Downloader middlewares.
  5. Sau khi hoàn tất việc tải trang Web, Dowloader tạo một đối tượng response gửi đến Engine, đi qua Downloader middlewares.
  6. Engine nhận respoonse từ Downloader,và gửi về Spider để xử lí, đi qua Spider middleware.
  7. Spider xử lí response và trả về các item đã được bóc tách,sau đó khởi tạo request đến Engine,thông qua Spider middleware.
  8. Engine gửi các item đã được xử lí đến Item Pipelines, sau đó gửi các requests đã được xử lí đến Scheduler và yêu cầu (nếu có ) request tiếp theo để crawl.
  9. Tiến trình lặp lại như bước 1,cho đến khi không còn request nào từ Scheduler.

## 1.3. Cấu trúc của Scrapy project
Để tạo một Scrapy project, ta thực hiện câu lệnh:
    
    scrapy startproject project_name

Hệ thống sẽ tạo một thư mục *project_name* có cấu trúc như sau:

    project_name/
        project_name/               # nơi chứa code của dự án
            __init__.py
            items.py                # nơi định nghĩa các trường dữ liệu cần lưu vào DB
            middlewares.py
            pipelines.py            # nơi xử lý các item trích xuất được và lưu vào DB
            settings.py             # cấu hình thêm các phần mở rộng và các thông số cấu hình khác
            spiders/                # thư mục chứa các spider
                __init__.py
        scrapy.config               # file cấu hình về deploy và setting của project

# 2. Spider

Spiders là các lớp định nghĩa cách thu thập một hoặc nhiều trang Web, bao gồm việc thực hiện thu thập và bóc tách các dữ liệu có cấu trúc từ các trang đó. Nói cách khác, Spiders là nơi mà chúng ta định nghĩa các hành vi tùy chỉnh cho việc thu thập dữ liệu và phân tích cú pháp cho từng trang cụ thể.

Chu trình thu thập dữ liệu với Spiders trải qua các bước như sau:

  1. Chúng ta bắt đầu tạo các *requests* ban đầu để thu thập thông tin từ các URLs đầu tiên và chỉ định hàm *callback* sẽ được gọi với các *response* được tải về qua các *requests* đó. Các *request* đầu tiên được thực hiện bằng cách gọi phương thức *start_request()*, phương thức này tạo các *requests* cho các URLs được chỉ định trong *start_urls* và phương thức *parse()* là hàm *callback* cho các *requests* đó.
  2. Trong hàm *callback*, *response* (Web page) sẽ được phân tích và trả về các đối tượng *Item*, *Request*. Những *requests* này cũng sẽ bao gồm một hàm *callback* và sau đó sẽ được tải xuống và *response* của chúng sẽ được xử lý bởi hàm *callback* đã được chỉ định.
  3. Nội dung trang sẽ được phân tích trong hàm *callback*, thường bằng cách sử dụng các *Selectors* (hoặc có thể sử dụng BeautifulSoup, Ixml, v.v...) và tạo ra các *items* với dữ liệu đã được phân tích.
  4. Cuối cùng các *items* được trả về từ *Spider* sẽ được duy trì trong cơ sở dữ liệu hoặc được ghi vào một tập tin sử dụng *Feed exports*.

Mặc dù chu trình này áp dụng cho mọi *Spider*, tuy nhiên vẫn có nhiều loại *Spider* mặc định khác nhau trong Scrapy cho các mục đích khác nhau.

## 2.1. scrapy.Spider
    class scrapy.spiders.Spider
    class scrapy.Spider

Đây là *Spider* đơn giản nhất, và là lớp mà mọi *Spider* khác đều phải kế thừa. Nó không cung cấp bất cứ chức năng đặc biệt nào mà chỉ cung cấp phương thức *start_requests()* mặc định thực hiện gửi các *requests* từ thuộc tính *start_urls* và gọi phương thức *parse()* của *Spider* cho mỗi *response* trả về.

## 2.2. Đối số Spider
*Spiders* có thể nhận các đối số sửa đổi hành vi của chúng. Một số các trường hợp phổ biến sử dụng đối số *Spider* là để xác định các URLs bắt đầu hoặc hạn chế thu thập thông tin đến các phần nhất định của trang Web. Tuy nhiên chúng có thể được sử dụng để cấu hình bất kỳ chức năng nào của *Spider*.

Các đối số *Spider* có thể được truyền thông qua lệnh *crawl* dùng tùy chọn *-a*. Ví dụ:

    scrapy crawl spider_name -a category=electronics

*Spider* có thể truy cập các đối số trong phương thức *__init__()* của chúng.

    import scrapy

    class MySpider(scrapy.Spider):
        name = 'myspider'

        def __init__(self, category=None, *args, **kwargs):
            super(MySpider, self).__init__(*args, **kwargs)
            self.start_urls = [f'http://www.example.com/categories/{category}']

Phương thức mặc định __init__ sẽ lấy bất kỳ đối số *Spider* nào và copy chúng vào trong *Spider* như các thuộc tính. Ví dụ trên cũng có thể viết như sau:

    import scrapy

    class MySpider(scrapy.Spider):
        name = 'myspider'

        def start_requests(self):
            yield scrapy.Request(f'http://www.example.com/categories/{category}')

## 2.3. Một vài Spiders phổ biến
Scrapy đi kèm với một số *Spiders* hữu ích mà có thể dùng để phân lớp các *Spiders*. Mục đích của chúng là cung cấp chức năng thuận tiện cho các trường hợp thu thập dữ liệu phổ biến như đi theo tất cả các liên kết trong một trang dựa trên một số quy tắc nhất định, thu thập từ *Sitemaps* hoặc phân tích nguồn cung cấp dữ liệu XML/CSV.

### CrawlSpider

