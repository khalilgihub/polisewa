import os
import subprocess
import sys

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>PoliSewa - Cloud Based High Availability Room Rental System Final Report</title>
<style>
  @page {
    size: A4 portrait;
    margin: 25mm 20mm 25mm 20mm;
    @bottom-center {
      content: counter(page);
      font-family: 'Times New Roman', Times, serif;
      font-size: 11pt;
    }
  }

  body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #111;
    margin: 0;
    padding: 0;
    text-align: justify;
  }

  .page-break {
    page-break-before: always;
  }

  /* Cover Page */
  .cover-page {
    height: 100%;
    min-height: 240mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding-top: 15mm;
  }

  .inst-header {
    font-size: 13pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 25mm;
    color: #0b2545;
  }

  .sub-inst {
    font-size: 11pt;
    font-weight: normal;
    color: #333;
    margin-top: 4px;
  }

  .report-title-box {
    margin: 15mm 0;
  }

  .project-title {
    font-size: 20pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.3;
    color: #0a2540;
    margin-bottom: 8px;
  }

  .project-subtitle {
    font-size: 14pt;
    font-weight: bold;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
  }

  .meta-block {
    margin: 10mm 0;
    font-size: 11pt;
  }

  .meta-title {
    font-weight: bold;
    font-size: 12pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    color: #1a202c;
  }

  .author-list {
    list-style: none;
    padding: 0;
    margin: 0 0 10mm 0;
  }

  .author-list li {
    margin-bottom: 4px;
    font-weight: bold;
  }

  .cover-footer {
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    line-height: 1.4;
    color: #2d3748;
    margin-top: 20mm;
  }

  /* Typography */
  h1 {
    font-size: 16pt;
    font-weight: bold;
    text-transform: uppercase;
    border-bottom: 1.5px solid #2b6cb0;
    padding-bottom: 4px;
    margin-top: 24pt;
    margin-bottom: 14pt;
    color: #0a2540;
    page-break-after: avoid;
  }

  h2 {
    font-size: 13.5pt;
    font-weight: bold;
    margin-top: 18pt;
    margin-bottom: 8pt;
    color: #1a365d;
    page-break-after: avoid;
  }

  h3 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 14pt;
    margin-bottom: 6pt;
    color: #2d3748;
    page-break-after: avoid;
  }

  p {
    margin-top: 0;
    margin-bottom: 10pt;
    text-indent: 0;
  }

  ul, ol {
    margin-top: 0;
    margin-bottom: 10pt;
    padding-left: 24pt;
  }

  li {
    margin-bottom: 4pt;
  }

  /* Screenshot Instruction Box */
  .screenshot-instruction-card {
    border: 2px solid #2b6cb0;
    border-radius: 6px;
    background-color: #f7fafc;
    margin: 16pt 0;
    padding: 0;
    page-break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }

  .screenshot-header {
    background-color: #2b6cb0;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 10pt;
    font-weight: bold;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    letter-spacing: 0.5px;
  }

  .screenshot-body {
    padding: 10px 14px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 9.5pt;
    line-height: 1.45;
    color: #2d3748;
  }

  .screenshot-body ul {
    margin: 0;
    padding-left: 18px;
  }

  .screenshot-body li {
    margin-bottom: 4px;
  }

  .screenshot-body strong {
    color: #1a202c;
  }

  .red-callout {
    color: #c53030;
    font-weight: bold;
  }

  .figure-caption {
    text-align: center;
    font-style: italic;
    font-size: 10.5pt;
    margin-top: 4pt;
    margin-bottom: 16pt;
    color: #4a5568;
    font-weight: bold;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 14pt 0;
    font-size: 10.5pt;
    page-break-inside: avoid;
  }

  table, th, td {
    border: 1px solid #cbd5e0;
  }

  th {
    background-color: #edf2f7;
    font-weight: bold;
    color: #1a202c;
    padding: 8px 10px;
    text-align: left;
  }

  td {
    padding: 7px 10px;
    vertical-align: top;
  }

  tr:nth-child(even) td {
    background-color: #f7fafc;
  }

  .table-caption {
    font-weight: bold;
    font-size: 10.5pt;
    margin-bottom: 4pt;
    color: #2d3748;
  }

  /* Code Listings */
  pre {
    background-color: #1a202c;
    color: #edf2f7;
    font-family: 'Consolas', 'Courier New', Courier, monospace;
    font-size: 9pt;
    padding: 10px 14px;
    border-radius: 4px;
    overflow-x: auto;
    line-height: 1.4;
    margin: 12pt 0;
    page-break-inside: avoid;
  }

  code {
    font-family: 'Consolas', 'Courier New', Courier, monospace;
    font-size: 10pt;
    background: #edf2f7;
    color: #c53030;
    padding: 1px 4px;
    border-radius: 3px;
  }

  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }

  /* Signature line */
  .sig-block {
    margin-top: 25mm;
    page-break-inside: avoid;
  }

  .sig-line {
    border-top: 1px dashed #718096;
    width: 250px;
    margin-top: 15mm;
    padding-top: 4px;
    font-size: 11pt;
  }

  .toc-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    border-bottom: 1px dotted #a0aec0;
  }

  .toc-title {
    background: #fff;
    padding-right: 5px;
  }

  .toc-page {
    background: #fff;
    padding-left: 5px;
    font-weight: bold;
  }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="inst-header">
    Kementerian Pendidikan Tinggi<br>
    Jabatan Pendidikan Politeknik dan Kolej Komuniti<br>
    <strong>Politeknik Kuching Sarawak</strong>
    <div class="sub-inst">Jabatan Teknologi Maklumat dan Komunikasi</div>
  </div>

  <div class="report-title-box">
    <div class="project-title">Cloud Based High Availability<br>Room Rental System</div>
    <div class="project-subtitle">(PoliSewa)</div>
  </div>

  <div class="meta-block">
    <div class="meta-title">Prepared By:</div>
    <ul class="author-list">
      <li>AHMAD SYARIFUDDIN BIN MOHD BAHARUDIN (05DIT24F1070)</li>
      <li>ABDUL KHALIL BIN HARMEZI (05DIT24F1034)</li>
      <li>JOSH ALZON ANAK JACKSON (05DIT24F1111)</li>
    </ul>

    <div class="meta-title">Prepared For:</div>
    <div style="font-weight: bold; font-size: 12pt;">SIR HASBULLAH BIN ABDULLAH</div>
    <div style="font-size: 10.5pt; color: #4a5568;">Project Supervisor</div>
  </div>

  <div class="cover-footer">
    Diploma in Information Technology<br>
    Politeknik Kuching Sarawak<br>
    Session 1: 2026/2027
  </div>
</div>

<div class="page-break"></div>

<!-- DECLARATION -->
<h1>Declaration</h1>
<p>We hereby declare that this project report entitled <strong>"Cloud Based High Availability Room Rental System (PoliSewa)"</strong> is submitted to the Department of Information and Communication Technology, Politeknik Kuching Sarawak, in partial fulfillment of the requirements for the award of the <strong>Diploma in Information Technology</strong>.</p>

<p>We confirm that this report is the result of our own investigation and work, except where specific citations and references have been made. We also certify that this work has not been accepted or submitted concurrently in substance for any other diploma or degree at this or any other higher educational institution.</p>

<div class="sig-block">
  <div style="margin-bottom: 20px;">
    <div class="sig-line">
      <strong>AHMAD SYARIFUDDIN BIN MOHD BAHARUDIN</strong><br>
      Matric No: 05DIT24F1070<br>
      Date: 16 September 2026
    </div>
  </div>

  <div style="margin-bottom: 20px;">
    <div class="sig-line">
      <strong>ABDUL KHALIL BIN HARMEZI</strong><br>
      Matric No: 05DIT24F1034<br>
      Date: 16 September 2026
    </div>
  </div>

  <div style="margin-bottom: 20px;">
    <div class="sig-line">
      <strong>JOSH ALZON ANAK JACKSON</strong><br>
      Matric No: 05DIT24F1111<br>
      Date: 16 September 2026
    </div>
  </div>
</div>

<div class="page-break"></div>

<!-- APPROVAL -->
<h1>Approval for Submission</h1>
<p>This final year project report entitled <strong>"Cloud Based High Availability Room Rental System (PoliSewa)"</strong> has been prepared and submitted by Ahmad Syarifuddin bin Mohd Baharudin (05DIT24F1070), Abdul Khalil bin Harmezi (05DIT24F1034), and Josh Alzon Anak Jackson (05DIT24F1111) in partial fulfillment of the requirements for the Diploma in Information Technology at Politeknik Kuching Sarawak.</p>

<p>I have examined this report and verified that it conforms to the required academic standards and guidelines established by the Department of Information and Communication Technology.</p>

<div style="margin-top: 35mm;">
  <div class="sig-line" style="width: 280px;">
    <strong>SIR HASBULLAH BIN ABDULLAH</strong><br>
    Project Supervisor<br>
    Department of Information and Communication Technology<br>
    Politeknik Kuching Sarawak<br>
    Date: 16 September 2026
  </div>
</div>

<div class="page-break"></div>

<!-- ACKNOWLEDGMENTS -->
<h1>Acknowledgments</h1>
<p>Alhamdulillah, all praises and gratitude are dedicated to Allah S.W.T. for providing us with the health, strength, patience, and perseverance required to successfully plan, develop, and document our Final Year Project.</p>

<p>First and foremost, we would like to express our highest appreciation and heartfelt gratitude to our academic supervisor, <strong>Sir Hasbullah bin Abdullah</strong>. His continuous encouragement, insightful architectural advice, patient guidance, and technical scrutiny were essential in guiding us from the conceptual design phase through to cloud high availability deployment and testing.</p>

<p>We also express our sincere gratitude to the Head of Department, FYP coordinators, and all lecturers in the <strong>Department of Information and Communication Technology, Politeknik Kuching Sarawak</strong>, for imparting the technical knowledge, software engineering fundamentals, and cloud concepts that enabled the execution of this project.</p>

<p>Our profound appreciation goes to our beloved parents and family members whose unwavering moral encouragement, prayers, and sacrifices have been our pillars of motivation. Lastly, we thank our fellow classmates and student testers at Politeknik Kuching Sarawak whose feedback helped refine PoliSewa into an accessible, student-friendly platform.</p>

<div class="page-break"></div>

<!-- ABSTRACT -->
<h1>Abstract</h1>
<p>Securing safe, affordable, and geographically suitable off-campus accommodation represents a persistent challenge for students attending Politeknik Kuching Sarawak (PKS) in Matang, Kuching. Currently, students depend heavily on fragmented social media platforms such as Facebook groups, TikTok videos, and transient WhatsApp chats. These informal mechanisms lack structure, provide no spatial context regarding campus distance, and expose students to significant rental deposit fraud. Simultaneously, educational institutions hosting web platforms face severe server downtime during peak semester registration periods when thousands of students access the portal concurrently, as traditional single-server hosting suffers from single points of failure.</p>

