"""
audit_and_sync_all_pages.py
Scans final_report.pdf using PyMuPDF to find the exact 1-indexed page number
where each section heading, figure, and table appears.
Then updates final_report.html and recompiles final_report.pdf.
"""
import os
import re
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")

doc = pymupdf.open(PDF_PATH)
print(f"Total pages in PDF: {len(doc)}")

# Build full text index per page
page_texts = {}
for i, page in enumerate(doc):
    page_texts[i + 1] = page.get_text("text")

# Let's define the items we need to find in the preliminary lists:
# Preliminaries
prelim_items = [
    ("Declaration", "DECLARATION"),
    ("Approval for Submission", "APPROVAL FOR SUBMISSION"),
    ("Acknowledgments", "ACKNOWLEDGMENTS"),
    ("Abstract", "ABSTRACT"),
    ("Abstrak", "ABSTRAK"),
    ("Table of Contents", "TABLE OF CONTENTS"),
    ("List of Figures", "LIST OF FIGURES"),
    ("List of Tables", "LIST OF TABLES"),
]

# Chapters and Sections
toc_items = [
    ("CHAPTER 1: INTRODUCTION", "CHAPTER 1: INTRODUCTION"),
    ("1.0 Introduction", "1.0 Introduction"),
    ("1.1 Problem Statement", "1.1 Problem Statement"),
    ("1.2 Project Scope", "1.2 Project Scope"),
    ("1.3 Aim and Objectives", "1.3 Aim and Objectives"),
    ("1.4 Methodology (Agile SDLC)", "1.4 Methodology (Agile SDLC)"),
    ("1.5 Significance of the Project", "1.5 Significance of the Project"),
    ("1.6 Project Schedule (Gantt Chart)", "1.6 Project Schedule (Gantt Chart)"),
    ("1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis", "1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis"),
    
    ("CHAPTER 2: LITERATURE REVIEW", "CHAPTER 2: LITERATURE REVIEW"),
    ("2.0 Introduction", "2.0 Introduction"),
    ("2.1 High Availability and Cloud Fault Tolerance Models", "2.1 High Availability and Cloud Fault Tolerance Models"),
    ("2.2 Student Rental Portals and Scam Prevention Studies", "2.2 Student Rental Portals and Scam Prevention Studies"),
    ("2.3 Cloud Infrastructure, Redundancy, and Load Balancing", "2.3 Cloud Infrastructure, Redundancy, and Load Balancing"),
    ("2.4 Comparative Analysis of Existing Systems vs. PoliSewa", "2.4 Comparative Analysis of Existing Systems vs. PoliSewa"),
    ("2.5 Chapter Summary", "2.5 Chapter Summary"),
    
    ("CHAPTER 3: ANALYSIS AND DESIGN", "CHAPTER 3: ANALYSIS AND DESIGN"),
    ("3.0 Introduction", "3.0 Introduction"),
    ("3.1 Requirement Analysis", "3.1 Requirement Analysis"),
    ("3.2 High Availability System Architecture", "3.2 High Availability System Architecture"),
    ("3.3 Data Flow Diagrams (DFD)", "3.3 Data Flow Diagrams (DFD)"),
    ("3.4 Database Design", "3.4 Database Design"),
    ("3.5 User Interface (UI/UX) Design", "3.5 User Interface (UI/UX) Design"),
    ("3.6 Chapter Summary", "3.6 Chapter Summary"),
    
    ("CHAPTER 4: IMPLEMENTATION", "CHAPTER 4: IMPLEMENTATION"),
    ("4.0 Introduction", "4.0 Introduction"),
    ("4.1 Cloud Infrastructure Deployment", "4.1 Cloud Infrastructure Deployment"),
    ("4.2 Application Code Development", "4.2 Application Code Development"),
    ("4.3 Chapter Summary", "4.3 Chapter Summary"),
    
    ("CHAPTER 5: TESTING AND VERIFICATION", "CHAPTER 5: TESTING AND VERIFICATION"),
    ("5.0 Introduction", "5.0 Introduction"),
    ("5.1 Cloud High Availability and Failover Testing", "5.1 Cloud High Availability and Failover Testing"),
    ("5.2 Functional and Usability Testing", "5.2 Functional and Usability Testing"),
    ("5.3 User Scenario Walkthroughs", "5.3 User Scenario Walkthroughs"),
    ("5.4 Testing Summary", "5.4 Testing Summary"),
    
    ("CHAPTER 6: CONCLUSION AND RECOMMENDATIONS", "CHAPTER 6: CONCLUSION AND RECOMMENDATIONS"),
    ("6.0 Introduction", "6.0 Introduction"),
    ("6.1 Project Achievements", "6.1 Project Achievements"),
    ("6.2 Challenges and Problem Solving", "6.2 Challenges and Problem Solving"),
    ("6.3 Future Work and Recommendations", "6.3 Future Work and Recommendations"),
    ("6.4 Final Concluding Remarks", "6.4 Final Concluding Remarks"),
    
    ("REFERENCES", "REFERENCES"),
    ("APPENDIX A: AZURE SQL DATABASE DATA DICTIONARY", "APPENDIX A: AZURE SQL DATABASE DATA DICTIONARY"),
    ("APPENDIX B: CORE ARCHITECTURAL SOURCE CODE LISTINGS", "APPENDIX B: CORE ARCHITECTURAL SOURCE CODE LISTINGS"),
    ("APPENDIX C: SYSTEM SCREENSHOT CATALOG AND TESTING EVIDENCE", "APPENDIX C: SYSTEM SCREENSHOT CATALOG AND TESTING EVIDENCE")
]

