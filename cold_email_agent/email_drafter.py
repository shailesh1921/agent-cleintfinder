import re
from email_templates import *
try:
    from config import *
except ImportError:
    pass # If config is not available yet

class ColdEmailDrafter:
    def __init__(self):
        self.banned_words = [
            "cutting-edge", "game-changer", "spearheaded", "synergy",
            "in today's digital era", "unleash potential"
        ]
        
    def get_template(self, industry):
        industry = industry.lower() if industry else ''
        if 'textile' in industry or 'fabric' in industry or 'garment' in industry:
            return TEXTILE_TEMPLATE
        elif 'clinic' in industry or 'medical' in industry or 'health' in industry:
            return CLINIC_TEMPLATE
        elif 'retail' in industry or 'showroom' in industry:
            return RETAIL_TEMPLATE
        elif 'diamond' in industry or 'jewellery' in industry:
            return DIAMOND_TEMPLATE
        elif 'manufacturing' in industry or 'chemical' in industry or 'auto' in industry:
            return MANUFACTURING_TEMPLATE
        else:
            return DEFAULT_TEMPLATE

    def get_proof_line(self, industry):
        industry = industry.lower() if industry else ''
        if 'textile' in industry or 'fabric' in industry or 'garment' in industry:
            return 'we recently built an order tracking system for a Surat manufacturer that eliminated paperwork and cut dispatch delays by ~40%.'
        elif 'diamond' in industry or 'jewellery' in industry:
            return 'we recently built a secure digital catalog for a Surat firm, enabling 24/7 inventory browsing for overseas buyers.'
        elif 'clinic' in industry or 'medical' in industry or 'health' in industry:
            return 'we recently integrated WhatsApp appointment alerts for a local clinic, cutting no-shows and front-desk workload.'
        elif 'retail' in industry or 'showroom' in industry:
            return 'we recently engineered a fashion storefront with live inventory sync and sub-2-second mobile load speeds.'
        elif 'manufacturing' in industry or 'chemical' in industry or 'auto' in industry:
            return 'we recently built a production tracking system for a manufacturer that replaced manual ledgers with real-time pipelines.'
        else:
            return 'we recently helped a local business replace paper ledgers with an automated digital system that saves hours daily.'

    def get_observation_hook(self, prospect):
        business_name = prospect.get('business_name', 'your business')
        area = prospect.get('area', 'your area')
        industry_product = prospect.get('industry', 'services')
        return f"I noticed that while {business_name} has a strong reputation in {area} for {industry_product}, customers searching online currently have no direct portal to browse your collection, check availability, or place inquiries after business hours."

    def get_cta(self):
        return "Would it be okay if I send over a 2-minute preview link tomorrow?"
        
    def get_signature(self):
        return SIGNATURE_TEMPLATE

    def personalize(self, template, prospect):
        # Handle empty/missing values gracefully
        contact_person = prospect.get('contact_person') or 'there'
        business_name = prospect.get('business_name') or 'your business'
        area = prospect.get('area') or 'your area'
        city = prospect.get('city') or 'Surat'
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
        if words < 100 or words > 140:
            print(f"WARNING: Email body word count is {words}. It should be between 100 and 140 words.")
        
        lower_body = body.lower()
        found_banned = []
        for word in self.banned_words:
            if word in lower_body:
                found_banned.append(word)
        if found_banned:
            print(f"WARNING: Found banned words in email body: {', '.join(found_banned)}")

    def draft_email(self, prospect):
        industry = prospect.get('industry', '')
        template = self.get_template(industry)
        body_text = self.personalize(template, prospect)
        
        self.validate_word_count(body_text)
        
        # Convert text to basic HTML paragraphs
        paragraphs = body_text.split('\n\n')
        html_paragraphs = [f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphs]
        body_content = "".join(html_paragraphs)
        body_html = HTML_WRAPPER.format(body_content=body_content)
        
        subject = f"Free demo website/catalog for {prospect.get('business_name', 'your business')}"
        
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
            'subject': f"Re: Free demo website/catalog for {prospect.get('business_name', 'your business')}",
            'body_text': self.personalize(template, prospect)
        }
        
    def draft_whatsapp(self, prospect):
        industry = prospect.get('industry', '').lower()
        if 'clinic' in industry or 'medical' in industry or 'health' in industry:
            template = WHATSAPP_CLINIC_TEMPLATE
        else:
            template = WHATSAPP_TEXTILE_TEMPLATE
            
        return self.personalize(template, prospect)

    def draft_instagram(self, prospect):
        bname = prospect.get('business_name', 'your brand')
        area = prospect.get('area', 'your city')
        ind = prospect.get('industry', 'business').lower()
        
        if 'textile' in ind or 'saree' in ind or 'fabric' in ind or 'retail' in ind:
            dm = (
                f"Hey {bname} team! 👋 Love your collection in {area}.\n\n"
                f"Noticed customers searching online can't browse your catalog or place orders after hours. "
                f"At Reflecter Technologies, we recently built an online catalog for a Surat textile firm that cut dispatch delays by 40%.\n\n"
                f"Can we send you a 100% FREE interactive demo website for {bname} tomorrow? Zero cost or obligation.\n\n"
                f"— Shailesh | Reflecter Technologies (+91 91731 08730)"
            )
        else:
            dm = (
                f"Hey {bname} team! 👋 Noticed your strong presence in {area}.\n\n"
                f"Right now clients searching online don't have a direct portal to check services or book appointments after hours. "
                f"We build custom high-speed websites & automated WhatsApp booking systems.\n\n"
                f"Can I share a 100% FREE 2-minute prototype website for {bname} tomorrow to see how it looks?\n\n"
                f"— Shailesh | Reflecter Technologies (+91 91731 08730)"
            )
        return dm

    def preview_email(self, prospect):
        email_draft = self.draft_email(prospect)
        print("="*50)
        print(f"SUBJECT: {email_draft['subject']}")
        print("="*50)
        print(email_draft['body_text'])
        print("="*50)
