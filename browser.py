import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import webview  # Thư viện pywebview để hiển thị trang web
from ttkthemes import ThemedTk

# Hàm thực hiện GET, POST hoặc HEAD request
def simple_browser(url, method='GET', data=None):
    try:
        if not url.startswith('https'):
            messagebox.showerror("Error", "Please enter a valid URL starting with http:// or https://")
            return
        
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, data=data)
        elif method == 'HEAD':
            response = requests.head(url)
            display_response(f"HEAD Request Information:\n\n")
            for header, value in response.headers.items():
                display_response(f"{header}: {value}\n")
            return
        else:
            messagebox.showerror("Error", "Invalid request method!")
            return

        # Kiểm tra status code
        display_response(f"Status Code: {response.status_code}\n")

        # Nếu là GET hoặc POST, phân tích nội dung HTML
        if method in ['GET', 'POST']:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Hiển thị tiêu đề của trang
            title = soup.title.string if soup.title else 'No title'
            display_response(f"\nPage Title: {title}\n")

            # Tính số lượng các thẻ HTML <p>, <div>, <span>, <img>
            p_tags = len(soup.find_all('p'))
            div_tags = len(soup.find_all('div'))
            span_tags = len(soup.find_all('span'))
            img_tags = len(soup.find_all('img'))

            # Hiển thị chiều dài nội dung và số lượng thẻ
            display_response(f"\nContent Length: {len(response.content)} bytes\n")
            display_response(f"Number of <p> tags: {p_tags}\n")
            display_response(f"Number of <div> tags: {div_tags}\n")
            display_response(f"Number of <span> tags: {span_tags}\n")
            display_response(f"Number of <img> tags: {img_tags}\n")

            # Hiển thị trang web trong webview
            open_webview(url)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Hàm hiển thị kết quả trong Text widget
def display_response(content):
    response_textbox.config(state=tk.NORMAL)
    response_textbox.insert(tk.END, content + "\n")
    response_textbox.config(state=tk.DISABLED)

# Hàm mở webview
def open_webview(url):
    webview.create_window('WebView Browser', url)
    webview.start()

# Hàm xử lý khi người dùng nhấn nút "GET"
def send_get_request():
    url = url_entry.get()
    response_textbox.config(state=tk.NORMAL)
    response_textbox.delete(1.0, tk.END)  # Xóa nội dung cũ
    response_textbox.config(state=tk.DISABLED)
    
    # Gọi hàm simple_browser để thực hiện GET request
    simple_browser(url, method='GET')

# Hàm xử lý khi người dùng nhấn nút "POST"
def send_post_request():
    url = url_entry.get()
    post_data = post_data_entry.get()
    data = None
    if post_data:
        data = dict(item.split("=") for item in post_data.split("&"))

    response_textbox.config(state=tk.NORMAL)
    response_textbox.delete(1.0, tk.END)  # Xóa nội dung cũ
    response_textbox.config(state=tk.DISABLED)
    
    # Gọi hàm simple_browser để thực hiện POST request
    simple_browser(url, method='POST', data=data)

# Hàm xử lý khi người dùng nhấn nút "HEAD"
def send_head_request():
    url = url_entry.get()
    response_textbox.config(state=tk.NORMAL)
    response_textbox.delete(1.0, tk.END)  # Xóa nội dung cũ
    response_textbox.config(state=tk.DISABLED)
    
    # Gọi hàm simple_browser để thực hiện HEAD request
    simple_browser(url, method='HEAD')

# Tạo cửa sổ giao diện với ThemedTk
root = ThemedTk(theme="breeze")  # Đổi sang theme 'breeze'
root.title("Lab4")
root.configure(bg="#282828")  # Đổi màu nền

# Sử dụng ttk style để cải thiện giao diện
style = ttk.Style()
style.configure('TButton', font=('Arial', 10), padding=6, background="#FF99FF", foreground="white")
style.configure('TLabel', font=('Arial', 10), background="#282828", foreground="#3399FF")

# URL Label và Entry
url_label = ttk.Label(root, text="Enter URL:")
url_label.grid(column=0, row=0, padx=15, pady=15, sticky=tk.W)
url_entry = ttk.Entry(root, width=60)
url_entry.grid(column=1, row=0, padx=15, pady=15, columnspan=2)

# POST data Entry (nếu người dùng chọn POST)
post_data_label = ttk.Label(root, text="POST Data:")
post_data_label.grid(column=0, row=1, padx=15, pady=15, sticky=tk.W)
post_data_entry = ttk.Entry(root, width=60)
post_data_entry.grid(column=1, row=1, padx=15, pady=15, columnspan=2)

# Frame chứa các nút request
button_frame = ttk.Frame(root, style="TFrame", padding="10 10 10 10")
button_frame.grid(column=0, row=2, columnspan=3, pady=10)

# Nút "GET Request"
get_button = ttk.Button(button_frame, text="GET", command=send_get_request, style="TButton")
get_button.grid(column=0, row=0, padx=10)

# Nút "POST Request"
post_button = ttk.Button(button_frame, text="POST", command=send_post_request, style="TButton")
post_button.grid(column=1, row=0, padx=10)

# Nút "HEAD Request"
head_button = ttk.Button(button_frame, text="HEAD", command=send_head_request, style="TButton")
head_button.grid(column=2, row=0, padx=10)

# Khu vực hiển thị kết quả (ScrolledText)
response_textbox = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD, state=tk.DISABLED, font=('Courier New', 10), background='#1E1E1E', foreground='#DCDCDC')
response_textbox.grid(column=0, row=3, columnspan=3, padx=15, pady=15)

# Bắt đầu giao diện
root.mainloop()
