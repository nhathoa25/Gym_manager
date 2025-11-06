import tkinter as tk
from tkinter import messagebox
import json
import os
from models.member import Member
from datetime import datetime


def _load_plans():
    path = "data/subscription_info.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def show_renew_subscription_window(username, window=None):
    plans = _load_plans()
    root = window if window is not None else tk.Toplevel()
    root.title("Renew / Subscribe")
    root.geometry("800x520")

    # Header
    header = tk.Frame(root, bg="#2C3E50")
    header.pack(fill="x")
    tk.Label(header, text="Renew or Subscribe to a New Plan", bg="#2C3E50", fg="white", font=("Helvetica", 18, "bold"), pady=12).pack()

    content = tk.Frame(root, padx=20, pady=12)
    content.pack(fill="both", expand=True)

    left = tk.Frame(content)
    left.pack(side="left", fill="y", padx=(0, 10))

    center = tk.Frame(content)
    center.pack(side="left", fill="both", expand=True, padx=10)

    right = tk.Frame(content)
    right.pack(side="right", fill="y", padx=(10, 0))

    # Current subscription info
    def _get_member_info():
        path = "data/member_info.json"
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            members = json.load(f)
        for m in members:
            if m.get("username") == username:
                return m
        return None

    member_info = _get_member_info()
    tk.Label(left, text="Your Current Plan", font=("Helvetica", 14, "bold")).pack(anchor="w")
    if member_info:
        tk.Label(left, text=f"Plan: {member_info.get('membership')}", font=("Helvetica", 12)).pack(anchor="w", pady=4)
        tk.Label(left, text=f"Expiry: {member_info.get('subscription_expiry')}", font=("Helvetica", 12)).pack(anchor="w", pady=4)
    else:
        tk.Label(left, text="No member info found.", font=("Helvetica", 12)).pack(anchor="w", pady=4)

    # Plan list
    tk.Label(center, text="Available Plans", font=("Helvetica", 14, "bold")).pack(anchor="w")
    listbox = tk.Listbox(center, font=("Helvetica", 12), height=12)
    scrollbar = tk.Scrollbar(center, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="left", fill="y")

    plan_names = sorted(plans.keys())
    for p in plan_names:
        listbox.insert("end", p)

    detail_frame = tk.Frame(right)
    detail_frame.pack(anchor="n")
    tk.Label(detail_frame, text="Plan Details", font=("Helvetica", 14, "bold")).pack()
    lbl_duration = tk.Label(detail_frame, text="Duration: -", font=("Helvetica", 12))
    lbl_duration.pack(anchor="w", pady=6)
    lbl_price = tk.Label(detail_frame, text="Price: -", font=("Helvetica", 12))
    lbl_price.pack(anchor="w", pady=6)

    selected_plan_var = tk.StringVar()

    def on_select(evt=None):
        sel = listbox.curselection()
        if not sel:
            return
        plan = listbox.get(sel[0])
        selected_plan_var.set(plan)
        detail = plans.get(plan)
        if isinstance(detail, list) and len(detail) >= 2:
            lbl_duration.config(text=f"Duration: {detail[0]} days")
            try:
                lbl_price.config(text=f"Price: {int(detail[1]):,} VND")
            except Exception:
                lbl_price.config(text=f"Price: {detail[1]}")
        elif isinstance(detail, list) and len(detail) == 1:
            lbl_duration.config(text=f"Duration: {detail[0]} days")
            lbl_price.config(text="Price: -")
        else:
            lbl_duration.config(text="Duration: -")
            lbl_price.config(text="Price: -")

    listbox.bind("<<ListboxSelect>>", on_select)

    # Buttons
    btn_frame = tk.Frame(root, pady=12)
    btn_frame.pack(fill="x")

    def on_confirm():
        plan = selected_plan_var.get()
        if not plan:
            messagebox.showwarning("No plan selected", "Please select a subscription plan first.")
            return

        member = Member(username)
        result = member.renew_subscribe_plan_with_name(plan)
        if result.get("success"):
            new_expiry = result.get("new_expiry")
            price = result.get("price")
            msg = f"Successfully updated subscription to '{plan}'.\nNew expiry: {new_expiry}"
            if price is not None:
                msg += f"\nPrice: {price:,} VND"
            messagebox.showinfo("Subscription updated", msg)
            # update displayed member info
            mi = _get_member_info()
            if mi:
                lbls = left.winfo_children()
                # replace text labels
                for w in lbls:
                    if isinstance(w, tk.Label) and w.cget("text").startswith("Plan:"):
                        w.config(text=f"Plan: {mi.get('membership')}")
                    if isinstance(w, tk.Label) and w.cget("text").startswith("Expiry:"):
                        w.config(text=f"Expiry: {mi.get('subscription_expiry')}")
        else:
            messagebox.showerror("Failed", result.get("message", "Unknown error"))

    def on_cancel():
        root.destroy()

    btn_confirm = tk.Button(btn_frame, text="Confirm", command=on_confirm, bg="#27AE60", fg="white", font=("Helvetica", 12, "bold"))
    btn_confirm.pack(side="right", padx=12)

    btn_cancel = tk.Button(btn_frame, text="Close", command=on_cancel, font=("Helvetica", 12))
    btn_cancel.pack(side="right")

    # Preselect first plan
    if plan_names:
        listbox.selection_set(0)
        on_select()

    # If this function was given a container window, we simply populate it and return it.
    # If not, we created a new Toplevel above.
    try:
        root.transient(window)
    except Exception:
        pass
    try:
        root.grab_set()
    except Exception:
        pass
    try:
        root.focus_force()
    except Exception:
        pass
    return root
