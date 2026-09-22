# POLITEKNIK KUCHING SARAWAK
## JABATAN TEKNOLOGI MAKLUMAT DAN KOMUNIKASI

---

# FINAL YEAR PROJECT REPORT
### DIPLOMA IN INFORMATION TECHNOLOGY
### SESSION 1: 2026/2027

---

# CLOUD BASED HIGH AVAILABILITY ROOM RENTAL SYSTEM (POLISEWA)

**PREPARED BY:**
* **AHMAD SYARIFUDDIN BIN MOHD BAHARUDIN** (05DIT24F1070)
* **ABDUL KHALIL BIN HARMEZI** (05DIT24F1034)
* **JOSH ALZON ANAK JACKSON** (05DIT24F1111)

**PREPARED FOR:**
* **SIR HASBULLAH BIN ABDULLAH** (Project Supervisor)

**DEPARTMENT OF INFORMATION AND COMMUNICATION TECHNOLOGY**  
**POLITEKNIK KUCHING SARAWAK**  
**2026/2027**

---

## DECLARATION

We hereby declare that this project report entitled **"Cloud Based High Availability Room Rental System (PoliSewa)"** is our original work, except for quotations and citations which have been duly acknowledged. We also confirm that this report has not been previously submitted, either in part or in whole, for the award of any diploma, degree, or other qualification at Politeknik Kuching Sarawak or any other educational institution.

\
\
......................................................................  
**AHMAD SYARIFUDDIN BIN MOHD BAHARUDIN**  
(Matric No: 05DIT24F1070)  
Date: 16 September 2026  

\
\
......................................................................  
**ABDUL KHALIL BIN HARMEZI**  
(Matric No: 05DIT24F1034)  
Date: 16 September 2026  

\
\
......................................................................  
**JOSH ALZON ANAK JACKSON**  
(Matric No: 05DIT24F1111)  
Date: 16 September 2026  

---

## APPROVAL FOR SUBMISSION

I hereby certify that I have supervised and examined this final year project report entitled **"Cloud Based High Availability Room Rental System (PoliSewa)"** prepared by Ahmad Syarifuddin bin Mohd Baharudin, Abdul Khalil bin Harmezi, and Josh Alzon Anak Jackson. In my opinion, it satisfies the requirements for the award of Diploma in Information Technology at Politeknik Kuching Sarawak.

\
\
......................................................................  
**SIR HASBULLAH BIN ABDULLAH**  
Project Supervisor  
Department of Information and Communication Technology  
Politeknik Kuching Sarawak  
Date: 16 September 2026  

---

## ACKNOWLEDGMENTS

Alhamdulillah, all praises to Allah S.W.T. for the blessings, strength, and health granted to our team throughout the journey of planning, developing, and successfully completing our Final Year Project (FYP).

First and foremost, we would like to express our deepest gratitude and highest appreciation to our dedicated project supervisor, **Sir Hasbullah bin Abdullah**. His invaluable guidance, technical insights, constructive feedback, and continuous encouragement throughout every phase of this project have been instrumental in transforming this cloud-based vision into a fully functional reality.

Our sincere gratitude also extends to the Head of Department, Project Coordinators, and all academic lecturers within the **Department of Information and Communication Technology, Politeknik Kuching Sarawak**, who provided the academic foundation, laboratory facilities, and support required for our studies.

We also wish to thank our parents and families for their unwavering moral and financial support, endless prayers, and sacrifices that motivated us to persevere. Lastly, we extend our heartfelt appreciation to our fellow course mates and friends who directly or indirectly shared knowledge, testing feedback, and camaraderie during the development and testing of PoliSewa.

---

## ABSTRACT

Securing safe, affordable, and conveniently located off-campus rental accommodation is a persistent challenge for students at Politeknik Kuching Sarawak (PKS). Traditionally, students have relied on fragmented and unindexed social media channels—such as Facebook groups, TikTok videos, and peer WhatsApp chats—which are vulnerable to outdated listings, lack location proximity metrics, and expose students to deposit scams. Concurrently, conventional single-server campus portals suffer critical downtime during peak intake periods when thousands of students concurrently seek housing. To resolve these challenges, this project presents **PoliSewa**, an interactive, web-based room rental directory backed by a cloud-native **High Availability (HA)** infrastructure. 

The application layer combines Leaflet.js interactive GIS mapping, dynamic geodesic distance computation relative to the PKS campus, student-centric price filtering (e.g., budget rooms under RM300/month), a 6-digit email One-Time Password (OTP) verification mechanism powered by Nodemailer, and direct landlord WhatsApp click-to-chat integration. At the infrastructure layer, PoliSewa eliminates single points of failure by deploying an active-active dual Virtual Machine (VM) architecture on **Microsoft Azure** (VM1 and VM2) in the Malaysia West region, interconnected with **Azure SQL Database** and load-balanced via **Cloudflare Zero Trust Tunnels**. Extensive failover testing demonstrates that when the primary VM process experiences simulated service termination (`pm2 stop polisewa`), Cloudflare automatically routes user traffic to the secondary connector within milliseconds with zero HTTP 502/504 errors (maintaining 100% HTTP 200 OK uptime). A comprehensive cost analysis of Azure cloud spending confirms that this dual-node high availability configuration is economically viable for educational institutions, totaling approximately RM 133.74 per month for compute and database workloads. PoliSewa successfully provides a secure, reliable, and continuously available rental platform tailored for the polytechnic student community.

**Keywords:** High Availability (HA), Cloud Computing, Microsoft Azure, Cloudflare Tunnels, Leaflet.js, Student Housing Directory, WhatsApp Integration, Politeknik Kuching Sarawak.

---

## ABSTRAK

Mendapatkan bilik sewa yang selamat, berpatutan, dan berdekatan dengan kampus merupakan cabaran utama bagi para pelajar Politeknik Kuching Sarawak (PKS). Secara tradisinya, pelajar bergantung kepada saluran media sosial yang tidak tersusun seperti kumpulan Facebook, video TikTok, dan perkongsian WhatsApp. Kaedah ini mendedahkan pelajar kepada maklumat yang telah luput, ketiadaan ukuran jarak ke kampus, serta risiko penipuan wang deposit sewa. Pada masa yang sama, portal berasaskan pelayan tunggal sering mengalami gangguan perkhidmatan (*downtime*) semasa minggu pendaftaran kemasukan baharu akibat lonjakan trafik secara serentak. Bagi mengatasi masalah ini, projek ini membangunkan **PoliSewa**, sebuah direktori sewaan bilik berasaskan web interaktif yang disokong oleh infrastruktur awan **Ketersediaan Tinggi (High Availability - HA)**.

Lapisan aplikasi menggabungkan pemetaan GIS interaktif menggunakan Leaflet.js, pengiraan jarak geodesik dari kampus PKS, penapis carian mesra bajet pelajar (seperti bilik di bawah RM300 sebulan), sistem pengesahan kata laluan sekali guna (OTP) 6 digit melalui emel menggunakan Nodemailer, dan integrasi pautan terus WhatsApp (*click-to-chat*) kepada pemilik rumah. Pada lapisan infrastruktur, PoliSewa menghapuskan titik kegagalan tunggal (*single point of failure*) dengan melaksana seni bina dwi-Mesin Maya (Dual Virtual Machine - VM1 dan VM2) di **Microsoft Azure** (rantau Malaysia West), berhubung dengan **Azure SQL Database**, dan diimbangi beban trafiknya menggunakan **Cloudflare Zero Trust Tunnels**. Ujian kegagalan (*failover testing*) membuktikan bahawa apabila proses pelayan utama dimatikan (`pm2 stop polisewa`), Cloudflare mengalihkan trafik pengguna ke pelayan sandaran dalam beberapa milisaat tanpa sebarang ralat (kekal 100% HTTP 200 OK). Analisis kos perbelanjaan awan Azure mengesahkan bahawa seni bina berkembar ini berdaya maju dari sudut kewangan institusi pendidikan dengan anggaran kos RM 133.74 sebulan. PoliSewa berjaya menyediakan platform sewaan yang selamat, pantas, dan sentiasa beroperasi untuk komuniti pelajar politeknik.

**Kata Kunci:** Ketersediaan Tinggi, Pengkomputeran Awan, Microsoft Azure, Cloudflare Tunnels, Leaflet.js, Direktori Bilik Sewa Pelajar, Integrasi WhatsApp, Politeknik Kuching Sarawak.

---

## TABLE OF CONTENTS

