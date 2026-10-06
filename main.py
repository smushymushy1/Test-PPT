"""main.py
Root Cause Analysis (RCA) Report Tool.

Install dependencies first:
    py -m pip install -r requirements.txt

Run:
    py main.py
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import rca_engine
import export_pptx


class RcaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("원인 분석 보고서 도구 (RCA Report Tool)")
        self.root.geometry("1100x700")

        self.df = None
        self.category_col = tk.StringVar()
        self.title_var = tk.StringVar(value="원인 분석 보고")

        self._build_layout()

    def _build_layout(self):
        left = ttk.Frame(self.root, width=320)
        left.pack(side="left", fill="y", padx=10, pady=10)
        right = ttk.Frame(self.root)
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ttk.Label(left, text="보고서 제목", font=("맑은 고딕", 10, "bold")).pack(anchor="w")
        ttk.Entry(left, textvariable=self.title_var).pack(fill="x", pady=(0, 15))

        ttk.Label(left, text="1. 엑셀 파일 불러오기", font=("맑은 고딕", 10, "bold")).pack(anchor="w")
        ttk.Button(left, text="파일 선택", command=self.load_file).pack(fill="x", pady=(0, 15))
        self.lbl_file = ttk.Label(left, text="선택된 파일 없음", foreground="gray", wraplength=300)
        self.lbl_file.pack(anchor="w", pady=(0, 15))

        ttk.Label(left, text="2. 원인 카테고리 컬럼 선택", font=("맑은 고딕", 10, "bold")).pack(anchor="w")
        self.cb_category = ttk.Combobox(left, textvariable=self.category_col, state="readonly")
        self.cb_category.pack(fill="x", pady=(0, 15))

        ttk.Button(left, text="🔄 미리보기", command=self.update_preview).pack(fill="x", pady=5)
        ttk.Button(left, text="💾 PPT로 저장", command=self.save_pptx).pack(fill="x", pady=5)

        self.canvas_frame = ttk.Frame(right)
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = None

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if not path:
            return
        try:
            self.df = rca_engine.load_excel(path)
        except Exception as e:
            messagebox.showerror("오류", f"엑셀 파일을 읽을 수 없습니다.\n{e}")
            return
        self.lbl_file.config(text=path, foreground="black")
        self.cb_category["values"] = list(self.df.columns)
        if len(self.df.columns):
            self.category_col.set(self.df.columns[0])

    def generate_figure(self):
        fig = plt.Figure(figsize=(8, 5.5), dpi=100)
        ax = fig.add_subplot(111)
        if self.df is None or not self.category_col.get():
            ax.text(0.5, 0.5, "엑셀 파일과 카테고리 컬럼을 먼저 선택해 주세요.",
                     ha="center", va="center", color="gray")
            ax.set_xticks([])
            ax.set_yticks([])
        else:
            counts = rca_engine.count_categories(self.df, self.category_col.get())
            rca_engine.draw_ranked_bar_chart(ax, counts, title=self.title_var.get())
        fig.tight_layout()
        return fig

    def update_preview(self):
        if self.df is None:
            messagebox.showinfo("안내", "엑셀 파일을 먼저 선택해 주세요.")
            return
        if not self.category_col.get():
            messagebox.showinfo("안내", "원인 카테고리 컬럼을 선택해 주세요.")
            return
        fig = self.generate_figure()
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def save_pptx(self):
        if self.df is None or not self.category_col.get():
            messagebox.showinfo("안내", "먼저 미리보기를 실행해 주세요.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".pptx", filetypes=[("PPT", "*.pptx")])
        if not save_path:
            return
        export_pptx.export_to_pptx(self.generate_figure(), save_path)
        messagebox.showinfo("성공", "PPT가 저장되었습니다.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RcaApp(root)
    root.mainloop()
