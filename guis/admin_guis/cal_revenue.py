import tkinter as tk
from tkinter import messagebox, filedialog
import json
import csv
import os
from datetime import datetime
from collections import defaultdict

def export_to_csv(revenue_data, filename=None):
    """Export revenue data to CSV file"""
    if not filename:
        filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write summary
            writer.writerow(['REVENUE SUMMARY REPORT'])
            writer.writerow(['Generated on:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            writer.writerow(['Total Revenue:', f"{revenue_data['total_revenue']:,} VND"])
            writer.writerow(['Total Members:', revenue_data['total_members']])
            writer.writerow([])
            
            # Revenue by subscription plan
            writer.writerow(['REVENUE BY SUBSCRIPTION PLAN'])
            writer.writerow(['Plan', 'Revenue (VND)', 'Number of Members'])
            for plan, revenue in revenue_data['revenue_by_plan'].items():
                member_count = sum(1 for member in revenue_data['member_details'] 
                                 if member['membership'] == plan)
                writer.writerow([plan, f"{revenue:,}", member_count])
            writer.writerow([])
            
            # Revenue by month
            writer.writerow(['REVENUE BY MONTH'])
            writer.writerow(['Month', 'Revenue (VND)'])
            for month, revenue in sorted(revenue_data['revenue_by_month'].items()):
                writer.writerow([month, f"{revenue:,}"])
            writer.writerow([])
            
            # Detailed member information
            writer.writerow(['DETAILED MEMBER INFORMATION'])
            writer.writerow(['Name', 'Username', 'Membership', 'Fee (VND)', 'Joined Date', 'Expiry Date'])
            for member in revenue_data['member_details']:
                writer.writerow([
                    member['name'],
                    member['username'],
                    member['membership'],
                    f"{member['fee']:,}",
                    member['joined_date'],
                    member['subscription_expiry']
                ])
        
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def on_cal_revenue(root, admin):
    """Main revenue calculation and export interface"""
    root.title("Revenue Calculation and Reports")
    
    # Calculate revenue data using admin's method
    revenue_data = admin.calculate_revenue()
    
    # Main frame
    main_frame = tk.Frame(root, bg=root["bg"])
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="Revenue Calculation and Reports", 
                          font=("Arial", 24, "bold"), bg=root["bg"])
    title_label.pack(pady=20)
    
    # Summary frame
    summary_frame = tk.Frame(main_frame, bg=root["bg"], relief="raised", bd=2)
    summary_frame.pack(pady=20, fill="x", padx=20)
    
    summary_title = tk.Label(summary_frame, text="Revenue Summary", 
                            font=("Arial", 16, "bold"), bg=root["bg"])
    summary_title.pack(pady=10)
    
    # Total revenue
    total_revenue_label = tk.Label(summary_frame, 
                                  text=f"Total Revenue: {revenue_data['total_revenue']:,} VND",
                                  font=("Arial", 14, "bold"), bg=root["bg"], fg="#4CAF50")
    total_revenue_label.pack(pady=5)
    
    # Total members
    total_members_label = tk.Label(summary_frame, 
                                  text=f"Total Members: {revenue_data['total_members']}",
                                  font=("Arial", 12), bg=root["bg"])
    total_members_label.pack(pady=5)
    
    # Revenue by plan frame
    plan_frame = tk.Frame(main_frame, bg=root["bg"])
    plan_frame.pack(pady=20, fill="both", expand=True, padx=20)
    
    plan_title = tk.Label(plan_frame, text="Revenue by Subscription Plan", 
                         font=("Arial", 16, "bold"), bg=root["bg"])
    plan_title.pack(pady=10)
    
    # Create scrollable frame for plan details
    canvas = tk.Canvas(plan_frame, bg=root["bg"], height=200)
    scrollbar = tk.Scrollbar(plan_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=root["bg"])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Header for plan details
    header_frame = tk.Frame(scrollable_frame, bg=root["bg"])
    header_frame.pack(fill="x", pady=5)
    
    tk.Label(header_frame, text="Plan", font=("Arial", 12, "bold"), 
            bg=root["bg"], width=20).pack(side="left", padx=5)
    tk.Label(header_frame, text="Revenue (VND)", font=("Arial", 12, "bold"), 
            bg=root["bg"], width=15).pack(side="left", padx=5)
    tk.Label(header_frame, text="Members", font=("Arial", 12, "bold"), 
            bg=root["bg"], width=10).pack(side="left", padx=5)
    
    # Plan details
    for plan, revenue in revenue_data['revenue_by_plan'].items():
        member_count = sum(1 for member in revenue_data['member_details'] 
                          if member['membership'] == plan)
        
        plan_row = tk.Frame(scrollable_frame, bg=root["bg"])
        plan_row.pack(fill="x", pady=2)
        
        tk.Label(plan_row, text=plan, font=("Arial", 11), 
                bg=root["bg"], width=20).pack(side="left", padx=5)
        tk.Label(plan_row, text=f"{revenue:,}", font=("Arial", 11), 
                bg=root["bg"], width=15).pack(side="left", padx=5)
        tk.Label(plan_row, text=str(member_count), font=("Arial", 11), 
                bg=root["bg"], width=10).pack(side="left", padx=5)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Export buttons frame
    button_frame = tk.Frame(main_frame, bg=root["bg"])
    button_frame.pack(pady=20)
    
    def export_report():
        """Export revenue report to CSV"""
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
        """Save report to default location"""
        filename = f"revenue_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        if export_to_csv(revenue_data, filename):
            messagebox.showinfo("Success", f"Revenue report saved to:\n{filename}")
        else:
            messagebox.showerror("Error", "Failed to save revenue report!")
    
    # Export buttons
    export_btn = tk.Button(button_frame, text="Export to CSV", command=export_report,
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                          relief="raised", bd=2)
    export_btn.pack(side="left", padx=10)
    
    save_btn = tk.Button(button_frame, text="Save Report", command=save_to_default_location,
                        font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                        relief="raised", bd=2)
    save_btn.pack(side="left", padx=10)
    
    def back_to_menu():
        root.destroy()
    
    back_btn = tk.Button(button_frame, text="Back to Menu", command=back_to_menu,
                        font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
                        relief="raised", bd=2)
    back_btn.pack(side="left", padx=10)