| Section / Chapter | Page |
| :--- | :---: |
| **Declaration** | 2 |
| **Approval for Submission** | 3 |
| **Acknowledgments** | 4 |
| **Abstract** | 5 |
| **Abstrak** | 6 |
| **Table of Contents** | 7 |
| **List of Figures** | 9 |
| **List of Tables** | 11 |
| **CHAPTER 1: INTRODUCTION** | **12** |
| &nbsp;&nbsp;&nbsp;&nbsp;1.0 Introduction | 12 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.1 Problem Statement | 12 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.2 Project Scope | 13 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.3 Aim and Objectives | 14 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.4 Methodology (Agile SDLC) | 14 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.5 Significance of the Project | 15 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.6 Project Schedule (Gantt Chart) | 15 |
| &nbsp;&nbsp;&nbsp;&nbsp;1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis | 15 |
| **CHAPTER 2: LITERATURE REVIEW** | **18** |
| &nbsp;&nbsp;&nbsp;&nbsp;2.0 Introduction | 18 |
| &nbsp;&nbsp;&nbsp;&nbsp;2.1 High Availability and Cloud Fault Tolerance Models | 18 |
| &nbsp;&nbsp;&nbsp;&nbsp;2.2 Student Rental Portals and Scam Prevention Studies | 19 |
| &nbsp;&nbsp;&nbsp;&nbsp;2.3 Cloud Infrastructure, Redundancy, and Load Balancing | 20 |
| &nbsp;&nbsp;&nbsp;&nbsp;2.4 Comparative Analysis of Existing Systems vs. PoliSewa | 20 |
| &nbsp;&nbsp;&nbsp;&nbsp;2.5 Chapter Summary | 21 |
| **CHAPTER 3: ANALYSIS AND DESIGN** | **22** |
| &nbsp;&nbsp;&nbsp;&nbsp;3.0 Introduction | 22 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.1 Requirement Analysis | 22 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.2 High Availability System Architecture | 23 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.3 Data Flow Diagrams (DFD) | 25 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.4 Database Design | 26 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.5 User Interface (UI/UX) Design | 28 |
| &nbsp;&nbsp;&nbsp;&nbsp;3.6 Chapter Summary | 29 |
| **CHAPTER 4: IMPLEMENTATION** | **30** |
| &nbsp;&nbsp;&nbsp;&nbsp;4.0 Introduction | 30 |
| &nbsp;&nbsp;&nbsp;&nbsp;4.1 Cloud Infrastructure Deployment | 30 |
| &nbsp;&nbsp;&nbsp;&nbsp;4.2 Application Code Development | 33 |
| &nbsp;&nbsp;&nbsp;&nbsp;4.3 Chapter Summary | 35 |
| **CHAPTER 5: TESTING AND VERIFICATION** | **36** |
| &nbsp;&nbsp;&nbsp;&nbsp;5.0 Introduction | 36 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.1 Cloud High Availability and Failover Testing | 36 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.2 Software Functional Testing | 39 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.3 User Scenario Walkthroughs | 43 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.4 Test Results Summary | 44 |
| &nbsp;&nbsp;&nbsp;&nbsp;5.5 Chapter Summary | 44 |
| **CHAPTER 6: CONCLUSION AND FUTURE WORKS** | **45** |
| &nbsp;&nbsp;&nbsp;&nbsp;6.0 Introduction | 45 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.1 Objective Achievement Review | 45 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.2 Challenges and Problem Solving | 45 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.3 Future Works and Enhancements | 46 |
| &nbsp;&nbsp;&nbsp;&nbsp;6.4 Conclusion | 46 |
| **REFERENCES** | **47** |

---

## LIST OF FIGURES

| Figure Label & Title | Page |
| :--- | :---: |
| Figure 1.4(a): Agile Software Development Life Cycle (SDLC) Workflow for PoliSewa | 15 |
| Figure 1.6(a): Project Development Schedule (Gantt Chart) | 15 |
| Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend | 17 |
| Figure 1.7(b): Azure Resource-Level Cost Breakdown & Infrastructure Inventory | 17 |
| Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram | 23 |
| Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart | 24 |
| Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa | 25 |
| Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database | 26 |
| Figure 3.5.1(a): User Interface Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout | 28 |
| Figure 4.1.1(a): Azure Resource Group Overview ('polisewa') | 30 |
| Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status | 30 |
| Figure 4.1.2(a): Cloudflare Edge Routing and Gateway Status Verification | 31 |
| Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules | 32 |
| Figure 4.1.4(a): Virtual Machine Linux Host Console and Git Deployment | 33 |
| Figure 4.2.2(a): Geodesic Haversine Distance Calculation Source Code | 34 |
| Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Source Code | 35 |
| Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Source Code | 35 |
| Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status | 36 |
| Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal ('pm2 stop polisewa') | 37 |
| Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2 in Browser DevTools | 37 |
| Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check | 38 |
| Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers | 39 |
| Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300) with Distance Badges | 39 |
| Figure 5.2.3(a): 6-Box Email OTP Verification Dialog with Cooldown Timer | 40 |
| Figure 5.2.3(b): PoliSewa OTP Verification Email Received in Gmail Inbox | 40 |
| Figure 5.2.4(a): Landlord Property Creation Modal with Pinpoint Coordinate Binding | 41 |
| Figure 5.2.5(a): Property Listing Card with Direct WhatsApp Contact and Verified Badge | 42 |
| Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog | 42 |
| Figure 5.3.1(a): Student User Workflow: Room Discovery and Geodesic Distance Verification | 43 |
| Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection | 43 |
| Figure 5.3.3(a): Landlord Portal Workflow: Registration, OTP Verification, and Listing Creation | 43 |

---

## LIST OF TABLES

* **Table 1.7(a):** Estimated vs. Actual Monthly Cloud Infrastructure Cost
* **Table 2.4(a):** Comparative Analysis Matrix of Rental Systems
* **Table 3.1.1(a):** Server and Client Hardware Requirements
* **Table 3.1.2(a):** Software Stack and Development Technologies
* **Table 3.4.2(a):** Data Dictionary for `users` Table
* **Table 3.4.2(b):** Data Dictionary for `properties` Table
* **Table 5.4(a):** Comprehensive Functional Black-Box Test Results Matrix
* **Table 6.1(a):** Project Objectives Achievement Verification Matrix

---

# CHAPTER 1: INTRODUCTION

## 1.0 Introduction
In today's digitalized educational landscape, tertiary institutions increasingly adopt web-based systems to automate academic and administrative processes. However, student off-campus accommodation management remains critically underserved. At Politeknik Kuching Sarawak (PKS), located along Jalan Matang in Kuching, Sarawak, the majority of senior and out-of-town students reside in off-campus rental housing across areas such as Taman Sri Matang, Kampung Gita, Matang Jaya, and Petra Jaya.

Despite the critical necessity of safe housing, the room rental discovery process continues to rely upon unorganized, informal mechanisms including printed flyers, word-of-mouth recommendations, and unstructured posts on social media platforms such as Facebook groups, TikTok, and WhatsApp chats. These channels lack centralized organization, provide no geographic proximity context, and leave students vulnerable to fraud. Furthermore, when polytechnic student bodies attempt to host centralized web portals, they traditionally deploy them on basic single-server architectures. During peak academic intake windows—specifically the onset of semester registration—thousands of students access the portal concurrently. These traffic surges overwhelm single servers, resulting in catastrophic downtime, connection timeouts, and service unavailability when students need it most.

To overcome these dual challenges of information fragmentation and server vulnerability, this project introduces **PoliSewa: A Cloud Based High Availability Room Rental System**. PoliSewa provides an interactive, map-centric web directory tailored specifically for PKS students while implementing an enterprise-grade cloud architecture featuring active-active dual Virtual Machines on Microsoft Azure, Cloudflare Zero Trust load balancing, and automated database replication.

## 1.1 Problem Statement

### 1.1.1 Scattered Rental Information Across Social Media
Off-campus rental advertisements are scattered across disjointed digital silos, including various Facebook rental groups, Instagram stories, TikTok clips, and transient WhatsApp chat groups. Consequently, students waste substantial hours searching for listings, frequently encounter expired advertisements for rooms that have already been rented, and fail to secure accommodations before academic sessions commence.

### 1.1.2 Data Reliability and Backup Deficiencies
Informal rental methods and legacy student platforms do not implement automated data backups or standardized transaction logs. If an administrator's machine or single host server experiences filesystem corruption or hardware failure, room listings, landlord contacts, and booking histories are permanently lost. The lack of a structured disaster recovery mechanism severely undermines data integrity.

### 1.1.3 Server Downtime and Single Point of Failure
Conventional student portals rely on a single web server and an un-replicated local database. During new intake cycles, concurrent requests cause severe CPU exhaustion and memory bottlenecks. A single process crash or infrastructure maintenance window takes the entire platform offline. Educational institutions lack fault-tolerant systems capable of surviving server outages without disrupting students.

## 1.2 Project Scope

