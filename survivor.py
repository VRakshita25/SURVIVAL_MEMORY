import tkinter as tk
from tkinter import messagebox, ttk
import random


# =========================
# GAME DATA
# =========================

ROUNDS = [
    {
        "objects": [
            "🔑 Key",
            "🧯 Fire Extinguisher",
            "🪢 Rope",
            "🔦 Flashlight",
            "🔨 Hammer"
        ],
        "question": (
            "🔥 Fire starts spreading across the room.\n"
            "The door is locked.\n"
            "What will you use to escape?"
        ),
        "correct_answers": [
            "fire extinguisher",
            "key"
        ]
    },

    {
        "objects": [
            "🔋 Battery",
            "🪛 Screwdriver",
            "📻 Radio",
            "🔦 Flashlight",
            "🪜 Ladder"
        ],
        "question": (
            "🌑 The power suddenly goes out underground.\n"
            "You hear strange sounds nearby.\n"
            "What will you use first?"
        ),
        "correct_answers": [
            "flashlight"
        ]
    },

    {
        "objects": [
            "🪢 Rope",
            "🍫 Chocolate",
            "🪝 Hook",
            "🗺️ Map",
            "🧲 Magnet"
        ],
        "question": (
            "🌉 A bridge collapses leaving a huge gap.\n"
            "How will you cross safely?"
        ),
        "correct_answers": [
            "rope",
            "hook"
        ]
    },

    {
        "objects": [
            "🔨 Hammer",
            "📦 Box",
            "🔑 Key",
            "🪓 Axe",
            "📱 Phone"
        ],
        "question": (
            "🚪 Wooden planks block the emergency exit.\n"
            "What will you use?"
        ),
        "correct_answers": [
            "axe",
            "hammer"
        ]
    }
]


# =========================
# SETTINGS
# =========================

DISPLAY_TIME = 8
TOTAL_LIVES = 3


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Memory Survival Game")
root.geometry("800x600")
root.configure(bg="#111111")
root.resizable(False, False)


# =========================
# VARIABLES
# =========================

round_index = 0
score = 0
lives = TOTAL_LIVES
countdown = DISPLAY_TIME
timer_running = False


# =========================
# UI ELEMENTS
# =========================

heading = tk.Label(
    root,
    text="🧠 MEMORY SURVIVAL GAME",
    font=("Arial", 26, "bold"),
    fg="#00ffcc",
    bg="#111111"
)
heading.pack(pady=15)


round_label = tk.Label(
    root,
    text="Round 1/4",
    font=("Arial", 15, "bold"),
    fg="orange",
    bg="#111111"
)
round_label.pack()


timer_label = tk.Label(
    root,
    text="",
    font=("Arial", 20, "bold"),
    fg="yellow",
    bg="#111111"
)
timer_label.pack(pady=10)


progress = ttk.Progressbar(
    root,
    length=400,
    maximum=DISPLAY_TIME
)
progress.pack(pady=5)


content_label = tk.Label(
    root,
    text="",
    font=("Arial", 18),
    fg="white",
    bg="#111111",
    justify="center",
    wraplength=700
)
content_label.pack(pady=40)


answer_entry = tk.Entry(
    root,
    font=("Arial", 18),
    width=30,
    justify="center",
    bg="#222222",
    fg="white",
    insertbackground="white"
)


submit_button = tk.Button(
    root,
    text="Submit Answer",
    font=("Arial", 15, "bold"),
    bg="#00aa00",
    fg="white",
    width=18,
    activebackground="#00ff00",
    command=lambda: check_answer()
)


restart_button = tk.Button(
    root,
    text="🔄 Play Again",
    font=("Arial", 15, "bold"),
    bg="#4444ff",
    fg="white",
    width=18,
    command=lambda: restart_game()
)


bottom_frame = tk.Frame(root, bg="#111111")
bottom_frame.pack(side="bottom", pady=20)


