#!/usr/bin/env python3
"""
REFLECTER TECHNOLOGIES — Cold Email Agent
==========================================
Main entry point with interactive CLI menu.
Researches businesses, drafts personalized emails, and sends them.
"""

import os
import sys
import time
import re
import urllib.parse
import webbrowser
from datetime import datetime, timedelta

# Ensure we can import from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import (
        SENDER_EMAIL, SENDER_PASSWORD, TARGET_CITIES, TARGET_INDUSTRIES,
        DATABASE_FILE, SENDER_NAME, SENDER_COMPANY
    )
    config_loaded = True
except ImportError:
    config_loaded = False
    DATABASE_FILE = 'prospects.csv'
    TARGET_CITIES = ['Surat', 'Ahmedabad', 'Mumbai']
    TARGET_INDUSTRIES = ['textile mill', 'dental clinic', 'saree showroom']

from prospector import BusinessProspector
from email_drafter import ColdEmailDrafter
from email_sender import EmailSender
from pipeline_manager import PipelineManager

# --- Colors (fallback if colorama not installed) ---
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = YELLOW = RED = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = ''


def print_banner():
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║   REFLECTER TECHNOLOGIES — Cold Email Agent      ║
║   B2B Client Acquisition System                  ║
╚══════════════════════════════════════════════════╝{Fore.RESET}
""")


def print_menu():
    print(f"""
{Fore.WHITE}  1. 🔍  Research & Find New Prospects
  2. 📧  Draft Emails for Ready Prospects
  3. 👀  Preview Drafted Emails
  4. 📤  Send Emails (with confirmation)
  5. 📊  View Pipeline Status
  6. 🔄  Send Follow-ups (due today)
  7. ➕  Add Prospect Manually
  8. 📱  Generate WhatsApp & Instagram Messages
  9. ⚙️   Test Email Connection
  10. 📋  Export Report
  0. ❌  Exit
{Fore.RESET}""")


def check_env_setup():
    """Check if .env is configured."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if not os.path.exists(env_path):
        print(f"""
{Fore.YELLOW}⚠️  No .env file found!

To send emails, you need to set up your credentials:
  1. Copy .env.example to .env
  2. Fill in your Gmail address and App Password
  3. Restart this agent

Research and drafting will still work without email config.{Fore.RESET}
""")
        return False
    return True