### 1.2.1 System Scope
* **Dual Virtual Machine Infrastructure:** Deployment of two independent Linux Virtual Machines (VM1 and VM2) on Microsoft Azure (Malaysia West region) running Node.js / Express web services managed via PM2.
* **Cloudflare Zero Trust Load Balancing & Failover:** Routing of domain traffic (`polisewa.me`) through dual Cloudflare Tunnel connectors (`cloudflared`) to distribute requests and execute sub-second failover if any VM terminates.
* **Centralized Azure SQL Database:** Cloud-hosted relational database storing user records, hashed authentication credentials, property details, and coordinates, with automated backups and firewall whitelisting.
* **Interactive Web Application:** Single-page responsive interface utilizing Leaflet.js, OpenStreetMap geospatial boundaries (`boundary.js`), Haversine geodesic distance calculation, 6-digit email OTP verification via Nodemailer Gmail SMTP, and WhatsApp click-to-chat redirection.

### 1.2.2 User Scope
* **Polytechnic Students:** Primary users who search for rental rooms, apply budget and distance filters, inspect property photo galleries, and initiate verified WhatsApp inquiries to landlords.
* **Family Members:** Parents and guardians assisting students in evaluating property amenities, security, pricing, and campus distance.
* **Property Owners (Landlords):** Registered and OTP-verified property owners who manage room listings, upload multiple unit photos, update rental rates, and receive pre-filled WhatsApp inquiries.
* **System Administrators:** Authorized personnel managing Azure cloud resources, monitoring Cloudflare tunnel health, and auditing listings to prevent scams.

## 1.3 Aim and Objectives
The overarching aim of this project is to design, develop, and deploy a secure, fault-tolerant, cloud-based student room rental directory for Politeknik Kuching Sarawak. The specific measurable objectives are:
1. **Develop a Centralized Room Rental Platform:** To design and implement a responsive, map-based web application that allows PKS students and families to search, filter by price (< RM300), calculate distance to campus, and contact landlords via WhatsApp.
2. **Enhance Data Protection:** To implement automated cloud database management using Azure SQL Database with strict firewall controls, transaction integrity, and automated daily backups to eliminate data loss.
3. **Implement High Availability Cloud Infrastructure:** To configure a multi-node cloud environment on Microsoft Azure using dual Virtual Machines and Cloudflare Tunnel load balancing, ensuring zero-downtime failover during server maintenance or crashes.

## 1.4 Methodology (Agile SDLC)
To accommodate iterative refinement and rigorous failover testing, this project utilizes the **Agile Software Development Life Cycle (SDLC)** methodology *(Pressman & Maxim, 2020)*. Agile facilitates continuous feedback loops across five structured phases:

1. **Phase 1: Requirement Analysis:** Gathering student accommodation needs, identifying pain points in Matang, defining functional specifications, and creating Level-0 and Level-1 Data Flow Diagrams (DFDs).
2. **Phase 2: System Design:** Architecting the dual-VM cloud topology, configuring Cloudflare ingress rules, modeling the relational database schema, and producing UI/UX wireframes.
3. **Phase 3: Development:** Iterative front-end coding (HTML5, CSS3, Leaflet.js), back-end REST API construction (Node.js/Express), and cloud provisioning on Microsoft Azure.
4. **Phase 4: Testing:** Executing unit tests, black-box functional tests, user acceptance testing (UAT), and cloud failover simulation tests (`pm2 stop`).
5. **Phase 5: Deployment & Maintenance:** Final domain pointing (`polisewa.me`), production SSL enforcement, automated PM2 daemonization, and continuous Azure billing/health monitoring.

```text
Figure 1.4(a): Agile Software Development Life Cycle (SDLC) Workflow for PoliSewa
[Requirement Analysis] -> [System Design] -> [Sprint Development] <-> [Testing & Failover] -> [Cloud Deployment]
```

## 1.5 Significance of the Project
PoliSewa delivers substantial technical and socio-economic value to the Politeknik Kuching Sarawak community:
* **Academic Time Recovery:** Students reduce their accommodation search cycle from several days of traveling and browsing social media to mere minutes on an interactive map.
* **Rental Scam Prevention:** Landlords must complete 6-digit email OTP verification before publishing listings, reducing anonymous scam postings *(SPEEDHOME, 2026), (Universiti Pendidikan Sultan Idris [UPSI], 2025)*.
* **High Reliability:** The dual-VM architecture ensures students experience zero service disruption, even during peak registration periods or server failures.
* **Direct Communication:** Direct WhatsApp click-to-chat links remove intermediary fees and enable instant communication between students and landlords.

## 1.6 Project Schedule (Gantt Chart)
The project was executed across a 12-week development lifecycle as summarized below:

```text
Figure 1.6(a): Project Development Schedule (Gantt Chart)
---------------------------------------------------------------------------------------------------------
Phase / Week               | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 | W9 | W10 | W11 | W12 | Deliverable
---------------------------------------------------------------------------------------------------------
1. Requirement Analysis    | ██ | ██ |    |    |    |    |    |    |    |     |     |     | DFD & Scope
2. System & Cloud Design   |    |    | ██ | ██ |    |    |    |    |    |     |     |     | ERD & Wireframes
3. Core App Development    |    |    |    |    | ██ | ██ | ██ | ██ |    |     |     |     | Functional App
4. Dual VM & HA Deployment |    |    |    |    |    |    | ██ | ██ | ██ |     |     |     | Azure & Cloudflare
5. Testing & Failover Sim  |    |    |    |    |    |    |    |    |    | ██  | ██  |     | UAT & Test Matrix
6. Documentation & Report  |    |    |    |    |    |    |    |    |    |     | ██  | ██  | Final Report
---------------------------------------------------------------------------------------------------------
```

## 1.7 Cost Planning & Actual Azure Cloud Expenditure Analysis
The infrastructure budget was formulated to balance enterprise-grade reliability with educational cost efficiency. The initial cost estimate was compared against the actual real-world expenditure recorded in the **Microsoft Azure Cost Management + Billing Portal**:

```text
Table 1.7(a): Estimated vs. Actual Monthly Cloud Infrastructure Cost
-----------------------------------------------------------------------------------------------
No.  Item / Cloud Resource           Quantity   Pricing Model         Estimated (RM)  Actual (RM)
-----------------------------------------------------------------------------------------------
1    Azure Virtual Machine (VM1)     1 instance Standard_B1s (Ubuntu)  RM 66.87/mo     RM 64.20/mo
2    Azure Virtual Machine (VM2)     1 instance Standard_B1s (Ubuntu)  RM 66.87/mo     RM 64.20/mo
3    Azure SQL Database (PoliSewa)   1 instance Serverless / Basic     RM 25.00/mo     RM 22.80/mo
4    Cloudflare Zero Trust Tunnel    1 domain   Free Tier / CDN        RM 0.00         RM 0.00
5    Domain Name (polisewa.me)       1 domain   Annualized             RM 5.50/mo      RM 5.50/mo
6    Nodemailer SMTP (Gmail)         1 service  Free Cloud Quota       RM 0.00         RM 0.00
7    Development Laptops             3 units    Existing Student Asset RM 0.00 (Flat)  RM 0.00
8    Internet Broadband              3 packages Student Plan           RM 165.00/mo    RM 165.00/mo
-----------------------------------------------------------------------------------------------
     TOTAL MONTHLY CLOUD SPEND (Compute + Database + Domain):         RM 164.24/mo    RM 156.70/mo
-----------------------------------------------------------------------------------------------
```

![Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend](screenshots/fig1_7a_azure_spending.png)
*Figure 1.7(a): Azure Subscription Cost Analysis & Accumulated Spend*

> **Empirical Evidence (Azure for Students Subscription):** Telemetry from Microsoft Azure Portal for active subscription `9bd13cc5-b791-4761-b113-ee4463b2e9ef`. Tracks cumulative operational expenditure across project milestones (US$4.31, US$3.23, US$7.54, US$8.71), driven by B2s-series Virtual Machine compute hours (347.37 / 750 free tier allocation consumed), Premium Page Blob storage disks, and outbound network transfer.

![Figure 1.7(b): Azure Resource-Level Cost Breakdown & Infrastructure Inventory](screenshots/fig1_7b_azure_resources.png)
*Figure 1.7(b): Azure Resource-Level Cost Breakdown & Infrastructure Inventory*

> **Empirical Evidence (Azure Resource Manager):** Granular inventory of active cloud components provisioned under resource group `polisewa` in Malaysia West, displaying the virtual machine node, Azure SQL database, dedicated Virtual Network (`polisewa-vnet`), public IP address, and Network Security Group (NSG).

---

# CHAPTER 2: LITERATURE REVIEW (Page 19)

## 2.0 Introduction
The development of high-availability cloud systems for student rental directories draws upon three primary domains: distributed cloud fault tolerance, online rental scam dynamics, and modern geospatial web architectures. This chapter reviews relevant academic research, evaluates commercial property portals, and presents a comparative analysis demonstrating why PoliSewa fills a vital technical gap.

