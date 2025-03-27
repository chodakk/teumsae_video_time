import os
import threading
import uuid
from tkinter import messagebox, filedialog, Toplevel, Label, Button, ttk
import pandas as pd
import tkfilebrowser
from pymediainfo import MediaInfo


def get_video_duration(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == "Video":
            duration_in_seconds = int(track.duration / 1000)
            hours = duration_in_seconds // 3600
            minutes = (duration_in_seconds % 3600) // 60
            seconds = duration_in_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"


def add_folder(folder_paths, text_folders):
    selected = tkfilebrowser.askopendirnames(title="파일 선택하기")
    if selected:
        for folder in selected:
            if folder not in folder_paths:
                folder_paths.append(folder)

        # 텍스트 업데이트
        text_folders.config(state="normal")
        text_folders.delete("1.0", "end")
        text_folders.insert("1.0", "\n".join(folder_paths))
        text_folders.config(state="disabled")


def update_table(file_data, tree):
    for row in tree.get_children():
        tree.delete(row)
    for idx, data in enumerate(file_data, 1):
        tree.insert("", "end", iid=data["id"], values=(idx, data["디렉토리"], data["파일명"], data["시간"]))


def delete_selected(file_data, tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("경고", "삭제할 항목을 선택하세요.")
        return
    new_file_data = [item for item in file_data if item["id"] not in selected]
    file_data.clear()
    file_data.extend(new_file_data)
    update_table(file_data, tree)


def process_videos_thread(folder_paths, file_data, tree, app, label_progress):
    total_files = 0
    for folder in folder_paths:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
                    total_files += 1
    if total_files == 0:
        app.after(0, lambda: messagebox.showwarning("경고", "선택한 폴더에 유효한 동영상 파일이 없습니다."))
        return
    current_count = 0
    for folder in folder_paths:
        for root, dirs, files in os.walk(folder):
            for file_name in files:
                if file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
                    file_path = os.path.join(root, file_name)
                    try:
                        duration = get_video_duration(file_path)
                        file_data.append({
                            "id": str(uuid.uuid4()),
                            "디렉토리": root,
                            "파일명": file_name,
                            "시간": duration
                        })
                    except Exception as e:
                        print(f"Error processing {file_name}: {e}")
                        file_data.append({
                            "id": str(uuid.uuid4()),
                            "디렉토리": root,
                            "파일명": file_name,
                            "시간": "Error"
                        })
                    current_count += 1
                    app.after(0, lambda c=current_count, t=total_files: label_progress.config(text=f"진행: {c}/{t}"))
    app.after(0, lambda: update_table(file_data, tree))
    app.after(0, lambda: messagebox.showinfo("완료", f"총 {len(file_data)}개의 동영상 파일을 처리했습니다."))


def start_processing(folder_paths, file_data, tree, app, label_progress):
    threading.Thread(target=process_videos_thread, args=(folder_paths, file_data, tree, app, label_progress), daemon=True).start()


def save_to_excel(file_data, app):
    if not file_data:
        messagebox.showwarning("경고", "먼저 동영상 파일을 처리하세요.")
        return

    sorted_data = sorted(file_data, key=lambda x: x["파일명"])

    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel 파일", "*.xlsx")],
                                             title="엑셀 파일 저장 경로 선택")

    if save_path:
        df = pd.DataFrame(sorted_data, columns=["파일명", "시간"])
        df["시간"] = df["시간"].str.replace("초", "", regex=False)
        df.to_excel(save_path, index=False)

        show_custom_popup(save_path, app)


def open_file(path):
    try:
        os.startfile(path)  # Windows 전용
    except Exception as e:
        messagebox.showerror("오류", f"파일을 여는 데 실패했습니다:\n{e}")


def show_custom_popup(path, app):
    popup = Toplevel(app)
    popup.title("엑셀 저장 완료")
    popup.geometry("500x100")
    popup.resizable(False, False)

    msg = Label(popup, text=f"엑셀 파일이 저장되었습니다!\n{path}", font=("Arial", 11), wraplength=450, justify="center")
    msg.pack(pady=10)

    btn_frame = ttk.Frame(popup)
    btn_frame.pack()

    open_btn = Button(btn_frame, text="파일 확인하기", font=("Arial", 11), command=lambda: open_file(path))
    open_btn.pack(side="left", padx=5)

    close_btn = Button(btn_frame, text="확인", font=("Arial", 11), command=popup.destroy)
    close_btn.pack(side="right", padx=5)


def reset_all(folder_paths, file_data, text_folders, label_progress, tree):
    folder_paths.clear()
    file_data.clear()

    text_folders.config(state="normal")
    text_folders.delete("1.0", "end")
    text_folders.insert("1.0", "없음")
    text_folders.config(state="disabled")
    label_progress.config(text="진행: 0/0")
    for row in tree.get_children():
        tree.delete(row)
