"""
Converts PoliSewa final report citations to IEEE / Numbered format [1] - [14].
Updates final_report.md, final_report.html, and recompiles final_report.pdf.
"""
import os
import re
import subprocess

BASE_DIR = r"c:\Users\abdul\OneDrive\Documents\polisewa"
MD_PATH = os.path.join(BASE_DIR, "final_report.md")
HTML_PATH = os.path.join(BASE_DIR, "final_report.html")
PDF_PATH = os.path.join(BASE_DIR, "final_report.pdf")

# 1. Update Markdown
with open(MD_PATH, "r", encoding="utf-8") as f:
    md = f.read()

# Replacements in Markdown
replacements = [
    (r"\(Pressman & Maxim, 2020\)", "[6]"),
    (r"\(UPSI, 2025; SPEEDHOME, 2026\)", "[11], [14]"),
    (r"\(Stallings, 2017\)", "[12]"),
    (r"Saxena et al\. \(2022\)", "Saxena et al. [9]"),
    (r"Saxena and Singh \(2022\)", "Saxena and Singh [8]"),
    (r"Clemente et al\. \(2022\)", "Clemente et al. [1]"),
    (r"Universiti Pendidikan Sultan Idris \(UPSI, 2025\)", "Universiti Pendidikan Sultan Idris (UPSI) [14]"),
    (r"The Sun Malaysia \(2023\)", "The Sun Malaysia [13]"),
    (r"SPEEDHOME \(2026\)", "SPEEDHOME [11]"),
    (r"\(Latif et al\., 2020\)", "[4]"),
    (r"Azure Architecture Center \(RobBagby, n\.d\.\)", "Azure Architecture Center (RobBagby) [7]"),
    (r"Gaurikasar \(2026\)", "Gaurikasar [3]"),
    (r"Cloudflare \(2023\)", "Cloudflare [2]"),
    (r"\(Sinnott, 1984\)", "[10]"),
    (r"\(Myers et al\., 2011\)", "[5]"),
]

for pattern, repl in replacements:
    md = re.sub(pattern, repl, md)

# Update References heading in MD to IEEE style
ieee_refs_md = """# REFERENCES

[1] R. Clemente, F. A. Silva, P. R. Maciel, and J. Araujo, "Availability evaluation of system service hosted in private cloud computing through hierarchical modeling process," *The Journal of Supercomputing*, vol. 78, no. 8, pp. 10412-10435, 2022. https://doi.org/10.1007/s11227-021-04217-1

[2] Cloudflare, "Cloudflare Load Balancing and Zero Trust Tunnel Documentation," *Cloudflare Developers*, Oct. 2023. [Online]. Available: https://developers.cloudflare.com/load-balancing/

[3] Gaurikasar, "High availability in Azure Database for PostgreSQL flexible server," *Microsoft Learn*, Jul. 2026. [Online]. Available: https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability

[4] A. A. Latif, N. Hashim, and M. Zulkifli, "Digital platforms for student rental accommodation: A Malaysian perspective," *Malaysian Journal of Information Technology*, vol. 12, no. 3, pp. 45-58, 2020.

[5] G. J. Myers, C. Sandler, and T. Badgett, *The Art of Software Testing*, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2011.

[6] R. S. Pressman and B. R. Maxim, *Software Engineering: A Practitioner's Approach*, 9th ed. New York: McGraw-Hill Education, 2020.

[7] RobBagby, "Baseline highly available zone-redundant app services web application," *Azure Architecture Center, Microsoft Learn*, 2026. [Online]. Available: https://learn.microsoft.com/en-us/azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant

[8] S. Saxena and J. Singh, "OFP-TM: An online VM failure prediction and tolerance model towards high availability of cloud computing environments," *The Journal of Supercomputing*, vol. 78, no. 8, pp. 10436-10465, 2022. https://doi.org/10.1007/s11227-021-04235-z

[9] S. Saxena, J. Singh, and W. Lee, "A high availability management model based on VM significance ranking and resource estimation," *IEEE Transactions on Network and Service Management*, vol. 19, no. 3, pp. 2912-2925, 2022. https://doi.org/10.1109/TNSM.2022.3189178

[10] R. W. Sinnott, "Virtues of the Haversine," *Sky and Telescope*, vol. 68, no. 2, p. 159, 1984.

[11] SPEEDHOME, "Rental scam prevention for international students in Malaysia," *SPEEDHOME Property Insights*, Jun. 2026. [Online]. Available: https://speedhome.com/blog/rental-scam-prevention-international-students-malaysia/

[12] W. Stallings, *Cryptography and Network Security: Principles and Practice*, 7th ed. Boston: Pearson, 2017.

[13] The Sun Malaysia, "Rental scams targeting tertiary students on the rise," *The Sun Daily*, Oct. 11, 2023. [Online]. Available: https://thesun.my/news/malaysia-news/rental-scams-ih11612921/

[14] Universiti Pendidikan Sultan Idris (UPSI), "Perception of undergraduate students in off-campus residential areas towards online scamming: A case study," *Jurnal Perspektif*, vol. 17, no. 1, pp. 112-125, 2025. https://ejournal.upsi.edu.my/index.php/PERS/article/view/9255/5135
"""

ref_idx = md.find("# REFERENCES")
if ref_idx != -1:
    md = md[:ref_idx] + ieee_refs_md

with open(MD_PATH, "w", encoding="utf-8") as f:
    f.write(md)