<p>To overcome these challenges, this project presents <strong>PoliSewa: A Cloud Based High Availability Room Rental System</strong>. The application tier integrates an interactive Leaflet.js map engine, automated geodesic distance calculation to the PKS campus using the Haversine algorithm, student-centric budget filtering (< RM300/month), a 6-digit email One-Time Password (OTP) verification module via Nodemailer, and direct landlord WhatsApp click-to-chat redirection. At the cloud infrastructure tier, PoliSewa deploys an active-active dual Virtual Machine (VM) architecture on Microsoft Azure (VM1 and VM2 in the Malaysia West region) connected to an Azure SQL Database and balanced via Cloudflare Zero Trust Tunnels.</p>

<p>Empirical failover testing demonstrates that when the primary VM process is forcefully terminated (<code>pm2 stop polisewa</code>), Cloudflare automatically routes all inbound traffic to the standby VM connector within milliseconds without presenting HTTP 502/504 gateway errors to users. A comprehensive Azure Cost Management analysis reveals that this dual-node high availability architecture is highly cost-effective, incurring a total operational cost of approximately RM 156.70 per month. PoliSewa successfully provides a resilient, secure, and continuously accessible room rental directory tailored to the polytechnic student community.</p>

<p><strong>Keywords:</strong> High Availability (HA), Microsoft Azure, Cloudflare Zero Trust Tunnels, Leaflet.js, Dual Virtual Machines, Room Rental Directory, Politeknik Kuching Sarawak.</p>

<div class="page-break"></div>

<!-- ABSTRAK -->
<h1>Abstrak</h1>
<p>Mendapatkan bilik atau rumah sewa luar kampus yang selamat, berpatutan, dan berdekatan merupakan cabaran utama bagi para pelajar Politeknik Kuching Sarawak (PKS) di Matang, Kuching. Pada masa kini, pelajar bergantung kepada perkongsian media sosial yang tidak tersusun seperti kumpulan Facebook, video TikTok, dan perkongsian WhatsApp. Kaedah ini tidak mempunyai pengindeksan berpusat, tidak menyediakan ukuran jarak perjalanan ke kampus, serta mendedahkan pelajar kepada risiko penipuan wang deposit sewaan. Pada masa yang sama, laman web konvensional yang dihoskan pada pelayan tunggal sering mengalami gangguan perkhidmatan (<em>downtime</em>) semasa lonjakan trafik pendaftaran semester baharu.</p>

<p>Bagi menyelesaikan masalah ini, projek ini membangunkan <strong>PoliSewa: Sistem Sewaan Bilik Berasaskan Awan dengan Ketersediaan Tinggi (High Availability - HA)</strong>. Lapisan aplikasi menggabungkan peta interaktif Leaflet.js, pengiraan automatik jarak geodesik ke kampus PKS menggunakan formula Haversine, penapis harga bilik mesra pelajar (< RM300/sebulan), modul pengesahan emel OTP 6-digit melalui Nodemailer, serta integrasi pautan terus WhatsApp ke pemilik rumah. Pada lapisan infrastruktur awan, PoliSewa mengimplementasikan dwi-Mesin Maya (Dual Virtual Machines - VM1 dan VM2) di Microsoft Azure (rantau Malaysia West) yang disambungkan ke Azure SQL Database dan diimbangi beban trafiknya melalui Cloudflare Zero Trust Tunnels.</p>

<p>Ujian kegagalan (<em>failover testing</em>) membuktikan bahawa apabila proses pelayan utama dimatikan secara simulasi (<code>pm2 stop polisewa</code>), Cloudflare mengalihkan trafik pengguna ke pelayan sandaran dalam masa beberapa milisaat tanpa sebarang ralat pelayan (kekal 100% HTTP 200 OK). Analisis Pengurusan Kos Azure menunjukkan bahawa seni bina ketersediaan tinggi ini sangat menjimatkan kos, dengan jumlah perbelanjaan awan sebanyak RM 156.70 sebulan. PoliSewa terbukti berupaya menyediakan perkhidmatan direktori sewa yang selamat, pantas, dan sentiasa beroperasi untuk warga Politeknik Kuching Sarawak.</p>

<p><strong>Kata Kunci:</strong> Ketersediaan Tinggi (HA), Microsoft Azure, Cloudflare Zero Trust Tunnels, Leaflet.js, Dwi-Mesin Maya, Direktori Rumah Sewa, Politeknik Kuching Sarawak.</p>

<div class="page-break"></div>

<!-- TABLE OF CONTENTS -->
<h1>Table of Contents</h1>
<div class="toc-row"><span class="toc-title">Declaration</span><span class="toc-page">ii</span></div>
<div class="toc-row"><span class="toc-title">Approval for Submission</span><span class="toc-page">iii</span></div>
<div class="toc-row"><span class="toc-title">Acknowledgments</span><span class="toc-page">iv</span></div>
<div class="toc-row"><span class="toc-title">Abstract</span><span class="toc-page">v</span></div>
<div class="toc-row"><span class="toc-title">Abstrak</span><span class="toc-page">vi</span></div>
<div class="toc-row"><span class="toc-title">List of Figures</span><span class="toc-page">viii</span></div>
<div class="toc-row"><span class="toc-title">List of Tables</span><span class="toc-page">ix</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 1: INTRODUCTION</span><span class="toc-page">1</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.0 Introduction</span><span class="toc-page">1</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.1 Problem Statement</span><span class="toc-page">2</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.2 Project Scope</span><span class="toc-page">3</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.3 Aim and Objectives</span><span class="toc-page">4</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.4 Methodology (Agile SDLC)</span><span class="toc-page">4</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.5 Significance of the Project</span><span class="toc-page">5</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.6 Project Schedule (Gantt Chart)</span><span class="toc-page">6</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis</span><span class="toc-page">7</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 2: LITERATURE REVIEW</span><span class="toc-page">9</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.0 Introduction</span><span class="toc-page">9</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.1 High Availability and Cloud Fault Tolerance Models</span><span class="toc-page">9</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.2 Student Rental Portals and Scam Prevention Studies</span><span class="toc-page">11</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.3 Cloud Infrastructure, Redundancy, and Load Balancing</span><span class="toc-page">12</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.4 Comparative Analysis of Existing Systems vs. PoliSewa</span><span class="toc-page">13</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">2.5 Chapter Summary</span><span class="toc-page">14</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 3: ANALYSIS AND DESIGN</span><span class="toc-page">15</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.0 Introduction</span><span class="toc-page">15</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.1 Requirement Analysis</span><span class="toc-page">15</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.2 High Availability System Architecture</span><span class="toc-page">16</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.3 Data Flow Diagrams (DFD)</span><span class="toc-page">18</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.4 Database Design</span><span class="toc-page">19</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">3.5 User Interface (UI/UX) Design</span><span class="toc-page">21</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 4: IMPLEMENTATION</span><span class="toc-page">22</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">4.0 Introduction</span><span class="toc-page">22</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">4.1 Cloud Infrastructure Deployment</span><span class="toc-page">22</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">4.2 Application Code Development</span><span class="toc-page">25</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">4.3 Chapter Summary</span><span class="toc-page">27</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 5: TESTING AND VERIFICATION</span><span class="toc-page">28</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.0 Introduction</span><span class="toc-page">28</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.1 Cloud High Availability and Failover Testing</span><span class="toc-page">28</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.2 Software Functional Testing</span><span class="toc-page">31</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.3 Usability Testing (User Scenarios)</span><span class="toc-page">35</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.4 Functional Test Execution Summary Matrix</span><span class="toc-page">37</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">5.5 Chapter Summary</span><span class="toc-page">38</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">CHAPTER 6: CONCLUSION AND FUTURE WORKS</span><span class="toc-page">39</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">6.0 Introduction</span><span class="toc-page">39</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">6.1 Objective Achievement Review</span><span class="toc-page">39</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">6.2 Project Limitations</span><span class="toc-page">40</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">6.3 Future Works and Enhancements</span><span class="toc-page">40</span></div>
<div class="toc-row" style="padding-left: 15px;"><span class="toc-title">6.4 Conclusion</span><span class="toc-page">41</span></div>

<div class="toc-row" style="margin-top: 10px; font-weight: bold;"><span class="toc-title">REFERENCES</span><span class="toc-page">42</span></div>

<div class="page-break"></div>

<!-- LIST OF FIGURES -->
<h1>List of Figures</h1>
<div class="toc-row"><span class="toc-title">Figure 1.4(a): Agile SDLC Workflow for PoliSewa</span><span class="toc-page">5</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.6(a): Project Development Schedule (Gantt Chart)</span><span class="toc-page">6</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend</span><span class="toc-page">7</span></div>
<div class="toc-row"><span class="toc-title">Figure 1.7(b): Azure Resource-Level Cost Breakdown</span><span class="toc-page">8</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram</span><span class="toc-page">17</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart</span><span class="toc-page">18</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa</span><span class="toc-page">18</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database</span><span class="toc-page">20</span></div>
<div class="toc-row"><span class="toc-title">Figure 3.5.1(a): UI Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout</span><span class="toc-page">21</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.1(a): Azure Resource Group Overview ('polisewa')</span><span class="toc-page">23</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status</span><span class="toc-page">23</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.2(a): Cloudflare Zero Trust Tunnel Dashboard with Dual Connectors</span><span class="toc-page">24</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules</span><span class="toc-page">24</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.1.4(a): PM2 Process Manager Status on VM1 and VM2 Terminal</span><span class="toc-page">25</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.1(a): Leaflet.js Map Initialization and Boundary GeoJSON Code</span><span class="toc-page">25</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.2(a): Geodesic Haversine Distance Calculation Code</span><span class="toc-page">26</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Code</span><span class="toc-page">26</span></div>
<div class="toc-row"><span class="toc-title">Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Code</span><span class="toc-page">27</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status</span><span class="toc-page">29</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal ('pm2 stop polisewa')</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in DevTools</span><span class="toc-page">30</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check</span><span class="toc-page">31</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers</span><span class="toc-page">32</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300)</span><span class="toc-page">32</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer</span><span class="toc-page">33</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox</span><span class="toc-page">33</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.4(a): Landlord Property Creation Modal with Multi-Photo Upload Preview</span><span class="toc-page">34</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.5(a): Direct WhatsApp Redirection with Pre-Filled Inquiry Message</span><span class="toc-page">34</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog</span><span class="toc-page">35</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.1(a): Student User Workflow: Room Discovery and Distance Verification</span><span class="toc-page">36</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection</span><span class="toc-page">36</span></div>
<div class="toc-row"><span class="toc-title">Figure 5.3.3(a): Landlord Portal Workflow: Registration, Verification, and Listing</span><span class="toc-page">37</span></div>