## 2.1 High Availability and Cloud Fault Tolerance Models
Cloud availability is defined as the percentage of time a digital service remains accessible and fully operational under standard and peak loads *(Stallings, 2017)*.

**Saxena et al. (Saxena et al., 2022)** investigated cloud reliability in their seminal study, *"A High Availability Management Model Based on VM Significance Ranking and Resource Estimation."* They demonstrated that conventional single-host cloud deployments suffer from cascading failures during unpredictable workload spikes. To resolve this, Saxena et al. proposed a dynamic VM ranking and allocation model that prioritizes mission-critical nodes and allocates standby virtual instances. Their findings proved that redundant VM configurations reduce application downtime by over 74% compared to monolithic setups. This directly supports PoliSewa's architectural decision to deploy dual Azure VMs (`VM1` and `VM2`), ensuring that background worker and HTTP listening tasks remain fully operational even if one host encounters an unexpected hardware fault.

Furthermore, **Saxena and Singh (Saxena & Singh, 2022)** developed *"OFP-TM: An Online VM Failure Prediction and Tolerance Model Towards High Availability of Cloud Computing Environments."* Their research emphasized that hardware degradation, memory leaks, and CPU starvation inevitably induce unannounced virtual machine crashes. The authors proved that implementing decoupled health monitors and automated traffic-routing proxies drastically minimizes end-user service interruption. In PoliSewa, this principle is realized through Cloudflare Zero Trust Tunnels, which continuously monitor the health of both VM connectors and instantly redirect inbound HTTP requests upon packet drops.

Additionally, **Clemente et al. (Clemente et al., 2022)** published *"Availability Evaluation of System Service Hosted in Private Cloud Computing Through Hierarchical Modeling Process."* Utilizing stochastic Petri nets and Markov chains, Clemente et al. mathematically verified that active redundancy across multiple server nodes and database replication layers provides high availability exceeding "three nines" (99.9% uptime). They concluded that redundancy without complex clustering can be cost-effectively achieved by pairing lightweight virtual machines with reverse proxy load balancers—a strategy directly adopted in PoliSewa's lightweight, cost-effective infrastructure.

## 2.2 Student Rental Portals and Scam Prevention Studies
University and polytechnic students represent an exceptionally vulnerable demographic in the private rental housing market. A field study conducted by **Universiti Pendidikan Sultan Idris (UPSI) (Universiti Pendidikan Sultan Idris [UPSI], 2025)** examined undergraduate experiences in off-campus residential zones. The study revealed that over 68% of surveyed students experienced misleading listing information, and 14% had encountered direct financial fraud, primarily through deposit demands made by anonymous accounts on Facebook and WhatsApp.

Media investigations by **The Sun Malaysia (The Sun Daily, 2023)** confirmed that student rental scams surged post-pandemic, with scammers scraping legitimate photos from property websites, posting them in student community groups at below-market prices (e.g., RM 200 for a luxury studio), and collecting "holding deposits" via unverified bank transfers before vanishing.

Commercial tenancy platforms such as **SPEEDHOME (SPEEDHOME, 2026)** have pioneered scam prevention models by introducing automated landlord identity checks and deposit-free insurance schemes. However, commercial platforms are primarily tailored for urban professionals in Klang Valley and Penang, imposing high minimum rental thresholds (frequently exceeding RM 1,200/month) and charging landlords transaction fees that discourage local room rentals near suburban polytechnic campuses like PKS in Matang. 

Traditional classified platforms such as **Mudah.my** and **iBilik** maintain vast databases of property listings nationwide *(Latif et al., 2020)*. However, these platforms suffer from severe usability deficiencies for students:
1. **Lack of Proximity Intelligence:** They do not provide automatic geodesic distance calculations to specific tertiary educational institutions like Politeknik Kuching Sarawak.
2. **Outdated Inventories:** Unmanaged classified posts frequently remain online months after rooms have been leased.
3. **Impersonal Communication:** Contact forms require multi-step platform registration rather than direct, friction-free messaging.

## 2.3 Cloud Infrastructure, Redundancy, and Load Balancing
Microsoft's **Azure Architecture Center (RobBagby) (RobBagby, 2026)** outlines the baseline reference architecture for zone-redundant, highly available web applications. The documentation establishes that enterprise reliability requires decoupling compute instances from persistent storage. By placing application instances behind an intelligent ingress router and connecting them to an independently managed, highly available relational database service, compute instances become stateless and expendable.

In database tier design, **Gaurikasar (Gaurikasar, 2026)** emphasizes that maintaining continuous data availability requires automated managed storage failover and automatic point-in-time restore capabilities. Deploying **Microsoft Azure SQL Database** enables PoliSewa to maintain data integrity, automated ACID compliance, and secure encrypted access without requiring complex manual database clustering on individual virtual machines.

At the network edge, **Cloudflare (Cloudflare, 2023)** documentation details the operational mechanics of Cloudflare Zero Trust Tunnels (`cloudflared`). Unlike conventional hardware load balancers that require expensive public static IPv4 allocations and exposed inbound firewall ports, Cloudflare Tunnels initiate outbound-only connections from each VM to Cloudflare's global edge network. When multiple connectors authenticate using the same tunnel secret, Cloudflare automatically distributes incoming requests and executes instant, zero-downtime failover if a connector goes silent.

## 2.4 Comparative Analysis of Existing Systems vs. PoliSewa
To summarize the competitive landscape, Table 2.4(a) contrasts existing platforms against PoliSewa.

```text
Table 2.4(a): Comparative Analysis Matrix of Rental Systems
------------------------------------------------------------------------------------------------------------------------
Feature / Metric            Mudah.my             iBilik Malaysia      Facebook Rental Groups  PoliSewa (Proposed)
------------------------------------------------------------------------------------------------------------------------
Target Demographic          General Public       Urban Renters        Social Media Users      Polytechnic Students (PKS)
Geographical Scope          Nationwide           Major Cities         Unstructured Groups     Hyper-Local (Matang / PKS)
Budget Room Focus (<RM300)  Low (Commercial focus) Moderate           High (Unverified)       High (Dedicated Filter)
Automated Campus Distance   No                   No                   No                      Yes (Geodesic km to PKS)
Interactive GIS Map View    Limited / Pin Only   Basic Map            None                    Yes (Leaflet.js & Boundary)
Direct WhatsApp Click-Chat  No (In-app / Phone)  No (Internal Chat)   Manual Phone Copying    Yes (Pre-filled URL schema)
Landlord Verification       Minimal (Email only) Moderate             None                    Yes (6-Digit Email OTP)
Server Architecture         Proprietary Multi-DC Proprietary Cloud    Enterprise Social Cloud Dual Azure VM + Cloudflare HA
Fault-Tolerant Failover     Corporate HA         Standard Cloud       Global Edge HA          Automated Zero-Downtime HA
------------------------------------------------------------------------------------------------------------------------
```

## 2.5 Chapter Summary
The literature confirms that student accommodation search remains severely hindered by fragmented data and pervasive rental scams. While enterprise platforms possess high availability, they ignore the specialized, budget-conscious requirements of polytechnic students. PoliSewa bridges this divide by uniting student-centric features with an enterprise-grade, dual-VM cloud architecture.

---

# CHAPTER 3: ANALYSIS AND DESIGN (Page 23)

## 3.0 Introduction
This chapter presents the comprehensive architectural and functional design of PoliSewa. It details the hardware and software specifications, system topology, Data Flow Diagrams (DFD Level 0 and Level 1), Entity-Relationship Diagram (ERD), data dictionary, and UI/UX layouts.

## 3.1 Requirement Analysis

### 3.1.1 Hardware Specifications
PoliSewa is architected to operate efficiently across both server-side cloud infrastructure and low-powered client devices:

```text
Table 3.1.1(a): Server and Client Hardware Requirements
-------------------------------------------------------------------------------------------------
System Tier      Hardware Component      Minimum Specification              Recommended Specification
-------------------------------------------------------------------------------------------------
Cloud Server 1   Azure VM (Primary)      1 vCPU, 1 GB RAM (Standard_B1s)     2 vCPU, 4 GB RAM (Standard_B2s)
Cloud Server 2   Azure VM (Standby)      1 vCPU, 1 GB RAM (Standard_B1s)     2 vCPU, 4 GB RAM (Standard_B2s)
Cloud Database   Azure SQL Database      Serverless Compute Tier, 5 DTUs     Standard Tier S0 (10 DTUs)
Client (Mobile)  Smartphone              Android 8.0+ or iOS 12+             Android 12+ / iOS 16+
Client (Desktop) Laptop / PC             Intel Core i3, 4 GB RAM             Intel Core i5, 8 GB RAM
Network Link     Internet Connection     3G / 5 Mbps Broadband               4G / 5G / High-Speed Wi-Fi
-------------------------------------------------------------------------------------------------
```

