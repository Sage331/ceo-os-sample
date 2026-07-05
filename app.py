import os
import traceback
import requests
import gspread
from google import genai
from playwright.sync_api import sync_playwright, Playwright
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def safe_float(value, default=0.0):
    """Safely converts dynamic cell types into normalized float primitives."""
    if value is None:
        return default
    try:
        clean_val = str(value).replace(",", "").replace("$", "").strip()
        return float(clean_val) if clean_val else default
    except ValueError:
        return default

def send_slack_notification(message):
    """Sends a formatted message to a Slack webhook URL."""
    payload = {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": message}}]}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {e}")

def error_notifier(func):
    """Decorator to catch exceptions and send a Slack notification."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            error_message = f"🚨 *Error in {func.__name__}* 🚨\n\n```\n{traceback.format_exc()}\n```"
            send_slack_notification(error_message)
            print(error_message)
            return None
    return wrapper

@error_notifier
def pnl_aggregator_hub():
    """Reads dynamic records from Google Sheets, aggregates cross-channel financial totals, and computes net profit metrics."""
    print("Running P&L Aggregator Hub from Google Sheets...")
    total_revenue = 0.0
    total_cost = 0.0
    
    creds_path = "google_creds.json"
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Missing absolute dependency: '{creds_path}' not found in runtime workspace.")

    # Authenticate service account connection
    gc = gspread.service_account(filename=creds_path)
    sheet_id = "1tZOxITWvzaTB79U1Zp3RBwstZmQR28Cnmzi1oH2eTlU"
    
    try:
        spreadsheet = gc.open_by_key(sheet_id)
    except gspread.exceptions.SpreadsheetNotFound:
        raise ValueError(f"Target spreadsheet ID '{sheet_id}' was not resolved or permission was denied.")

    # 1. Parse Shopify Orders
    try:
        shopify_sheet = spreadsheet.worksheet("shopify_orders")
        shopify_records = shopify_sheet.get_all_records()
        for order in shopify_records:
            if isinstance(order, dict):
                total_revenue += safe_float(order.get("total_price"))
    except gspread.exceptions.WorksheetNotFound:
        print("Warning: 'shopify_orders' worksheet absent. Calculation fallback executed.")

    # 2. Parse TikTok Revenue & Built-in Costs
    try:
        tiktok_sheet = spreadsheet.worksheet("tiktok_revenue")
        tiktok_records = tiktok_sheet.get_all_records()
        for row in tiktok_records:
            if isinstance(row, dict):
                val = row.get("total_revenue") if row.get("total_revenue") is not None else row.get("total")
                total_revenue += safe_float(val)
                # Extract and add the platform-specific internal costs
                total_cost += safe_float(row.get("built_in_costs"))
    except gspread.exceptions.WorksheetNotFound:
        print("Warning: 'tiktok_revenue' worksheet absent. Calculation fallback executed.")

    # 3. Parse Meta Campaigns
    try:
        meta_sheet = spreadsheet.worksheet("meta_campaigns")
        meta_records = meta_sheet.get_all_records()
        for campaign in meta_records:
            if isinstance(campaign, dict):
                total_cost += safe_float(campaign.get("spend"))
    except gspread.exceptions.WorksheetNotFound:
        print("Warning: 'meta_campaigns' worksheet absent. Calculation fallback executed.")

    net_profit_margin = ((total_revenue - total_cost) / total_revenue) * 100 if total_revenue > 0 else 0.0

    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Costs: ${total_cost:,.2f}")
    print(f"Net Profit Margin: {net_profit_margin:.2f}%")
    print("-" * 30)
    return total_revenue, total_cost, net_profit_margin

@error_notifier
def playwright_website_qc_monitor(playwright: Playwright):
    """Launches a headless browser to monitor a website's status."""
    print("Running Playwright Website QC Monitor...")
    with playwright.chromium.launch(headless=True) as browser:
        page = browser.new_page()
        start_time = page.evaluate("() => performance.now()")
        page.goto("https://www.jumia.com.ng/", timeout=30000)
        end_time = page.evaluate("() => performance.now()")

        latency = end_time - start_time
        title = page.title()
        body_structure = page.evaluate("() => document.body.tagName")

        print(f"Page Title: {title}")
        print(f"Page Latency: {latency:.2f} ms")
        print(f"Body Tag: {body_structure}")
        print("-" * 30)
        return title, latency, body_structure

