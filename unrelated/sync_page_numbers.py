"""
Re-syncs the Table of Contents, List of Figures, and List of Tables
to the exact page numbers of the new 43-page PDF (without empty page 2).
"""
import os
import re
import subprocess

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# TOC Page Number updates (shift by 1)
toc_replacements = [
    ('<span class="toc-title">Declaration</span><span class="toc-page">ii</span>', '<span class="toc-title">Declaration</span><span class="toc-page">2</span>'),
    ('<span class="toc-title">Approval for Submission</span><span class="toc-page">iii</span>', '<span class="toc-title">Approval for Submission</span><span class="toc-page">3</span>'),
    ('<span class="toc-title">Acknowledgments</span><span class="toc-page">iv</span>', '<span class="toc-title">Acknowledgments</span><span class="toc-page">4</span>'),
    ('<span class="toc-title">Abstract</span><span class="toc-page">v</span>', '<span class="toc-title">Abstract</span><span class="toc-page">5</span>'),
    ('<span class="toc-title">Abstrak</span><span class="toc-page">vi</span>', '<span class="toc-title">Abstrak</span><span class="toc-page">6</span>'),
    ('<span class="toc-title">List of Figures</span><span class="toc-page">viii</span>', '<span class="toc-title">List of Figures</span><span class="toc-page">9</span>'),
    ('<span class="toc-title">List of Tables</span><span class="toc-page">ix</span>', '<span class="toc-title">List of Tables</span><span class="toc-page">11</span>'),

    ('<span class="toc-title">CHAPTER 1: INTRODUCTION</span><span class="toc-page">13</span>', '<span class="toc-title">CHAPTER 1: INTRODUCTION</span><span class="toc-page">12</span>'),
    ('<span class="toc-title">1.0 Introduction</span><span class="toc-page">13</span>', '<span class="toc-title">1.0 Introduction</span><span class="toc-page">12</span>'),
    ('<span class="toc-title">1.1 Problem Statement</span><span class="toc-page">13</span>', '<span class="toc-title">1.1 Problem Statement</span><span class="toc-page">12</span>'),
    ('<span class="toc-title">1.2 Project Scope</span><span class="toc-page">14</span>', '<span class="toc-title">1.2 Project Scope</span><span class="toc-page">13</span>'),
    ('<span class="toc-title">1.3 Aim and Objectives</span><span class="toc-page">15</span>', '<span class="toc-title">1.3 Aim and Objectives</span><span class="toc-page">14</span>'),
    ('<span class="toc-title">1.4 Methodology (Agile SDLC)</span><span class="toc-page">15</span>', '<span class="toc-title">1.4 Methodology (Agile SDLC)</span><span class="toc-page">14</span>'),
    ('<span class="toc-title">1.5 Significance of the Project</span><span class="toc-page">16</span>', '<span class="toc-title">1.5 Significance of the Project</span><span class="toc-page">15</span>'),
    ('<span class="toc-title">1.6 Project Schedule (Gantt Chart)</span><span class="toc-page">16</span>', '<span class="toc-title">1.6 Project Schedule (Gantt Chart)</span><span class="toc-page">15</span>'),
    ('<span class="toc-title">1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis</span><span class="toc-page">16</span>', '<span class="toc-title">1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis</span><span class="toc-page">15</span>'),
    
    ('<span class="toc-title">CHAPTER 2: LITERATURE REVIEW</span><span class="toc-page">19</span>', '<span class="toc-title">CHAPTER 2: LITERATURE REVIEW</span><span class="toc-page">18</span>'),
    ('<span class="toc-title">2.0 Introduction</span><span class="toc-page">19</span>', '<span class="toc-title">2.0 Introduction</span><span class="toc-page">18</span>'),
    ('<span class="toc-title">2.1 High Availability and Cloud Fault Tolerance Models</span><span class="toc-page">19</span>', '<span class="toc-title">2.1 High Availability and Cloud Fault Tolerance Models</span><span class="toc-page">18</span>'),
    ('<span class="toc-title">2.2 Student Rental Portals and Scam Prevention Studies</span><span class="toc-page">20</span>', '<span class="toc-title">2.2 Student Rental Portals and Scam Prevention Studies</span><span class="toc-page">19</span>'),
    ('<span class="toc-title">2.3 Cloud Infrastructure, Redundancy, and Load Balancing</span><span class="toc-page">21</span>', '<span class="toc-title">2.3 Cloud Infrastructure, Redundancy, and Load Balancing</span><span class="toc-page">20</span>'),
    ('<span class="toc-title">2.4 Comparative Analysis of Existing Systems vs. PoliSewa</span><span class="toc-page">21</span>', '<span class="toc-title">2.4 Comparative Analysis of Existing Systems vs. PoliSewa</span><span class="toc-page">20</span>'),
    ('<span class="toc-title">2.5 Chapter Summary</span><span class="toc-page">22</span>', '<span class="toc-title">2.5 Chapter Summary</span><span class="toc-page">21</span>'),
    
    ('<span class="toc-title">CHAPTER 3: ANALYSIS AND DESIGN</span><span class="toc-page">23</span>', '<span class="toc-title">CHAPTER 3: ANALYSIS AND DESIGN</span><span class="toc-page">22</span>'),
    ('<span class="toc-title">3.0 Introduction</span><span class="toc-page">23</span>', '<span class="toc-title">3.0 Introduction</span><span class="toc-page">22</span>'),
    ('<span class="toc-title">3.1 Requirement Analysis</span><span class="toc-page">23</span>', '<span class="toc-title">3.1 Requirement Analysis</span><span class="toc-page">22</span>'),
    ('<span class="toc-title">3.2 High Availability System Architecture</span><span class="toc-page">24</span>', '<span class="toc-title">3.2 High Availability System Architecture</span><span class="toc-page">23</span>'),
    ('<span class="toc-title">3.3 Data Flow Diagrams (DFD)</span><span class="toc-page">26</span>', '<span class="toc-title">3.3 Data Flow Diagrams (DFD)</span><span class="toc-page">25</span>'),
    ('<span class="toc-title">3.4 Database Design</span><span class="toc-page">26</span>', '<span class="toc-title">3.4 Database Design</span><span class="toc-page">25</span>'),
    ('<span class="toc-title">3.5 User Interface (UI/UX) Design</span><span class="toc-page">28</span>', '<span class="toc-title">3.5 User Interface (UI/UX) Design</span><span class="toc-page">28</span>'),
    
    ('<span class="toc-title">CHAPTER 4: IMPLEMENTATION</span><span class="toc-page">31</span>', '<span class="toc-title">CHAPTER 4: IMPLEMENTATION</span><span class="toc-page">30</span>'),
    ('<span class="toc-title">4.0 Introduction</span><span class="toc-page">31</span>', '<span class="toc-title">4.0 Introduction</span><span class="toc-page">30</span>'),
    ('<span class="toc-title">4.1 Cloud Infrastructure Deployment</span><span class="toc-page">31</span>', '<span class="toc-title">4.1 Cloud Infrastructure Deployment</span><span class="toc-page">30</span>'),
    ('<span class="toc-title">4.2 Application Code Development</span><span class="toc-page">33</span>', '<span class="toc-title">4.2 Application Code Development</span><span class="toc-page">32</span>'),
    ('<span class="toc-title">4.3 Chapter Summary</span><span class="toc-page">34</span>', '<span class="toc-title">4.3 Chapter Summary</span><span class="toc-page">33</span>'),
    
    ('<span class="toc-title">CHAPTER 5: TESTING AND VERIFICATION</span><span class="toc-page">35</span>', '<span class="toc-title">CHAPTER 5: TESTING AND VERIFICATION</span><span class="toc-page">34</span>'),
    ('<span class="toc-title">5.0 Introduction</span><span class="toc-page">35</span>', '<span class="toc-title">5.0 Introduction</span><span class="toc-page">34</span>'),
    ('<span class="toc-title">5.1 Cloud High Availability and Failover Testing</span><span class="toc-page">35</span>', '<span class="toc-title">5.1 Cloud High Availability and Failover Testing</span><span class="toc-page">34</span>'),
    ('<span class="toc-title">5.2 Software Functional Testing</span><span class="toc-page">37</span>', '<span class="toc-title">5.2 Software Functional Testing</span><span class="toc-page">36</span>'),
    ('<span class="toc-title">5.3 Usability Testing (User Scenarios)</span><span class="toc-page">39</span>', '<span class="toc-title">5.3 Usability Testing (User Scenarios)</span><span class="toc-page">38</span>'),
    ('<span class="toc-title">5.4 Functional Test Execution Summary Matrix</span><span class="toc-page">40</span>', '<span class="toc-title">5.4 Functional Test Execution Summary Matrix</span><span class="toc-page">39</span>'),
    ('<span class="toc-title">5.5 Chapter Summary</span><span class="toc-page">41</span>', '<span class="toc-title">5.5 Chapter Summary</span><span class="toc-page">40</span>'),
    
    ('<span class="toc-title">CHAPTER 6: CONCLUSION AND FUTURE WORKS</span><span class="toc-page">42</span>', '<span class="toc-title">CHAPTER 6: CONCLUSION AND FUTURE WORKS</span><span class="toc-page">41</span>'),
    ('<span class="toc-title">6.0 Introduction</span><span class="toc-page">42</span>', '<span class="toc-title">6.0 Introduction</span><span class="toc-page">41</span>'),
    ('<span class="toc-title">6.1 Objective Achievement Review</span><span class="toc-page">42</span>', '<span class="toc-title">6.1 Objective Achievement Review</span><span class="toc-page">41</span>'),
    ('<span class="toc-title">6.2 Project Limitations</span><span class="toc-page">42</span>', '<span class="toc-title">6.2 Project Limitations</span><span class="toc-page">41</span>'),
    ('<span class="toc-title">6.3 Future Works and Enhancements</span><span class="toc-page">43</span>', '<span class="toc-title">6.3 Future Works and Enhancements</span><span class="toc-page">42</span>'),
    ('<span class="toc-title">6.4 Conclusion</span><span class="toc-page">43</span>', '<span class="toc-title">6.4 Conclusion</span><span class="toc-page">42</span>'),
    ('<span class="toc-title">REFERENCES</span><span class="toc-page">44</span>', '<span class="toc-title">REFERENCES</span><span class="toc-page">43</span>')
]

