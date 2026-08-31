# Autonomous Executive Briefing & P&L Operations Engine

A production-grade Python automation pipeline that consolidates financial performance, storefront uptime, and generative marketing copy into an automated daily Slack executive briefing.

---

## Core System Architecture

* **Multi-Channel Financial Aggregation:** Ingests e-commerce records (Shopify orders, TikTok revenue, Meta ad spend) via the `gspread` API, sanitizes dynamic cell inputs, and computes net profit margins.
* **Headless Storefront QC & Latency Monitoring:** Executes a headless Chromium browser instance using Playwright to track storefront availability, roundtrip latency, and DOM structural integrity.
* **Generative Ad Matrix:** Connects to the `google-genai` SDK (Gemini 2.5 Flash) to generate structured, multichannel marketing copy variants on demand.
* **Fault Tolerance & Real-Time Alerting:** Implements a Python decorator (`@error_notifier`) to intercept exceptions, capture stack traces, and broadcast diagnostic alerts to Slack without breaking execution pipelines.

---

## Tech Stack

* **Language:** Python 3.10+
* **Automation & Scraping:** Playwright (Chromium)
* **Spreadsheet Integration:** `gspread`, Google Service Account OAuth
* **Generative AI:** `google-genai` (Gemini API)
* **Notifications & Webhooks:** Slack Incoming Webhooks (`requests`)
* **Environment Management:** `python-dotenv`

---

## Prerequisites & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/automated-pnl-slack-briefing.git](https://github.com/your-username/automated-pnl-slack-briefing.git)
cd automated-pnl-slack-briefing
