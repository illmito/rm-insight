import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from tkinter.ttk import Progressbar, Button, Label, Style

import numpy as np
import pandas as pd


class PrioritySummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RM Insight")
        self.root.minsize(600, 400)

        style = Style()
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))

        self.file_path = None
        self.summary_df = None
        self.agent_frame = None
        self.controls_frame = None
        self.filename_label = None

        self.init_ui()

    def build_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Help", command=self.show_help)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def init_ui(self):
        self.build_menu()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        Button(
            self.root,
            text="Upload CSV",
            command=self.upload_file
        ).grid(row=0, column=0, pady=(20, 5), padx=20, sticky="ew")

        Button(
            self.root,
            text="Process",
            command=self.process_data
        ).grid(row=1, column=0, pady=5, padx=20, sticky="ew")

        self.progress = Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate"
        )
        self.progress.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

        self.status_label = Label(
            self.root,
            text="Select CSV file",
            anchor="center"
        )
        self.status_label.grid(row=3, column=0, pady=(0, 5))

    def upload_file(self):
        filetypes = [("CSV files", "*.csv")]
        path = filedialog.askopenfilename(title="Open file", filetypes=filetypes)

        if path:
            self.file_path = path
            base_name = os.path.basename(path)
            self.status_label.config(text=f"Loaded: {base_name}")

    def process_data(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please upload a CSV file first.")
            return

        self.progress["value"] = 10
        self.root.update()

        try:
            df = pd.read_csv(self.file_path)

            for col in ["Users", "Subject", "Total Handle"]:
                if col not in df.columns:
                    raise ValueError(f"Missing expected column: {col}")

            df["Total Handle"] = pd.to_numeric(df["Total Handle"], errors="coerce")

            def clean_users(user_entry):
                if pd.isna(user_entry):
                    return user_entry

                parts = [
                    part.strip()
                    for part in re.split(r"[;,]", str(user_entry))
                    if part.strip()
                ]

                return parts[-1] if parts else user_entry

            df["Users"] = df["Users"].apply(clean_users)

            def extract_priority(subject):
                if pd.isna(subject):
                    return "Nil"

                patterns = {
                    r"\bP1\b": "P1",
                    r"\bP2\b": "P2",
                    r"\bP3\.5\b": "P3.5",
                    r"\bP3\b": "P3",
                    r"\bP4\b": "P4",
                    r"P5 \(within 7 days\)": "P5 7D",
                    r"\bP5\b": "P5",
                }

                for pattern, label in patterns.items():
                    if re.search(pattern, subject):
                        return label

                return "Nil"

            df["Priority"] = df["Subject"].apply(extract_priority)

            self.progress["value"] = 40
            self.root.update()

            priorities = ["P1", "P2", "P3", "P3.5", "P4", "P5", "P5 7D"]
            summary = {}

            for user in df["Users"].dropna().unique():
                user_data = df[df["Users"] == user]
                user_summary = {}
                total_jobs = 0
                total_handle = []

                for p in priorities:
                    p_data = user_data[user_data["Priority"] == p]

                    count = len(p_data)
                    aht = p_data["Total Handle"].mean() if count > 0 else 0

                    total_jobs += count
                    total_handle.extend(p_data["Total Handle"].dropna().tolist())

                    user_summary[p] = count
                    user_summary[f"{p} AHT"] = (
                        pd.to_timedelta(aht, unit="s") if aht else pd.NaT
                    )

                user_summary["P Total"] = total_jobs

                avg_total_handle = np.mean(total_handle) if total_handle else 0
                user_summary["Average Total Handle"] = (
                    pd.to_timedelta(avg_total_handle, unit="s")
                    if avg_total_handle
                    else pd.NaT
                )

                summary[user] = user_summary

            summary_df = pd.DataFrame.from_dict(summary, orient="index")
            summary_df.reset_index(inplace=True)
            summary_df.rename(columns={"index": "RM AGENT"}, inplace=True)

            time_columns = [
                col
                for col in summary_df.columns
                if "AHT" in col or "Average Total Handle" in col
            ]

            for col in time_columns:
                summary_df[col] = summary_df[col].apply(self.format_timedelta)

            ordered_columns = [
                "RM AGENT",
                "P1",
                "P2",
                "P3",
                "P3.5",
                "P4",
                "P5",
                "P5 7D",
                "P Total",
                "P1 AHT",
                "P2 AHT",
                "P3 AHT",
                "P3.5 AHT",
                "P4 AHT",
                "P5 AHT",
                "P5 7D AHT",
                "Average Total Handle",
            ]

            self.summary_df = summary_df[ordered_columns]

            self.progress["value"] = 100
            self.root.update()

            self.display_agent_selection()

        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def display_agent_selection(self):
        if self.agent_frame:
            self.agent_frame.destroy()

        if self.controls_frame:
            self.controls_frame.destroy()

        if self.filename_label:
            self.filename_label.destroy()

        self.agent_list = sorted(
            agent
            for agent in self.summary_df["RM AGENT"].unique()
            if agent != "TOTAL / TOTAL AVG"
        )

        self.filename_label = Label(
            self.root,
            text="Select Relevant Users/Agents:",
            font=("Segoe UI", 10, "italic")
        )
        self.filename_label.grid(row=4, column=0, sticky="sw", padx=20)

        self.agent_frame = tk.Frame(self.root)
        self.agent_frame.grid(row=5, column=0, sticky="nsew", padx=20, pady=10)

        self.root.grid_rowconfigure(5, weight=1)

        self.listbox = tk.Listbox(
            self.agent_frame,
            selectmode="multiple",
            exportselection=False,
            font=("Segoe UI", 10)
        )
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(
            self.agent_frame,
            orient="vertical",
            command=self.listbox.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)

        for agent in self.agent_list:
            self.listbox.insert("end", agent)

        def toggle_selection(event):
            index = self.listbox.nearest(event.y)

            if index >= 0:
                if index in self.listbox.curselection():
                    self.listbox.selection_clear(index)
                else:
                    self.listbox.selection_set(index)

            self.update_save_button()
            return "break"

        self.listbox.bind("<Button-1>", toggle_selection)

        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.grid(row=6, column=0, pady=(0, 15), sticky="ew")

        Button(
            self.controls_frame,
            text="Select All",
            command=self.select_all
        ).pack(side="left", padx=10)

        Button(
            self.controls_frame,
            text="Deselect All",
            command=self.deselect_all
        ).pack(side="left", padx=10)

        self.save_btn = Button(
            self.controls_frame,
            text="Save",
            command=self.on_save,
            state="disabled"
        )
        self.save_btn.pack(side="right", padx=10)

    def update_save_button(self):
        if len(self.listbox.curselection()) > 0:
            self.save_btn["state"] = "normal"
        else:
            self.save_btn["state"] = "disabled"

    def select_all(self):
        self.listbox.select_set(0, "end")
        self.update_save_button()

    def deselect_all(self):
        self.listbox.selection_clear(0, "end")
        self.update_save_button()

    def on_save(self):
        selected_indices = self.listbox.curselection()
        selected_agents = [self.listbox.get(i) for i in selected_indices]

        filtered_df = self.summary_df[
            self.summary_df["RM AGENT"].isin(selected_agents)
        ]

        summary_row = {"RM AGENT": "TOTAL / TOTAL AVG"}

        for p in ["P1", "P2", "P3", "P3.5", "P4", "P5", "P5 7D", "P Total"]:
            summary_row[p] = filtered_df[p].astype(int).sum()

        for col in [
            "P1 AHT",
            "P2 AHT",
            "P3 AHT",
            "P3.5 AHT",
            "P4 AHT",
            "P5 AHT",
            "P5 7D AHT",
            "Average Total Handle",
        ]:
            times = pd.to_timedelta(filtered_df[col], errors="coerce")
            avg = times.mean()
            summary_row[col] = self.format_timedelta(avg)

        final_df = pd.concat(
            [filtered_df, pd.DataFrame([summary_row])],
            ignore_index=True
        )

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if filepath:
            final_df.to_excel(filepath, index=False)
            messagebox.showinfo("Saved", f"File saved to: {filepath}")

    def format_timedelta(self, td):
        if pd.isna(td) or td == pd.NaT:
            return "0:00:00"

        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours}:{minutes:02}:{seconds:02}"

    def show_help(self):
        help_win = tk.Toplevel(self.root)
        help_win.title("Help & Data Requirements")
        help_win.geometry("600x480")
        help_win.configure(bg="#f4f4f4")

        title = tk.Label(
            help_win,
            text="🛠️ Help & Data Requirements",
            font=("Segoe UI", 14, "bold"),
            bg="#f4f4f4",
            fg="#333"
        )
        title.pack(pady=(15, 5))

        frame = tk.Frame(help_win, bg="#f4f4f4")
        frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            wrap="word",
            font=("Segoe UI", 10),
            bg="white",
            fg="#333",
            borderwidth=1,
            relief="solid",
            yscrollcommand=scrollbar.set
        )
        text.pack(fill="both", expand=True)

        scrollbar.config(command=text.yview)

        text.tag_configure("heading", font=("Segoe UI", 10, "bold"), spacing3=4)
        text.tag_configure(
            "section",
            font=("Segoe UI", 10),
            lmargin1=10,
            lmargin2=10,
            spacing1=4,
            spacing3=6
        )
        text.tag_configure(
            "footer",
            font=("Segoe UI", 9, "italic"),
            foreground="#555",
            justify="center",
            spacing1=10
        )

        text.insert("end", "📌 Purpose:\n", "heading")
        text.insert(
            "end",
            "This tool processes RM Agent CSV data to produce a structured "
            "summary of task volumes and average handle times by priority.\n\n",
            "section"
        )

        text.insert("end", "📄 Required Columns in the CSV:\n", "heading")
        text.insert(
            "end",
            "- Users: RM Agent names (last name retained if multiple listed).\n",
            "section"
        )
        text.insert(
            "end",
            "- Subject: Used to detect the priority, e.g. P3 - Light Issue.\n",
            "section"
        )
        text.insert(
            "end",
            "- Total Handle: Numeric value in seconds.\n\n",
            "section"
        )

        text.insert("end", "🔍 Recognized Priorities:\n", "heading")
        text.insert(
            "end",
            "- P1, P2, P3, P3.5, P4, P5, P5 (within 7 days) → renamed to P5 7D\n",
            "section"
        )
        text.insert("end", "- If none found, marked as Nil\n\n", "section")

        text.insert("end", "📈 Summary Output:\n", "heading")
        text.insert("end", "- Count per priority\n", "section")
        text.insert("end", "- AHT per priority\n", "section")
        text.insert("end", "- Total jobs and overall AHT\n", "section")
        text.insert("end", "- Final row = TOTAL / TOTAL AVG\n\n", "section")

        text.insert("end", "⚠️ Common Issues:\n", "heading")
        text.insert("end", "- Column names must match exactly\n", "section")
        text.insert("end", "- Total Handle must be numeric\n", "section")
        text.insert("end", "- File must be saved as .csv\n\n", "section")

        text.insert("end", "👤 Created by Thomas Brayovic © 2025", "footer")
        text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = PrioritySummaryApp(root)
    root.mainloop()
