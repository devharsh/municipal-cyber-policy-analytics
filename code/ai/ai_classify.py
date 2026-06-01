"""
AI-Assisted NIST CSF 2.0 Policy Classification
Prompt: "You are a cybersecurity auditor. Classify the following policy according to
NIST CSF 2.0: Govern Identify Protect Detect Respond Recover
For each category provide: 0=absent 1=partial 2=present. Explain your reasoning."

Classifications below are produced by Claude (claude-sonnet-4-6) applied to
the first 12,000 characters of each document extracted via PyMuPDF.
"""

import os
import pandas as pd

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# AI Classification Results (0=absent, 1=partial, 2=present)
# Columns: Policy, Govern, Identify, Protect, Detect, Respond, Recover,
#          DocumentType, Reasoning
# ─────────────────────────────────────────────────────────────────────────────

AI_SCORES = [
    # ── Genuine cybersecurity / IT security policy documents ──────────────────
    {
        "Policy": "MD_DOIT_CyberRiskMgmt_Policy.pdf",
        "Govern": 2, "Identify": 2, "Protect": 1, "Detect": 1, "Respond": 1, "Recover": 0,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "State-level risk management policy (MD-POL-201-01, 2026). GV=2: defines risk "
            "appetite/tolerance, enterprise risk strategy, third-party risk management, and "
            "explicit SCISO/AO roles. ID=2: mandates vulnerability, privacy-impact, network, "
            "software, physical, and threat-intelligence assessments. PR=1: references ZTA "
            "access control and least-privilege but delegates specifics to other policies. "
            "DE=1: continuous monitoring referenced (section 200.2.7) but not detailed here. "
            "RS=1: risk response framed but no incident-response procedures. RC=0: no "
            "recovery/continuity content."
        ),
    },
    {
        "Policy": "MD_DOIT_ContinuousMonitoring_Policy.pdf",
        "Govern": 1, "Identify": 0, "Protect": 1, "Detect": 2, "Respond": 1, "Recover": 0,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "State Continuous Monitoring Policy (MD-POL-208-01, 2026). Explicitly maps to "
            "NIST CSF 2.0 DE.CM and DE.AE. GV=1: SCISO/ISO roles and policy authority "
            "established. ID=0: no asset-management or broader risk-assessment content. "
            "PR=1: least-privilege enforcement and authentication monitoring cited within "
            "ZTA goals. DE=2: comprehensive network, system, physical-environment, personnel, "
            "and external-provider monitoring plus event-analysis and incident-declaration "
            "criteria. RS=1: incident declaration references MD-STD-308-IR but does not "
            "detail response procedures. RC=0: no recovery content."
        ),
    },
    {
        "Policy": "MD_DOIT_SystemNetworkSecurity_Policy.pdf",
        "Govern": 1, "Identify": 1, "Protect": 2, "Detect": 1, "Respond": 0, "Recover": 2,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "State System & Network Security Policy (MD-POL-207-01, 2026). Maps to "
            "NIST CSF 2.0 PR.PS (Platform Security) and PR.IR (Infrastructure Resilience). "
            "GV=1: governance structure and SCISO/ISO roles defined. ID=1: cybersecurity "
            "inventory management mandated (section 200.1.7). PR=2: configuration "
            "management, software/hardware security, audit logging, approved-software lists, "
            "secure SDLC, network segmentation. DE=1: audit logging supports detection. "
            "RS=0: no incident-response content. RC=2: resilience section explicitly addresses "
            "recovery from disruptions, load balancing, redundant storage, and geographically "
            "dispersed architecture."
        ),
    },
    {
        "Policy": "MD_IT_SecurityManual.pdf",
        "Govern": 2, "Identify": 2, "Protect": 2, "Detect": 2, "Respond": 2, "Recover": 2,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "Maryland IT Security Manual v1.2 (2019), 200+ pages. The most comprehensive "
            "document in the corpus. GV=2: risk management, security authorization, planning, "
            "roles (AO, CISO, SO, IRT), procurement policy. ID=2: asset management, "
            "information classification, system security categorization, risk assessment. "
            "PR=2: access control, identification/authentication, encryption, awareness and "
            "training, configuration management, media protection, physical/personnel "
            "security. DE=2: audit and accountability, system and information integrity, "
            "continuous monitoring. RS=2: incident response (section 6.4), IT Incident "
            "Reporting Form (Appendix B), incident handling checklist (Appendix G). "
            "RC=2: contingency planning, disaster recovery, business continuity, backup plans."
        ),
    },
    {
        "Policy": "MD_Judicial_InfoSecurity_Policy.pdf",
        "Govern": 2, "Identify": 2, "Protect": 2, "Detect": 2, "Respond": 2, "Recover": 2,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "Maryland Judiciary Information Security Policy (Jan 2026). GV=2: CIO/ISO/CTO "
            "roles, AOC/CTechCom governance body, annual review requirement. ID=2: asset "
            "inventory, data classification, security categorization. PR=2: access control, "
            "authentication, configuration management, security education/awareness, media "
            "protection, physical/personnel security, DLP, SDLC. DE=2: audit and "
            "accountability, system integrity. RS=2: incident management (section 6.5). "
            "RC=2: disaster preparedness plan (section 6.4), backup plans (section 6.11), "
            "business continuity. Explicitly cites NIST and CIS Frameworks."
        ),
    },
    {
        "Policy": "MD_DHMH_IT_SecurityPolicy.pdf",
        "Govern": 2, "Identify": 2, "Protect": 2, "Detect": 2, "Respond": 2, "Recover": 1,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "DHMH IT Technical Security Policy v4.0 (2014). GV=2: risk management, security "
            "authorization, planning, network service agreements, governance roles. ID=2: "
            "asset inventory, classification, risk assessment, system security categorization. "
            "PR=2: access control, authentication, encryption, training, configuration "
            "management, media protection, physical/personnel security, information integrity. "
            "DE=2: audit and accountability (section 7.2), system integrity. RS=2: incident "
            "response (section 6.4) and Incident Response Protocol (SAR-15). RC=1: "
            "contingency planning (section 6.3) mentioned but backup/DR less detailed than "
            "newer policies."
        ),
    },
    {
        "Policy": "MD_MSDE_AUP_2024.pdf",
        "Govern": 1, "Identify": 0, "Protect": 2, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Cybersecurity Policy",
        "Reasoning": (
            "MSDE Cybersecurity Acceptable Use and Communications Policy v2.0 (Oct 2024). "
            "GV=1: CISO authority established, policy scope and applicability defined. "
            "ID=0: no asset management or risk assessment content. PR=2: focuses on "
            "acceptable use of systems, device management, access controls, and "
            "communications policy. DE=0: no monitoring or detection requirements. "
            "RS=0: no incident response procedures. RC=0: no recovery content."
        ),
    },
    {
        "Policy": "MD_UMGC_LocalGov_Cybersecurity_2021.pdf",
        "Govern": 2, "Identify": 1, "Protect": 1, "Detect": 1, "Respond": 1, "Recover": 1,
        "DocumentType": "Advisory Report",
        "Reasoning": (
            "UMGC report on Maryland State and Local Government Cybersecurity (Dec 2021). "
            "Analysis and recommendations, not an implementing policy. GV=2: comprehensive "
            "governance analysis, organizational recommendations, legislation review. "
            "ID=1: risk assessment discussed in recommendations. PR=1: protection measures "
            "in recommendations. DE=1: detection discussed. RS=1: response discussed. "
            "RC=1: recovery discussed. All at partial (1) because conceptual/advisory rather "
            "than binding operational requirements."
        ),
    },
    {
        "Policy": "MD_CybersecurityCouncil_Report_2025.pdf",
        "Govern": 2, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Advisory Report",
        "Reasoning": (
            "Maryland Cybersecurity Council Biennial Activities Report (July 2025). "
            "Strategic overview of council activities and legislation. GV=2: governance "
            "activities, legislative connections, policy-setting described. ID/PR/DE/RS/RC=0: "
            "no operational requirements — this is a reporting/activity document, not an "
            "implementing policy with technical controls."
        ),
    },
    # ── Partial relevance documents ───────────────────────────────────────────
    {
        "Policy": "MD_Procurement_Manual.pdf",
        "Govern": 0, "Identify": 0, "Protect": 1, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Procurement Document",
        "Reasoning": (
            "State of Maryland Procurement Manual (2019). Primarily an administrative "
            "procurement guide. GV=0: no cybersecurity governance. ID=0: no asset "
            "identification. PR=1: vendor security requirements exist in the procurement "
            "context; IT contracts reference security obligations, but cybersecurity is "
            "secondary to the procurement process. DE/RS/RC=0: no detection, response, "
            "or recovery content."
        ),
    },
    {
        "Policy": "87bb47f3-ff2c-4353-a25e-d2c103b62a0c.pdf",
        "Govern": 1, "Identify": 1, "Protect": 1, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Data Management Plan",
        "Reasoning": (
            "MD iMap Data Management Plan (Jan 2015). Geographic data governance document. "
            "GV=1: data governance structure and roles defined. ID=1: data inventory and "
            "classification aspects present. PR=1: data access controls referenced. "
            "DE/RS/RC=0: no monitoring, incident response, or recovery content. Not a "
            "cybersecurity policy; data management with security elements."
        ),
    },
    {
        "Policy": "mpi3-25-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 1,
        "DocumentType": "Workforce Policy",
        "Reasoning": (
            "QUEST Disaster Recovery Dislocated Worker Grant Policy (May 2025). A workforce "
            "development policy for workers displaced by natural disasters. RC=1: 'disaster "
            "recovery' is in the title and scope, but refers to economic/workforce recovery "
            "from natural disasters, not IT/cyber recovery. No cybersecurity content whatsoever. "
            "Keyword tools falsely flag this document due to the terms 'disaster recovery' "
            "and 'training' appearing in a non-cybersecurity context."
        ),
    },
    # ── Completely irrelevant documents (correctly score 0 on all) ────────────
    {
        "Policy": "09880433-9572-4fdf-a9d3-8cd4a11e32b6.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Municipal Code",
        "Reasoning": "Town of Kensington Code of Ordinances (1992 Edition). Municipal law "
                     "codification. No cybersecurity content.",
    },
    {
        "Policy": "1625df13-6b8e-4692-b06f-aab290812197.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting Agenda (Aug 8, 2022). Administrative "
                     "meeting agenda. No cybersecurity content.",
    },
    {
        "Policy": "1ef3c6b9-1d3f-4ddf-ba57-73d602ebf5f3.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "Maryland Apprenticeship and Training Council Meeting Minutes (Jan 14, "
                     "2025). Workforce apprenticeship program minutes. No cybersecurity content.",
    },
    {
        "Policy": "2019 Business Plan-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Business Plan",
        "Reasoning": "Maryland Correctional Enterprises (MCE) Business Plan 2019. Correctional "
                     "industry operations document. Keywords like 'training' refer to inmate "
                     "vocational training, not security awareness. No cybersecurity content.",
    },
    {
        "Policy": "2023-03-13-Agenda-and-Documents-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting (Mar 13, 2023). Municipal meeting "
                     "agenda and documents. No cybersecurity content.",
    },
    {
        "Policy": "2023-04-10-Agenda-and-Documents-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting (Apr 10, 2023). Municipal meeting "
                     "agenda and documents. No cybersecurity content.",
    },
    {
        "Policy": "2023-11-20-Agenda-and-Documnts-1-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting (Nov 20, 2023). Municipal meeting "
                     "agenda and documents. No cybersecurity content.",
    },
    {
        "Policy": "2023-12-13-Agenda-and-Documents-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting (Dec 13, 2023). Municipal meeting "
                     "agenda and documents. No cybersecurity content.",
    },
    {
        "Policy": "2cdfbc5a-64bb-4c70-9925-db7e4f63019f.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Special Session (Jul 2020). Correctional "
                     "enterprises operations meeting. No cybersecurity content.",
    },
    {
        "Policy": "35a86486-3ed0-4e94-8a93-72644e187279.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Maryland Apprenticeship & Training Council Supplemental Agenda (Jan "
                     "2025). Lists 'Cyber Security Technician' as an apprenticeship occupation "
                     "but contains no cybersecurity policy content.",
    },
    {
        "Policy": "4cc680a2-3dd5-4020-aaef-346559eaffee.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Agenda",
        "Reasoning": "Town of Kensington Council Meeting (Oct 10, 2024). Municipal meeting "
                     "agenda and documents. No cybersecurity content.",
    },
    {
        "Policy": "56a4821c-1064-4144-940c-170ff3cd1612.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Meeting Minutes (Mar 2018). Correctional "
                     "enterprises operations and financials. No cybersecurity content.",
    },
    {
        "Policy": "97c51d56-6691-4349-a926-3873852e2c51.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Meeting Minutes (Sep 2021). Operations update "
                     "including ERP infrastructure upgrade; IT context but no cybersecurity "
                     "policy content.",
    },
    {
        "Policy": "9189cf3d-fec6-4172-8f5b-f2ab92b1f113.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Financial Statement",
        "Reasoning": "Town of Kensington Financial Statements FY2024 and FY2023. Audited "
                     "municipal financial statements. No cybersecurity content.",
    },
    {
        "Policy": "9ae7b499-22a0-4535-9e7d-3bb899f8c5a0.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Municipal Code",
        "Reasoning": "Town of Kensington Code of Ordinances (full version, 140 pages). "
                     "Municipal law codification. No cybersecurity policy content.",
    },
    {
        "Policy": "9cbf23f9-4e46-4900-a169-222b1c1ec17f.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Procurement RFP",
        "Reasoning": "Town of Kensington RFP for Bridge Engineering Design and Construction "
                     "Management (Dec 2022). Civil engineering procurement. No cybersecurity "
                     "content.",
    },
    {
        "Policy": "af348882-aa0c-4882-a61c-1074246ecd14.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Unclassifiable",
        "Reasoning": "Scanned/image document with garbled OCR output. Cannot extract "
                     "meaningful text. No classifiable cybersecurity content.",
    },
    {
        "Policy": "annualreport2024-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Annual Report",
        "Reasoning": "Annual report document (image-heavy). Extracted text is minimal. "
                     "No discernible cybersecurity policy content in accessible text.",
    },
    {
        "Policy": "b0c0eb31-4fcb-4a22-92fd-ea5822647891.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Unclassifiable",
        "Reasoning": "Scanned document with no extractable text (0 chars). Cannot classify.",
    },
    {
        "Policy": "b6821233-35a3-4a8e-92f7-809f28d35a61.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Financial Statement",
        "Reasoning": "Town of Kensington Financial Statements FY2025. Audited municipal "
                     "financial statements. No cybersecurity content.",
    },
    {
        "Policy": "Business Plan 2019 (1)-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Business Plan",
        "Reasoning": "MCE Business Plan 2019 (full version). Correctional industry plan. "
                     "Keyword hits on 'training', 'vendor', 'contractor' reflect correctional "
                     "program context, not cybersecurity. No cybersecurity content.",
    },
    {
        "Policy": "Business Plan 2020 12_09-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Business Plan",
        "Reasoning": "MCE Business Plan 2020. Correctional industry operations and financials. "
                     "High keyword scores (Protect=37) are false positives from 'training' "
                     "appearing in workforce/vocational context. No cybersecurity content.",
    },
    {
        "Policy": "c68baa0c-8afd-4088-9462-e3cda376a615.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Unclassifiable",
        "Reasoning": "Scanned document with no extractable text (0 chars). Cannot classify.",
    },
    {
        "Policy": "Connecticut-Avenue-TLC-report-FINAL-Package-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Urban Planning Report",
        "Reasoning": "Connecticut Avenue Technical/Land-Use Committee report. Urban planning "
                     "and community development document. No cybersecurity content.",
    },
    {
        "Policy": "ctecomm-ert-report-cecil-county24-25final-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Education Report",
        "Reasoning": "GWDB Career and Technical Education Expert Review Team Post-Visit Report, "
                     "Cecil County Public Schools (Feb 2026). Education program review. No "
                     "cybersecurity policy content.",
    },
    {
        "Policy": "empguide-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Reference Guide",
        "Reasoning": "Maryland Dept of Labor Employers' Quick Reference Guide (Unemployment "
                     "Insurance). HR/employment law reference guide. Keyword hits on "
                     "'vendor'/'contractor' reflect employer-employee context, not cybersecurity.",
    },
    {
        "Policy": "f5ca30b5-b88e-4a55-bb56-690c0181674d.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Customer Council Meeting Minutes (2016-2017). Correctional "
                     "enterprises customer/business meeting minutes. No cybersecurity content.",
    },
    {
        "Policy": "MCE Business Report FY18 Combined-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Business Report",
        "Reasoning": "MCE Annual Business Report FY2018. Correctional industry financials. "
                     "No cybersecurity content.",
    },
    {
        "Policy": "MCE FY2016-FY2018 Business Plan-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Business Plan",
        "Reasoning": "MCE Business Plan FY2016-FY2018. Correctional industry strategic plan. "
                     "No cybersecurity content.",
    },
    {
        "Policy": "MCE Management Council Meeting Minutes FY23-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Minutes FY2023. Correctional enterprises "
                     "operations. Keyword hits on 'vendor'/'contractor' are from procurement "
                     "context, not cybersecurity. No cybersecurity content.",
    },
    {
        "Policy": "MCE Management Council Meeting Minutes FY24-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Minutes FY2024. Correctional enterprises "
                     "operations. No cybersecurity content.",
    },
    {
        "Policy": "MCE Management Council Meeting Minutes FY25-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Meeting Minutes",
        "Reasoning": "MCE Management Council Minutes FY2025. Correctional enterprises "
                     "operations. No cybersecurity content.",
    },
    {
        "Policy": "mdpy2023wiaannrep-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Annual Report",
        "Reasoning": "Maryland WIOA Annual Report 2023. Workforce Innovation and Opportunity "
                     "Act program outcomes. Keyword hit on 'governance' (GV=1 in keyword) "
                     "refers to workforce program governance, not cybersecurity.",
    },
    {
        "Policy": "mpi4-13-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Workforce Policy",
        "Reasoning": "Maryland Policy Issuance 04-2013 on WIA Youth Grants. Workforce "
                     "development policy. No cybersecurity content.",
    },
    {
        "Policy": "Resolution-R-11-2023-ULI-TAP-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Municipal Resolution",
        "Reasoning": "Resolution R-11-2023 authorizing ULI Technical Assistance Panel. "
                     "Urban planning/development resolution. No cybersecurity content.",
    },
    {
        "Policy": "September-Journal-2021-a-web-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Community Newsletter",
        "Reasoning": "Town of Kensington community events newsletter (September 2021). "
                     "Community news and events. No cybersecurity content.",
    },
    {
        "Policy": "Town-of-Kensington-2022-Financial-Statements-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Financial Statement",
        "Reasoning": "Town of Kensington Financial Statements 2022. Municipal audit report. "
                     "No cybersecurity content.",
    },
    {
        "Policy": "Town-of-Kensington-FS-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Financial Statement",
        "Reasoning": "Town of Kensington Financial Statements (additional year). Municipal "
                     "audit report. No cybersecurity content.",
    },
    {
        "Policy": "Town-of-Kensington-TAP-Report-compressed.pdf",
        "Govern": 0, "Identify": 0, "Protect": 0, "Detect": 0, "Respond": 0, "Recover": 0,
        "DocumentType": "Urban Planning Report",
        "Reasoning": "Town of Kensington Technical Assistance Panel (TAP) Report. Urban "
                     "planning and community development. No cybersecurity content.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Save AI scores to CSV
# ─────────────────────────────────────────────────────────────────────────────
categories = ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]

df_ai = pd.DataFrame(AI_SCORES)
df_ai.to_csv(os.path.join(OUTPUT_DIR, "ai_scores.csv"), index=False)
print(f"AI scores saved: {len(df_ai)} documents")
print(df_ai[["Policy", "DocumentType"] + categories])
