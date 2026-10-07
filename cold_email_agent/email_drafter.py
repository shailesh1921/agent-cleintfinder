import re
from email_templates import *
try:
    from config import *
except ImportError:
    pass

class ColdEmailDrafter:
    def __init__(self):
        self.banned_words = [
            "cutting-edge", "game-changer", "spearheaded", "synergy",
            "in today's digital era", "unleash potential", "paradigm shift"
        ]
        
    def get_template(self, industry):
        industry = industry.lower() if industry else ''
        if any(w in industry for w in ['roof', 'hvac', 'plumb', 'contractor', 'builder', 'landscap', 'repair', 'clean']):
            return CONTRACTOR_SERVICES_TEMPLATE
        elif any(w in industry for w in ['clinic', 'dent', 'chiro', 'physio', 'med spa', 'doctor', 'health']):
            return CLINIC_HEALTHCARE_TEMPLATE
        elif any(w in industry for w in ['retail', 'showroom', 'saree', 'fabric', 'textile', 'jewel', 'furniture', 'boutique']):
            return RETAIL_SHOWROOM_TEMPLATE
        elif any(w in industry for w in ['manufacturing', 'metal', 'fabrication', 'packaging', 'chemical', 'industrial']):
            return MANUFACTURING_B2B_TEMPLATE
        else:
            return INTERNATIONAL_B2B_TEMPLATE

    def get_proof_line(self, industry):
        industry = industry.lower() if industry else ''
        if any(w in industry for w in ['roof', 'hvac', 'plumb', 'contractor', 'builder', 'repair']):
            return 'we recently built a custom quote estimator & mobile client capture portal that increased inbound project leads by over 35% without paid ads.'
        elif any(w in industry for w in ['clinic', 'dent', 'chiro', 'physio', 'med spa', 'health']):
            return 'we recently deployed an automated mobile appointment scheduling system for a clinic that cut patient no-shows by 45%.'
        elif any(w in industry for w in ['retail', 'showroom', 'furniture', 'saree', 'boutique', 'fashion']):
            return 'we engineered high-speed digital catalogs and e-commerce storefronts that load in under 2 seconds and capture after-hours orders seamlessly.'
        elif any(w in industry for w in ['manufacturing', 'metal', 'fabrication', 'packaging']):
            return 'we built an end-to-end B2B client portal and order tracking pipeline that completely replaced manual paperwork and reduced dispatch turnaround times by 40%.'
        else:
            return 'we recently helped an offline business transition to an automated digital portal, capturing after-hours inbound clients and eliminating manual follow-ups.'

    def get_observation_hook(self, prospect):
        business_name = prospect.get('business_name', 'your business')
        area = prospect.get('area', 'your city')
        industry_product = prospect.get('industry', 'services')
        return f"I noticed that while {business_name} has a strong local reputation in {area} for {industry_product}, customers searching online currently have no direct portal to browse your collection, request quotes, or submit inquiries after business hours."

    def get_cta(self):
        return "Would it be okay if I send over a quick 2-minute clickable preview link tomorrow showing what your platform would look like?"
        
    def get_signature(self):
        return SIGNATURE_TEMPLATE

    def personalize(self, template, prospect):
        contact_person = prospect.get('contact_person') or 'there'
        business_name = prospect.get('business_name') or 'your business'
        area = prospect.get('area') or prospect.get('city') or 'your area'
        city = prospect.get('city') or 'your city'
        industry = prospect.get('industry') or 'services'
        
        proof_line = self.get_proof_line(industry)
        cta = self.get_cta()
        signature = self.get_signature()
        
        personalized = template.format(
            contact_person=contact_person,
            business_name=business_name,
            area=area,
            city=city,
            industry_product=industry,
            proof_line=proof_line,
            cta=cta,
            signature=signature
        )
        return personalized

    def validate_word_count(self, body):
        words = len(re.findall(r'\b\w+\b', body))
        if words < 90 or words > 150:
            pass # Keep advisory warning silent unless debugging
        
        lower_body = body.lower()
        found_banned = [w for w in self.banned_words if w in lower_body]
        if found_banned:
            print(f"WARNING: Found banned words in email body: {', '.join(found_banned)}")

    def draft_email(self, prospect):
        industry = prospect.get('industry', '')
        template = self.get_template(industry)
        body_text = self.personalize(template, prospect)
        
        self.validate_word_count(body_text)
        
        paragraphs = body_text.split('\n\n')
        html_paragraphs = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs]
        body_content = "".join(html_paragraphs)
        body_html = HTML_WRAPPER.format(body_content=body_content)
        
        subject = f"Free prototype & client portal for {prospect.get('business_name', 'your brand')}"
        
        return {
            'subject': subject,
            'body_text': body_text,
            'body_html': body_html
        }

    def draft_followup(self, prospect, followup_number):
        if followup_number == 1:
            template = FOLLOWUP_1_TEMPLATE
        elif followup_number == 2:
            template = FOLLOWUP_2_TEMPLATE
        else:
            template = FINAL_NUDGE_TEMPLATE
            
        return {
            'subject': f"Re: Free prototype & client portal for {prospect.get('business_name', 'your brand')}",
            'body_text': self.personalize(template, prospect)
        }
        
    def draft_whatsapp(self, prospect):
        industry = prospect.get('industry', '').lower()
        city = prospect.get('city', '').lower()
        
        # If targeting India, use high-converting Hinglish; for US/UK/UAE/etc., use international English
        if city in ['surat', 'ahmedabad', 'mumbai', 'jaipur', 'rajkot', 'delhi', 'pune']:
            if 'clinic' in industry or 'medical' in industry or 'health' in industry:
                template = WHATSAPP_CLINIC_TEMPLATE
            else:
                template = WHATSAPP_TEXTILE_TEMPLATE
        else:
            template = WHATSAPP_INTERNATIONAL_TEMPLATE
            
        return self.personalize(template, prospect)

    def draft_instagram(self, prospect):
        bname = prospect.get('business_name', 'your brand')
        area = prospect.get('area', prospect.get('city', 'your area'))
        ind = prospect.get('industry', 'business').lower()
        
        dm = (
            f"Hey {bname} team! 👋 Love the quality of work you're doing in {area}.\n\n"
            f"I noticed that prospective clients searching online outside business hours currently don't have a direct portal to explore your work, request pricing, or book your services.\n\n"
            f"At Reflecter Technologies, we build high-converting client acquisition websites & automated booking portals.\n\n"
            f"Could I share a 100% FREE interactive prototype website designed for {bname} tomorrow? Zero cost or obligation—just to show you what's possible.\n\n"
            f"— Shailesh | Reflecter Technologies (WhatsApp: +91 91731 08730 | www.reflecter.in)"
        )
        return dm

    def preview_email(self, prospect):
        email_draft = self.draft_email(prospect)
        print("="*60)
        print(f"SUBJECT: {email_draft['subject']}")
        print("="*60)
        print(email_draft['body_text'])
        print("="*60)
