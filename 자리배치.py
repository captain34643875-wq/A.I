import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class SeatingChartApp:
    def __init__(self, master):
        self.master = master
        master.title("자리 배치 프로그램 v2.0")
        master.geometry("800x700") # 창 크기 기본 설정
        master.configure(bg="#f4f4f9")

        self.rows = 5
        self.cols = 5
        self.names = []
        self.seating_plan = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.fixed_seats = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.selected_seat = None

        # 폰트 스타일 설정
        self.font_large = ('Helvetica', 12, 'bold')
        self.font_medium = ('Helvetica', 10)

        # 3개의 주요 프레임: 입력/설정, 실행 버튼, 자리 배치도
        self.main_frame = tk.Frame(master, bg="#f4f4f9")
        self.main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.setup_ui()
        self.draw_seating_chart()

    def setup_ui(self):
        # ----------------------------------------------------
        # 1. 좌측 패널 (이름 관리 및 설정)
        # ----------------------------------------------------
        left_panel = tk.Frame(self.main_frame, bg="#ffffff", padx=15, pady=15, relief=tk.SUNKEN, borderwidth=1)
        left_panel.pack(side=tk.LEFT, fill="y", padx=(0, 15))

        # 이름 입력
        tk.Label(left_panel, text="📌 이름 관리", font=self.font_large, bg="#ffffff", fg="#333333").pack(pady=(0, 10))
        
        name_input_frame = tk.Frame(left_panel, bg="#ffffff")
        name_input_frame.pack(fill="x", pady=5)
        
        tk.Label(name_input_frame, text="이름:", font=self.font_medium, bg="#ffffff").pack(side=tk.LEFT)
        self.single_name_entry = tk.Entry(name_input_frame, width=15, font=self.font_medium)
        self.single_name_entry.pack(side=tk.LEFT, padx=5, expand=True, fill="x")
        
        tk.Button(name_input_frame, text="추가", command=self.add_single_name, font=self.font_medium, bg="#4CAF50", fg="white", activebackground="#66BB6A").pack(side=tk.LEFT)

        # 이름 리스트박스
        listbox_frame = tk.Frame(left_panel, bg="#ffffff")
        listbox_frame.pack(fill="both", expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        self.name_listbox = tk.Listbox(listbox_frame, height=15, font=self.font_medium, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, borderwidth=1, relief="solid")
        self.name_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.name_listbox.yview)

        # 이름 제거 버튼
        tk.Button(left_panel, text="선택 이름 제거", command=self.remove_selected_name, font=self.font_medium, bg="#F44336", fg="white", activebackground="#E57373").pack(fill="x", pady=(0, 10))
        
        # 책상 크기 설정
        tk.Label(left_panel, text="📐 책상 크기 설정", font=self.font_large, bg="#ffffff", fg="#333333").pack(pady=(10, 5))
        
        size_frame = tk.Frame(left_panel, bg="#ffffff")
        size_frame.pack(fill="x")
        
        tk.Label(size_frame, text="행:", font=self.font_medium, bg="#ffffff").pack(side=tk.LEFT)
        self.row_entry = tk.Entry(size_frame, width=5, font=self.font_medium)
        self.row_entry.insert(0, str(self.rows))
        self.row_entry.pack(side=tk.LEFT, padx=(5, 10))

        tk.Label(size_frame, text="열:", font=self.font_medium, bg="#ffffff").pack(side=tk.LEFT)
        self.col_entry = tk.Entry(size_frame, width=5, font=self.font_medium)
        self.col_entry.insert(0, str(self.cols))
        self.col_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(left_panel, text="크기 변경 적용", command=self.resize_chart, font=self.font_medium, bg="#2196F3", fg="white", activebackground="#64B5F6").pack(fill="x", pady=(10, 0))


        # ----------------------------------------------------
        # 2. 우측 상단 (제어 버튼)
        # ----------------------------------------------------
        right_panel = tk.Frame(self.main_frame, bg="#f4f4f9")
        right_panel.pack(side=tk.TOP, fill="x")

        tk.Button(right_panel, text="✨ 랜덤 배치 실행", command=self.random_seating, font=self.font_large, bg="#FFC107", fg="black", activebackground="#FFD54F").pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10), pady=10)
        tk.Button(right_panel, text="🔄 전체 자리 비우기", command=self.clear_seating, font=self.font_medium, bg="#BDBDBD", fg="black", activebackground="#E0E0E0").pack(side=tk.LEFT, fill="x", expand=True, pady=10)

        # ----------------------------------------------------
        # 3. 우측 하단 (자리 배치도)
        # ----------------------------------------------------
        self.seating_container = tk.Frame(self.main_frame, bg="#e0e0e0", padx=10, pady=10, relief=tk.RIDGE, borderwidth=2)
        self.seating_container.pack(side=tk.BOTTOM, fill="both", expand=True)

        tk.Label(self.seating_container, text="🧑‍🏫 자리 배치도 (좌클릭: 배치/고정, 우클릭: 스왑 시작)", font=self.font_large, bg="#e0e0e0", fg="#333333").pack(pady=(0, 10))
        self.seating_frame = tk.Frame(self.seating_container, bg="#e0e0e0")
        self.seating_frame.pack(expand=True)
        
    # --- 이름 관리 함수 ---

    def update_name_listbox(self):
        """이름 리스트를 Listbox에 반영합니다."""
        self.name_listbox.delete(0, tk.END)
        for name in self.names:
            self.name_listbox.insert(tk.END, name)

    def add_single_name(self):
        """한 명의 이름을 입력받아 리스트에 추가합니다."""
        name = self.single_name_entry.get().strip()
        if name:
            if name not in self.names:
                self.names.append(name)
                self.single_name_entry.delete(0, tk.END)
                self.update_name_listbox()
            else:
                messagebox.showwarning("경고", f"'{name}'은(는) 이미 등록된 이름입니다.")
        else:
            messagebox.showwarning("경고", "이름을 입력해 주세요.")
            
    def remove_selected_name(self):
        """Listbox에서 선택된 이름을 리스트에서 제거합니다."""
        selected_indices = self.name_listbox.curselection()
        if selected_indices:
            index = selected_indices[0]
            name_to_remove = self.names.pop(index)
            self.update_name_listbox()
            # 배치된 자리에서 이름 제거 (선택적)
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.seating_plan[r][c] == name_to_remove:
                        self.seating_plan[r][c] = ''
                        self.fixed_seats[r][c] = False
            self.draw_seating_chart()
            messagebox.showinfo("제거 완료", f"'{name_to_remove}' 이름을 리스트에서 제거했습니다. 배치된 자리도 비워졌습니다.")
        else:
            messagebox.showwarning("경고", "제거할 이름을 목록에서 선택해 주세요.")

    # --- 설정 및 배치 함수 (이전과 동일) ---

    def resize_chart(self):
        """사용자 입력에 따라 책상 크기를 변경하고 다시 그립니다."""
        try:
            new_rows = int(self.row_entry.get())
            new_cols = int(self.col_entry.get())
            if new_rows <= 0 or new_cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("오류", "행과 열은 1 이상의 정수로 입력해야 합니다.")
            return

        self.rows = new_rows
        self.cols = new_cols
        self.seating_plan = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.fixed_seats = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_seating_chart()
        messagebox.showinfo("크기 변경", f"책상 배치가 {self.rows}행 {self.cols}열로 변경되었습니다.")

    def clear_seating(self):
        """모든 자리의 배치와 고정 설정을 초기화합니다."""
        self.seating_plan = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        self.fixed_seats = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.draw_seating_chart()
        messagebox.showinfo("초기화", "모든 자리가 비워졌습니다.")
    
    def random_seating(self):
        """고정된 자리를 제외하고 나머지 이름을 무작위로 배치합니다."""
        if not self.names:
            messagebox.showwarning("경고", "먼저 이름을 등록해 주세요.")
            return

        fixed_names = []
        available_names = list(self.names)
        new_seating_plan = [['' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 1. 고정된 자리 유지 및 사용된 이름 리스트에서 제거
        for r in range(self.rows):
            for c in range(self.cols):
                if self.fixed_seats[r][c] and self.seating_plan[r][c]:
                    name = self.seating_plan[r][c]
                    new_seating_plan[r][c] = name
                    if name in available_names:
                        available_names.remove(name)

        # 2. 무작위 배치할 빈 자리 찾기
        empty_seats = []
        for r in range(self.rows):
            for c in range(self.cols):
                if not new_seating_plan[r][c]:
                    empty_seats.append((r, c))

        # 3. 남은 이름을 빈자리에 무작위로 배치
        random.shuffle(available_names)
        
        if len(available_names) > len(empty_seats):
            messagebox.showwarning("경고", f"자리({len(empty_seats)}개)보다 이름({len(available_names)}개)이 더 많아 모든 이름을 배치할 수 없습니다.")
            available_names = available_names[:len(empty_seats)]

        for (r, c), name in zip(empty_seats, available_names):
            new_seating_plan[r][c] = name
            
        self.seating_plan = new_seating_plan
        self.draw_seating_chart()
        messagebox.showinfo("완료", "랜덤 배치가 완료되었습니다.")

    def seat_click(self, r, c):
        """자리 버튼 클릭 시 동작: 이름 입력, 고정, 스왑"""
        current_name = self.seating_plan[r][c]
        
        # --- 1. 위치 스왑 기능 (두 번째 클릭) ---
        if self.selected_seat:
            r1, c1 = self.selected_seat
            
            if r1 == r and c1 == c: # 같은 자리 다시 누른 경우 스왑 취소
                self.selected_seat = None
                self.draw_seating_chart()
                return
            
            # 스왑 로직
            name1 = self.seating_plan[r1][c1]
            name2 = self.seating_plan[r][c]
            
            fixed1 = self.fixed_seats[r1][c1]
            fixed2 = self.fixed_seats[r][c]
            
            self.seating_plan[r1][c1] = name2
            self.seating_plan[r][c] = name1
            
            self.fixed_seats[r1][c1] = fixed2
            self.fixed_seats[r][c] = fixed1
            
            self.selected_seat = None
            self.draw_seating_chart()
            messagebox.showinfo("스왑 완료", f"({r1+1}, {c1+1})와 ({r+1}, {c+1}) 자리의 위치가 교환되었습니다.")
            return

        # --- 2. 이름 입력/제거 및 고정 기능 ---
        
        if current_name:
            if self.fixed_seats[r][c]:
                # 고정된 자리: 고정 해제
                self.fixed_seats[r][c] = False
                messagebox.showinfo("고정 해제", f"{current_name}님의 자리가 고정 해제되었습니다.")
            else:
                # 고정되지 않은 자리: 이름 제거 또는 고정 설정 옵션 제공
                response = messagebox.askyesnocancel("자리 관리", f"'{current_name}'님의 자리를 어떻게 하시겠습니까?\n\n[예]: 자리 고정\n[아니오]: 이름 제거 (빈자리)\n[취소]: 아무것도 안함")
                
                if response is True:
                    self.fixed_seats[r][c] = True
                    messagebox.showinfo("고정 설정", f"{current_name}님의 자리가 고정되었습니다.")
                elif response is False:
                    self.seating_plan[r][c] = ''
                    self.fixed_seats[r][c] = False
                    messagebox.showinfo("이름 제거", f"{current_name}님이 자리에서 제거되었습니다.")
        
        else: # 자리가 빈 경우
            new_name = simpledialog.askstring("이름 배치", f"({r+1}행, {c+1}열)에 배치할 이름을 입력하세요.", parent=self.master)
            if new_name:
                self.seating_plan[r][c] = new_name.strip()
                self.fixed_seats[r][c] = True 
                messagebox.showinfo("배치 완료", f"{new_name.strip()}님이 ({r+1}행, {c+1}열)에 배치 및 고정되었습니다.")
        
        self.draw_seating_chart()

    def start_swap(self, r, c):
        """위치 스왑 기능을 시작하고 첫 번째 자리를 선택합니다."""
        if not self.seating_plan[r][c]:
             messagebox.showwarning("경고", "빈 자리는 스왑할 수 없습니다. 먼저 이름을 배치하거나 랜덤 배치를 해주세요.")
             return
             
        self.selected_seat = (r, c)
        self.draw_seating_chart()
        messagebox.showinfo("스왑 시작", f"({r+1}, {c+1}) 자리를 선택했습니다. 다른 자리를 우클릭하여 스왑을 완료하세요.")


    # --- GUI 드로잉 함수 ---

    def draw_seating_chart(self):
        """책상 배치도(버튼)를 화면에 그립니다."""
        # 기존 프레임의 내용을 모두 지웁니다.
        for widget in self.seating_frame.winfo_children():
            widget.destroy()

        self.seat_buttons = []

        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                name = self.seating_plan[r][c]
                
                display_text = name if len(name) <= 8 else name[:7] + '...'
                
                # 색상 설정: 배경색을 좀 더 현대적으로 변경
                bg_color = "#e0e0e0" # 빈 자리
                if self.fixed_seats[r][c] and name:
                    bg_color = "#00BFA5" # 고정된 자리 (청록색)
                    fg_color = "white"
                elif name:
                    bg_color = "#64B5F6" # 일반 배치 자리 (하늘색)
                    fg_color = "white"
                else:
                    fg_color = "#333333"
                
                # 스왑을 위해 선택된 자리
                if self.selected_seat == (r, c):
                    bg_color = "#FFD54F" # 노란색 하이라이트
                    fg_color = "black"

                # 버튼 생성
                btn = tk.Button(self.seating_frame,
                                text=display_text,
                                width=12, height=3,
                                bg=bg_color,
                                fg=fg_color,
                                font=self.font_medium,
                                borderwidth=1,
                                relief="flat")
                                
                # 일반 클릭 (좌클릭): 이름 입력/고정/해제
                btn.bind("<Button-1>", lambda event, r=r, c=c: self.seat_click(r, c))
                
                # 스왑 시작 (우클릭): 위치 스왑의 첫 번째 자리 선택
                btn.bind("<Button-3>", lambda event, r=r, c=c: self.start_swap(r, c))

                btn.grid(row=r, column=c, padx=5, pady=5)
                row_buttons.append(btn)
            self.seat_buttons.append(row_buttons)

# 메인 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = SeatingChartApp(root)
    root.mainloop()