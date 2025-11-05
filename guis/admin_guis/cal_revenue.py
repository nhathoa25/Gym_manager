import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import csv
import os
from datetime import datetime
from collections import defaultdict

def export_to_csv(revenue_data, filename=None):
    if not filename:
        filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile: # Thêm -sig
            writer = csv.writer(csvfile)
            
            writer.writerow(['REVENUE SUMMARY REPORT'])
            writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            writer.writerow(['Total Revenue:', f"{revenue_data['total_revenue']:,} VND"])
            writer.writerow(['Total Members:', revenue_data['total_members']])
            writer.writerow([])
            
            writer.writerow(['REVENUE BY SUBSCRIPTION PLAN'])
            writer.writerow(['Plan', 'Revenue (VND)', 'Number of Members'])
            for plan, revenue in revenue_data['revenue_by_plan'].items():
                member_count = sum(1 for member in revenue_data['member_details'] 
                                 if member['membership'] == plan)
                writer.writerow([plan, f"{revenue:,}", member_count])
            writer.writerow([])
            
            writer.writerow(['REVENUE BY MONTH'])
            writer.writerow(['Month', 'Revenue (VND)'])
            for month, revenue in sorted(revenue_data['revenue_by_month'].items()):
                writer.writerow([month, f"{revenue:,}"])
            writer.writerow([])
            
            writer.writerow(['DETAILED MEMBER INFORMATION'])
            writer.writerow(['Name', 'Username', 'Membership', 'Fee (VND)', 'Joined Date', 'Expiry Date'])
            for member in revenue_data['member_details']:
                writer.writerow([
                    member['name'], member['username'],
                    member['membership'], f"{member['fee']:,}",
                    member['joined_date'], member['subscription_expiry']
                ])
        
        return True
    except Exception as e:
        messagebox.showerror(f"Error exporting to CSV: {e}")
        return False

def on_cal_revenue(root, admin):
    root.title("Revenue Calculation and Reports")
    
    try:
        revenue_data = admin.calculate_revenue()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate revenue: {e}")
        root.destroy()
        return

    main_frame = ttk.Frame(root)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    title_label = ttk.Label(main_frame, text="Revenue Calculation and Reports", 
                          font=("Arial", 24, "bold"))
    title_label.pack(pady=20)
    
    # Summary frame
    summary_frame = ttk.Frame(main_frame, relief="raised", borderwidth=2)
    summary_frame.pack(pady=20, fill="x", padx=20)
    
    summary_title = ttk.Label(summary_frame, text="Revenue Summary", 
                            font=("Arial", 16, "bold"))
    summary_title.pack(pady=10)
    
    total_revenue_label = ttk.Label(summary_frame, 
                                  text=f"Total Revenue: {revenue_data['total_revenue']:,} VND",
                                  font=("Arial", 14, "bold"), foreground="#4CAF50")
    total_revenue_label.pack(pady=5)
    
    total_members_label = ttk.Label(summary_frame, 
                                  text=f"Total Members: {revenue_data['total_members']}",
                                  font=("Arial", 12))
    total_members_label.pack(pady=5)
    
    # Plan frame
    plan_frame = ttk.Frame(main_frame)
    plan_frame.pack(pady=20, fill="both", expand=True, padx=20)
    
    plan_title = ttk.Label(plan_frame, text="Revenue by Subscription Plan", 
                         font=("Arial", 16, "bold"))
    plan_title.pack(pady=10)
    
    # Treeview cho plan
    plan_tree_frame = ttk.Frame(plan_frame)
    plan_tree_frame.pack(fill="both", expand=True)

    columns = ("Plan", "Revenue (VND)", "Members")
    plan_tree = ttk.Treeview(plan_tree_frame, columns=columns, show="headings", height=5)
    
    plan_tree.heading("Plan", text="Plan")
    plan_tree.heading("Revenue (VND)", text="Revenue (VND)")
    plan_tree.heading("Members", text="Members")
    
    plan_tree.column("Plan", width=150)
    plan_tree.column("Revenue (VND)", width=150, anchor="e")
    plan_tree.column("Members", width=100, anchor="center")

    scrollbar = ttk.Scrollbar(plan_tree_frame, orient="vertical", command=plan_tree.yview)
    plan_tree.configure(yscrollcommand=scrollbar.set)
    
    plan_tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    for plan, revenue in revenue_data['revenue_by_plan'].items():
        member_count = sum(1 for member in revenue_data['member_details'] 
                          if member['membership'] == plan)
        plan_tree.insert("", "end", values=(plan, f"{revenue:,}", member_count))
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(side="bottom", pady=20)
    
    def export_report():
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Revenue Report As"
        )
        if filename:
            if export_to_csv(revenue_data, filename):
                messagebox.showinfo("Success", f"Revenue report exported successfully to:\n{filename}")
            else:
                messagebox.showerror("Error", "Failed to export revenue report!")
    
    def save_to_default_location():
        filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if export_to_csv(revenue_data, filename):
            messagebox.showinfo("Success", f"Revenue report saved to:\n{os.path.abspath(filename)}")
        else:
            messagebox.showerror("Error", "Failed to save revenue report!")
    
    export_btn = ttk.Button(button_frame, text="Export to CSV", command=export_report, style="Success.TButton")
    export_btn.pack(side="left", padx=10)
    
    save_btn = ttk.Button(button_frame, text="Save Report (Default)", command=save_to_default_location, style="Primary.TButton")
    save_btn.pack(side="left", padx=10)
    
    back_btn = ttk.Button(button_frame, text="Back to Menu", command=root.destroy, style="Warning.TButton")
    back_btn.pack(side="left", padx=10)