def option_research(prospector, pipeline):
    """Option 1: Research & Find New Prospects"""
    print(f"\n{Fore.CYAN}=== Research Mode ==={Fore.RESET}")
    print(f"\nAvailable cities ({len(TARGET_CITIES)}):")
    for i, city in enumerate(TARGET_CITIES, 1):
        print(f"  {i}. {city}")
    print(f"  A. All cities")

    city_input = input(f"\nSelect cities (comma-separated numbers, or A for all): ").strip()

    if city_input.upper() == 'A':
        selected_cities = TARGET_CITIES
    else:
        try:
            indices = [int(x.strip()) - 1 for x in city_input.split(',')]
            selected_cities = [TARGET_CITIES[i] for i in indices if 0 <= i < len(TARGET_CITIES)]
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid selection. Using default: Surat{Fore.RESET}")
            selected_cities = ['Surat']

    print(f"\nAvailable industries ({len(TARGET_INDUSTRIES)}):")
    for i, ind in enumerate(TARGET_INDUSTRIES, 1):
        print(f"  {i}. {ind}")
    print(f"  A. All industries")

    ind_input = input(f"\nSelect industries (comma-separated numbers, or A for all): ").strip()

    if ind_input.upper() == 'A':
        selected_industries = TARGET_INDUSTRIES
    else:
        try:
            indices = [int(x.strip()) - 1 for x in ind_input.split(',')]
            selected_industries = [TARGET_INDUSTRIES[i] for i in indices if 0 <= i < len(TARGET_INDUSTRIES)]
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid selection. Using defaults.{Fore.RESET}")
            selected_industries = ['textile mill', 'dental clinic']

    print(f"\n{Fore.CYAN}Starting scan: {len(selected_cities)} cities × {len(selected_industries)} industries{Fore.RESET}")
    print(f"Estimated time: ~{len(selected_cities) * len(selected_industries) * 15} seconds\n")

    confirm = input("Proceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return

    prospects = prospector.run_full_scan(
        selected_cities,
        selected_industries,
        DATABASE_FILE
    )

    # Add to pipeline
    for p in prospects:
        p['status'] = 'Ready'
        pipeline.add_prospect(p)

    print(f"\n{Fore.GREEN}✅ Found {len(prospects)} new prospects without websites!{Fore.RESET}")
    print(f"Saved to: {DATABASE_FILE}")


def option_draft_emails(drafter, pipeline):
    """Option 2: Draft Emails for Ready Prospects"""
    print(f"\n{Fore.CYAN}=== Drafting Emails ==={Fore.RESET}")

    ready = pipeline.get_ready_prospects()
    if not ready:
        print(f"{Fore.YELLOW}No prospects with 'Ready' status found.{Fore.RESET}")
        print("Run Research (option 1) or Add Manually (option 7) first.")
        return

    print(f"Found {len(ready)} prospects ready for outreach.\n")

    # Create drafts directory
    drafts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts')
    os.makedirs(drafts_dir, exist_ok=True)

    drafted_count = 0
    for prospect in ready:
        if not prospect.get('email') and not prospect.get('phone'):
            print(f"{Fore.YELLOW}  ⚠ Skipping {prospect.get('business_name', 'Unknown')} — no email or phone{Fore.RESET}")
            continue

        email_draft = drafter.draft_email(prospect)
        business_name = prospect.get('business_name', 'Unknown').replace(' ', '_').replace('/', '_')

        # Save as text file
        draft_file = os.path.join(drafts_dir, f"{business_name}.txt")
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(f"TO: {prospect.get('email', 'N/A')}\n")
            f.write(f"PHONE: {prospect.get('phone', 'N/A')}\n")
            f.write(f"SUBJECT: {email_draft['subject']}\n")
            f.write(f"{'='*50}\n\n")
            f.write(email_draft['body_text'])

        print(f"{Fore.GREEN}  ✓ Drafted: {prospect.get('business_name')}{Fore.RESET}")
        drafted_count += 1

    print(f"\n{Fore.GREEN}✅ Drafted {drafted_count} emails → saved to ./drafts/{Fore.RESET}")


def option_preview(drafter, pipeline):
    """Option 3: Preview Drafted Emails"""
    drafts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'drafts')

    if not os.path.exists(drafts_dir):
        print(f"{Fore.YELLOW}No drafts found. Run option 2 first.{Fore.RESET}")
        return

    files = sorted([f for f in os.listdir(drafts_dir) if f.endswith('.txt')])
    if not files:
        print(f"{Fore.YELLOW}No draft files found.{Fore.RESET}")
        return

    print(f"\n{Fore.CYAN}Found {len(files)} drafts:{Fore.RESET}\n")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    print(f"  A. Show all")

    choice = input(f"\nSelect draft to preview (number or A): ").strip()

    if choice.upper() == 'A':
        selected = files
    else:
        try:
            idx = int(choice) - 1
            selected = [files[idx]]
        except (ValueError, IndexError):
            print(f"{Fore.RED}Invalid selection.{Fore.RESET}")
            return

    for f in selected:
        filepath = os.path.join(drafts_dir, f)
        print(f"\n{'='*60}")
        print(f"{Fore.CYAN}📧 {f}{Fore.RESET}")
        print(f"{'='*60}")
        with open(filepath, 'r', encoding='utf-8') as df:
            print(df.read())
        print(f"{'='*60}\n")