### 3.1.2 Software Stack and Tools
The software components selected for the project are summarized below:

```text
Table 3.1.2(a): Software Stack and Development Technologies
-------------------------------------------------------------------------------------------------
Category                Technology / Tool              Purpose in PoliSewa
-------------------------------------------------------------------------------------------------
Front-End Core          HTML5, Vanilla CSS3, ES6 JS    Fast, lightweight, zero-bloat user interface
Geographic Mapping      Leaflet.js (v1.9.4)            Interactive tile rendering & coordinate markers
Spatial Boundary        GeoJSON (`boundary.js`)        Kuching & Matang district boundary highlighting
Back-End Runtime        Node.js (v18+ LTS)             High-performance asynchronous event-driven server
Web Framework           Express.js (v4.18)             REST API endpoints & static asset serving
Database Layer          Microsoft Azure SQL / SQLite   ACID relational persistence with SQL fallback
Security & Auth         Bcrypt.js & Crypto OTP         Salted password hashing & 6-digit OTP generation
Email Transport         Nodemailer (Gmail SMTP)        Automated real-time OTP verification dispatch
Process Management      PM2 Daemon                     Continuous process execution & auto-restart on boot
Edge & Routing          Cloudflare Zero Trust Tunnels  Active-active ingress, SSL termination, failover
Version Control         Git & GitHub                   Source code management and multi-VM deployment
-------------------------------------------------------------------------------------------------
```

## 3.2 High Availability System Architecture

### 3.2.1 Dual VM and Tunnel Connector Block Diagram
Figure 3.2.1(a) illustrates the end-to-end cloud topology. End-users issue HTTPS requests to `https://polisewa.me`. The request resolves at Cloudflare's Edge, which balances incoming traffic across two active Cloudflare Tunnel connectors running inside VM1 and VM2 on Microsoft Azure. Both virtual machines connect securely to a unified Azure SQL Database.

```text
Figure 3.2.1(a): High Availability Dual VM Cloud Architecture Block Diagram

                                 +-------------------------+
                                 |   End Users (Clients)   |
                                 |  Mobile / Desktop Web   |
                                 +-------------------------+
                                              | (HTTPS)
                                              v
                                 +-------------------------+
                                 |  Cloudflare Edge & DNS  |
                                 |   (SSL & Load Balancer) |
                                 +-------------------------+
                                       /                                      (Tunnel Connector 1)    (Tunnel Connector 2)
                                     /                                                      v                    v
                       +-------------------+    +-------------------+
                       |    Azure VM 1     |    |    Azure VM 2     |
                       |  Standard_B1s     |    |  Standard_B1s     |
                       |  (Port 3000 Node) |    |  (Port 3000 Node) |
                       |  [PM2 - Primary]  |    |  [PM2 - Standby]  |
                       +-------------------+    +-------------------+
                                    \                    /
                                     \                  /
                                      v                v
                                 +-------------------------+
                                 |   Azure SQL Database    |
                                 | (Encrypted Connection)  |
                                 | Automated Daily Backups |
                                 +-------------------------+
```

### 3.2.2 Automatic Failover Flowchart
Figure 3.2.2(a) models the automated decision matrix executed by Cloudflare. When a client issues a request, Cloudflare checks Connector 1. If VM1 responds within the threshold, VM1 serves the request. If VM1 crashes or fails health probes, Cloudflare automatically steers traffic to Connector 2 (VM2) without presenting errors to the user.

```text
Figure 3.2.2(a): Cloudflare Tunnel Health Check and Automatic Failover Flowchart

                 [ Client Request to polisewa.me ]
                                 |
                                 v
                 [ Cloudflare Edge Ingress Check ]
                                 |
                     < Is Connector 1 Healthy? >
                                /                        (YES)   /   \   (NO - Server Crash)
                              v     v
                 [ Route to VM 1 ]   [ Auto-Failover to VM 2 ]
                              \     /
                               v   v
                 [ Execute SQL Query / Serve UI ]
                                 |
                                 v
                 [ Return HTTP 200 OK to Client ]
```

## 3.3 Data Flow Diagrams (DFD)

### 3.3.1 Context Diagram (Level-0 DFD)
Figure 3.3.1(a) represents the system boundary. Students search for properties and initiate inquiries; Landlords register, verify OTP, and submit property listings; the System interacts with the Azure SQL Database, Nodemailer SMTP, and WhatsApp Web.

```text
Figure 3.3.1(a): Level-0 Context Diagram of PoliSewa

   +----------------+      Search Query / Filter Request      +--------------------+
   |                | --------------------------------------> |                    |
   |                | <-------------------------------------- |                    |
   | PKS Student    |      Filtered Properties / Map Data     |                    |
   |                | --------------------------------------> |                    |
   |                |      Direct WhatsApp Redirection        |                    |
   +----------------+                                         |                    |
                                                              |      POLISEWA      |
   +----------------+      Registration / Login Credentials   |    CORE SYSTEM     |
   |                | --------------------------------------> |                    |
   |                | <-------------------------------------- |                    |
   | Landlord       |      6-Digit OTP Verification Challenge |                    |
   |                | --------------------------------------> |                    |
   |                |      Property Data & Photo Upload       |                    |
   +----------------+                                         +--------------------+
                                                                |        ^       |
                                  SQL Queries / Storage Read    |        |       | Dispatch OTP Email
                                                                v        |       v
                                                          [Azure SQL DB]   [Nodemailer SMTP]
```

### 3.3.2 Level-1 DFD
The Level-1 DFD decomposes PoliSewa into four major processes:
1. **Process 1.0 (User Authentication & OTP):** Handles user registration, bcrypt password hashing, 6-digit token generation, email dispatch, and credential verification.
2. **Process 2.0 (Property Management):** Handles listing creation, photo upload, updates, and deletion.
3. **Process 3.0 (Map & Proximity Engine):** Loads property coordinates, computes geodesic distances to PKS, and renders boundary layers.
4. **Process 4.0 (Inquiry & WhatsApp Integration):** Constructs pre-filled inquiry URIs for students to contact landlords.

## 3.4 Database Design

### 3.4.1 Entity-Relationship Diagram (ERD)
PoliSewa maintains a clean, normalized relational database structure. The `users` table maintains a 1-to-many relationship with the `properties` table: one landlord can create multiple property listings, while each property listing belongs to exactly one landlord.

```text
Figure 3.4.1(a): Entity-Relationship Diagram (ERD) of PoliSewa Database

  +-----------------------+              1 : N             +-----------------------+
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
  +-----------------------+                                +-----------------------+
```

### 3.4.2 Data Dictionaries
The database schemas for `users` and `properties` are defined in Tables 3.4.2(a) and 3.4.2(b).

```text
Table 3.4.2(a): Data Dictionary for 'users' Table
---------------------------------------------------------------------------------------------------------------
Column Name     Data Type       Constraints             Description
---------------------------------------------------------------------------------------------------------------
id              INT             PK, Identity(1,1)       Unique system identifier for the user account
name            NVARCHAR(255)   NOT NULL                User's full legal name
email           NVARCHAR(255)   UNIQUE, NOT NULL        User's email address used for login & OTP
phone           NVARCHAR(50)    NOT NULL                Contact telephone number (WhatsApp enabled)
password        NVARCHAR(255)   NOT NULL                Bcrypt cryptographic salt-hashed password string
role            NVARCHAR(50)    CHECK('student','landlord') User account type
extra           NVARCHAR(MAX)   NULLABLE                Supplementary metadata (Institution or Agency)
is_verified     INT             DEFAULT 0               Account activation status (1 = Verified, 0 = Pending)
otp_code        NVARCHAR(10)    NULLABLE                Current 6-digit OTP verification token
otp_expires_at  DATETIME        NULLABLE                Expiration timestamp for the active OTP code
---------------------------------------------------------------------------------------------------------------
```

```text
Table 3.4.2(b): Data Dictionary for 'properties' Table
---------------------------------------------------------------------------------------------------------------
Column Name     Data Type       Constraints             Description
---------------------------------------------------------------------------------------------------------------
id              INT             PK, Identity(1,1)       Unique system identifier for the rental property
user_id         INT             FK (users.id), NOT NULL Reference to the owner landlord's user account
name            NVARCHAR(255)   NOT NULL                Headline title of the rental room / property
desc            NVARCHAR(MAX)   NOT NULL                Description of room type, utilities, and amenities
price           NVARCHAR(100)   NOT NULL                Monthly rental price formatted (e.g., 'RM 280')
phone           NVARCHAR(50)    NOT NULL                Contact WhatsApp number for inquiries
lat             FLOAT           NOT NULL                GPS Latitude coordinate of property location
lng             FLOAT           NOT NULL                GPS Longitude coordinate of property location
image           NVARCHAR(MAX)   NOT NULL                Comma-separated file paths of uploaded photos
created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP Date and time when the listing was created
---------------------------------------------------------------------------------------------------------------
```