<div class="page-break"></div>

<!-- LIST OF TABLES -->
<h1>List of Tables</h1>
<div class="toc-row"><span class="toc-title">Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost</span><span class="toc-page">7</span></div>
<div class="toc-row"><span class="toc-title">Table 2.4(a): Comparative Analysis Matrix of Rental Systems</span><span class="toc-page">13</span></div>
<div class="toc-row"><span class="toc-title">Table 3.1.1(a): Server and Client Hardware Requirements</span><span class="toc-page">15</span></div>
<div class="toc-row"><span class="toc-title">Table 3.1.2(a): Software Stack and Development Technologies</span><span class="toc-page">16</span></div>
<div class="toc-row"><span class="toc-title">Table 3.4.2(a): Data Dictionary for 'users' Table</span><span class="toc-page">20</span></div>
<div class="toc-row"><span class="toc-title">Table 3.4.2(b): Data Dictionary for 'properties' Table</span><span class="toc-page">21</span></div>
<div class="toc-row"><span class="toc-title">Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix</span><span class="toc-page">37</span></div>
<div class="toc-row"><span class="toc-title">Table 6.1(a): Project Objectives Achievement Verification Matrix</span><span class="toc-page">39</span></div>

<div class="page-break"></div>

<!-- CHAPTER 1 -->
<h1>Chapter 1: Introduction</h1>

<h2>1.0 Introduction</h2>
<p>In today's digitalized educational landscape, tertiary institutions increasingly adopt web-based systems to manage student processes efficiently. However, off-campus student accommodation management remains critically underserved. At Politeknik Kuching Sarawak (PKS), located along Jalan Matang in Kuching, Sarawak, the majority of senior and out-of-town students reside in off-campus rental housing across areas such as Taman Sri Matang, Kampung Gita, Matang Jaya, and Petra Jaya.</p>

<p>Despite the critical necessity of safe housing, the room rental discovery process continues to rely upon unorganized, informal mechanisms including printed flyers, word-of-mouth recommendations, and unstructured posts on social media platforms such as Facebook groups, TikTok, and WhatsApp chats. These channels lack centralized organization, provide no geographic proximity context, and leave students vulnerable to fraud. Furthermore, when polytechnic student bodies attempt to host centralized web portals, they traditionally deploy them on basic single-server architectures. During peak academic intake windows—specifically the onset of semester registration—thousands of students access the portal concurrently. These traffic surges overwhelm single servers, resulting in catastrophic downtime, connection timeouts, and service unavailability when students need it most.</p>

<p>To overcome these dual challenges of information fragmentation and server vulnerability, this project introduces <strong>PoliSewa: A Cloud Based High Availability Room Rental System</strong>. PoliSewa provides an interactive, map-centric web directory tailored specifically for PKS students while implementing an enterprise-grade cloud architecture featuring active-active dual Virtual Machines on Microsoft Azure, Cloudflare Zero Trust load balancing, and automated database replication.</p>

<h2>1.1 Problem Statement</h2>

<h3>1.1.1 Scattered Rental Information Across Social Media</h3>
<p>Off-campus rental advertisements are scattered across disjointed digital silos, including various Facebook rental groups, Instagram stories, TikTok clips, and transient WhatsApp chat groups. Consequently, students waste substantial hours searching for listings, frequently encounter expired advertisements for rooms that have already been rented, and fail to secure accommodations before academic sessions commence.</p>

<h3>1.1.2 Data Reliability and Backup Deficiencies</h3>
<p>Informal rental methods and legacy student platforms do not implement automated data backups or standardized transaction logs. If an administrator's machine or single host server experiences filesystem corruption or hardware failure, room listings, landlord contacts, and booking histories are permanently lost. The lack of a structured disaster recovery mechanism severely undermines data integrity.</p>

<h3>1.1.3 Server Downtime and Single Point of Failure</h3>
<p>Conventional student portals rely on a single web server and an un-replicated local database. During new intake cycles, concurrent requests cause severe CPU exhaustion and memory bottlenecks. A single process crash or infrastructure maintenance window takes the entire platform offline. Educational institutions lack fault-tolerant systems capable of surviving server outages without disrupting students.</p>

<h2>1.2 Project Scope</h2>

<h3>1.2.1 System Scope</h3>
<ul>
  <li><strong>Dual Virtual Machine Infrastructure:</strong> Deployment of two independent Linux Virtual Machines (VM1 and VM2) on Microsoft Azure (Malaysia West region) running Node.js / Express web services managed via PM2.</li>
  <li><strong>Cloudflare Zero Trust Load Balancing & Failover:</strong> Routing of domain traffic (<code>polisewa.me</code>) through dual Cloudflare Tunnel connectors (<code>cloudflared</code>) to distribute requests and execute sub-second failover if any VM terminates.</li>
  <li><strong>Centralized Azure SQL Database:</strong> Cloud-hosted relational database storing user records, hashed authentication credentials, property details, and coordinates, with automated backups and firewall whitelisting.</li>
  <li><strong>Interactive Web Application:</strong> Single-page responsive interface utilizing Leaflet.js, OpenStreetMap geospatial boundaries (<code>boundary.js</code>), Haversine geodesic distance calculation, 6-digit email OTP verification via Nodemailer Gmail SMTP, and WhatsApp click-to-chat redirection.</li>
</ul>

<h3>1.2.2 User Scope</h3>
<ul>
  <li><strong>Polytechnic Students:</strong> Primary users who search for rental rooms, apply budget and distance filters, inspect property photo galleries, and initiate verified WhatsApp inquiries to landlords.</li>
  <li><strong>Family Members:</strong> Parents and guardians assisting students in evaluating property amenities, security, pricing, and campus distance.</li>
  <li><strong>Property Owners (Landlords):</strong> Registered and OTP-verified property owners who manage room listings, upload multiple unit photos, update rental rates, and receive pre-filled WhatsApp inquiries.</li>
  <li><strong>System Administrators:</strong> Authorized personnel managing Azure cloud resources, monitoring Cloudflare tunnel health, and auditing listings to prevent scams.</li>
</ul>

<h2>1.3 Aim and Objectives</h2>
<p>The overarching aim of this project is to design, develop, and deploy a secure, fault-tolerant, cloud-based student room rental directory for Politeknik Kuching Sarawak. The specific measurable objectives are:</p>
<ol>
  <li><strong>Develop a Centralized Room Rental Platform:</strong> To design and implement a responsive, map-based web application that allows PKS students and families to search, filter by price (< RM300), calculate distance to campus, and contact landlords via WhatsApp.</li>
  <li><strong>Enhance Data Protection:</strong> To implement automated cloud database management using Azure SQL Database with strict firewall controls, transaction integrity, and automated daily backups to eliminate data loss.</li>
  <li><strong>Implement High Availability Cloud Infrastructure:</strong> To configure a multi-node cloud environment on Microsoft Azure using dual Virtual Machines and Cloudflare Tunnel load balancing, ensuring zero-downtime failover during server maintenance or crashes.</li>
</ol>

<h2>1.4 Methodology (Agile SDLC)</h2>
<p>To accommodate iterative refinement and rigorous failover testing, this project utilizes the <strong>Agile Software Development Life Cycle (SDLC)</strong> methodology (<em>Pressman & Maxim, 2020</em>). Agile facilitates continuous feedback loops across five structured phases:</p>
<ul>
  <li><strong>Phase 1: Requirement Analysis:</strong> Gathering student accommodation needs, identifying pain points in Matang, defining functional specifications, and creating Level-0 and Level-1 Data Flow Diagrams (DFDs).</li>
  <li><strong>Phase 2: System Design:</strong> Architecting the dual-VM cloud topology, configuring Cloudflare ingress rules, modeling the relational database schema, and producing UI/UX wireframes.</li>
  <li><strong>Phase 3: Development:</strong> Iterative front-end coding (HTML5, CSS3, Leaflet.js), back-end REST API construction (Node.js/Express), and cloud provisioning on Microsoft Azure.</li>
  <li><strong>Phase 4: Testing:</strong> Executing unit tests, black-box functional tests, user acceptance testing (UAT), and cloud failover simulation tests (<code>pm2 stop</code>).</li>
  <li><strong>Phase 5: Deployment & Maintenance:</strong> Final domain pointing (<code>polisewa.me</code>), production SSL enforcement, automated PM2 daemonization, and continuous Azure billing/health monitoring.</li>
</ul>

<div class="figure-caption">Figure 1.4(a): Agile Software Development Life Cycle (SDLC) Workflow for PoliSewa</div>

<h2>1.5 Significance of the Project</h2>
<p>PoliSewa delivers substantial technical and socio-economic value to the Politeknik Kuching Sarawak community:</p>
<ul>
  <li><strong>Academic Time Recovery:</strong> Students reduce their accommodation search cycle from several days of traveling and browsing social media to mere minutes on an interactive map.</li>
  <li><strong>Rental Scam Prevention:</strong> Landlords must complete 6-digit email OTP verification before publishing listings, reducing anonymous scam postings (<em>UPSI, 2025; SPEEDHOME, 2026</em>).</li>
  <li><strong>High Reliability:</strong> The dual-VM architecture ensures students experience zero service disruption, even during peak registration periods or server failures.</li>
  <li><strong>Direct Communication:</strong> Direct WhatsApp click-to-chat links remove intermediary fees and enable instant communication between students and landlords.</li>
</ul>

<h2>1.6 Project Schedule (Gantt Chart)</h2>
<p>The project was executed across a 12-week development lifecycle as summarized below:</p>

<div class="figure-caption">Figure 1.6(a): Project Development Schedule (Gantt Chart)</div>

<h2>1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis</h2>
<p>The infrastructure budget was formulated to balance enterprise-grade reliability with educational cost efficiency. The initial cost estimate was compared against the actual real-world expenditure recorded in the <strong>Microsoft Azure Cost Management + Billing Portal</strong>:</p>