for old, new in toc_replacements:
    html = html.replace(old, new)

# List of Figures updates (shift by 1)
fig_replacements = [
    ('Figure 1.4(a): Agile SDLC Workflow for PoliSewa</span><span class="toc-page">16</span>', 'Figure 1.4(a): Agile SDLC Workflow for PoliSewa</span><span class="toc-page">15</span>'),
    ('Figure 1.6(a): Project Development Schedule (Gantt Chart)</span><span class="toc-page">16</span>', 'Figure 1.6(a): Project Development Schedule (Gantt Chart)</span><span class="toc-page">15</span>'),
    ('Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend</span><span class="toc-page">17</span>', 'Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend</span><span class="toc-page">16</span>'),
    ('Figure 1.7(b): Azure Resource-Level Cost Breakdown</span><span class="toc-page">18</span>', 'Figure 1.7(b): Azure Resource-Level Cost Breakdown</span><span class="toc-page">17</span>'),
    ('Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram</span><span class="toc-page">24</span>', 'Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram</span><span class="toc-page">23</span>'),
    ('Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart</span><span class="toc-page">25</span>', 'Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart</span><span class="toc-page">24</span>'),
    ('Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa</span><span class="toc-page">26</span>', 'Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa</span><span class="toc-page">25</span>'),
    ('Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database</span><span class="toc-page">27</span>', 'Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database</span><span class="toc-page">26</span>'),
    ('Figure 3.5.1(a): UI Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout</span><span class="toc-page">29</span>', 'Figure 3.5.1(a): UI Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout</span><span class="toc-page">28</span>'),
    ('Figure 4.1.1(a): Azure Resource Group Overview (\'polisewa\')</span><span class="toc-page">31</span>', 'Figure 4.1.1(a): Azure Resource Group Overview (\'polisewa\')</span><span class="toc-page">30</span>'),
    ('Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status</span><span class="toc-page">31</span>', 'Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status</span><span class="toc-page">30</span>'),
    ('Figure 4.1.2(a): Cloudflare Zero Trust Tunnel Dashboard with Dual Connectors</span><span class="toc-page">32</span>', 'Figure 4.1.2(a): Cloudflare Zero Trust Tunnel Dashboard with Dual Connectors</span><span class="toc-page">31</span>'),
    ('Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules</span><span class="toc-page">32</span>', 'Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules</span><span class="toc-page">31</span>'),
    ('Figure 4.1.4(a): PM2 Process Manager Status on VM1 and VM2 Terminal</span><span class="toc-page">32</span>', 'Figure 4.1.4(a): PM2 Process Manager Status on VM1 and VM2 Terminal</span><span class="toc-page">31</span>'),
    ('Figure 4.2.1(a): Leaflet.js Map Initialization and Boundary GeoJSON Code</span><span class="toc-page">33</span>', 'Figure 4.2.1(a): Leaflet.js Map Initialization and Boundary GeoJSON Code</span><span class="toc-page">32</span>'),
    ('Figure 4.2.2(a): Geodesic Haversine Distance Calculation Code</span><span class="toc-page">33</span>', 'Figure 4.2.2(a): Geodesic Haversine Distance Calculation Code</span><span class="toc-page">32</span>'),
    ('Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Code</span><span class="toc-page">34</span>', 'Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Code</span><span class="toc-page">33</span>'),
    ('Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Code</span><span class="toc-page">34</span>', 'Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Code</span><span class="toc-page">33</span>'),
    ('Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status</span><span class="toc-page">35</span>', 'Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status</span><span class="toc-page">34</span>'),
    ('Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal (\'pm2 stop polisewa\')</span><span class="toc-page">36</span>', 'Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal (\'pm2 stop polisewa\')</span><span class="toc-page">35</span>'),
    ('Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in DevTools</span><span class="toc-page">36</span>', 'Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in DevTools</span><span class="toc-page">35</span>'),
    ('Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check</span><span class="toc-page">36</span>', 'Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check</span><span class="toc-page">35</span>'),
    ('Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers</span><span class="toc-page">37</span>', 'Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers</span><span class="toc-page">36</span>'),
    ('Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300)</span><span class="toc-page">37</span>', 'Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300)</span><span class="toc-page">36</span>'),
    ('Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer</span><span class="toc-page">37</span>', 'Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer</span><span class="toc-page">36</span>'),
    ('Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox</span><span class="toc-page">38</span>', 'Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox</span><span class="toc-page">37</span>'),
    ('Figure 5.2.4(a): Landlord Property Creation Modal with Multi-Photo Upload Preview</span><span class="toc-page">38</span>', 'Figure 5.2.4(a): Landlord Property Creation Modal with Multi-Photo Upload Preview</span><span class="toc-page">37</span>'),
    ('Figure 5.2.5(a): Direct WhatsApp Redirection with Pre-Filled Inquiry Message</span><span class="toc-page">38</span>', 'Figure 5.2.5(a): Direct WhatsApp Redirection with Pre-Filled Inquiry Message</span><span class="toc-page">37</span>'),
    ('Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog</span><span class="toc-page">39</span>', 'Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog</span><span class="toc-page">38</span>'),
    ('Figure 5.3.1(a): Student User Workflow: Room Discovery and Distance Verification</span><span class="toc-page">39</span>', 'Figure 5.3.1(a): Student User Workflow: Room Discovery and Distance Verification</span><span class="toc-page">38</span>'),
    ('Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection</span><span class="toc-page">39</span>', 'Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection</span><span class="toc-page">38</span>'),
    ('Figure 5.3.3(a): Landlord Portal Workflow: Registration, Verification, and Listing</span><span class="toc-page">40</span>', 'Figure 5.3.3(a): Landlord Portal Workflow: Registration, Verification, and Listing</span><span class="toc-page">39</span>')
]