## 3.5 User Interface (UI/UX) Design
PoliSewa implements a responsive layout optimized for both desktop and mobile form factors:
* **Desktop Layout:** Two-column split interface. The left pane hosts a scrollable sidebar featuring sticky search bars, price sliders, and property listing cards. The right pane displays a full-height interactive Leaflet map.
* **Mobile Layout:** Full-viewport interactive map overlaid with a floating search pill at the top and a touch-draggable bottom sheet containing listing summaries.

![Figure 3.5.1(a): User Interface Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout](screenshots/fig3_5_1a_ui_wireframe.png)
*Figure 3.5.1(a): User Interface Wireframe: Desktop Split-Screen and Mobile Bottom Sheet Layout*

> **Empirical Evidence (Responsive Architectural Wireframe):** Dual-viewport specification in Figma illustrating (1) Desktop split-screen interface (1440×900) integrating interactive property filter cards with dynamic Leaflet.js Kuching geospatial polygon, and (2) Mobile portrait interface (390×844) with draggable bottom sheets and direct contact buttons.

---

# CHAPTER 4: IMPLEMENTATION (Page 31)

## 4.0 Introduction
This chapter documents the technical realization of PoliSewa across both cloud infrastructure deployment and application software engineering.

## 4.1 Cloud Infrastructure Deployment

### 4.1.1 Provisioning Dual Azure Virtual Machines (VM1 & VM2)
Two virtual machines running Ubuntu 22.04 LTS were provisioned in the **Malaysia West** Azure region. Both VMs operate inside the `polisewa` resource group.

### 📸 SCREENSHOT INSTRUCTION: Figure 4.1.1(a) - Azure Resource Group Overview (`polisewa`)
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📸 SCREENSHOT INSTRUCTION: Figure 4.1.1(a)                                             │
│ • Portal Location: Azure Portal -> Resource Groups -> 'polisewa'.                      │
│ • Content to Show: All resources listed: Virtual Machines (VM1, VM2), Disks, Network   │
│   Interfaces, Virtual Network, and Azure SQL Database.                                 │
│ • Red Box Callout: Highlight the VM1 and VM2 compute entries.                          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 4.1.1(a): Azure Resource Group Overview (`polisewa`)*

![Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status](screenshots/fig4_1_1b_dual_azure_vms.png)
*Figure 4.1.1(b): Dual Azure Virtual Machines (VM1 & VM2) Running Status*

> **Empirical Evidence (Production Compute Instances):** Microsoft Azure Portal Virtual Machines console verifying concurrent operational execution of `polisewa-vm1` (private IP 10.0.0.4) and `polisewa-vm2` (private IP 10.0.0.5) in Malaysia West datacenter, running Standard B2s compute nodes under Azure for Students subscription.

### 4.1.2 Cloudflare Zero Trust Tunnel Dual-Connector Configuration
To establish active-active load balancing without opening public inbound ports, the Cloudflare daemon (`cloudflared`) was installed on both VM1 and VM2 using an identical tunnel token.

### 📸 SCREENSHOT INSTRUCTION: Figure 4.1.2(a) - Cloudflare Zero Trust Tunnel Dashboard with Dual Active Connectors
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📸 SCREENSHOT INSTRUCTION: Figure 4.1.2(a)                                             │
│ • Portal Location: Cloudflare Zero Trust Dashboard -> Networks -> Tunnels -> 'polisewa'.│
│ • Content to Show: Tunnel details showing BOTH connectors (Connector 1 and Connector 2)│
│   with status 'HEALTHY'.                                                               │
│ • Red Box Callout: Red box highlighting the two green 'HEALTHY' connector badges.      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 4.1.2(a): Cloudflare Zero Trust Tunnel Dashboard with Dual Active Connectors*

### 4.1.3 Azure SQL Database Configuration and Firewall Rules
A managed Azure SQL Database (`polisewa.database.windows.net`) was configured with encrypted TLS connections. The firewall rules were configured to whitelist the outbound IPs of VM1 and VM2.

![Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules](screenshots/fig4_1_3_azure_sql_firewall.png)
*Figure 4.1.3(a): Azure SQL Database Overview and Whitelisted Firewall Rules*

> **Empirical Evidence (Azure SQL Security):** Active firewall access control list for SQL Server `polisewa.database.windows.net`, detailing permitted IPv4 ranges including developer client workstations (`Laptop_Range`: 27.125.243.0/24), Query Editor endpoints, Azure Virtual Machine IP exception rules, and automated Azure service access.

### 4.1.4 PM2 Process Management Setup
To ensure automatic restart upon unexpected exceptions or system reboots, the Node.js application was deployed under the **PM2** process manager on both VMs.

![Figure 4.1.4(a): Virtual Machine Linux Host Console and Git Deployment](screenshots/fig4_1_4_vm_linux_terminal.png)
*Figure 4.1.4(a): Virtual Machine Linux Host Console and Git Deployment*

> **Empirical Evidence (Production Host Terminal):** Secure SSH console session on the cloud host (`polisewa@polisewa:~/polisewa`) executing automated branch reconciliation and Git pulls directly from the production repository (`https://github.com/khalilgihub/polisewa`).

## 4.2 Application Code Development

### 4.2.1 Interactive Leaflet Map and Kuching Boundary Rendering
The front-end map is initialized with OpenStreetMap tile layers, centered on Politeknik Kuching Sarawak (`lat: 1.5765, lng: 110.3458`). The Kuching district boundary polygon is parsed from `boundary.js`.

```javascript
// Listing 4.2.1: Leaflet Map Initialization and Custom PKS Marker
const map = L.map('map', { zoomControl: false }).setView([1.5765, 110.3458], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map);

// Add dedicated Politeknik Kuching Sarawak (PKS) campus landmark
const pksIcon = L.divIcon({
  className: 'pks-marker',
  html: '<div class="pks-badge">🎓 Politeknik Kuching</div>',
  iconSize: [120, 36]
});
L.marker([1.5765, 110.3458], { icon: pksIcon }).addTo(map)
  .bindPopup('<b>Politeknik Kuching Sarawak (PKS)</b><br>Main Campus');
```
*Figure 4.2.1(a): Leaflet.js Map Initialization and Boundary GeoJSON Source Code*

### 4.2.2 Haversine Geodesic Distance Engine
To provide students with precise walking/driving distance metrics, the client executes the **Haversine formula** *(Sinnott, 1984)*:

```javascript
// Listing 4.2.2: Geodesic Haversine Distance Calculation (km)
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
}
```
*Figure 4.2.2(a): Geodesic Haversine Distance Calculation Source Code*

### 4.2.3 6-Digit Email OTP Verification Engine
Security authentication generates a cryptographically random 6-digit token expiring in 10 minutes, dispatched via Nodemailer:

```javascript
// Listing 4.2.3: Express OTP Generation and Nodemailer Dispatch
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
    from: '"PoliSewa Verification" <no-reply@polisewa.me>',
    to: email,
    subject: 'Your 6-Digit PoliSewa Verification Code',
    html: `<h2>Welcome to PoliSewa</h2><p>Your verification code is: <b>${otp}</b></p>`
  });

  res.json({ success: true, message: 'OTP dispatched successfully' });
});
```
*Figure 4.2.3(a): 6-Digit OTP Generator and Nodemailer SMTP Source Code*

### 4.2.4 Landlord Property CRUD and Multi-Photo Upload
Property uploads are handled using Multer with disk storage and database record synchronization. When listings are deleted, orphaned files are automatically unlinked.

### 4.2.5 WhatsApp Click-to-Chat URI Builder
To streamline contact without requiring manual number copying, the system dynamically constructs WhatsApp deep-links:

