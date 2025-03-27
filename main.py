import os
import sys
from tkinter import Tk, Button, Label, ttk, Scrollbar, RIGHT, Y, Text
from functions import add_folder, delete_selected, start_processing, save_to_excel, reset_all

# GUI 구성
app = Tk()

if hasattr(sys, '_MEIPASS'):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_path, "pokemon.ico")
app.iconbitmap(True, icon_path)
app.title("동영상 재생 시간 계산기")
app.geometry("1000x650")

label = Label(app, text="동영상 재생시간 계산 프로그램", font=("Arial", 16, "bold"))
label.pack(pady=10)

folder_paths = []
file_data = []

# "1. 폴더 추가" 버튼
add_folder_button = Button(app, text="1. 폴더 추가", command=lambda: add_folder(folder_paths, text_folders), font=("Arial", 13))
add_folder_button.pack(pady=5)

# 선택된 폴더를 보여줄 영역 (Text + Scrollbar)
label_selected_folder = Label(app, text="선택된 폴더", font=("Arial", 12))
label_selected_folder.pack(anchor='w', padx=15)

folder_frame = ttk.Frame(app)
folder_frame.pack(pady=5, fill="x", padx=15)

folder_scrollbar = Scrollbar(folder_frame)
folder_scrollbar.pack(side=RIGHT, fill=Y)

text_folders = Text(folder_frame, height=4, font=("Arial", 11), wrap="word", yscrollcommand=folder_scrollbar.set)
text_folders.pack(fill="both", expand=True)
text_folders.insert("1.0", "없음")
text_folders.config(state="disabled")

folder_scrollbar.config(command=text_folders.yview)

# 2. 파일 확인
process_button = Button(app, text="2. 파일 확인",
                        command=lambda: start_processing(folder_paths, file_data, tree, app, label_progress),
                        font=("Arial", 13))
process_button.pack(pady=5)

label_progress = Label(app, text="진행: 0/0", font=("Arial", 11))
label_progress.pack(pady=5)

# 표 구성
table_frame = ttk.Frame(app)
table_frame.pack(padx=15, pady=10, fill="both", expand=True)

tree_scrollbar = ttk.Scrollbar(table_frame)
tree_scrollbar.pack(side="right", fill="y")

tree = ttk.Treeview(table_frame, columns=("순번", "파일명", "폴더", "시간"),
                    show="headings", yscrollcommand=tree_scrollbar.set, height=10)
tree.pack(side="left", fill="both", expand=True)
tree_scrollbar.config(command=tree.yview)

tree.heading("순번", text="순번")
tree.heading("파일명", text="파일명")
tree.heading("폴더", text="폴더")
tree.heading("시간", text="재생시간")

tree.column("순번", width=30, anchor="center")
tree.column("파일명", width=280)
tree.column("폴더", width=400)
tree.column("시간", width=100, anchor="center")

# 하단 버튼
button_frame = ttk.Frame(app)
button_frame.pack(pady=3)
# 선택된 파일 제외 버튼
delete_button = Button(
    button_frame,
    text="선택된 파일 제외",
    command=lambda: delete_selected(file_data, tree),
    font=("Arial", 10)
)
delete_button.pack(side="left", padx=5)
# 모두 초기화 버튼
reset_button = Button(
    button_frame,
    text="모두 초기화",
    command=lambda: reset_all(folder_paths, file_data, text_folders, label_progress, tree),
    font=("Arial", 10)
)
reset_button.pack(side="left", padx=5)

# 3. 엑셀 다운로드 버튼
save_button = Button(app, text="3. 엑셀 다운로드", command=lambda: save_to_excel(file_data, app), font=("Arial", 13))
save_button.pack(pady=10)

app.mainloop()