def option_send(drafter, sender, pipeline):
    """Option 4: Send Emails (with confirmation)"""
    print(f"\n{Fore.CYAN}=== Send Emails ==={Fore.RESET}")

    if not sender.username or not sender.password:
        print(f"{Fore.RED}❌ Email credentials not configured. Set up .env first.{Fore.RESET}")
        return

    ready = pipeline.get_ready_prospects()
    sendable = [p for p in ready if p.get('email')]

    if not sendable:
        print(f"{Fore.YELLOW}No prospects with email addresses in 'Ready' status.{Fore.RESET}")
        return

    # Check daily limit
    if not sender.can_send_more():
        print(f"{Fore.RED}❌ Daily email limit reached. Try again tomorrow.{Fore.RESET}")
        return

    stats = sender.get_send_stats()
    remaining = sender.max_daily - stats['today_count']

    print(f"\n  Prospects ready to send: {len(sendable)}")
    print(f"  Daily limit remaining:  {remaining}")
    print(f"  Delay between emails:   {sender.delay} seconds")
    print(f"\n  Emails to send:\n")

    for i, p in enumerate(sendable[:remaining], 1):
        print(f"    {i}. {p.get('business_name')} → {p.get('email')}")

    print(f"\n{Fore.YELLOW}⚠️  This will send REAL emails. Are you sure?{Fore.RESET}")
    confirm = input("Type 'SEND' to confirm: ").strip()

    if confirm != 'SEND':
        print("Aborted. No emails sent.")
        return

    # Draft and send each email
    sent_count = 0
    for p in sendable[:remaining]:
        email_draft = drafter.draft_email(p)
        print(f"\n  [{sent_count+1}/{min(len(sendable), remaining)}] Sending to {p.get('email')}...")

        success, err = sender.send_email(
            p['email'],
            email_draft['subject'],
            email_draft['body_text'],
            email_draft['body_html']
        )

        if success:
            print(f"  {Fore.GREEN}✓ Sent!{Fore.RESET}")
            followup_date = (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d')
            pipeline.mark_email_sent(p['business_name'])
            pipeline.update_status(p['business_name'], 'Sent')
            sent_count += 1
        else:
            print(f"  {Fore.RED}✗ Failed: {err}{Fore.RESET}")

        # Rate limit delay
        if sent_count < min(len(sendable), remaining):
            print(f"  ⏳ Waiting {sender.delay}s before next email...")
            time.sleep(sender.delay)

    sender.disconnect()
    print(f"\n{Fore.GREEN}✅ Batch complete: {sent_count} sent, {len(sendable) - sent_count} failed{Fore.RESET}")


def option_pipeline(pipeline):
    """Option 5: View Pipeline Status"""
    print(f"\n{Fore.CYAN}=== Pipeline Status ==={Fore.RESET}\n")
    pipeline.display_pipeline()
    stats = pipeline.get_stats()

    print(f"\n{Fore.WHITE}📊 Summary:{Fore.RESET}")
    for key, val in stats.items():
        print(f"  {key}: {val}")


def option_followups(drafter, sender, pipeline):
    """Option 6: Send Follow-ups"""
    print(f"\n{Fore.CYAN}=== Follow-up Emails ==={Fore.RESET}")

    due = pipeline.get_followup_due()
    if not due:
        print(f"{Fore.YELLOW}No follow-ups due today.{Fore.RESET}")
        return

    print(f"Found {len(due)} follow-ups due:\n")
    for i, p in enumerate(due, 1):
        print(f"  {i}. {p.get('business_name')} ({p.get('email', 'no email')})")

    confirm = input(f"\nDraft and send follow-ups? (y/n): ").strip().lower()
    if confirm != 'y':
        return

    for p in due:
        if not p.get('email'):
            continue

        followup = drafter.draft_followup(p, 1)
        success, err = sender.send_email(
            p['email'],
            followup['subject'],
            followup['body_text']
        )

        if success:
            print(f"  {Fore.GREEN}✓ Follow-up sent to {p.get('business_name')}{Fore.RESET}")
            pipeline.update_status(p['business_name'], 'Follow-up')
        else:
            print(f"  {Fore.RED}✗ Failed for {p.get('business_name')}: {err}{Fore.RESET}")

        time.sleep(sender.delay)

    sender.disconnect()


def option_add_manual(pipeline):
    """Option 7: Add Prospect Manually"""
    print(f"\n{Fore.CYAN}=== Add Prospect Manually ==={Fore.RESET}\n")

    name = input("  Business Name: ").strip()
    if not name:
        print("Business name is required.")
        return

    industry = input("  Industry (textile/retail/clinic/diamond/manufacturing): ").strip()
    city = input("  City: ").strip() or "Surat"
    area = input("  Area/Market: ").strip()
    contact = input("  Contact Person: ").strip()
    phone = input("  Phone/WhatsApp: ").strip()
    email = input("  Email: ").strip()
    notes = input("  Notes: ").strip()

    prospect = {
        'business_name': name,
        'industry': industry,
        'city': city,
        'area': area,
        'contact_person': contact,
        'phone': phone,
        'email': email,
        'has_website': False,
        'source': 'Manual',
        'found_date': datetime.now().strftime('%Y-%m-%d'),
        'email_sent': 'No',
        'email_sent_date': '',
        'followup_date': '',
        'status': 'Ready',
        'notes': notes
    }

    success, msg = pipeline.add_prospect(prospect)
    if success:
        print(f"\n{Fore.GREEN}✅ {name} added to pipeline!{Fore.RESET}")
    else:
        print(f"\n{Fore.YELLOW}⚠️  {msg}{Fore.RESET}")


def option_whatsapp(drafter, pipeline):
    """Option 8: Generate WhatsApp & Instagram Outreach"""
    import urllib.parse
    import webbrowser
    print(f"\n{Fore.CYAN}=== WhatsApp & Instagram Outreach Generator ==={Fore.RESET}")

    ready = pipeline.get_ready_prospects()
    with_phone = [p for p in ready if p.get('phone')]

    if not with_phone:
        print(f"{Fore.YELLOW}No prospects with phone numbers found.{Fore.RESET}")
        return

    print(f"\nGenerating customized messages for {len(with_phone)} prospects:\n")

    wa_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'whatsapp_messages')
    insta_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instagram_dms')
    os.makedirs(wa_dir, exist_ok=True)
    os.makedirs(insta_dir, exist_ok=True)

    links_summary = []

    for p in with_phone:
        msg = drafter.draft_whatsapp(p)
        insta_msg = drafter.draft_instagram(p)
        business_name = p.get('business_name', 'Unknown').replace(' ', '_').replace('/', '_')

        # Clean 10-digit / 12-digit Indian phone number
        raw_phone = re.sub(r'\D', '', p.get('phone', ''))
        if len(raw_phone) == 10:
            clean_phone = '91' + raw_phone
        elif len(raw_phone) >= 11 and raw_phone.startswith('0'):
            clean_phone = '91' + raw_phone[1:]
        elif len(raw_phone) >= 12 and raw_phone.startswith('91'):
            clean_phone = raw_phone
        else:
            clean_phone = raw_phone

        # 1-Click WhatsApp web / app link
        encoded_msg = urllib.parse.quote(msg)
        wa_link = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"
        links_summary.append((p.get('business_name'), clean_phone, wa_link))

        # Save WhatsApp file with 1-click link
        wa_path = os.path.join(wa_dir, f"{business_name}_wa.txt")
        with open(wa_path, 'w', encoding='utf-8') as f:
            f.write(f"BUSINESS: {p.get('business_name')}\n")
            f.write(f"PHONE: {p.get('phone')}\n")
            f.write(f"1-CLICK WHATSAPP LINK:\n{wa_link}\n")
            f.write(f"{'='*50}\n\n")
            f.write(msg)

        # Save Instagram DM file
        insta_path = os.path.join(insta_dir, f"{business_name}_insta.txt")
        with open(insta_path, 'w', encoding='utf-8') as f:
            f.write(f"BUSINESS: {p.get('business_name')}\n")
            f.write(f"INSTAGRAM SEARCH: https://www.instagram.com/explore/tags/{p.get('business_name', '').replace(' ', '').lower()}/\n")
            f.write(f"{'='*50}\n\n")
            f.write(insta_msg)

        print(f"  {Fore.GREEN}✓ {p.get('business_name')} → WhatsApp Link + Insta DM saved{Fore.RESET}")

    print(f"\n{Fore.GREEN}✅ Saved {len(with_phone)} WhatsApp links in ./whatsapp_messages/{Fore.RESET}")
    print(f"{Fore.GREEN}✅ Saved {len(with_phone)} Instagram DMs in ./instagram_dms/{Fore.RESET}")

    # Interactive 1-click launcher
    open_choice = input(f"\n{Fore.CYAN}Do you want to open 1-click WhatsApp chats in your browser now? (y/n): {Fore.RESET}").strip().lower()
    if open_choice == 'y':
        for bname, phone, link in links_summary[:5]:
            print(f"Opening chat for {bname} ({phone})...")
            webbrowser.open(link)
            time.sleep(1.5)
        print(f"{Fore.GREEN}✓ Opened top chats!{Fore.RESET}")