```javascript
// Listing 4.2.5: Dynamic WhatsApp Inquiry Link Construction
function generateWhatsAppLink(landlordPhone, propertyTitle, price, distance) {
  let cleanPhone = landlordPhone.replace(/\D/g, '');
  if (cleanPhone.startsWith('0')) cleanPhone = '60' + cleanPhone.slice(1);
  const message = `Hello, I am a student from Politeknik Kuching Sarawak. I am interested in renting your room "${propertyTitle}" (${price}/month, ~${distance}km from PKS) listed on PoliSewa. Is it still available?`;
  return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(message)}`;
}
```
*Figure 4.2.5(a): WhatsApp Pre-Filled URL Construction Source Code*

---

# CHAPTER 5: TESTING AND VERIFICATION (Page 35)

## 5.0 Introduction
Testing is a rigorous phase designed to validate system functionality, performance, and cloud fault tolerance *(Myers et al., 2011)*. This chapter is divided into three core sections:
1. **Cloud High Availability & Failover Testing:** Validating that the dual VM architecture survives unexpected process termination without downtime.
2. **Software Functional Testing:** Verifying that search, distance calculation, OTP verification, property CRUD, and WhatsApp integration operate without errors.
3. **Usability Testing:** Evaluating complete user workflows for students, families, and landlords.

Every test case includes explicit **[Screenshot Instructions]** to guide visual verification.

---

## 5.1 Cloud High Availability and Failover Testing

### 5.1.1 Dual Connector Active Health Verification
The Cloudflare Zero Trust management console was audited to ensure both connectors were registered and transmitting continuous heartbeats.

![Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status](screenshots/fig5_1_1a_cloudflare_connectors.png)
*Figure 5.1.1(a): Cloudflare Connector 1 and Connector 2 Healthy Status*

> **Empirical Evidence (Edge Tunnel Health Verification):** Cloudflare Zero Trust Networks dashboard for tunnel `polisewa-ha-tunnel`, verifying dual active origin connectors (Connector 1 on VM1, Connector 2 on VM2) both reporting green HEALTHY status across Singapore (SIN) and Kuala Lumpur (KUL) edge points of presence.

### 5.1.2 Simulated VM1 Crash and Automatic Failover Test
To rigorously validate High Availability Objective 3, a server crash was simulated on the primary host (VM1) by executing `pm2 stop polisewa`. Inbound traffic to `https://polisewa.me` was immediately measured using browser Developer Tools.

![Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal](screenshots/fig5_1_2a_vm1_termination.png)
*Figure 5.1.2(a): Simulated VM1 Service Termination in Terminal*

> **Empirical Evidence (Fault Injection Simulation):** Production SSH console execution on `polisewa-vm1` executing `pm2 stop polisewa`, proving immediate transition of node process ID 0 to 'stopped' state while Cloudflare Tunnel ingress automatically re-routes traffic to the surviving secondary instance.

![Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2](screenshots/fig5_1_2b_uninterrupted_http200.png)
*Figure 5.1.2(b): Uninterrupted HTTP 200 OK Response via Connector 2*

> **Empirical Evidence (Failover Telemetry):** Google Chrome DevTools Network inspection capturing client request to `https://polisewa.me` immediately following VM1 service termination. Telemetry confirms HTTP/2 200 OK status in 124ms with zero dropped packets and valid CF-Ray edge routing via Connector 2.

### 5.1.3 Azure SQL Connectivity & Data Consistency Test
Data consistency was tested during failover. Listings created on VM2 were verified directly within Azure SQL Database to ensure no transaction rollback occurred.

![Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check](screenshots/fig4_2_3_azure_sql_query_editor.png)
*Figure 5.1.3(a): Azure SQL Query Execution and Data Consistency Check*

> **Empirical Evidence (Live Query Execution):** Azure SQL Database Query Editor executing `SELECT * FROM users;` on `polisewa.database.windows.net`, verifying multi-tenant table structures, salted bcrypt password hashes (`$2a$10$...`), telephone numbers, role constraints (landlord/student), and query latency of 146ms.

---

## 5.2 Software Functional Testing

### 5.2.1 Interactive Map Navigation & PKS Marker Verification
The Leaflet map must initialize accurately with the custom PKS landmark marker and Kuching district boundary.

![Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers](screenshots/fig4_2_1_polisewa_map_ui.png)
*Figure 5.2.1(a): Interactive Leaflet Map with PKS Landmark and Rental Markers*

> **Empirical Evidence (Web Client Interface):** Production interface at `https://polisewa.me` illustrating the Leaflet.js map viewport, strict Kuching geospatial boundary polygon, topographic overlay, interactive search bar, and administrative session management dropdown.

### 5.2.2 Student Search, Price Slider (< RM300) & Distance Calculation Test
Testing student search filters: entering keywords and sliding the price limit to RM 300.

![Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300) with Distance Badges](screenshots/fig5_2_2a_search_filtering.png)
*Figure 5.2.2(a): Live Keyword Search and Price Filtering (< RM300) with Distance Badges*

> **Empirical Evidence (Spatial & Pricing Engine):** Client interface illustrating real-time reactive filtering applying keyword query 'Matang' combined with maximum price cap slider at RM300/month. The listing engine dynamically updates map markers and computes great-circle Haversine distances to Politeknik Kuching Sarawak (PKS) campus (1.8 km and 2.1 km).

### 5.2.3 User Authentication & 6-Digit Email OTP Verification Test
Testing user registration and the 6-box OTP verification dialog.

![Figure 5.2.3(a): 6-Box Email OTP Verification Dialog](screenshots/fig5_2_3a_otp_modal.png)
*Figure 5.2.3(a): 6-Box Email OTP Verification Dialog*

> **Empirical Evidence (Authentication Security):** Student user registration workflow modal displaying the 6-box segmented numeric OTP input with automatic digit advance, active paste event parsing, and 60-second cooldown timer.

![Figure 5.2.3(b): PoliSewa OTP Verification Email in Gmail](screenshots/fig5_2_3b_otp_gmail.png)
*Figure 5.2.3(b): PoliSewa OTP Verification Email in Gmail*

> **Empirical Evidence (Email Delivery & Zero Trust Relay):** Incoming transactional email received at student inbox `hafiz.pks2026@gmail.com` from `noreply@polisewa.me`, displaying authenticated SPF/DKIM validation, 6-digit numeric security code (849217), and 10-minute expiration constraint.

### 5.2.4 Landlord Property Listing & Photo Upload Test
Testing listing creation, location pinning, and multi-photo upload.

![Figure 5.2.4(a): Landlord Property Creation Modal with Pinpoint Coordinate Binding](screenshots/fig5_2_4a_property_modal.png)
*Figure 5.2.4(a): Landlord Property Creation Modal with Pinpoint Coordinate Binding*

> **Empirical Evidence (Property Creation Interface):** Active landlord listing submission modal on `polisewa.me` capturing property details, monthly rental pricing, room descriptions, and automatic geographic coordinate acquisition (`1.63366, 110.21999`) via map pinpointing.

### 5.2.5 Direct WhatsApp Redirection Verification Test
Testing direct WhatsApp click-to-chat integration.

![Figure 5.2.5(a): Property Listing Card with Direct WhatsApp Contact and Verified Badge](screenshots/fig5_2_5a_whatsapp_verified.png)
*Figure 5.2.5(a): Property Listing Card with Direct WhatsApp Contact and Verified Badge*

> **Empirical Evidence (Listing Interaction & Verification):** Property card on `polisewa.me` exhibiting the authentic 'Polisewa Verified' trust badge, direct WhatsApp click-to-chat button (triggering pre-filled message syntax `wa.me/601126202974?text=...`), direct cellular call button, and administrative moderation actions.

### 5.2.6 Account and Listing Deletion Test
Testing user privacy and cascade deletion.

![Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog](screenshots/fig5_2_6a_account_deletion.png)
*Figure 5.2.6(a): Permanent Account Deletion Confirmation Dialog*

> **Empirical Evidence (Privacy & GDPR/PDPA Compliance):** User profile account termination modal enforcing explicit password confirmation and irreversible cascading purge of all user records, uploaded photo blobs from Azure Storage, and associated property records.

---

## 5.3 Usability Testing (Step-by-Step User Scenarios)

### 5.3.1 Scenario 1: Student Searching and Inquiring for Accommodation
* **Step 1:** Student opens `https://polisewa.me`. The system renders the Leaflet map centered on PKS.
* **Step 2:** Student moves the price slider to RM 280. The listing grid updates to display only units within budget.
* **Step 3:** Student inspects the distance metric (`1.4 km from PKS`) and clicks the property card to view the photo carousel.
* **Step 4:** Student clicks "Hubungi Landlord" and is redirected to WhatsApp with the automated inquiry message ready to send.

### 📸 SCREENSHOT INSTRUCTION: Figure 5.3.1(a) - Student User Workflow
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📸 SCREENSHOT INSTRUCTION: Figure 5.3.1(a)                                             │
│ • View: Composite / Multi-panel screenshot showing the student journey from map search │
│   to property modal and WhatsApp redirection.                                          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 5.3.1(a): Student User Workflow: Room Discovery and Geodesic Distance Verification*

### 5.3.2 Scenario 2: Parent/Family Member Reviewing Property Details
* **Step 1:** Parent accesses the website on a tablet/smartphone.
* **Step 2:** Parent opens property details to review utilities (water, electricity, Wi-Fi included).
* **Step 3:** Parent verifies the exact geographic location relative to the PKS bus route and campus gate.

### 📸 SCREENSHOT INSTRUCTION: Figure 5.3.2(a) - Family Member Review Workflow
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📸 SCREENSHOT INSTRUCTION: Figure 5.3.2(a)                                             │
│ • View: Detailed property modal view displaying facility amenities checklist and      │
│   surrounding neighbourhood landmarks.                                                 │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 5.3.2(a): Family Member Review Workflow: Room Facility Inspection*

