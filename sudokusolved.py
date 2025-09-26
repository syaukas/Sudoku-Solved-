import tkinter as tk
from tkinter import messagebox
import random, time, copy

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")

        # Colors
        self.bg_color = "#f0f0f0"
        self.grid_color = "#cccccc"
        self.given_color = "#e0e0e0"
        self.user_color = "#ffffff"
        self.selected_color = "#c0ddff"

        # Fonts
        self.font = ("Arial", 16, "bold")

        # Variables
        self.grid = [[0]*9 for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.labels = [[None]*9 for _ in range(9)]
        self.given = [[False]*9 for _ in range(9)]
        self.selected_cell = (0, 0)
        self.difficulty = "Easy"

        # Timer
        self.start_time = None
        self.elapsed_time = 0
        self.timer_running = False

        # UI
        self.setup_ui()
        self.root.bind("<Key>", self.on_key_press)
        self.restart_game()

    # ============= UI SETUP ============= #
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(padx=20, pady=20)

        title_label = tk.Label(main_frame, text="SUDOKU", font=("Arial", 24, "bold"),
                               bg=self.bg_color, fg="#333")
        title_label.pack(pady=(0, 10))

        instr_label = tk.Label(main_frame, text="Arrow keys: move • 1–9: input • 0/Space: clear",
                               font=("Arial", 10), bg=self.bg_color, fg="#666")
        instr_label.pack(pady=(0, 10))

        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(pady=(0, 20))

        self.timer_label = tk.Label(info_frame, text="Time: 00:00", font=("Arial", 14, "bold"),
                                    bg=self.bg_color, fg="#333")
        self.timer_label.pack(side=tk.LEFT, padx=20)

        self.status_label = tk.Label(info_frame, text="Playing", font=("Arial", 14, "bold"),
                                     bg=self.bg_color, fg="#070")
        self.status_label.pack(side=tk.LEFT)

        # Sudoku Grid
        grid_frame = tk.Frame(main_frame, bg=self.grid_color, bd=3, relief="raised")
        grid_frame.pack(pady=(0, 20))

        for i in range(9):
            for j in range(9):
                frame = tk.Frame(grid_frame, bg=self.grid_color)
                border_left = 3 if j % 3 == 0 and j > 0 else 1
                border_top = 3 if i % 3 == 0 and i > 0 else 1
                frame.grid(row=i, column=j, padx=(border_left, 0), pady=(border_top, 0))
                lbl = tk.Label(frame, text="", width=3, height=2, font=self.font,
                               bg=self.user_color, relief="solid", bd=1)
                lbl.pack()
                lbl.bind("<Button-1>", lambda e, r=i, c=j: self.select_cell(r, c))
                self.labels[i][j] = lbl

        # Buttons
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(pady=15)

        row1 = tk.Frame(buttons_frame, bg=self.bg_color); row1.pack(pady=5)
        tk.Button(row1, text="New Game", command=self.restart_game, width=12, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Check", command=self.check_solution, width=12, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Help", command=self.show_help, width=12, bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(buttons_frame, bg=self.bg_color); row2.pack(pady=5)
        tk.Button(row2, text="Solve", command=self.solve_puzzle, width=12, bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Clear All", command=self.clear_user_entries, width=12, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Hint", command=self.give_hint, width=12, bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)

        row3 = tk.Frame(buttons_frame, bg=self.bg_color); row3.pack(pady=5)
        tk.Button(row3, text="Pause/Resume", command=self.toggle_pause, width=12, bg="#795548", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="About", command=self.show_about, width=12, bg="#009688", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="Exit", command=self.root.quit, width=12, bg="#000", fg="white").pack(side=tk.LEFT, padx=5)

        diff_frame = tk.Frame(main_frame, bg=self.bg_color)
        diff_frame.pack(pady=(20, 0))
        tk.Label(diff_frame, text="Difficulty:", font=("Arial", 12, "bold"),
                 bg=self.bg_color).pack(side=tk.LEFT, padx=10)
        for level in ["Easy", "Medium", "Hard"]:
            tk.Button(diff_frame, text=level, command=lambda l=level: self.set_difficulty(l),
                     width=10, bg="#607D8B" if level != self.difficulty else "#FF5722", fg="white").pack(side=tk.LEFT, padx=5)

    # ============= Game Logic ============= #
    def generate_full_grid(self):
        grid = [[0]*9 for _ in range(9)]
        def is_valid(r,c,n):
            if n in grid[r]: return False
            if n in [grid[i][c] for i in range(9)]: return False
            sr, sc = (r//3)*3, (c//3)*3
            for i in range(sr,sr+3):
                for j in range(sc,sc+3):
                    if grid[i][j]==n: return False
            return True
        def solve(pos=0):
            if pos==81: return True
            r,c = divmod(pos,9)
            nums = list(range(1,10)); random.shuffle(nums)
            for n in nums:
                if is_valid(r,c,n):
                    grid[r][c]=n
                    if solve(pos+1): return True
                    grid[r][c]=0
            return False
        solve()
        return grid

    def make_puzzle(self, full):
        puzzle = copy.deepcopy(full)
        if self.difficulty=="Easy": remove=35
        elif self.difficulty=="Medium": remove=45
        else: remove=55
        cells = [(i,j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for k in range(remove):
            r,c = cells[k]
            puzzle[r][c]=0
        return puzzle

    def restart_game(self):
        self.stop_timer()
        self.start_time = time.time()
        self.elapsed_time = 0
        self.start_timer()
        self.status_label.config(text="Playing", fg="#070")

        full = self.generate_full_grid()
        self.solution = full
        puzzle = self.make_puzzle(full)
        self.grid = puzzle
        self.given = [[puzzle[i][j]!=0 for j in range(9)] for i in range(9)]
        self.update_grid()
        self.select_cell(0,0)

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                val=self.grid[i][j]
                lbl=self.labels[i][j]
                if val!=0:
                    lbl.config(text=str(val), fg="black",
                               bg=self.given_color if self.given[i][j] else self.user_color)
                else:
                    lbl.config(text="", bg=self.user_color)
        self.highlight_selected()

    def select_cell(self,r,c):
        self.selected_cell=(r,c)
        self.highlight_selected()

    def highlight_selected(self):
        for i in range(9):
            for j in range(9):
                if (i,j)==self.selected_cell:
                    self.labels[i][j].config(bg=self.selected_color if not self.given[i][j] else self.given_color)
                elif not self.given[i][j]:
                    self.labels[i][j].config(bg=self.user_color)
                else:
                    self.labels[i][j].config(bg=self.given_color)

    def on_key_press(self,e):
        r,c=self.selected_cell
        if e.keysym in ["Up","Down","Left","Right"]:
            if e.keysym=="Up": r=(r-1)%9
            elif e.keysym=="Down": r=(r+1)%9
            elif e.keysym=="Left": c=(c-1)%9
            elif e.keysym=="Right": c=(c+1)%9
            self.select_cell(r,c)
        elif e.char in "123456789" and not self.given[r][c]:
            self.grid[r][c]=int(e.char)
            self.update_grid()
        elif e.keysym in ["space","0"] and not self.given[r][c]:
            self.grid[r][c]=0
            self.update_grid()

    def check_solution(self):
        if self.grid==self.solution:
            self.status_label.config(text="Solved!", fg="#070")
            messagebox.showinfo("Sudoku","Congratulations! You solved it!")
            self.stop_timer()
        else:
            messagebox.showwarning("Sudoku","Not solved correctly yet!")

    def show_help(self):
        messagebox.showinfo("Help","Fill the grid so that each row, column and 3x3 box contains 1-9 without repetition.")

    def solve_puzzle(self):
        self.grid=copy.deepcopy(self.solution)
        self.update_grid()
        self.status_label.config(text="Solved!", fg="#070")
        self.stop_timer()

    def clear_user_entries(self):
        for i in range(9):
            for j in range(9):
                if not self.given[i][j]:
                    self.grid[i][j]=0
        self.update_grid()

    def give_hint(self):
        empty=[(i,j) for i in range(9) for j in range(9) if self.grid[i][j]==0]
        if not empty:
            messagebox.showinfo("Hint","No empty cells left!")
            return
        r,c=random.choice(empty)
        self.grid[r][c]=self.solution[r][c]
        self.update_grid()

    def toggle_pause(self):
        if self.timer_running:
            self.stop_timer()
            self.status_label.config(text="PAUSED", fg="#a00")
        else:
            self.start_time=time.time()-self.elapsed_time
            self.start_timer()
            self.status_label.config(text="Playing", fg="#070")

    def show_about(self):
        messagebox.showinfo("About","Sudoku Game\nCreated with Python & Tkinter.")

    def set_difficulty(self,level):
        self.difficulty=level
        self.restart_game()

    # ============= Timer ============= #
    def start_timer(self):
        self.timer_running=True
        self.update_timer()

    def stop_timer(self):
        self.timer_running=False

    def update_timer(self):
        if self.timer_running:
            self.elapsed_time=int(time.time()-self.start_time)
            m,s=divmod(self.elapsed_time,60)
            self.timer_label.config(text=f"Time: {m:02d}:{s:02d}")
            self.root.after(1000,self.update_timer)

    def run(self):
        self.root.mainloop()

if __name__=="__main__":
    root=tk.Tk()
    game=SudokuGame(root)
    game.run()