def option_test_connection(sender):
    """Option 9: Test Email Connection"""
    print(f"\n{Fore.CYAN}=== Testing SMTP Connection ==={Fore.RESET}\n")

    if not sender.username:
        print(f"{Fore.RED}❌ No email configured. Set up .env file first.{Fore.RESET}")
        return

    print(f"  Server:   {sender.smtp_server}")
    print(f"  Port:     {sender.smtp_port}")
    print(f"  Username: {sender.username}")
    print(f"  Testing...")

    if sender.test_connection():
        test_to = input(f"\n  Send a test email? Enter recipient (or press Enter to skip): ").strip()
        if test_to:
            sender.send_test_email(test_to)


def option_export(pipeline):
    """Option 10: Export Report"""
    print(f"\n{Fore.CYAN}=== Exporting Report ==={Fore.RESET}\n")
    filename = pipeline.export_report()
    print(f"{Fore.GREEN}✅ Report exported to: {filename}{Fore.RESET}")


def main():
    print_banner()
    check_env_setup()

    # Initialize modules
    prospector = BusinessProspector()
    drafter = ColdEmailDrafter()
    sender = EmailSender()
    pipeline = PipelineManager(DATABASE_FILE)

    while True:
        print_menu()
        choice = input(f"  {Fore.CYAN}Choose an option:{Fore.RESET} ").strip()

        try:
            if choice == '1':
                option_research(prospector, pipeline)
            elif choice == '2':
                option_draft_emails(drafter, pipeline)
            elif choice == '3':
                option_preview(drafter, pipeline)
            elif choice == '4':
                option_send(drafter, sender, pipeline)
            elif choice == '5':
                option_pipeline(pipeline)
            elif choice == '6':
                option_followups(drafter, sender, pipeline)
            elif choice == '7':
                option_add_manual(pipeline)
            elif choice == '8':
                option_whatsapp(drafter, pipeline)
            elif choice == '9':
                option_test_connection(sender)
            elif choice == '10':
                option_export(pipeline)
            elif choice == '0':
                print(f"\n{Fore.CYAN}Goodbye! Happy prospecting. 🚀{Fore.RESET}\n")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Fore.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Returning to menu...{Fore.RESET}")
        except Exception as e:
            print(f"\n{Fore.RED}Error: {e}{Fore.RESET}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