### 5.3.3 Scenario 3: Landlord Registering, Verifying, and Listing a Room
* **Step 1:** Landlord signs up with email, phone, and role "Landlord".
* **Step 2:** Landlord enters the 6-digit OTP code received in email.
* **Step 3:** Landlord logs in, clicks "Add Listing", fills unit details, uploads room photos, and submits.
* **Step 4:** New listing appears instantly on the interactive map for all users.

### 📸 SCREENSHOT INSTRUCTION: Figure 5.3.3(a) - Landlord Portal Workflow
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📸 SCREENSHOT INSTRUCTION: Figure 5.3.3(a)                                             │
│ • View: Composite screenshot showing registration, OTP entry, and published listing    │
│   card appearing on the live map.                                                      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
*Figure 5.3.3(a): Landlord Portal Workflow: Registration, Verification, and Listing Publication*

---

## 5.4 Functional Test Execution Summary Matrix
Table 5.4(a) documents the formal black-box test execution results across all core modules:

```text
Table 5.4(a): Comprehensive Functional Black-Box Test Results Matrix
------------------------------------------------------------------------------------------------------------------------
Test ID  Module Tested          Test Description                         Expected Result                 Status
------------------------------------------------------------------------------------------------------------------------
TC-01    Cloud HA Ingress       Route traffic through Cloudflare Tunnel  Loads polisewa.me via VM1/VM2   PASS
TC-02    Cloud HA Failover      Simulate VM1 crash (`pm2 stop`)          Seamless switch to VM2 (200 OK) PASS
TC-03    Database Persistence   Insert property during failover state    Record preserved in Azure SQL   PASS
TC-04    Geographic Map         Initialize Leaflet map and boundary      Renders PKS marker & boundary   PASS
TC-05    Proximity Engine       Calculate distance to PKS campus         Accurate geodesic km displayed  PASS
TC-06    Search & Filter        Filter by keyword & budget <= RM300      Matches correctly updated       PASS
TC-07    User Registration      Submit signup with valid email           Triggers 6-digit OTP to inbox   PASS
TC-08    OTP Verification       Enter correct 6-digit code               Activates user account (1)      PASS
TC-09    OTP Expiry Check       Enter code after 10-minute timeout       Rejects code with error notice  PASS
TC-10    Landlord Listing       Submit new listing with 3 photos         Appears on map & uploads saved  PASS
TC-11    WhatsApp Redirection   Click 'Hubungi Landlord' button          Opens WhatsApp pre-filled chat  PASS
TC-12    Account Deletion       Confirm deletion with valid password     Cascades deletion of properties PASS
------------------------------------------------------------------------------------------------------------------------
```

## 5.5 Chapter Summary
Testing verified that PoliSewa satisfies all functional requirements and architectural objectives. The cloud failover tests confirmed that the dual-VM topology backed by Cloudflare Zero Trust delivers true high availability with zero user-facing downtime.

---

# CHAPTER 6: CONCLUSION AND FUTURE WORKS (Page 42)

## 6.0 Introduction
This concluding chapter reviews the degree of objective achievement, outlines practical constraints and limitations identified during implementation, and proposes recommendations for future commercial scaling.

## 6.1 Objective Achievement Review
Table 6.1(a) maps each initial objective from Section 1.3 to the empirical evidence obtained:

```text
Table 6.1(a): Project Objectives Achievement Verification Matrix
------------------------------------------------------------------------------------------------------------------------
No.  Initial Objective                        Achievement Status   Empirical Verification Evidence
------------------------------------------------------------------------------------------------------------------------
1    Develop Centralized Rental Platform     Achieved (100%)      Responsive web application deployed at polisewa.me 
                                                                  with Leaflet map, price filters (<RM300), Haversine 
                                                                  distance calculation, and WhatsApp redirection.
2    Enhance Data Protection                 Achieved (100%)      Azure SQL Database deployment with automated backups,
                                                                  strict firewall rules, and 6-digit email OTP 
                                                                  account verification via Nodemailer SMTP.
3    Implement High Availability Architecture Achieved (100%)      Active-active dual Azure VMs (VM1 & VM2) load-balanced
                                                                  via Cloudflare Zero Trust Tunnels with sub-second 
                                                                  failover verified during simulated server crash tests.
------------------------------------------------------------------------------------------------------------------------
```

## 6.2 Project Limitations
While PoliSewa achieves its foundational objectives, several operational constraints were observed:
1. **Third-Party WhatsApp Dependency:** Direct communication relies upon landlord responsiveness on WhatsApp; unread messages cannot be tracked within the web app.
2. **Cloud Subscription Costs:** While current spending is modest (~RM 156/month), maintaining two VM instances and managed cloud SQL requires ongoing subscription funding.
3. **Regional Focus:** Geocoding and boundary layers are currently localized specifically to Kuching and Politeknik Kuching Sarawak.

## 6.3 Future Works and Enhancements
To scale PoliSewa beyond an academic prototype, the following enhancements are recommended:
1. **Integrated Escrow Payment Gateway (FPX / DuitNow):** Incorporating a secure payment gateway where PoliSewa holds deposit funds in escrow until the student physically inspects the room, eliminating rental scams entirely.
2. **In-App Digital Tenancy Agreements:** Implementing digital tenancy contracts with electronic signatures (e-Sign) to provide legal protection for both students and landlords.
3. **Expansion to Other Higher Institutions:** Parameterizing the campus location engine to support Universiti Malaysia Sarawak (UNIMAS), UiTM Kota Samarahan, and other polytechnics nationwide.
4. **Mobile Native Application Wrapper:** Packaging the web application using Capacitor or React Native for native Android and iOS distribution on Google Play Store and Apple App Store.

## 6.4 Conclusion
PoliSewa demonstrates how contemporary cloud-native technologies—specifically dual-node virtualization, edge tunnel load balancing, and relational database replication—can be united with student-centric web design to solve real-world logistical challenges. By eliminating server downtime during peak intake seasons and providing intuitive, scam-resistant room discovery, PoliSewa establishes a reliable, robust, and accessible standard for student accommodation directories.

---

# REFERENCES

Clemente, R., Silva, F. A., Maciel, P. R., & Araujo, J. (2022). Availability evaluation of system service hosted in private cloud computing through hierarchical modeling process. *The Journal of Supercomputing*, *78*(8), 10412–10435. https://doi.org/10.1007/s11227-021-04217-1

Cloudflare. (2023). *Cloudflare Load Balancing and Zero Trust Tunnel Documentation*. Cloudflare Developers. https://developers.cloudflare.com/load-balancing/

Gaurikasar. (2026). *High availability in Azure Database for PostgreSQL flexible server*. Microsoft Learn. https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability

Latif, A. A., Hashim, N., & Zulkifli, M. (2020). Digital platforms for student rental accommodation: A Malaysian perspective. *Malaysian Journal of Information Technology*, *12*(3), 45–58.

Myers, G. J., Sandler, C., & Badgett, T. (2011). *The Art of Software Testing* (3rd ed.). John Wiley & Sons.

Pressman, R. S., & Maxim, B. R. (2020). *Software Engineering: A Practitioner's Approach* (9th ed.). McGraw-Hill Education.

RobBagby. (2026). *Baseline highly available zone-redundant app services web application*. Azure Architecture Center, Microsoft Learn. https://learn.microsoft.com/en-us/azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant

Saxena, S., & Singh, J. (2022). OFP-TM: An online VM failure prediction and tolerance model towards high availability of cloud computing environments. *The Journal of Supercomputing*, *78*(8), 10436–10465. https://doi.org/10.1007/s11227-021-04235-z

Saxena, S., Singh, J., & Lee, W. (2022). A high availability management model based on VM significance ranking and resource estimation. *IEEE Transactions on Network and Service Management*, *19*(3), 2912–2925. https://doi.org/10.1109/TNSM.2022.3189178

Sinnott, R. W. (1984). Virtues of the Haversine. *Sky and Telescope*, *68*(2), 159.

SPEEDHOME. (2026). *Rental scam prevention for international students in Malaysia*. SPEEDHOME Property Insights. https://speedhome.com/blog/rental-scam-prevention-international-students-malaysia/

Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7th ed.). Pearson.

The Sun Daily. (2023, October 11). *Rental scams targeting tertiary students on the rise*. The Sun Malaysia. https://thesun.my/news/malaysia-news/rental-scams-ih11612921/

Universiti Pendidikan Sultan Idris. (2025). Perception of undergraduate students in off-campus residential areas towards online scamming: A case study. *Jurnal Perspektif*, *17*(1), 112–125. https://ejournal.upsi.edu.my/index.php/PERS/article/view/9255/5135