score_label = tk.Label(
    bottom_frame,
    text="Score: 0",
    font=("Arial", 16, "bold"),
    fg="lightgreen",
    bg="#111111"
)
score_label.grid(row=0, column=0, padx=20)


lives_label = tk.Label(
    bottom_frame,
    text=f"Lives: {TOTAL_LIVES}",
    font=("Arial", 16, "bold"),
    fg="red",
    bg="#111111"
)
lives_label.grid(row=0, column=1, padx=20)


# =========================
# FUNCTIONS
# =========================

def show_objects():
    global countdown
    global timer_running

    timer_running = True

    answer_entry.pack_forget()
    submit_button.pack_forget()

    round_data = ROUNDS[round_index]

    round_label.config(
        text=f"Round {round_index + 1}/{len(ROUNDS)}"
    )

    objects = round_data["objects"][:]
    random.shuffle(objects)

    objects_text = "\n".join(objects)

    content_label.config(
        text=f"🧠 MEMORIZE THESE OBJECTS\n\n{objects_text}"
    )

    countdown = DISPLAY_TIME
    progress["value"] = DISPLAY_TIME

    update_timer()


def update_timer():
    global countdown
    global timer_running

    if not timer_running:
        return

    timer_label.config(
        text=f"⏳ Time Left: {countdown} sec"
    )

    progress["value"] = countdown

    if countdown <= 3:
        timer_label.config(fg="red")
        root.bell()
    else:
        timer_label.config(fg="yellow")

    if countdown > 0:
        countdown -= 1
        root.after(1000, update_timer)
    else:
        timer_running = False
        show_question()


def show_question():
    timer_label.config(text="")
    progress["value"] = 0

    round_data = ROUNDS[round_index]

    content_label.config(
        text=round_data["question"]
    )

    answer_entry.delete(0, tk.END)

    answer_entry.pack(pady=15)
    submit_button.pack(pady=10)

    answer_entry.focus()


def check_answer():
    global score
    global round_index
    global lives

    user_answer = answer_entry.get().lower().strip()

    correct_answers = ROUNDS[round_index]["correct_answers"]

    is_correct = any(
        ans in user_answer
        for ans in correct_answers
    )

    if is_correct:
        score += 1

        messagebox.showinfo(
            "Correct",
            "✅ Correct Answer!"
        )

    else:
        lives -= 1

        messagebox.showerror(
            "Wrong",
            "❌ Wrong Answer!"
        )

        lives_label.config(
            text=f"Lives: {lives}"
        )

        if lives <= 0:
            end_game()
            return

    score_label.config(
        text=f"Score: {score}"
    )

    round_index += 1

    if round_index < len(ROUNDS):
        show_objects()
    else:
        end_game()


def end_game():
    answer_entry.pack_forget()
    submit_button.pack_forget()

    timer_label.config(text="")
    progress["value"] = 0

    if score == len(ROUNDS):
        ending = "🏆 PERFECT MEMORY MASTER 🏆"
    elif score >= 2:
        ending = "🎯 GOOD SURVIVOR 🎯"
    else:
        ending = "💀 BETTER LUCK NEXT TIME 💀"

    content_label.config(
        text=(
            f"{ending}\n\n"
            f"Final Score: {score}/{len(ROUNDS)}\n"
            f"Lives Left: {lives}"
        )
    )

    restart_button.pack(pady=20)


def restart_game():
    global score
    global round_index
    global lives
    global countdown

    score = 0
    round_index = 0
    lives = TOTAL_LIVES
    countdown = DISPLAY_TIME

    score_label.config(text="Score: 0")
    lives_label.config(text=f"Lives: {TOTAL_LIVES}")

    restart_button.pack_forget()

    show_objects()


# =========================
# KEYBOARD SUPPORT
# =========================

root.bind("<Return>", lambda event: check_answer())


# =========================
# START GAME
# =========================

show_objects()

root.mainloop()

