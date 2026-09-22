"""
sync_dft50114_final.py
Synchronizes Table of Contents, List of Figures, and List of Tables in final_report.html
to match the exact page layout of the DFT50114 48-page PDF.
"""
import os
import re
import subprocess
import pymupdf

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")
MD_PATH = os.path.join(BASE_DIR, "final_report.md")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# New Table of Contents Block
new_toc = """<!-- TABLE OF CONTENTS -->
<h1>Table of Contents</h1>
<div class="toc-row"><span class="toc-title">Declaration</span><span class="toc-page">2</span></div>
<div class="toc-row"><span class="toc-title">Approval for Submission</span><span class="toc-page">3</span></div>
<div class="toc-row"><span class="toc-title">Acknowledgments</span><span class="toc-page">4</span></div>
<div class="toc-row"><span class="toc-title">Abstract</span><span class="toc-page">5</span></div>
<div class="toc-row"><span class="toc-title">Abstrak</span><span class="toc-page">6</span></div>
<div class="toc-row"><span class="toc-title">List of Figures</span><span class="toc-page">9</span></div>
<div class="toc-row"><span class="toc-title">List of Tables</span><span class="toc-page">11</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 1: INTRODUCTION</strong></span><span class="toc-page"><strong>12</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.0 Introduction</span><span class="toc-page">12</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.1 Problem Statement</span><span class="toc-page">12</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.2 Project Scope</span><span class="toc-page">13</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.3 Aim and Objectives</span><span class="toc-page">14</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.4 Methodology (Agile SDLC)</span><span class="toc-page">14</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.5 Significance of the Project</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.6 Project Schedule (Gantt Chart)</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis</span><span class="toc-page">15</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 2: LITERATURE REVIEW</strong></span><span class="toc-page"><strong>18</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.0 Introduction</span><span class="toc-page">18</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.1 High Availability and Cloud Fault Tolerance Models</span><span class="toc-page">18</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.2 Student Rental Portals and Scam Prevention Studies</span><span class="toc-page">19</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.3 Cloud Infrastructure, Redundancy, and Load Balancing</span><span class="toc-page">20</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.4 Comparative Analysis of Existing Systems vs. PoliSewa</span><span class="toc-page">20</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;2.5 Chapter Summary</span><span class="toc-page">21</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 3: ANALYSIS AND DESIGN</strong></span><span class="toc-page"><strong>22</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.0 Introduction</span><span class="toc-page">22</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.1 Requirement Analysis</span><span class="toc-page">22</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.2 High Availability System Architecture</span><span class="toc-page">23</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.3 Data Flow Diagrams (DFD)</span><span class="toc-page">25</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.4 Database Design</span><span class="toc-page">26</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.5 User Interface (UI/UX) Design</span><span class="toc-page">28</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;3.6 Chapter Summary</span><span class="toc-page">29</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 4: IMPLEMENTATION</strong></span><span class="toc-page"><strong>30</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;4.0 Introduction</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;4.1 Cloud Infrastructure Deployment</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;4.2 Application Code Development</span><span class="toc-page">33</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;4.3 Chapter Summary</span><span class="toc-page">35</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 5: TESTING AND VERIFICATION</strong></span><span class="toc-page"><strong>36</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.0 Introduction</span><span class="toc-page">36</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.1 Cloud High Availability and Failover Testing</span><span class="toc-page">36</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.2 Software Functional Testing</span><span class="toc-page">39</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.3 User Scenario Walkthroughs</span><span class="toc-page">43</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.4 Test Results Summary</span><span class="toc-page">44</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;5.5 Chapter Summary</span><span class="toc-page">44</span></div>

<div class="toc-row"><span class="toc-title"><strong>CHAPTER 6: CONCLUSION AND FUTURE WORKS</strong></span><span class="toc-page"><strong>45</strong></span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;6.0 Introduction</span><span class="toc-page">45</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;6.1 Objective Achievement Review</span><span class="toc-page">45</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;6.2 Challenges and Problem Solving</span><span class="toc-page">45</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;6.3 Future Works and Enhancements</span><span class="toc-page">46</span></div>
<div class="toc-row"><span class="toc-title">&nbsp;&nbsp;&nbsp;&nbsp;6.4 Conclusion</span><span class="toc-page">46</span></div>

<div class="toc-row"><span class="toc-title"><strong>REFERENCES</strong></span><span class="toc-page"><strong>47</strong></span></div>"""