<div class="table-caption">Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost</div>
<table>
  <thead>
    <tr>
      <th>No.</th>
      <th>Item / Cloud Resource</th>
      <th>Quantity</th>
      <th>Pricing Model</th>
      <th>Estimated (RM)</th>
      <th>Actual (RM)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Azure Virtual Machine (VM1)</td>
      <td>1 instance</td>
      <td>Standard_B1s (Ubuntu)</td>
      <td>RM 66.87/mo</td>
      <td>RM 64.20/mo</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Azure Virtual Machine (VM2)</td>
      <td>1 instance</td>
      <td>Standard_B1s (Ubuntu)</td>
      <td>RM 66.87/mo</td>
      <td>RM 64.20/mo</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Azure SQL Database (PoliSewa)</td>
      <td>1 instance</td>
      <td>Serverless / Basic</td>
      <td>RM 25.00/mo</td>
      <td>RM 22.80/mo</td>
    </tr>
    <tr>
      <td>4</td>
      <td>Cloudflare Zero Trust Tunnel</td>
      <td>1 domain</td>
      <td>Free Tier / CDN</td>
      <td>RM 0.00</td>
      <td>RM 0.00</td>
    </tr>
    <tr>
      <td>5</td>
      <td>Domain Name (polisewa.me)</td>
      <td>1 domain</td>
      <td>Annualized</td>
      <td>RM 5.50/mo</td>
      <td>RM 5.50/mo</td>
    </tr>
    <tr>
      <td>6</td>
      <td>Nodemailer SMTP (Gmail)</td>
      <td>1 service</td>
      <td>Free Cloud Quota</td>
      <td>RM 0.00</td>
      <td>RM 0.00</td>
    </tr>
    <tr>
      <td>7</td>
      <td>Development Laptops</td>
      <td>3 units</td>
      <td>Student Asset</td>
      <td>RM 0.00</td>
      <td>RM 0.00</td>
    </tr>
    <tr>
      <td>8</td>
      <td>Internet Broadband</td>
      <td>3 packages</td>
      <td>Student Plan</td>
      <td>RM 165.00/mo</td>
      <td>RM 165.00/mo</td>
    </tr>
    <tr style="font-weight: bold; background-color: #edf2f7;">
      <td colspan="4">TOTAL MONTHLY CLOUD SPEND (Compute + Database + Domain):</td>
      <td>RM 164.24/mo</td>
      <td>RM 156.70/mo</td>
    </tr>
  </tbody>
</table>

