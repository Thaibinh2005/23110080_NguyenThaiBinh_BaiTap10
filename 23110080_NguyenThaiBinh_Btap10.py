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

        tk.Button(control_frame, text="Simulated Annealing (Cars)", 
            command=self.simulated_annealing, width=22)\
            .grid(row=0, column=2, padx=10)

        tk.Button(control_frame, text="Genetic Algorithm (Cars)", 
            command=self.genetic_algorithm, width=22)\
            .grid(row=0, column=4, padx=10)

        
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

    def simulated_annealing(self, max_iter=5000, start_temp=100.0, cooling=0.99):
        # Khởi tạo trạng thái ngẫu nhiên
        current = [random.randint(0, 7) for _ in range(8)]
        current_value = -self.heuristic(current)  

        temp = start_temp
        for step in range(max_iter):
            # Sinh neighbor ngẫu nhiên
            row = random.randint(0, 7)
            col = random.randint(0, 7)
            while col == current[row]:
                col = random.randint(0, 7)

            neighbor = current[:]
            neighbor[row] = col
            neighbor_value = -self.heuristic(neighbor)

            delta = neighbor_value - current_value
            # Nếu tốt hơn hoặc chấp nhận theo xác suất
            if delta > 0 or random.random() < pow(2.71828, delta / temp):
                current, current_value = neighbor, neighbor_value

            temp *= cooling
            if temp < 1e-3:  # nhiệt độ gần 0 thì dừng
                break

        self.drawxe(current, self.buttons_right)
        print("Simulated Annealing kết thúc:", current, "Conflicts =", self.heuristic(current))


    def genetic_algorithm(self, population_size=50, generations=200, mutation_rate=0.1):
        # Khởi tạo quần thể: mỗi cá thể là mảng 8 số (mỗi hàng chọn 1 cột)
        def random_state():
            return [random.randint(0, 7) for _ in range(8)]

        def fitness(state):
            return -self.heuristic(state)  # ít xung đột hơn thì fitness cao

        def crossover(parent1, parent2):
            point = random.randint(1, 7)
            child = parent1[:point] + parent2[point:]
            return child

        def mutate(state):
            if random.random() < mutation_rate:
                row = random.randint(0, 7)
                state[row] = random.randint(0, 7)
            return state

        population = [random_state() for _ in range(population_size)]

        for gen in range(generations):
            # Tính fitness
            scored = [(fitness(ind), ind) for ind in population]
            scored.sort(reverse=True)

            # Nếu đạt nghiệm tốt thì dừng
            best_fit, best_ind = scored[0]
            if best_fit == 0:
                break

            # Chọn lọc: lấy nửa tốt nhất
            parents = [ind for _, ind in scored[:population_size // 2]]

            # Tạo thế hệ mới
            next_gen = []
            while len(next_gen) < population_size:
                p1, p2 = random.sample(parents, 2)
                child = crossover(p1, p2)
                child = mutate(child)
                next_gen.append(child)

            population = next_gen

        self.drawxe(best_ind, self.buttons_right)
        print("Genetic Algorithm kết thúc:", best_ind, "Conflicts =", self.heuristic(best_ind))


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