# New List of Figures Block
new_lof = """<!-- LIST OF FIGURES -->
<h1>List of Figures</h1>
<div class="toc-row"><span class="toc-title">Figure 1.4(a): Agile Software Development Life Cycle (SDLC) Workflow for PoliSewa</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.6(a): Project Development Schedule (Gantt Chart)</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend</span><span class="toc-page">17</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.7(b): Azure Resource-Level Cost Breakdown & Infrastructure Inventory</span><span class="toc-page">17</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram</span><span class="toc-page">23</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart</span><span class="toc-page">24</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa</span><span class="toc-page">25</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database</span><span class="toc-page">26</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.5.1(a): User Interface Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout</span><span class="toc-page">28</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.1(a): Azure Resource Group Overview ('polisewa')</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.2(a): Cloudflare Edge Routing and Gateway Status Verification</span><span class="toc-page">31</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules</span><span class="toc-page">32</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.4(a): Virtual Machine Linux Host Console and Git Deployment</span><span class="toc-page">33</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.2(a): Geodesic Haversine Distance Calculation Source Code</span><span class="toc-page">34</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Source Code</span><span class="toc-page">35</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Source Code</span><span class="toc-page">35</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status</span><span class="toc-page">36</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal ('pm2 stop polisewa')</span><span class="toc-page">37</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in Browser DevTools</span><span class="toc-page">37</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check</span><span class="toc-page">38</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers</span><span class="toc-page">39</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300) with Distance Badges</span><span class="toc-page">39</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer</span><span class="toc-page">40</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox</span><span class="toc-page">40</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.4(a): Landlord Property Creation Modal with Pinpoint Coordinate Binding</span><span class="toc-page">41</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.5(a): Property Listing Card with Direct WhatsApp Contact and Verified Badge</span><span class="toc-page">42</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog</span><span class="toc-page">42</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.1(a): Student User Workflow: Room Discovery and Geodesic Distance Verification</span><span class="toc-page">43</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection</span><span class="toc-page">43</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.3(a): Landlord Portal Workflow: Registration, OTP Verification, and Listing Creation</span><span class="toc-page">43</span></div>"""

# New List of Tables Block
new_lot = """<!-- LIST OF TABLES -->
<h1>List of Tables</h1>
<div class="toc-row"><span class="toc-title">Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">Table 2.4(a): Comparative Analysis Matrix of Rental Systems</span><span class="toc-page">20</span></div>
<div class="toc-row"><span class="toc-title">Table 3.1.1(a): Server and Client Hardware Requirements</span><span class="toc-page">22</span></div>
<div class="toc-row"><span class="toc-title">Table 3.1.2(a): Software Stack and Development Technologies</span><span class="toc-page">22</span></div>
<div class="toc-row"><span class="toc-title">Table 3.4.2(a): Data Dictionary for 'users' Table</span><span class="toc-page">26</span></div>
<div class="toc-row"><span class="toc-title">Table 3.4.2(b): Data Dictionary for 'properties' Table</span><span class="toc-page">27</span></div>
<div class="toc-row"><span class="toc-title">Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix</span><span class="toc-page">43</span></div>
<div class="toc-row"><span class="toc-title">Table 6.1(a): Project Objectives Achievement Verification Matrix</span><span class="toc-page">45</span></div>"""

# Replace in HTML
html = re.sub(r'<!-- TABLE OF CONTENTS -->.*?<!-- LIST OF FIGURES -->', new_toc + '\n\n<div class="page-break"></div>\n\n<!-- LIST OF FIGURES -->', html, flags=re.DOTALL)
html = re.sub(r'<!-- LIST OF FIGURES -->.*?<!-- LIST OF TABLES -->', new_lof + '\n\n<div class="page-break"></div>\n\n<!-- LIST OF TABLES -->', html, flags=re.DOTALL)
html = re.sub(r'<!-- LIST OF TABLES -->.*?<!-- CHAPTER 1: INTRODUCTION -->', new_lot + '\n\n<div class="page-break"></div>\n\n<!-- CHAPTER 1: INTRODUCTION -->', html, flags=re.DOTALL)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

# Recompile PDF
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

print("Recompiling PDF with Edge...")
subprocess.run(cmd, check=True)

doc = pymupdf.open(PDF_PATH)
print(f"Final PDF page count: {len(doc)}")
