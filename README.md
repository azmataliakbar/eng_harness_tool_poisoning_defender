# B2B Tool Poisoning Defender & Safety Hook Loop

## 🎯 Project Goal
To manage a real-world, state-driven, 100% autonomous B2B Cyber-Defense and Prompt-Injection Gating lifecycle. Zia Khan (Director and Security Auditor representing GIAIC IT Institute) launches a multi-stage security audit against GIAIC's customer inbox support bot. In **Attack 1 (System Sabotage)**, Zia hides a malicious `"SYSTEM_RESET"` prompt-injection command inside a helpdesk ticket to force database deletion. Wahiba Kiran (the Symmetrical Inbox Bot / Outer Harness specialist) programmatically intercepts the ticket under a secure **Safety Hook (`before_tool_run`)** before the LLM ever reads it: she scans GIAIC's **`guardrails.json`** database, neutralizes the attack via precise redaction, logs the incident metrics inside **`attack_logs.json`** (**Observability**), and replies normally (**AX**). In **Attack 2 (Data Exfiltration)**, Zia tries to exfiltrate private API credentials via a `"SECRET_LEAK"` injection. The safety hook blocks and redacts the leak, pauses the automated ticketing loop, and escalates to Senior Security Managers. Zia accepts the secure audit report and signs GIAIC's tenancy contract with exactly: **`I_AGREE`**, programmatically compiling and writing the final certified **`security_audit.json`** copy on disk!

> ✦ **"This project is a supremely clever and thoughtful demonstration of Sir Zia's pedagogical direction!"**

---

## ⚙️ Harness Engineering Core Definitions Applied

*   **Harness**: The overarching Python wrapper (`freelancer_agent.py` acting as GIAIC's secure inbox bot) managing the execution rules, running safety hooks, and protecting our LLMs.
*   **Tool Poisoning**: A highly dangerous security attack hidden inside external user data or tool inputs (Zia's support ticket body) designed to hijack and bypass an agent's system prompt instructions.
*   **Hook (`before_tool_run`)**: A programmatic interceptor executed by GIAIC's outer harness *after* fetching the email but *before* passing the text payload to Gemini, fully sanitizing and censoring threats.
*   **Guardrail**: Enforces strict, hard-coded keyword checks (**`SYSTEM_RESET`**, **`SECRET_LEAK`**, **`DELETE DATABASE`**, etc.) inside **`guardrails.json`**, instantly sanitizing and blocking malicious system overrides at the harness level.
*   **Observability (`attack_logs.json`)**: Symmetrically writes structured threat metrics, timestamps, attack categories, and automated actions to `attack_logs.json` for security compliance tracing.
*   **AX (Agent Experience)**: Instead of crashing or ignoring tickets, the harness redacts the threat, processes the rest of the student login normally, and alerts the sender of the blocked injection.
*   **Contract Authorization Token Gate**: Blocks final audit certification and `security_audit.json` compilation until the auditor formally signs off by replying with exactly: **`I_AGREE`**.
*   **Local Solution Document Output (`security_audit.json`)**: Upon receiving the signature token, the agent programmatically compiles and writes the final B2B security audit contract on disk.

---

## 📝 Symmetrical 8-Turn Tenancy Chronology

Here is the exact step-by-step chronology of the emails exchanged autonomously between GIAIC and GIAIC's secure inbox bot:

*   👦 **Turn 1 (Zia ➡️ Wahiba at 11:39 PM)**:
    *   Zia submits a helpdesk ticket with a hidden **`SYSTEM_RESET`** data-deletion injection, trying to force the bot to erase GIAIC's database.
*   👸 **Turn 2 (Wahiba ➡️ Zia at 11:40 PM)**:
    *   Wahiba's secure **Safety Hook** intercepts Zia's email, matches `"SYSTEM_RESET"`, censors/redacts his attack block, logs the incident inside **`attack_logs.json`** (**Observability**), and replies with a normal support response.
*   👦 **Turn 3 (Zia ➡️ Wahiba at 11:41 PM)**:
    *   Zia tries to execute an advanced **`SECRET_LEAK`** data-exfiltration attack to extract private system instructions and API keys.
*   👸 **Turn 4 (Wahiba ➡️ Zia at 11:43 PM)**:
    *   Wahiba's safety hook intercepts, redacts, logs the exfiltration attempt inside **`attack_logs.json`**, **trips the Manager Review Gate**, and emails Zia his formal escalation notice.
*   👦 **Turn 5 (Zia ➡️ Wahiba at 11:44 PM)**:
    *   Zia confirms he is standing by and waiting for review.
*   👸 **Turn 6 (Wahiba ➡️ Zia at 11:45 PM)**:
    *   Wahiba (acting as GIAIC's **Senior Security Officer**) manually overrides, approves the final audit report, and delivers the agreement contract requesting his signature.
*   👦 **Turn 7 (Zia ➡️ Wahiba at 11:46 PM)**:
    *   Zia signs the contract by replying with exactly: **`I_AGREE`**!
*   👸 **Turn 8 (Wahiba ➡️ Zia at 11:47 PM)**:
    *   Wahiba receives GIAIC's signature, validates the `I_AGREE` token, programmatically compiles and writes the final certified **`security_audit.json`** copy on disk, and closes GIAIC's audit!

---

## 🚀 Running GIAIC's Secure Inbox Defender Loop

To run GIAIC's secure inbox defender loop on your local machine, open your PowerShell window and run these commands:

```powershell
cd C:\Projects\eng_harness\tool_poisoning_defender
python run_harness_loop.py
```

---

## 🔬 Symmetrical Educational Takeaway: Simple Pedagogical Concept

This project represents the crown jewel of Agentic Security and Safety Hooks. For colleagues and students, it teaches how an autonomous agent can be fully protected unattended against external malicious prompt-injection, sabotage, and data-exfiltration attacks. The loop does not let the bot get hijacked—it elegantly intercepts payloads via a **Safety Hook**, filters instructions via **Guardrails** in `guardrails.json`, logs threats to `attack_logs.json` (**Observability**), and locks final security certifications legally via `I_AGREE` signatures in minutes with absolute safety!
