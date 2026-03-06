import tkinter as tk
import random
import time

word_banks = {
    "Normal": ["animals", "fruits", "countries"],
    "Hard": ["chemistry", "history", "geography"],
    "Nightmare": [
        "practice makes perfect",
        "pseudopseudohypoparathyroidism",
        "floccinaucinihiliparathyroidism",
    ],
}

word_list = word_banks["Normal"]
current_word = ""
time_left = 10
score = 0
game_running = False
current_round = 0
total_rounds = 5
start_time = None


def start_game():
    global time_left, score, game_running, current_round, total_rounds, start_time
    try:
        total_rounds = int(entry_rounds.get())
    except:
        total_rounds = 5
        entry_rounds.delete(0, tk.END)
        entry_rounds.insert(0, "5")

    score = 0
    current_round = 0
    game_running = True
    time_left = 10
    entry_input.config(state="normal")
    lbl_score.config(text=f"Score: {score}")
    lbl_wpm.config(text="WPM: 0")
    next_round()
    countdown()


def next_round():
    global current_round, total_rounds, time_left, start_time
    if current_round < total_rounds:
        current_round += 1
        lbl_round.config(text=f"Round: {current_round}/{total_rounds}")
        time_left = 10
        start_time = time.time()
        show_word()
    else:
        end_game()


def countdown():
    global time_left, game_running
    if game_running:
        lbl_timer.config(text=f"Time: {time_left}s")
        if time_left <= 3:
            lbl_timer.config(fg="red")
        else:
            lbl_timer.config(fg="black")
        if time_left > 0:
            time_left -= 1
            root.after(1000, countdown)
        else:
            end_game()


def end_game():
    global game_running
    game_running = False
    lbl_timer.config(text="Time's up!")
    entry_input.config(state="disabled")
    lbl_word.config(text="Game Over!")
    lbl_score.config(text=f"Final Score: {score}")
    lbl_wpm.config(text="WPM: 0")


def set_difficulty(level):
    global word_list
    word_list = word_banks[level]
    if not game_running:
        show_word()


def show_word():
    global current_word
    current_word = random.choice(word_list)
    lbl_word_display(current_word)
    entry_input.delete(0, tk.END)


def lbl_word_display(word, typed=""):
    lbl_word.config(text="")
    for i, char in enumerate(word):
        if i < len(typed):
            if typed[i] == char:
                lbl_word.config(text=lbl_word.cget("text") + char, fg="green")
            else:
                lbl_word.config(text=lbl_word.cget("text") + char, fg="red")
        else:
            lbl_word.config(text=lbl_word.cget("text") + char, fg="gray")


def check_input(event=None):
    global score
    if not game_running:
        return

    typed = entry_input.get()
    update_colored_text(typed)
    update_wpm(typed)

    if typed.strip() == current_word:
        score += 1
        animate_score()
        lbl_score.config(text=f"Score: {score}")
        next_round()


def update_colored_text(typed):
    display = ""
    for i, c in enumerate(current_word):
        if i < len(typed):
            if typed[i] == c:
                display += c
            else:
                display += c
        else:
            display += c
    colored_text = ""
    for i, char in enumerate(current_word):
        if i < len(typed):
            if typed[i] == char:
                colored_text += char
            else:
                colored_text += char
        else:
            colored_text += char
    lbl_word.config(text="")
    for i, char in enumerate(current_word):
        if i < len(typed):
            if typed[i] == char:
                lbl_word.config(text=lbl_word.cget("text") + char)
            else:
                lbl_word.config(text=lbl_word.cget("text") + char)
        else:
            lbl_word.config(text=lbl_word.cget("text") + char)


def update_wpm(typed):
    if start_time:
        elapsed_min = max((time.time() - start_time) / 60, 0.01)
        wpm = (len(typed) / 5) / elapsed_min
        lbl_wpm.config(text=f"WPM: {int(wpm)}")


def animate_score():
    lbl_score.config(fg="green")
    root.after(300, lambda: lbl_score.config(fg="black"))


root = tk.Tk()
root.title("SPEED TYPING CHALLENGE")
root.geometry("800x600")
tk.Label(root, text="Speed Typing Challenge", font=("Arial", 24, "bold")).pack(pady=20)
frame_round = tk.Frame(root)
frame_round.pack(pady=10)
tk.Label(frame_round, text="Rounds:", font=("Arial", 16)).pack(side="left", padx=5)
entry_rounds = tk.Entry(frame_round, width=6, font=("Arial", 16))
entry_rounds.insert(0, "5")
entry_rounds.pack(side="left")
frame_diff = tk.Frame(root)
frame_diff.pack(pady=10)
tk.Button(
    frame_diff, text="Normal", width=10, command=lambda: set_difficulty("Normal")
).pack(side="left", padx=5)
tk.Button(
    frame_diff, text="Hard", width=10, command=lambda: set_difficulty("Hard")
).pack(side="left", padx=5)
tk.Button(
    frame_diff, text="Nightmare", width=10, command=lambda: set_difficulty("Nightmare")
).pack(side="left", padx=5)
lbl_word = tk.Label(root, text="", font=("Consolas", 32, "bold"))
lbl_word.pack(pady=20)
lbl_timer = tk.Label(root, text=f"Time: {time_left}s", font=("Arial", 20))
lbl_timer.pack(pady=10)
lbl_score = tk.Label(root, text=f"Score: {score}", font=("Arial", 16))
lbl_score.pack(pady=5)
lbl_wpm = tk.Label(root, text="WPM: 0", font=("Arial", 16))
lbl_wpm.pack(pady=5)
lbl_round = tk.Label(root, text=f"Round:0/{total_rounds}", font=("Arial", 16))
lbl_round.pack(pady=5)
btn_start = tk.Button(
    root, text="Start Game", font=("Arial", 16, "bold"), width=12, command=start_game
)
btn_start.pack(pady=10)
entry_input = tk.Entry(root, font=("Arial", 16))
entry_input.pack(pady=20)
entry_input.bind("<KeyRelease>", check_input)

root.mainloop()