@error_notifier
def slack_ai_ad_copy_generator():
    """Generates ad copy variants using the updated google-genai SDK module."""
    print("Running Slack AI Ad Copy Generator...")
    
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = """
    Generate 3 distinct ad copy variants for a new line of noise-cancelling headphones.
    Each variant should have a unique headline, body, and call-to-action (CTA).
    Format the output as a numbered list.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    print(response.text)
    print("-" * 30)
    return response.text

@error_notifier
def simulate_error():
    """Intentionally raises an exception to test the error notifier."""
    print("Simulating an error...")
    raise ValueError("This is a test exception to verify Slack error notifications.")

if __name__ == "__main__":
    print("=== Initiating Core Automated Report Build ===\n")
    
    # 1. Run Dynamic Data Aggregation Layer
    pnl_data = pnl_aggregator_hub()
    
    # 2. Run Live Browser Verification Layer
    with sync_playwright() as playwright:
        qc_data = playwright_website_qc_monitor(playwright)
        
    # 3. Run Intent GenAI Generation Layer
    ad_data = slack_ai_ad_copy_generator()
    
    # 4. Construct Production-Grade Structured Briefing Report
    briefing_components = []
    briefing_components.append("☀️ *CEO OPERATING SYSTEM: MORNING BRIEFING RUN* ☀️\n---")
    
    # Check for P&L data extraction failures
    if pnl_data:
        revenue, cost, margin = pnl_data
        status_indicator = "🟢" if margin >= 0 else "🔴"
        briefing_components.append(
            f"📊 *Financial P&L Dashboard Summary*\n"
            f"• *Total Computed Revenue:* ${revenue:,.2f}\n"
            f"• *Total Aggregated Costs:* ${cost:,.2f} _(Ad Spend + Platform Costs)_\n"
            f"• *Net Profit Margin:* {status_indicator} `{margin:.2f}%`"
        )
    else:
        briefing_components.append("📊 *Financial P&L Dashboard Summary*\n⚠️ Diagnostic Alert: Failed to safely parse upstream financial schemas.")

    briefing_components.append("---")

    # Check for browser verification crawler failures
    if qc_data:
        page_title, page_latency, body_tag = qc_data
        briefing_components.append(
            f"🔍 *Website Quality Control (QC) Status*\n"
            f"• *Monitored Storefront:* `https://www.jumia.com.ng/`\n"
            f"• *Document Title:* _{page_title}_\n"
            f"• *Scrape Roundtrip Latency:* `{page_latency:.2f} ms`\n"
            f"• *DOM Tree Structural Integrity:* Verified (`<{body_tag}>` root tag active)"
        )
    else:
        briefing_components.append("🔍 *Website Quality Control (QC) Status*\n⚠️ Diagnostic Alert: Headless browser crawler dropped connection or was blocked.")

    briefing_components.append("---")

    # Check for AI copy pipe failures
    if ad_data:
        briefing_components.append(
            f"🤖 *AI-Powered On-Demand Ad Copy Matrix*\n"
            f"{ad_data}"
        )
    else:
        briefing_components.append("🤖 *AI-Powered On-Demand Ad Copy Matrix*\n⚠️ Diagnostic Alert: LLM token completion pipeline generated an empty response.")

    # Bundle components into a unified text document payload
    compiled_briefing = "\n\n".join(briefing_components)
    
    print("Transmitting operational dashboard summary directly to Slack...")
    send_slack_notification(compiled_briefing)
    print("Briefing transmit routine finalized.")
    
    # simulate_error()