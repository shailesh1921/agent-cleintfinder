import csv
import os
from datetime import datetime

class PipelineManager:
    def __init__(self, csv_file="pipeline.csv"):
        self.csv_file = csv_file
        self.fieldnames = ['business_name', 'industry', 'city', 'area', 'contact_person', 'phone', 'email', 'has_website', 'source', 'found_date', 'email_sent', 'email_sent_date', 'followup_date', 'status', 'notes']
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()

    def _read_all(self):
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def _write_all(self, rows):
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def add_prospect(self, prospect_dict):
        rows = self._read_all()
        
        # Check for duplicates
        phone = prospect_dict.get('phone', '').strip()
        email = prospect_dict.get('email', '').strip()
        
        for r in rows:
            if (phone and r['phone'] == phone) or (email and r['email'] == email):
                return False, "Duplicate phone or email found"
                
        # Fill missing fields with defaults
        for field in self.fieldnames:
            if field not in prospect_dict:
                prospect_dict[field] = ""
                
        if not prospect_dict.get('found_date'):
            prospect_dict['found_date'] = datetime.now().date().isoformat()
        if not prospect_dict.get('status'):
            prospect_dict['status'] = 'New'
            
        rows.append(prospect_dict)
        self._write_all(rows)
        return True, "Added successfully"

    def update_status(self, business_name, new_status):
        rows = self._read_all()
        updated = False
        for r in rows:
            if r['business_name'] == business_name:
                r['status'] = new_status
                updated = True
                break
        if updated:
            self._write_all(rows)
        return updated

    def mark_email_sent(self, business_name, date=None):
        rows = self._read_all()
        updated = False
        for r in rows:
            if r['business_name'] == business_name:
                r['email_sent'] = 'Yes'
                r['email_sent_date'] = date or datetime.now().date().isoformat()
                r['status'] = 'Sent'
                updated = True
                break
        if updated:
            self._write_all(rows)
        return updated

    def get_ready_prospects(self):
        rows = self._read_all()
        return [r for r in rows if r['status'].lower() == 'ready']

    def get_followup_due(self):
        rows = self._read_all()
        today = datetime.now().date().isoformat()
        due = []
        for r in rows:
            if r['status'].lower() == 'sent' and r['followup_date']:
                if r['followup_date'] <= today:
                    due.append(r)
        return due

    def get_stats(self):
        rows = self._read_all()
        stats = {
            'total': len(rows),
            'ready': 0,
            'sent': 0,
            'followup': 0,
            'demo_accepted': 0,
            'closed': 0,
            'opt_out': 0
        }
        for r in rows:
            status = r['status'].lower()
            if status in stats:
                stats[status] += 1
        return stats

    def export_report(self, filename="pipeline_report.txt"):
        stats = self.get_stats()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Pipeline Report ===\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for k, v in stats.items():
                f.write(f"{k.replace('_', ' ').title()}: {v}\n")
        return filename

    def remove_prospect(self, business_name):
        return self.update_status(business_name, "Opt-Out")

    def display_pipeline(self):
        rows = self._read_all()
        print(f"{'Business':<25} | {'Email':<25} | {'Status':<15} | {'Follow-up':<15}")
        print("-" * 85)
        for r in rows:
            name = (r['business_name'][:22] + '...') if len(r['business_name']) > 25 else r['business_name']
            email = (r['email'][:22] + '...') if len(r['email']) > 25 else r['email']
            print(f"{name:<25} | {email:<25} | {r['status']:<15} | {r['followup_date']:<15}")

    def import_from_csv(self, filepath):
        if not os.path.exists(filepath):
            return False, "File not found"
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    normalized = {}
                    for k, v in row.items():
                        clean_k = k.strip().lower().replace(' ', '_').replace('/', '_').replace('-', '_')
                        normalized[clean_k] = v

                    prospect = {
                        'business_name': normalized.get('business_name', ''),
                        'industry': normalized.get('industry_category', normalized.get('industry', '')),
                        'city': normalized.get('city', 'Surat'),
                        'area': normalized.get('area___market_location', normalized.get('area', '')),
                        'contact_person': normalized.get('contact_person___designation', normalized.get('contact_person', '')),
                        'phone': normalized.get('email___whatsapp_number', normalized.get('phone', '')),
                        'email': normalized.get('email', ''),
                        'has_website': 'No',
                        'source': 'Research',
                        'found_date': normalized.get('outreach_date', datetime.now().date().isoformat()),
                        'email_sent': normalized.get('demo_sent_(yes_no)', 'No'),
                        'email_sent_date': '',
                        'followup_date': normalized.get('follow_up_date', ''),
                        'status': normalized.get('status', 'Ready'),
                        'notes': normalized.get('notes___observations', normalized.get('notes', ''))
                    }
                    if '@' in prospect['phone'] and not prospect['email']:
                        prospect['email'] = prospect['phone']
                        prospect['phone'] = ''

                    success, _ = self.add_prospect(prospect)
                    if success:
                        count += 1
            return True, f"Imported {count} prospects"
        except Exception as e:
            return False, str(e)