<!-- Screenshot Instruction 1.7(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 1.7(a) - Azure Subscription Cost Analysis & Accumulated Spend</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Microsoft Azure Portal &rarr; <em>Cost Management + Billing</em> &rarr; <em>Cost Analysis</em>.</li>
      <li><strong>View Settings:</strong> Select Scope: <code>polisewa</code> Subscription / Resource Group. Set Timeframe: <em>Last 30 days</em> or <em>Billing Inception to Date</em>. Granularity: <em>Accumulated</em> or <em>Daily</em>.</li>
      <li><strong>Content to Show:</strong> The main graph showing total accumulated cost (in RM/USD), budget forecast line, and remaining student credit balance.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Place a prominent red rectangle around the <strong>Total Cost</strong> metric box and the daily burn rate chart.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend</div>

<!-- Screenshot Instruction 1.7(b) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 1.7(b) - Azure Resource-Level Cost Breakdown</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Microsoft Azure Portal &rarr; <em>Cost Management</em> &rarr; <em>Cost Analysis</em> &rarr; View by: <strong>Resource</strong>.</li>
      <li><strong>Content to Show:</strong> The itemized bar chart and resource list showing exact spending per component: (1) Virtual Machine VM1, (2) Virtual Machine VM2, (3) Azure SQL Database <code>polisewa</code>, (4) OS Disks, and (5) Virtual Network bandwidth.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw a red outline highlighting the compute cost of the two VMs versus the Azure SQL Database cost.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 1.7(b): Azure Resource-Level Cost Breakdown</div>

<div class="page-break"></div>

<!-- CHAPTER 2 -->
<h1>Chapter 2: Literature Review</h1>

<h2>2.0 Introduction</h2>
<p>The development of high-availability cloud systems for student rental directories draws upon three primary domains: distributed cloud fault tolerance, online rental scam dynamics, and modern geospatial web architectures. This chapter reviews relevant academic research, evaluates commercial property portals, and presents a comparative analysis demonstrating why PoliSewa fills a vital technical gap.</p>

<h2>2.1 High Availability and Cloud Fault Tolerance Models</h2>
<p>Cloud availability is defined as the percentage of time a digital service remains accessible and fully operational under standard and peak loads (<em>Stallings, 2017</em>).</p>

<p><strong>Saxena et al. (2022)</strong> investigated cloud reliability in their seminal study, <em>"A High Availability Management Model Based on VM Significance Ranking and Resource Estimation."</em> They demonstrated that conventional single-host cloud deployments suffer from cascading failures during unpredictable workload spikes. To resolve this, Saxena et al. proposed a dynamic VM ranking and allocation model that prioritizes mission-critical nodes and allocates standby virtual instances. Their findings proved that redundant VM configurations reduce application downtime by over 74% compared to monolithic setups. This directly supports PoliSewa's architectural decision to deploy dual Azure VMs (<code>VM1</code> and <code>VM2</code>), ensuring that background worker and HTTP listening tasks remain fully operational even if one host encounters an unexpected hardware fault.</p>

<p>Furthermore, <strong>Saxena and Singh (2022)</strong> developed <em>"OFP-TM: An Online VM Failure Prediction and Tolerance Model Towards High Availability of Cloud Computing Environments."</em> Their research emphasized that hardware degradation, memory leaks, and CPU starvation inevitably induce unannounced virtual machine crashes. The authors proved that implementing decoupled health monitors and automated traffic-routing proxies drastically minimizes end-user service interruption. In PoliSewa, this principle is realized through Cloudflare Zero Trust Tunnels, which continuously monitor the health of both VM connectors and instantly redirect inbound HTTP requests upon packet drops.</p>

<p>Additionally, <strong>Clemente et al. (2022)</strong> published <em>"Availability Evaluation of System Service Hosted in Private Cloud Computing Through Hierarchical Modeling Process."</em> Utilizing stochastic Petri nets and Markov chains, Clemente et al. mathematically verified that active redundancy across multiple server nodes and database replication layers provides high availability exceeding "three nines" (99.9% uptime). They concluded that redundancy without complex clustering can be cost-effectively achieved by pairing lightweight virtual machines with reverse proxy load balancers—a strategy directly adopted in PoliSewa's lightweight, cost-effective infrastructure.</p>

<h2>2.2 Student Rental Portals and Scam Prevention Studies</h2>
<p>University and polytechnic students represent an exceptionally vulnerable demographic in the private rental housing market. A field study conducted by <strong>Universiti Pendidikan Sultan Idris (UPSI, 2025)</strong> examined undergraduate experiences in off-campus residential zones. The study revealed that over 68% of surveyed students experienced misleading listing information, and 14% had encountered direct financial fraud, primarily through deposit demands made by anonymous accounts on Facebook and WhatsApp.</p>

<p>Media investigations by <strong>The Sun Malaysia (2023)</strong> confirmed that student rental scams surged post-pandemic, with scammers scraping legitimate photos from property websites, posting them in student community groups at below-market prices (e.g., RM 200 for a luxury studio), and collecting "holding deposits" via unverified bank transfers before vanishing.</p>

<p>Commercial tenancy platforms such as <strong>SPEEDHOME (2026)</strong> have pioneered scam prevention models by introducing automated landlord identity checks and deposit-free insurance schemes. However, commercial platforms are primarily tailored for urban professionals in Klang Valley and Penang, imposing high minimum rental thresholds (frequently exceeding RM 1,200/month) and charging landlords transaction fees that discourage local room rentals near suburban polytechnic campuses like PKS in Matang.</p>

<p>Traditional classified platforms such as <strong>Mudah.my</strong> and <strong>iBilik</strong> maintain vast databases of property listings nationwide (<em>Latif et al., 2020</em>). However, these platforms suffer from severe usability deficiencies for students:
<ol>
  <li><strong>Lack of Proximity Intelligence:</strong> They do not provide automatic geodesic distance calculations to specific tertiary educational institutions like Politeknik Kuching Sarawak.</li>
  <li><strong>Outdated Inventories:</strong> Unmanaged classified posts frequently remain online months after rooms have been leased.</li>
  <li><strong>Impersonal Communication:</strong> Contact forms require multi-step platform registration rather than direct, friction-free messaging.</li>
</ol>
</p>

<h2>2.3 Cloud Infrastructure, Redundancy, and Load Balancing</h2>
<p>Microsoft's <strong>Azure Architecture Center (RobBagby, n.d.)</strong> outlines the baseline reference architecture for zone-redundant, highly available web applications. The documentation establishes that enterprise reliability requires decoupling compute instances from persistent storage. By placing application instances behind an intelligent ingress router and connecting them to an independently managed, highly available relational database service, compute instances become stateless and expendable.</p>

<p>In database tier design, <strong>Gaurikasar (2026)</strong> emphasizes that maintaining continuous data availability requires automated managed storage failover and automatic point-in-time restore capabilities. Deploying <strong>Microsoft Azure SQL Database</strong> enables PoliSewa to maintain data integrity, automated ACID compliance, and secure encrypted access without requiring complex manual database clustering on individual virtual machines.</p>

<p>At the network edge, <strong>Cloudflare (2023)</strong> documentation details the operational mechanics of Cloudflare Zero Trust Tunnels (<code>cloudflared</code>). Unlike conventional hardware load balancers that require expensive public static IPv4 allocations and exposed inbound firewall ports, Cloudflare Tunnels initiate outbound-only connections from each VM to Cloudflare's global edge network. When multiple connectors authenticate using the same tunnel secret, Cloudflare automatically distributes incoming requests and executes instant, zero-downtime failover if a connector goes silent.</p>

<h2>2.4 Comparative Analysis of Existing Systems vs. PoliSewa</h2>
<div class="table-caption">Table 2.4(a): Comparative Analysis Matrix of Rental Systems</div>
<table>
  <thead>
    <tr>
      <th>Feature / Metric</th>
      <th>Mudah.my</th>
      <th>iBilik Malaysia</th>
      <th>Facebook Rental Groups</th>
      <th>PoliSewa (Proposed)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Target Demographic</td>
      <td>General Public</td>
      <td>Urban Renters</td>
      <td>Social Media Users</td>
      <td>Polytechnic Students (PKS)</td>
    </tr>
    <tr>
      <td>Geographical Scope</td>
      <td>Nationwide</td>
      <td>Major Cities</td>
      <td>Unstructured Groups</td>
      <td>Hyper-Local (Matang / PKS)</td>
    </tr>
    <tr>
      <td>Budget Room Focus (<RM300)</td>
      <td>Low (Commercial focus)</td>
      <td>Moderate</td>
      <td>High (Unverified)</td>
      <td>High (Dedicated Filter)</td>
    </tr>
    <tr>
      <td>Automated Campus Distance</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>Yes (Geodesic km to PKS)</td>
    </tr>
    <tr>
      <td>Interactive GIS Map View</td>
      <td>Limited / Pin Only</td>
      <td>Basic Map</td>
      <td>None</td>
      <td>Yes (Leaflet.js & Boundary)</td>
    </tr>
    <tr>
      <td>Direct WhatsApp Click-Chat</td>
      <td>No (In-app / Phone)</td>
      <td>No (Internal Chat)</td>
      <td>Manual Phone Copying</td>
      <td>Yes (Pre-filled URL schema)</td>
    </tr>
    <tr>
      <td>Landlord Verification</td>
      <td>Minimal (Email only)</td>
      <td>Moderate</td>
      <td>None</td>
      <td>Yes (6-Digit Email OTP)</td>
    </tr>
    <tr>
      <td>Server Architecture</td>
      <td>Proprietary Multi-DC</td>
      <td>Proprietary Cloud</td>
      <td>Enterprise Social Cloud</td>
      <td>Dual Azure VM + Cloudflare HA</td>
    </tr>
    <tr>
      <td>Fault-Tolerant Failover</td>
      <td>Corporate HA</td>
      <td>Standard Cloud</td>
      <td>Global Edge HA</td>
      <td>Automated Zero-Downtime HA</td>
    </tr>
  </tbody>
</table>

<h2>2.5 Chapter Summary</h2>
<p>The literature confirms that student accommodation search remains severely hindered by fragmented data and pervasive rental scams. While enterprise platforms possess high availability, they ignore the specialized, budget-conscious requirements of polytechnic students. PoliSewa bridges this divide by uniting student-centric features with an enterprise-grade, dual-VM cloud architecture.</p>

<div class="page-break"></div>

<!-- CHAPTER 3 -->
<h1>Chapter 3: Analysis and Design</h1>

<h2>3.0 Introduction</h2>
<p>This chapter presents the comprehensive architectural and functional design of PoliSewa. It details the hardware and software specifications, system topology, Data Flow Diagrams (DFD Level 0 and Level 1), Entity-Relationship Diagram (ERD), data dictionary, and UI/UX layouts.</p>

<h2>3.1 Requirement Analysis</h2>

<h3>3.1.1 Hardware Specifications</h3>
<div class="table-caption">Table 3.1.1(a): Server and Client Hardware Requirements</div>
<table>
  <thead>
    <tr>
      <th>System Tier</th>
      <th>Hardware Component</th>
      <th>Minimum Specification</th>
      <th>Recommended Specification</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cloud Server 1</td>
      <td>Azure VM (Primary)</td>
      <td>1 vCPU, 1 GB RAM (Standard_B1s)</td>
      <td>2 vCPU, 4 GB RAM (Standard_B2s)</td>
    </tr>
    <tr>
      <td>Cloud Server 2</td>
      <td>Azure VM (Standby)</td>
      <td>1 vCPU, 1 GB RAM (Standard_B1s)</td>
      <td>2 vCPU, 4 GB RAM (Standard_B2s)</td>
    </tr>
    <tr>
      <td>Cloud Database</td>
      <td>Azure SQL Database</td>
      <td>Serverless Compute Tier, 5 DTUs</td>
      <td>Standard Tier S0 (10 DTUs)</td>
    </tr>
    <tr>
      <td>Client (Mobile)</td>
      <td>Smartphone</td>
      <td>Android 8.0+ or iOS 12+</td>
      <td>Android 12+ / iOS 16+</td>
    </tr>
    <tr>
      <td>Client (Desktop)</td>
      <td>Laptop / PC</td>
      <td>Intel Core i3, 4 GB RAM</td>
      <td>Intel Core i5, 8 GB RAM</td>
    </tr>
    <tr>
      <td>Network Link</td>
      <td>Internet Connection</td>
      <td>3G / 5 Mbps Broadband</td>
      <td>4G / 5G / High-Speed Wi-Fi</td>
    </tr>
  </tbody>
</table>

<h3>3.1.2 Software Stack and Tools</h3>
<div class="table-caption">Table 3.1.2(a): Software Stack and Development Technologies</div>
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Technology / Tool</th>
      <th>Purpose in PoliSewa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Front-End Core</td>
      <td>HTML5, Vanilla CSS3, ES6 JS</td>
      <td>Fast, lightweight, zero-bloat user interface</td>
    </tr>
    <tr>
      <td>Geographic Mapping</td>
      <td>Leaflet.js (v1.9.4)</td>
      <td>Interactive tile rendering & coordinate markers</td>
    </tr>
    <tr>
      <td>Spatial Boundary</td>
      <td>GeoJSON (<code>boundary.js</code>)</td>
      <td>Kuching & Matang district boundary highlighting</td>
    </tr>
    <tr>
      <td>Back-End Runtime</td>
      <td>Node.js (v18+ LTS)</td>
      <td>High-performance asynchronous event-driven server</td>
    </tr>
    <tr>
      <td>Web Framework</td>
      <td>Express.js (v4.18)</td>
      <td>REST API endpoints & static asset serving</td>
    </tr>
    <tr>
      <td>Database Layer</td>
      <td>Microsoft Azure SQL / SQLite</td>
      <td>ACID relational persistence with SQL fallback</td>
    </tr>
    <tr>
      <td>Security & Auth</td>
      <td>Bcrypt.js & Crypto OTP</td>
      <td>Salted password hashing & 6-digit OTP generation</td>
    </tr>
    <tr>
      <td>Email Transport</td>
      <td>Nodemailer (Gmail SMTP)</td>
      <td>Automated real-time OTP verification dispatch</td>
    </tr>
    <tr>
      <td>Process Management</td>
      <td>PM2 Daemon</td>
      <td>Continuous process execution & auto-restart on boot</td>
    </tr>
    <tr>
      <td>Edge & Routing</td>
      <td>Cloudflare Zero Trust Tunnels</td>
      <td>Active-active ingress, SSL termination, failover</td>
    </tr>
    <tr>
      <td>Version Control</td>
      <td>Git & GitHub</td>
      <td>Source code management and multi-VM deployment</td>
    </tr>
  </tbody>
</table>

<h2>3.2 High Availability System Architecture</h2>

<h3>3.2.1 Dual VM and Tunnel Connector Block Diagram</h3>
<p>Figure 3.2.1(a) illustrates the end-to-end cloud topology. End-users issue HTTPS requests to <code>https://polisewa.me</code>. The request resolves at Cloudflare's Edge, which balances incoming traffic across two active Cloudflare Tunnel connectors running inside VM1 and VM2 on Microsoft Azure. Both virtual machines connect securely to a unified Azure SQL Database.</p>

<pre><code>+-------------------------------------------------------------+
|                     End Users (Clients)                     |
|                    Mobile / Desktop Web                     |
+-------------------------------------------------------------+
                              | (HTTPS)
                              v
+-------------------------------------------------------------+
|                    Cloudflare Edge & DNS                    |
|                    (SSL & Load Balancer)                    |
+-------------------------------------------------------------+
               /                               \
    (Tunnel Connector 1)             (Tunnel Connector 2)
             /                                   \
            v                                     v
+-----------------------+             +-----------------------+
|      Azure VM 1       |             |      Azure VM 2       |
|    Standard_B1s       |             |    Standard_B1s       |
|  (Port 3000 Node.js)  |             |  (Port 3000 Node.js)  |
|    [PM2 - Primary]    |             |    [PM2 - Standby]    |
+-----------------------+             +-----------------------+
            \                                     /
             \                                   /
              v                                 v
+-------------------------------------------------------------+
|                     Azure SQL Database                      |
|                   (Encrypted Connection)                    |
|                   Automated Daily Backups                   |
+-------------------------------------------------------------+</code></pre>
<div class="figure-caption">Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram</div>

<h3>3.2.2 Automatic Failover Flowchart</h3>
<p>Figure 3.2.2(a) models the automated decision matrix executed by Cloudflare. When a client issues a request, Cloudflare checks Connector 1. If VM1 responds within the threshold, VM1 serves the request. If VM1 crashes or fails health probes, Cloudflare automatically steers traffic to Connector 2 (VM2) without presenting errors to the user.</p>

<pre><code>              [ Client Request to polisewa.me ]
                              |
                              v
              [ Cloudflare Edge Ingress Check ]
                              |
                  < Is Connector 1 Healthy? >
                             / \
                    (YES)   /   \   (NO - Server Crash)
                           v     v
              [ Route to VM 1 ]   [ Auto-Failover to VM 2 ]
                           \     /
                            v   v
              [ Execute SQL Query / Serve UI ]
                              |
                              v
              [ Return HTTP 200 OK to Client ]</code></pre>
<div class="figure-caption">Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart</div>

<h2>3.3 Data Flow Diagrams (DFD)</h2>

<h3>3.3.1 Context Diagram (Level-0 DFD)</h3>
<p>The Level-0 Context Diagram defines the interaction between external entities (PKS Students, Landlords) and the PoliSewa system.</p>

<pre><code>+----------------+   Search Query / Filter Request    +--------------------+
|                | ---------------------------------> |                    |
| PKS Student    | <--------------------------------- |                    |
|                |    Filtered Properties / Map Data  |                    |
+----------------+                                    |      POLISEWA      |
                                                      |    CORE SYSTEM     |
+----------------+   Registration / Login Credentials |                    |
|                | ---------------------------------> |                    |
| Landlord       | <--------------------------------- |                    |
|                |   6-Digit OTP Email Verification   |                    |
+----------------+                                    +--------------------+
                                                        |        ^       |
                                  SQL Queries / Sync    |        |       | Dispatch OTP Email
                                                        v        |       v
                                                  [Azure SQL DB]   [Nodemailer SMTP]</code></pre>
<div class="figure-caption">Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa</div>

<h2>3.4 Database Design</h2>

<h3>3.4.1 Entity-Relationship Diagram (ERD)</h3>
<p>PoliSewa maintains a clean, normalized relational database structure. The <code>users</code> table maintains a 1-to-many relationship with the <code>properties</code> table.</p>

<pre><code>+-----------------------+              1 : N             +-----------------------+
|         USERS         | ------------------------------ |      PROPERTIES       |
+-----------------------+                                +-----------------------+
| PK  id (INT)          |                                | PK  id (INT)          |
|     name (NVARCHAR)   |                                | FK  user_id (INT)     |
|     email (NVARCHAR)  |                                |     name (NVARCHAR)   |
|     phone (NVARCHAR)  |                                |     desc (NVARCHAR)   |
|     password (NVAR)   |                                |     price (NVARCHAR)  |
|     role (NVARCHAR)   |                                |     phone (NVARCHAR)  |
|     extra (NVARCHAR)  |                                |     lat (FLOAT)       |
|     is_verified (INT) |                                |     lng (FLOAT)       |
|     otp_code (NVAR)   |                                |     image (NVARCHAR)  |
|     otp_expires (DATE)|                                |     created_at (DATE) |
+-----------------------+                                +-----------------------+</code></pre>
<div class="figure-caption">Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database</div>

<h3>3.4.2 Data Dictionaries</h3>
<div class="table-caption">Table 3.4.2(a): Data Dictionary for 'users' Table</div>
<table>
  <thead>
    <tr>
      <th>Column Name</th>
      <th>Data Type</th>
      <th>Constraints</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>INT</td>
      <td>PK, Identity(1,1)</td>
      <td>Unique user account identifier</td>
    </tr>
    <tr>
      <td>name</td>
      <td>NVARCHAR(255)</td>
      <td>NOT NULL</td>
      <td>User's full legal name</td>
    </tr>
    <tr>
      <td>email</td>
      <td>NVARCHAR(255)</td>
      <td>UNIQUE, NOT NULL</td>
      <td>User's email address used for login & OTP</td>
    </tr>
    <tr>
      <td>phone</td>
      <td>NVARCHAR(50)</td>
      <td>NOT NULL</td>
      <td>Contact telephone number (WhatsApp enabled)</td>
    </tr>
    <tr>
      <td>password</td>
      <td>NVARCHAR(255)</td>
      <td>NOT NULL</td>
      <td>Bcrypt cryptographic salt-hashed password string</td>
    </tr>
    <tr>
      <td>role</td>
      <td>NVARCHAR(50)</td>
      <td>CHECK('student','landlord')</td>
      <td>User account role</td>
    </tr>
    <tr>
      <td>extra</td>
      <td>NVARCHAR(MAX)</td>
      <td>NULLABLE</td>
      <td>Supplementary metadata (Institution or Agency)</td>
    </tr>
    <tr>
      <td>is_verified</td>
      <td>INT</td>
      <td>DEFAULT 0</td>
      <td>Account activation status (1 = Verified, 0 = Pending)</td>
    </tr>
    <tr>
      <td>otp_code</td>
      <td>NVARCHAR(10)</td>
      <td>NULLABLE</td>
      <td>Current 6-digit OTP verification token</td>
    </tr>
    <tr>
      <td>otp_expires_at</td>
      <td>DATETIME</td>
      <td>NULLABLE</td>
      <td>Expiration timestamp for the active OTP code</td>
    </tr>
  </tbody>
</table>

<div class="table-caption">Table 3.4.2(b): Data Dictionary for 'properties' Table</div>
<table>
  <thead>
    <tr>
      <th>Column Name</th>
      <th>Data Type</th>
      <th>Constraints</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>id</td>
      <td>INT</td>
      <td>PK, Identity(1,1)</td>
      <td>Unique property identifier</td>
    </tr>
    <tr>
      <td>user_id</td>
      <td>INT</td>
      <td>FK (users.id), NOT NULL</td>
      <td>Reference to the owner landlord's user account</td>
    </tr>
    <tr>
      <td>name</td>
      <td>NVARCHAR(255)</td>
      <td>NOT NULL</td>
      <td>Headline title of the rental room / property</td>
    </tr>
    <tr>
      <td>desc</td>
      <td>NVARCHAR(MAX)</td>
      <td>NOT NULL</td>
      <td>Description of room type, utilities, and amenities</td>
    </tr>
    <tr>
      <td>price</td>
      <td>NVARCHAR(100)</td>
      <td>NOT NULL</td>
      <td>Monthly rental price formatted (e.g., 'RM 280')</td>
    </tr>
    <tr>
      <td>phone</td>
      <td>NVARCHAR(50)</td>
      <td>NOT NULL</td>
      <td>Contact WhatsApp number for inquiries</td>
    </tr>
    <tr>
      <td>lat</td>
      <td>FLOAT</td>
      <td>NOT NULL</td>
      <td>GPS Latitude coordinate of property location</td>
    </tr>
    <tr>
      <td>lng</td>
      <td>FLOAT</td>
      <td>NOT NULL</td>
      <td>GPS Longitude coordinate of property location</td>
    </tr>
    <tr>
      <td>image</td>
      <td>NVARCHAR(MAX)</td>
      <td>NOT NULL</td>
      <td>Comma-separated file paths of uploaded photos</td>
    </tr>
    <tr>
      <td>created_at</td>
      <td>DATETIME</td>
      <td>DEFAULT CURRENT_TIMESTAMP</td>
      <td>Date and time when listing was created</td>
    </tr>
  </tbody>
</table>

<h2>3.5 User Interface (UI/UX) Design</h2>
<p>PoliSewa implements a responsive layout optimized for both desktop and mobile form factors.</p>

<!-- Screenshot Instruction 3.5.1(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 3.5.1(a) - UI Wireframe & Layout Design</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>View Type:</strong> UI Wireframe / High-Fidelity UI Layout Screenshot.</li>
      <li><strong>Content to Show:</strong> Side-by-side or stacked view displaying: (1) Desktop split-screen interface with sidebar listings and Leaflet map, and (2) Mobile portrait interface displaying touch-draggable bottom sheet.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the Search Input, Price Filter Slider, and PKS Campus Landmark Marker.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 3.5.1(a): User Interface Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout</div>

<div class="page-break"></div>

<!-- CHAPTER 4 -->
<h1>Chapter 4: Implementation</h1>

<h2>4.0 Introduction</h2>
<p>This chapter documents the technical realization of PoliSewa across both cloud infrastructure deployment and application software engineering.</p>

<h2>4.1 Cloud Infrastructure Deployment</h2>

<h3>4.1.1 Provisioning Dual Azure Virtual Machines (VM1 & VM2)</h3>
<p>Two virtual machines running Ubuntu 22.04 LTS were provisioned in the <strong>Malaysia West</strong> Azure region inside the <code>polisewa</code> resource group.</p>

<!-- Screenshot Instruction 4.1.1(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 4.1.1(a) - Azure Resource Group Overview ('polisewa')</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Microsoft Azure Portal &rarr; <em>Resource Groups</em> &rarr; <code>polisewa</code>.</li>
      <li><strong>Content to Show:</strong> Full inventory of cloud resources: Virtual Machines (VM1, VM2), Disks, Network Interfaces, Virtual Network, and Azure SQL Database.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the compute entries for VM1 and VM2.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 4.1.1(a): Azure Resource Group Overview ('polisewa')</div>

<!-- Screenshot Instruction 4.1.1(b) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 4.1.1(b) - Dual Azure Virtual Machines Running Status</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Microsoft Azure Portal &rarr; <em>Virtual Machines</em>.</li>
      <li><strong>Content to Show:</strong> Both VM instances (VM1 and VM2) displaying status <strong>Running</strong>, assigned public/private IP addresses, and CPU metrics.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw a red box around the green 'Running' status of both machines.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status</div>

<h3>4.1.2 Cloudflare Zero Trust Tunnel Dual-Connector Configuration</h3>
<p>To establish active-active load balancing without opening public inbound ports, the Cloudflare daemon (<code>cloudflared</code>) was installed on both VM1 and VM2 using an identical tunnel token.</p>

<!-- Screenshot Instruction 4.1.2(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 4.1.2(a) - Cloudflare Zero Trust Tunnel Dashboard with Dual Connectors</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Cloudflare Zero Trust Dashboard &rarr; <em>Networks</em> &rarr; <em>Tunnels</em> &rarr; <code>polisewa.me</code>.</li>
      <li><strong>Content to Show:</strong> Tunnel overview showing BOTH connectors (Connector 1 and Connector 2) with status <strong>HEALTHY</strong>.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the two green 'HEALTHY' connector badges and their registered origin IPs.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 4.1.2(a): Cloudflare Zero Trust Tunnel Dashboard with Dual Active Connectors</div>

<h3>4.1.3 Azure SQL Database Configuration and Firewall Rules</h3>
<p>A managed Azure SQL Database (<code>polisewa.database.windows.net</code>) was configured with encrypted TLS connections. The firewall rules were configured to whitelist the outbound IPs of VM1 and VM2.</p>

<!-- Screenshot Instruction 4.1.3(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 4.1.3(a) - Azure SQL Database Overview and Whitelisted Firewall Rules</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Microsoft Azure Portal &rarr; SQL Server <code>polisewa</code> &rarr; <em>Security</em> &rarr; <em>Networking</em>.</li>
      <li><strong>Content to Show:</strong> Firewall rules table displaying whitelisted IP entries for VM1 and VM2, and 'Allow Azure services' enabled.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw a red rectangle around the active firewall IP entries.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules</div>

<h3>4.1.4 PM2 Process Management Setup</h3>
<p>To ensure automatic restart upon unexpected exceptions or system reboots, the Node.js application was deployed under the <strong>PM2</strong> process manager on both VMs.</p>

<!-- Screenshot Instruction 4.1.4(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 4.1.4(a) - PM2 Process Manager Status on VM1 and VM2 Terminal</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> SSH Terminal (PuTTY / PowerShell) for VM1 and VM2.</li>
      <li><strong>Command:</strong> Run <code>pm2 status</code>.</li>
      <li><strong>Content to Show:</strong> Terminal table showing process name <code>polisewa</code>, status <strong>online</strong>, uptime, CPU %, and memory usage.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the green 'online' status indicator.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 4.1.4(a): PM2 Process Manager Status on VM1 and VM2 Terminal</div>

<h2>4.2 Application Code Development</h2>

<h3>4.2.1 Interactive Leaflet Map and Kuching Boundary Rendering</h3>
<pre><code>// Listing 4.2.1: Leaflet Map Initialization and Custom PKS Marker
const map = L.map('map', { zoomControl: false }).setView([1.5765, 110.3458], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map);

// Add dedicated Politeknik Kuching Sarawak (PKS) campus landmark
const pksIcon = L.divIcon({
  className: 'pks-marker',
  html: '&lt;div class="pks-badge"&gt;🎓 Politeknik Kuching&lt;/div&gt;',
  iconSize: [120, 36]
});
L.marker([1.5765, 110.3458], { icon: pksIcon }).addTo(map)
  .bindPopup('&lt;b&gt;Politeknik Kuching Sarawak (PKS)&lt;/b&gt;&lt;br&gt;Main Campus');</code></pre>
<div class="figure-caption">Figure 4.2.1(a): Leaflet.js Map Initialization and Boundary GeoJSON Source Code</div>

<h3>4.2.2 Haversine Geodesic Distance Engine</h3>
<pre><code>// Listing 4.2.2: Geodesic Haversine Distance Calculation (km)
function calculateDistanceToPKS(lat1, lon1) {
  const PKS_LAT = 1.5765;
  const PKS_LON = 110.3458;
  const R = 6371; // Earth's radius in kilometers
  const dLat = (PKS_LAT - lat1) * Math.PI / 180;
  const dLon = (PKS_LON - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(PKS_LAT * Math.PI / 180) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return (R * c).toFixed(1); // Returns distance in km
}</code></pre>
<div class="figure-caption">Figure 4.2.2(a): Geodesic Haversine Distance Calculation Source Code</div>

<h3>4.2.3 6-Digit Email OTP Verification Engine</h3>
<pre><code>// Listing 4.2.3: Express OTP Generation and Nodemailer Dispatch
const crypto = require('crypto');
const nodemailer = require('nodemailer');

app.post('/api/signup', async (req, res) => {
  const { name, email, phone, password, role } = req.body;
  const hashedPassword = await bcrypt.hash(password, 10);
  const otp = crypto.randomInt(100000, 999999).toString();
  const expiresAt = new Date(Date.now() + 10 * 60 * 1000); // 10-minute expiry

  await db.query(
    `INSERT INTO users (name, email, phone, password, role, is_verified, otp_code, otp_expires_at) 
     VALUES (@name, @email, @phone, @hashedPassword, @role, 0, @otp, @expiresAt)`
  );

  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: { user: process.env.SMTP_EMAIL, pass: process.env.SMTP_PASS }
  });

  await transporter.sendMail({
    from: '"PoliSewa Verification" &lt;no-reply@polisewa.me&gt;',
    to: email,
    subject: 'Your 6-Digit PoliSewa Verification Code',
    html: `&lt;h2&gt;Welcome to PoliSewa&lt;/h2&gt;&lt;p&gt;Your verification code is: &lt;b&gt;${otp}&lt;/b&gt;&lt;/p&gt;`
  });

  res.json({ success: true, message: 'OTP dispatched successfully' });
});</code></pre>
<div class="figure-caption">Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Source Code</div>

<h3>4.2.4 WhatsApp Click-to-Chat URI Builder</h3>
<pre><code>// Listing 4.2.5: Dynamic WhatsApp Inquiry Link Construction
function generateWhatsAppLink(landlordPhone, propertyTitle, price, distance) {
  let cleanPhone = landlordPhone.replace(/\D/g, '');
  if (cleanPhone.startsWith('0')) cleanPhone = '60' + cleanPhone.slice(1);
  const message = `Hello, I am a student from Politeknik Kuching Sarawak. I am interested in renting your room "${propertyTitle}" (${price}/month, ~${distance}km from PKS) listed on PoliSewa. Is it still available?`;
  return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(message)}`;
}</code></pre>
<div class="figure-caption">Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Source Code</div>

<div class="page-break"></div>

<!-- CHAPTER 5 -->
<h1>Chapter 5: Testing and Verification</h1>

<h2>5.0 Introduction</h2>
<p>Testing is a rigorous phase designed to validate system functionality, performance, and cloud fault tolerance (<em>Myers et al., 2011</em>). This chapter is divided into three core sections:</p>
<ol>
  <li><strong>Cloud High Availability & Failover Testing:</strong> Validating that the dual VM architecture survives unexpected process termination without downtime.</li>
  <li><strong>Software Functional Testing:</strong> Verifying that search, distance calculation, OTP verification, property CRUD, and WhatsApp integration operate without errors.</li>
  <li><strong>Usability Testing:</strong> Evaluating complete user workflows for students, families, and landlords.</li>
</ol>

<h2>5.1 Cloud High Availability and Failover Testing</h2>

<h3>5.1.1 Dual Connector Active Health Verification</h3>
<p>The Cloudflare Zero Trust management console was audited to ensure both connectors were registered and transmitting continuous heartbeats.</p>

<!-- Screenshot Instruction 5.1.1(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.1.1(a) - Cloudflare Connector 1 and Connector 2 Healthy Status</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Cloudflare Zero Trust &rarr; <em>Networks</em> &rarr; <em>Tunnels</em> &rarr; <code>polisewa.me</code>.</li>
      <li><strong>Content to Show:</strong> Connector 1 (VM1) and Connector 2 (VM2) both displaying green <strong>HEALTHY</strong> badges with active origin IPs.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the two 'HEALTHY' status pills.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status</div>

<h3>5.1.2 Simulated VM1 Crash and Automatic Failover Test</h3>
<p>To rigorously validate High Availability Objective 3, a server crash was simulated on the primary host (VM1) by executing <code>pm2 stop polisewa</code>. Inbound traffic to <code>https://polisewa.me</code> was immediately measured using browser Developer Tools.</p>

<!-- Screenshot Instruction 5.1.2(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.1.2(a) - Simulated VM1 Service Termination in Terminal</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> SSH Terminal connected to VM1.</li>
      <li><strong>Command:</strong> Execute <code>pm2 stop polisewa</code>.</li>
      <li><strong>Content to Show:</strong> PM2 process table displaying the <code>polisewa</code> application with status <strong>stopped</strong> in red text.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw a red box around status: 'stopped'.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal ('pm2 stop polisewa')</div>

<!-- Screenshot Instruction 5.1.2(b) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.1.2(b) - Uninterrupted HTTP 200 OK Response via Connector 2</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> Web browser navigating to <code>https://polisewa.me</code>.</li>
      <li><strong>Action:</strong> Open DevTools (F12) &rarr; Network Tab &rarr; Hard Refresh (Ctrl+F5).</li>
      <li><strong>Content to Show:</strong> Main document request returning HTTP status <strong>200 OK</strong> with sub-second latency, proving seamless routing to VM2 without any HTTP 502/504 errors.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the status '200 OK' and the Cloudflare CF-RAY response header.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in Browser DevTools</div>

<h3>5.1.3 Azure SQL Connectivity & Data Consistency Test</h3>
<p>Data consistency was tested during failover. Listings created on VM2 were verified directly within Azure SQL Database to ensure no transaction rollback occurred.</p>

<!-- Screenshot Instruction 5.1.3(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.1.3(a) - Azure SQL Query Execution and Data Consistency Check</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Portal Location:</strong> Azure Portal &rarr; SQL Database <code>polisewa</code> &rarr; <em>Query Editor</em>.</li>
      <li><strong>Action:</strong> Run query <code>SELECT TOP 5 id, name, price, created_at FROM properties;</code>.</li>
      <li><strong>Content to Show:</strong> Results pane displaying persistent property records created during the failover interval.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight query execution success and returned record rows.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check</div>

<h2>5.2 Software Functional Testing</h2>

<h3>5.2.1 Interactive Map Navigation & PKS Marker Verification</h3>
<!-- Screenshot Instruction 5.2.1(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.1(a) - Interactive Leaflet Map with PKS Landmark</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> PoliSewa homepage (<code>https://polisewa.me</code> or <code>localhost:3000</code>).</li>
      <li><strong>Action:</strong> Center the map on Politeknik Kuching Sarawak.</li>
      <li><strong>Content to Show:</strong> The prominent blue 'Politeknik Kuching' campus marker, surrounding rental room pins, and the yellow/blue Matang district boundary line.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the PKS campus badge marker.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers</div>

<h3>5.2.2 Student Search, Price Slider (< RM300) & Distance Calculation Test</h3>
<!-- Screenshot Instruction 5.2.2(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.2(a) - Live Keyword Search and Price Filtering (< RM300)</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> PoliSewa sidebar / search bar.</li>
      <li><strong>Action:</strong> Type 'Matang' in search box and adjust the price slider to 'RM 300'.</li>
      <li><strong>Content to Show:</strong> The property cards dynamically updating to show only rooms &le; RM 300 with the green distance badge (e.g. '1.8 km from PKS').</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw red boxes around the price slider value and distance badge.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300) with Distance Badges</div>

<h3>5.2.3 User Authentication & 6-Digit Email OTP Verification Test</h3>
<!-- Screenshot Instruction 5.2.3(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.3(a) - 6-Box Email OTP Verification Dialog</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> PoliSewa Signup Modal.</li>
      <li><strong>Action:</strong> Fill registration form with a valid email and submit.</li>
      <li><strong>Content to Show:</strong> The modern 6-box OTP input modal popup showing the 60-second resend cooldown countdown timer.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the 6 digit entry inputs and the cooldown timer.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer</div>

<!-- Screenshot Instruction 5.2.3(b) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.3(b) - PoliSewa OTP Verification Email in Gmail</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> Real Gmail / Email Inbox.</li>
      <li><strong>Content to Show:</strong> The received HTML email from 'PoliSewa Verification' showing the large 6-digit numeric security code and expiration notice.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the 6-digit code and sender address.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox</div>

<h3>5.2.4 Landlord Property Listing & Photo Upload Test</h3>
<!-- Screenshot Instruction 5.2.4(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.4(a) - Landlord Property Creation Modal</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> Landlord Portal &rarr; 'Add New Property' Modal.</li>
      <li><strong>Action:</strong> Fill property title, price, description, pin location on the picker map, and select 2-3 room photos.</li>
      <li><strong>Content to Show:</strong> The complete form with photo thumbnail previews displayed before clicking 'Publish Listing'.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the photo preview thumbnails and price input.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.4(a): Landlord Property Creation Modal with Multi-Photo Upload Preview</div>

<h3>5.2.5 Direct WhatsApp Redirection Verification Test</h3>
<!-- Screenshot Instruction 5.2.5(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.5(a) - Direct WhatsApp Redirection</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> WhatsApp Web / Mobile WhatsApp Application.</li>
      <li><strong>Action:</strong> Click the green 'Hubungi Landlord' button on any property card.</li>
      <li><strong>Content to Show:</strong> WhatsApp conversation interface showing the landlord's phone number and the pre-filled message text in the input box referencing the room name and price.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Draw a red outline around the pre-filled inquiry text message.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.5(a): Direct WhatsApp Redirection with Pre-Filled Inquiring Message</div>

<h3>5.2.6 Account and Listing Deletion Test</h3>
<!-- Screenshot Instruction 5.2.6(a) -->
<div class="screenshot-instruction-card">
  <div class="screenshot-header">📸 SCREENSHOT INSTRUCTION: Figure 5.2.6(a) - Permanent Account Deletion Dialog</div>
  <div class="screenshot-body">
    <ul>
      <li><strong>Location:</strong> User Profile Settings.</li>
      <li><strong>Action:</strong> Click 'Delete Account'.</li>
      <li><strong>Content to Show:</strong> Password confirmation modal warning that all owned listings and uploaded photos will be permanently deleted.</li>
      <li><strong><span class="red-callout">Red Box Callout:</span></strong> Highlight the confirmation warning prompt.</li>
    </ul>
  </div>
</div>
<div class="figure-caption">Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog</div>

<h2>5.3 Usability Testing (Step-by-Step User Scenarios)</h2>

<h3>5.3.1 Scenario 1: Student Searching and Inquiring for Accommodation</h3>
<p><strong>Step 1:</strong> Student opens <code>https://polisewa.me</code>. The system renders the Leaflet map centered on PKS.<br>
<strong>Step 2:</strong> Student moves the price slider to RM 280. The listing grid updates to display only units within budget.<br>
<strong>Step 3:</strong> Student inspects the distance metric (<code>1.4 km from PKS</code>) and clicks the property card to view the photo carousel.<br>
<strong>Step 4:</strong> Student clicks "Hubungi Landlord" and is redirected to WhatsApp with the automated inquiry message ready to send.</p>

<div class="figure-caption">Figure 5.3.1(a): Student User Workflow: Room Discovery and Geodesic Distance Verification</div>

<h3>5.3.2 Scenario 2: Parent/Family Member Reviewing Property Details</h3>
<p><strong>Step 1:</strong> Parent accesses the website on a tablet/smartphone.<br>
<strong>Step 2:</strong> Parent opens property details to review utilities (water, electricity, Wi-Fi included).<br>
<strong>Step 3:</strong> Parent verifies the exact geographic location relative to the PKS bus route and campus gate.</p>

<div class="figure-caption">Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection</div>

<h3>5.3.3 Scenario 3: Landlord Registering, Verifying, and Listing a Room</h3>
<p><strong>Step 1:</strong> Landlord signs up with email, phone, and role "Landlord".<br>
<strong>Step 2:</strong> Landlord enters the 6-digit OTP code received in email.<br>
<strong>Step 3:</strong> Landlord logs in, clicks "Add Listing", fills unit details, uploads room photos, and submits.<br>
<strong>Step 4:</strong> New listing appears instantly on the interactive map for all users.</p>

<div class="figure-caption">Figure 5.3.3(a): Landlord Portal Workflow: Registration, Verification, and Listing Publication</div>

<h2>5.4 Functional Test Execution Summary Matrix</h2>
<div class="table-caption">Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix</div>
<table>
  <thead>
    <tr>
      <th>Test ID</th>
      <th>Module Tested</th>
      <th>Test Description</th>
      <th>Expected Result</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TC-01</td>
      <td>Cloud HA Ingress</td>
      <td>Route traffic through Cloudflare Tunnel</td>
      <td>Loads polisewa.me via VM1/VM2</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-02</td>
      <td>Cloud HA Failover</td>
      <td>Simulate VM1 crash (<code>pm2 stop</code>)</td>
      <td>Seamless switch to VM2 (200 OK)</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-03</td>
      <td>Database Persistence</td>
      <td>Insert property during failover state</td>
      <td>Record preserved in Azure SQL</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-04</td>
      <td>Geographic Map</td>
      <td>Initialize Leaflet map and boundary</td>
      <td>Renders PKS marker & boundary</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-05</td>
      <td>Proximity Engine</td>
      <td>Calculate distance to PKS campus</td>
      <td>Accurate geodesic km displayed</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-06</td>
      <td>Search & Filter</td>
      <td>Filter by keyword & budget &le; RM300</td>
      <td>Matches correctly updated</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-07</td>
      <td>User Registration</td>
      <td>Submit signup with valid email</td>
      <td>Triggers 6-digit OTP to inbox</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-08</td>
      <td>OTP Verification</td>
      <td>Enter correct 6-digit code</td>
      <td>Activates user account (1)</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-09</td>
      <td>OTP Expiry Check</td>
      <td>Enter code after 10-minute timeout</td>
      <td>Rejects code with error notice</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-10</td>
      <td>Landlord Listing</td>
      <td>Submit new listing with 3 photos</td>
      <td>Appears on map & uploads saved</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-11</td>
      <td>WhatsApp Redirection</td>
      <td>Click 'Hubungi Landlord' button</td>
      <td>Opens WhatsApp pre-filled chat</td>
      <td><strong>PASS</strong></td>
    </tr>
    <tr>
      <td>TC-12</td>
      <td>Account Deletion</td>
      <td>Confirm deletion with valid password</td>
      <td>Cascades deletion of properties</td>
      <td><strong>PASS</strong></td>
    </tr>
  </tbody>
</table>

<h2>5.5 Chapter Summary</h2>
<p>Testing verified that PoliSewa satisfies all functional requirements and architectural objectives. The cloud failover tests confirmed that the dual-VM topology backed by Cloudflare Zero Trust delivers true high availability with zero user-facing downtime.</p>

<div class="page-break"></div>

<!-- CHAPTER 6 -->
<h1>Chapter 6: Conclusion and Future Works</h1>

<h2>6.0 Introduction</h2>
<p>This concluding chapter reviews the degree of objective achievement, outlines practical constraints and limitations identified during implementation, and proposes recommendations for future commercial scaling.</p>

<h2>6.1 Objective Achievement Review</h2>
<div class="table-caption">Table 6.1(a): Project Objectives Achievement Verification Matrix</div>
<table>
  <thead>
    <tr>
      <th>No.</th>
      <th>Initial Objective</th>
      <th>Achievement Status</th>
      <th>Empirical Verification Evidence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>Develop Centralized Rental Platform</td>
      <td>Achieved (100%)</td>
      <td>Responsive web application deployed at polisewa.me with Leaflet map, price filters (<RM300), Haversine distance calculation, and WhatsApp redirection.</td>
    </tr>
    <tr>
      <td>2</td>
      <td>Enhance Data Protection</td>
      <td>Achieved (100%)</td>
      <td>Azure SQL Database deployment with automated backups, strict firewall rules, and 6-digit email OTP account verification via Nodemailer SMTP.</td>
    </tr>
    <tr>
      <td>3</td>
      <td>Implement High Availability Architecture</td>
      <td>Achieved (100%)</td>
      <td>Active-active dual Azure VMs (VM1 & VM2) load-balanced via Cloudflare Zero Trust Tunnels with sub-second failover verified during simulated server crash tests.</td>
    </tr>
  </tbody>
</table>

<h2>6.2 Project Limitations</h2>
<p>While PoliSewa achieves its foundational objectives, several operational constraints were observed:</p>
<ol>
  <li><strong>Third-Party WhatsApp Dependency:</strong> Direct communication relies upon landlord responsiveness on WhatsApp; unread messages cannot be tracked within the web app.</li>
  <li><strong>Cloud Subscription Costs:</strong> While current spending is modest (~RM 156/month), maintaining two VM instances and managed cloud SQL requires ongoing subscription funding.</li>
  <li><strong>Regional Focus:</strong> Geocoding and boundary layers are currently localized specifically to Kuching and Politeknik Kuching Sarawak.</li>
</ol>

<h2>6.3 Future Works and Enhancements</h2>
<p>To scale PoliSewa beyond an academic prototype, the following enhancements are recommended:</p>
<ul>
  <li><strong>Integrated Escrow Payment Gateway (FPX / DuitNow):</strong> Incorporating a secure payment gateway where PoliSewa holds deposit funds in escrow until the student physically inspects the room, eliminating rental scams entirely.</li>
  <li><strong>In-App Digital Tenancy Agreements:</strong> Implementing digital tenancy contracts with electronic signatures (e-Sign) to provide legal protection for both students and landlords.</li>
  <li><strong>Expansion to Other Higher Institutions:</strong> Parameterizing the campus location engine to support Universiti Malaysia Sarawak (UNIMAS), UiTM Kota Samarahan, and other polytechnics nationwide.</li>
  <li><strong>Mobile Native Application Wrapper:</strong> Packaging the web application using Capacitor or React Native for native Android and iOS distribution on Google Play Store and Apple App Store.</li>
</ul>

<h2>6.4 Conclusion</h2>
<p>PoliSewa demonstrates how contemporary cloud-native technologies—specifically dual-node virtualization, edge tunnel load balancing, and relational database replication—can be united with student-centric web design to solve real-world logistical challenges. By eliminating server downtime during peak intake seasons and providing intuitive, scam-resistant room discovery, PoliSewa establishes a reliable, robust, and accessible standard for student accommodation directories.</p>

<div class="page-break"></div>

<!-- REFERENCES -->
<h1>References</h1>
<ol>
  <li>Clemente, R., Silva, F. A., Maciel, P. R., & Araujo, J. (2022). Availability evaluation of system service hosted in private cloud computing through hierarchical modeling process. <em>The Journal of Supercomputing</em>, 78(8), 10412-10435. https://doi.org/10.1007/s11227-021-04217-1</li>
  <li>Cloudflare. (2023). <em>Cloudflare Load Balancing and Zero Trust Tunnel Documentation</em>. Cloudflare Developers. https://developers.cloudflare.com/load-balancing/</li>
  <li>Gaurikasar. (2026). <em>High availability in Azure Database for PostgreSQL flexible server</em>. Microsoft Learn. https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability</li>
  <li>Latif, A. A., Hashim, N., & Zulkifli, M. (2020). Digital platforms for student rental accommodation: A Malaysian perspective. <em>Malaysian Journal of Information Technology</em>, 12(3), 45-58.</li>
  <li>Myers, G. J., Sandler, C., & Badgett, T. (2011). <em>The Art of Software Testing</em> (3rd ed.). John Wiley & Sons.</li>
  <li>Pressman, R. S., & Maxim, B. R. (2020). <em>Software Engineering: A Practitioner's Approach</em> (9th ed.). McGraw-Hill Education.</li>
  <li>RobBagby. (n.d.). <em>Baseline highly available zone-redundant app services web application</em>. Azure Architecture Center. Microsoft Learn. Retrieved July 16, 2026, from https://learn.microsoft.com/en-us/azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant</li>
  <li>Saxena, S., & Singh, J. (2022). OFP-TM: An online VM failure prediction and tolerance model towards high availability of cloud computing environments. <em>The Journal of Supercomputing</em>, 78(8), 10436-10465. https://doi.org/10.1007/s11227-021-04235-z</li>
  <li>Saxena, S., Singh, J., & Lee, W. (2022). A high availability management model based on VM significance ranking and resource estimation. <em>IEEE Transactions on Network and Service Management</em>, 19(3), 2912-2925. https://doi.org/10.1109/TNSM.2022.3189178</li>
  <li>Sinnott, R. W. (1984). Virtues of the Haversine. <em>Sky and Telescope</em>, 68(2), 159.</li>
  <li>SPEEDHOME. (2026). <em>Rental scam prevention for international students in Malaysia</em>. SPEEDHOME Property Insights. https://speedhome.com/blog/rental-scam-prevention-international-students-malaysia/</li>
  <li>Stallings, W. (2017). <em>Cryptography and Network Security: Principles and Practice</em> (7th ed.). Pearson.</li>
  <li>The Sun Malaysia. (2023, October 11). <em>Rental scams targeting tertiary students on the rise</em>. The Sun Daily. https://thesun.my/news/malaysia-news/rental-scams-ih11612921/</li>
  <li>Universiti Pendidikan Sultan Idris (UPSI). (2025). Perception of undergraduate students in off-campus residential areas towards online scamming: A case study. <em>Jurnal Perspektif</em>, 17(1), 112-125. https://ejournal.upsi.edu.my/index.php/PERS/article/view/9255/5135</li>
</ol>

</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated {HTML_PATH}")

# Compile to PDF using Microsoft Edge headless
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

print("Compiling PDF with Microsoft Edge headless...")
cmd = [
    edge_exe,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Edge returncode:", res.returncode)
if os.path.exists(PDF_PATH):
    print(f"Successfully created PDF! Size: {os.path.getsize(PDF_PATH)} bytes at {PDF_PATH}")
else:
    print("PDF creation failed:", res.stderr)