for old, new in fig_replacements:
    html = html.replace(old, new)

# List of Tables updates (shift by 1)
tbl_replacements = [
    ('Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost</span><span class="toc-page">16</span>', 'Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost</span><span class="toc-page">15</span>'),
    ('Table 2.4(a): Comparative Analysis Matrix of Rental Systems</span><span class="toc-page">21</span>', 'Table 2.4(a): Comparative Analysis Matrix of Rental Systems</span><span class="toc-page">20</span>'),
    ('Table 3.1.1(a): Server and Client Hardware Requirements</span><span class="toc-page">23</span>', 'Table 3.1.1(a): Server and Client Hardware Requirements</span><span class="toc-page">22</span>'),
    ('Table 3.1.2(a): Software Stack and Development Technologies</span><span class="toc-page">23</span>', 'Table 3.1.2(a): Software Stack and Development Technologies</span><span class="toc-page">22</span>'),
    ('Table 3.4.2(a): Data Dictionary for \'users\' Table</span><span class="toc-page">27</span>', 'Table 3.4.2(a): Data Dictionary for \'users\' Table</span><span class="toc-page">26</span>'),
    ('Table 3.4.2(b): Data Dictionary for \'properties\' Table</span><span class="toc-page">28</span>', 'Table 3.4.2(b): Data Dictionary for \'properties\' Table</span><span class="toc-page">27</span>'),
    ('Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix</span><span class="toc-page">40</span>', 'Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix</span><span class="toc-page">39</span>'),
    ('Table 6.1(a): Project Objectives Achievement Verification Matrix</span><span class="toc-page">42</span>', 'Table 6.1(a): Project Objectives Achievement Verification Matrix</span><span class="toc-page">41</span>')
]

for old, new in tbl_replacements:
    html = html.replace(old, new)

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

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

subprocess.run(cmd, check=True)
print("Synced all page references to 43-page PDF.")