print("Updated final_report.md with IEEE citations.")

# 2. Update HTML
with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Add CSS for IEEE ref list
ieee_css = """
  .ref-list {
    list-style: none;
    padding-left: 0;
  }
  .ref-item {
    margin-bottom: 8pt;
    padding-left: 28pt;
    text-indent: -28pt;
    line-height: 1.5;
    font-size: 11pt;
  }
  .ref-num {
    font-weight: bold;
    color: #0a2540;
    display: inline-block;
    width: 28pt;
  }
"""

if ".ref-item" not in html:
    html = html.replace("</style>", ieee_css + "\n</style>")

for pattern, repl in replacements:
    # Also handle html encoded strings like &amp;
    html_pat = pattern.replace("&", "&amp;")
    html = re.sub(html_pat, repl, html)
    html = re.sub(pattern, repl, html)

ieee_refs_html = """<h1>References</h1>
<table style="border: none; width: 100%; border-collapse: collapse; margin-top: 6pt;">
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[1]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">R. Clemente, F. A. Silva, P. R. Maciel, and J. Araujo, "Availability evaluation of system service hosted in private cloud computing through hierarchical modeling process," <em>The Journal of Supercomputing</em>, vol. 78, no. 8, pp. 10412&ndash;10435, 2022. https://doi.org/10.1007/s11227-021-04217-1</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[2]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">Cloudflare, "Cloudflare Load Balancing and Zero Trust Tunnel Documentation," <em>Cloudflare Developers</em>, Oct. 2023. [Online]. Available: https://developers.cloudflare.com/load-balancing/</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[3]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">Gaurikasar, "High availability in Azure Database for PostgreSQL flexible server," <em>Microsoft Learn</em>, Jul. 2026. [Online]. Available: https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[4]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">A. A. Latif, N. Hashim, and M. Zulkifli, "Digital platforms for student rental accommodation: A Malaysian perspective," <em>Malaysian Journal of Information Technology</em>, vol. 12, no. 3, pp. 45&ndash;58, 2020.</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[5]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">G. J. Myers, C. Sandler, and T. Badgett, <em>The Art of Software Testing</em>, 3rd ed. Hoboken, NJ: John Wiley & Sons, 2011.</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[6]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">R. S. Pressman and B. R. Maxim, <em>Software Engineering: A Practitioner's Approach</em>, 9th ed. New York: McGraw-Hill Education, 2020.</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[7]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">RobBagby, "Baseline highly available zone-redundant app services web application," <em>Azure Architecture Center, Microsoft Learn</em>, 2026. [Online]. Available: https://learn.microsoft.com/en-us/azure/architecture/web-apps/app-service/architectures/baseline-zone-redundant</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[8]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">S. Saxena and J. Singh, "OFP-TM: An online VM failure prediction and tolerance model towards high availability of cloud computing environments," <em>The Journal of Supercomputing</em>, vol. 78, no. 8, pp. 10436&ndash;10465, 2022. https://doi.org/10.1007/s11227-021-04235-z</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[9]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">S. Saxena, J. Singh, and W. Lee, "A high availability management model based on VM significance ranking and resource estimation," <em>IEEE Transactions on Network and Service Management</em>, vol. 19, no. 3, pp. 2912&ndash;2925, 2022. https://doi.org/10.1109/TNSM.2022.3189178</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[10]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">R. W. Sinnott, "Virtues of the Haversine," <em>Sky and Telescope</em>, vol. 68, no. 2, p. 159, 1984.</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[11]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">SPEEDHOME, "Rental scam prevention for international students in Malaysia," <em>SPEEDHOME Property Insights</em>, Jun. 2026. [Online]. Available: https://speedhome.com/blog/rental-scam-prevention-international-students-malaysia/</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[12]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">W. Stallings, <em>Cryptography and Network Security: Principles and Practice</em>, 7th ed. Boston: Pearson, 2017.</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[13]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">The Sun Malaysia, "Rental scams targeting tertiary students on the rise," <em>The Sun Daily</em>, Oct. 11, 2023. [Online]. Available: https://thesun.my/news/malaysia-news/rental-scams-ih11612921/</td>
  </tr>
  <tr>
    <td style="border: none; width: 36px; vertical-align: top; font-weight: bold; color: #0a2540; font-size: 10.5pt; padding: 2.5px 4px 3px 0;">[14]</td>
    <td style="border: none; vertical-align: top; text-align: justify; font-size: 10.5pt; line-height: 1.4; padding: 2.5px 0 3px 0;">Universiti Pendidikan Sultan Idris (UPSI), "Perception of undergraduate students in off-campus residential areas towards online scamming: A case study," <em>Jurnal Perspektif</em>, vol. 17, no. 1, pp. 112&ndash;125, 2025. https://ejournal.upsi.edu.my/index.php/PERS/article/view/9255/5135</td>
  </tr>
</table>
"""

ref_html_idx = html.find("<h1>References</h1>")
if ref_html_idx != -1:
    end_html_idx = html.find("</body>", ref_html_idx)
    html = html[:ref_html_idx] + ieee_refs_html + "\n" + html[end_html_idx:]

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print("Updated final_report.html with IEEE citations.")

# 3. Recompile PDF with Edge
edge_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_exe):
    edge_exe = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

print("Recompiling PDF with Microsoft Edge headless...")
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
    print(f"Successfully recompiled PDF with IEEE Citations! Size: {os.path.getsize(PDF_PATH)} bytes")