# Figures
figure_items = [
    ("Figure 1.4(a)", "Figure 1.4(a): Agile"),
    ("Figure 1.6(a)", "Figure 1.6(a): Project Development Schedule"),
    ("Figure 1.7(a)", "Figure 1.7(a): Azure Subscription Cost Analysis"),
    ("Figure 1.7(b)", "Figure 1.7(b): Azure Resource-Level Cost Breakdown"),
    ("Figure 3.2.1(a)", "Figure 3.2.1(a): High Availability Dual VM Cloud Architecture"),
    ("Figure 3.2.2(a)", "Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Sequence"),
    ("Figure 3.3.1(a)", "Figure 3.3.1(a): Level-0 Context Diagram"),
    ("Figure 3.4.1(a)", "Figure 3.4.1(a): Entity-Relationship Diagram"),
    ("Figure 3.5.1(a)", "Figure 3.5.1(a): User Interface Wireframe"),
    ("Figure 4.1.1(a)", "Figure 4.1.1(a): Azure Resource Group Overview"),
    ("Figure 4.1.1(b)", "Figure 4.1.1(b): Dual Azure Virtual Machines"),
    ("Figure 4.1.2(a)", "Figure 4.1.2(a): Cloudflare Edge Routing and Gateway Status Verification"),
    ("Figure 4.1.3(a)", "Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules"),
    ("Figure 4.1.4(a)", "Figure 4.1.4(a): Virtual Machine Linux Host Console and Git Deployment"),
    ("Figure 5.1.1(a)", "Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2"),
    ("Figure 5.1.2(a)", "Figure 5.1.2(a): Simulated VM1 Service Termination"),
    ("Figure 5.1.2(b)", "Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response"),
    ("Figure 5.1.3(a)", "Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check"),
    ("Figure 5.2.1(a)", "Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark"),
    ("Figure 5.2.2(a)", "Figure 5.2.2(a): Live Keyword Search and Price Filtering"),
    ("Figure 5.2.3(a)", "Figure 5.2.3(a): 6-Box Email OTP Verification Dialog"),
    ("Figure 5.2.3(b)", "Figure 5.2.3(b): PoliSewa OTP Verification Email Received"),
    ("Figure 5.2.4(a)", "Figure 5.2.4(a): Landlord Property Creation Modal with Pinpoint Coordinate Binding"),
    ("Figure 5.2.5(a)", "Figure 5.2.5(a): Property Listing Card with Direct WhatsApp Contact"),
    ("Figure 5.2.6(a)", "Figure 5.2.6(a): Permanent Account Deletion Confirmation"),
    ("Figure 5.3.1(a)", "Figure 5.3.1(a): Student User Workflow"),
    ("Figure 5.3.2(a)", "Figure 5.3.2(a): Family Member Review Workflow"),
    ("Figure 5.3.3(a)", "Figure 5.3.3(a): Landlord Portal Workflow")
]

# Tables
table_items = [
    ("Table 1.7(a)", "Table 1.7(a): Cumulative Azure Infrastructure Expenditure"),
    ("Table 2.4(a)", "Table 2.4(a): Feature and Architecture Comparison"),
    ("Table 3.1.1(a)", "Table 3.1.1(a): Functional Requirements Specification"),
    ("Table 3.1.2(a)", "Table 3.1.2(a): Non-Functional Requirements Specification"),
    ("Table 5.1.2(a)", "Table 5.1.2(a): Automated Cloud Failover Test Results"),
    ("Table 5.2.7(a)", "Table 5.2.7(a): Functional Black-Box Test Results"),
    ("Table 5.2.7(b)", "Table 5.2.7(b): Non-Functional Performance & Resiliency Test Results"),
    ("Table 5.3.4(a)", "Table 5.3.4(a): Usability Verification Metrics Across User Personas"),
    ("Table A.1", "Table A.1: Data Dictionary for users Table"),
    ("Table A.2", "Table A.2: Data Dictionary for properties Table"),
    ("Table A.3", "Table A.3: Data Dictionary for otp_verifications Table")
]

def find_page(search_str, min_page=1):
    search_lower = search_str.lower()
    for p in range(min_page, len(doc) + 1):
        if search_lower in page_texts[p].lower():
            return p
    return None

print("\n--- DETECTED PAGE NUMBERS ---")
found_prelim = {}
for label, needle in prelim_items:
    p = find_page(needle, 2)
    found_prelim[label] = p
    print(f"Prelim: {label} -> Page {p}")

found_toc = {}
curr_page = 11
for label, needle in toc_items:
    p = find_page(needle, curr_page)
    if p:
        curr_page = p
    found_toc[label] = p
    print(f"TOC: {label} -> Page {p}")

found_figures = {}
curr_page = 11
for label, needle in figure_items:
    p = find_page(needle, 11)
    found_figures[label] = p
    print(f"Figure: {label} -> Page {p}")

found_tables = {}
for label, needle in table_items:
    p = find_page(needle, 11)
    found_tables[label] = p
    print(f"Table: {label} -> Page {p}")
