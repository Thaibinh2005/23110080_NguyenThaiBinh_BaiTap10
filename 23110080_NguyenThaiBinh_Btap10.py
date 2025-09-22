import tkinter as tk
from PIL import Image, ImageTk
import random
import heapq

class EightCarQueen:
    def __init__(self, root):
        self.root = root
        self.root.title("Cars(DFS) & Queens")
        self.root.configure(bg="lightgray")

        frame_left = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_left.grid(row=0, column=0, padx=10, pady=10)

        frame_right = tk.Frame(self.root, bg="lightgray", relief="solid", borderwidth=1)
        frame_right.grid(row=0, column=1, padx=10, pady=10)

        self.whiteX = ImageTk.PhotoImage(Image.open("whiteC.png").resize((60, 60)))
        self.blackX = ImageTk.PhotoImage(Image.open("blackC.png").resize((60, 60)))
        self.img_null = tk.PhotoImage(width=1, height=1)

        self.buttons_left = self.create_board(frame_left)
        self.buttons_right = self.create_board(frame_right)

        control_frame = tk.Frame(self.root, bg="lightgray")
        control_frame.grid(row=1, column=0, columnspan=2, pady=20)

        tk.Button(control_frame, text="Beam Search (Cars)", 
            command=lambda: self.beam_search(self.beam_var.get()), width=18)\
            .grid(row=0, column=3, padx=10)

        tk.Button(control_frame, text="Hill Climbing (Cars)", 
            command=self.hill_climbing, width=18)\
            .grid(row=0, column=1, padx=10)
        
        # Chọn beam width
        tk.Label(control_frame, text="Beam width:", bg="lightgray").grid(row=1, column=0, pady=10)
        self.beam_var = tk.IntVar(value=2)  # mặc định k=2
        tk.Spinbox(control_frame, from_=1, to=8, textvariable=self.beam_var, width=5)\
            .grid(row=1, column=1, pady=10)

    def create_board(self, frame):
        buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                color = "white" if (i + j) % 2 == 0 else "black"
                btn = tk.Button(frame, image=self.img_null,
                                width=60, height=60,
                                bg=color, relief="flat", 
                                borderwidth=0)
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            buttons.append(row)
        return buttons  
         
    def drawxe(self, solution, board):
        for i in range(8):
            for j in range(8):
                board[i][j].configure(image=self.img_null)
        for r, c in enumerate(solution):
            color = "white" if (r + c) % 2 == 0 else "black"
            img = self.whiteX if color == "black" else self.blackX
            board[r][c].configure(image=img)
    def heuristic(self, state):
        attacks = 0
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                if state[i] == state[j]:  # cùng cột
                    attacks += 1
        return attacks
    
    def hill_climbing(self):
        # sinh trạng thái ngẫu nhiên: mỗi hàng random một cột
        current = [random.randint(0, 7) for _ in range(8)]
        current_value = -self.heuristic(current)   # ít xung đột hơn thì giá trị lớn hơn

        while True:
            neighbors = []
            # tạo tất cả trạng thái neighbor bằng cách đổi cột ở từng hàng
            for row in range(8):
                for col in range(8):
                    if col != current[row]:
                        new_state = current[:]
                        new_state[row] = col
                        neighbors.append(new_state)

            if not neighbors:
                break

            # chọn neighbor tốt nhất (ít xung đột nhất)
            neighbor = max(neighbors, key=lambda s: -self.heuristic(s))
            neighbor_value = -self.heuristic(neighbor)

            if neighbor_value <= current_value:  # không cải thiện nữa thì dừng
                break
            current, current_value = neighbor, neighbor_value

        self.drawxe(current, self.buttons_right)
        print("Hill Climbing (Cars) kết thúc:", current, "Conflicts =", self.heuristic(current))


    def beam_search(self, k=2, delay=800, start_state=None):
        self.k = k
        self.delay = delay

        # Nếu không truyền vào start_state thì random vị trí ban đầu
        if start_state is None:
            first_col = random.randint(0, 7)
            start_state = [first_col]

        h = self.heuristic(start_state)
        self.beam = [(h, start_state)]
        self.current_row = len(start_state)

        #trạng thái khởi tạo
        self.drawxe(start_state, self.buttons_right)
        print("Trạng thái ban đầu:", start_state, "Heuristic =", h)

        def step():
            if self.current_row >= 8:  # kết thúc
                best_cost, best_state = min(self.beam, key=lambda x: x[0])  
                self.drawxe(best_state, self.buttons_right)
                print("Kết thúc Beam Search:", best_state, "Heuristic =", best_cost)
                return

            candidate = []
            for cost, state in self.beam:
                for col in range(8):
                    if col not in state:
                        new_state = state + [col]
                        h = self.heuristic(new_state)
                        candidate.append((h, new_state))

            # chọn k trạng thái tốt nhất
            self.beam = heapq.nsmallest(self.k, candidate, key=lambda x: x[0])

            # vẽ trạng thái đầu tiên trong beam
            if self.beam:
                self.drawxe(self.beam[0][1], self.buttons_right)
                print(f"Hàng {self.current_row+1}: giữ {len(self.beam)} trạng thái, tốt nhất = {self.beam[0]}")

            self.current_row += 1
            self.root.after(self.delay, step)

        step()

class Node:
    def __init__(self, state, f_cost, g_cost=0, h_cost=0):
        self.state = state      # state = [cột đặt xe mỗi hàng]
        self.f_cost = f_cost    # f(n) = g(n) + h(n) - Total cost
        self.g_cost = g_cost    # g(n) = Actual cost from start
        self.h_cost = h_cost    # h(n) = Heuristic cost to goal

    def __lt__(self, other):  # so sánh cho heapq
        return self.f_cost < other.f_cost
    
if __name__ == "__main__":
    root = tk.Tk()
    app = EightCarQueen(root)
    root.mainloop()
