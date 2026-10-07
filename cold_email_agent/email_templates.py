# email_templates.py
"""
High-Converting B2B & International Outreach Templates for Reflecter Technologies.
Engineered for:
1. International businesses (US, UK, UAE, Canada, Australia) seeking clients, digital presence, and operational automation.
2. Zero AI buzzwords, mobile-first brevity (100-140 words).
3. 100% Free interactive prototype hook.
"""

INTERNATIONAL_B2B_TEMPLATE = """\
Hi {contact_person},

I noticed that while {business_name} has built a solid reputation in {area} for {industry_product}, your business currently doesn't have a dedicated web portal where potential clients searching online can view your past work, check availability, or submit project inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype website for {business_name}—customized to your brand and services, so you can see firsthand how a high-converting digital storefront would bring you more local and out-of-town clients, with zero cost and no obligation.

{cta}

{signature}"""

CONTRACTOR_SERVICES_TEMPLATE = """\
Hi {contact_person},

I came across {business_name} while looking at top-rated {industry_product} providers in {area}. You have fantastic word-of-mouth reviews, but homeowners searching on Google after hours currently have no direct portal to request quotes, browse your recent projects, or verify your licensing details.

At Reflecter Technologies, {proof_line}

We would love to build a 100% free clickable prototype website for {business_name} with an instant quote estimator and mobile booking form—at zero cost and zero obligation.

{cta}

{signature}"""

CLINIC_HEALTHCARE_TEMPLATE = """\
Dear {contact_person},

I noticed {business_name} has strong patient feedback in {area}, but new patients searching online outside regular hours currently have no modern portal to browse treatments, review specialist profiles, or book an appointment directly.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype website for {business_name} with automated mobile booking and service overviews, so you can see exactly how it reduces front-desk load and attracts new patients—with zero cost or strings attached.

{cta}

{signature}"""

RETAIL_SHOWROOM_TEMPLATE = """\
Hi {contact_person},

I noticed that while {business_name} is well-regarded in {area} for {industry_product}, buyers searching online currently have no interactive portal to browse your catalog, check real-time stock, or submit inquiries after your showroom closes.

At Reflecter Technologies, {proof_line}

We would love to build a 100% free interactive digital catalog and demo website for {business_name}—so you can see how easily it showcases your collection and captures inbound orders from outside your immediate city, with zero cost or obligation.

{cta}

{signature}"""

MANUFACTURING_B2B_TEMPLATE = """\
Hi {contact_person},

I noticed that while {business_name} has strong manufacturing capabilities in {area}, procurement managers searching online currently have no dedicated portal to inspect your production specs, request custom RFQs, or review your quality certifications.

At Reflecter Technologies, {proof_line}

We would love to build a 100% free clickable demo platform for {business_name} with an automated quote request engine, so you can see how it drives qualified commercial contracts—completely free with zero obligation.

{cta}

{signature}"""

DEFAULT_TEMPLATE = INTERNATIONAL_B2B_TEMPLATE

# --- Follow-up Sequences ---
FOLLOWUP_1_TEMPLATE = """\
Hi {contact_person},

Just floating this to the top of your inbox. Did you get a chance to review my note regarding {business_name}?

I've already outlined a rough concept of how a custom digital presence could capture inbound client leads for you in {area} after business hours.

I'd still love to share that 2-minute clickable preview link with you—takes under two minutes to inspect and costs absolutely nothing.

{cta}

{signature}"""

FOLLOWUP_2_TEMPLATE = """\
Hi {contact_person},

I know running {business_name} keeps your calendar full, so I'll be brief.

We help traditional offline businesses establish modern, high-converting digital client acquisition pipelines without heavy upfront fees or agency overhead.

Would it be alright if I send over a quick 2-minute video preview of the prototype we envisioned for your brand?

{signature}"""

FINAL_NUDGE_TEMPLATE = """\
Hi {contact_person},

This will be my final message—I don't want to crowd your inbox.

If turning online searchers in {area} into paying clients for {business_name} ever becomes a priority this quarter, our team would be glad to help. I'm always available at +91 91731 08730 or contact@reflecter.in.

Wishing {business_name} continued growth.

{signature}"""

# --- WhatsApp Outreach (Hinglish / English) ---
WHATSAPP_INTERNATIONAL_TEMPLATE = """\
Hello {contact_person}! 👋

This is Shailesh from Reflecter Technologies. I came across {business_name} in {area}.

Noticed that clients searching online currently don't have a direct portal to review your services, browse previous work, or submit project inquiries after hours.

We build custom high-speed websites & automated client lead pipelines. We'd love to share a 100% FREE interactive demo website built specifically for {business_name} so you can see how it looks and captures leads.

Zero cost or obligation. Would you like me to send over the 2-minute preview link?

Best regards,
Shailesh Singh | Reflecter Technologies
www.reflecter.in"""

WHATSAPP_TEXTILE_TEMPLATE = """\
Namaste {contact_person} ji,

Main Reflecter Technologies se baat kar raha hoon. Humne dekha ki {business_name} {area} mein kaafi well-known hai, par online inquiries ke liye aapka koi direct portal nahi hai.

Humne haal hi mein ek textile manufacturer ke liye ERP aur real-time order tracking system banaya tha, jisse unka manual paperwork khatam ho gaya aur dispatch speed 40% badh gayi.

Kya main aapko ek 2-minute ka free demo link bhejoon jisme aap dekh sakein ki aapke brand ke liye ek modern digital presence kaisa lagega? Bilkul free hai, koi obligation nahi.

Agar theek lage toh bas 'Yes' reply kar dijiye."""

WHATSAPP_CLINIC_TEMPLATE = """\
Hello Dr. {contact_person},

This is Shailesh from Reflecter Technologies. I noticed {business_name} has great patient trust in {area}, but new patients currently have no direct portal to book appointments or explore treatments after hours.

We recently built an automated patient appointment system that reduced clinic no-shows and front-desk workload significantly.

Can I share a 100% FREE interactive demo website for {business_name} showing how automated mobile booking would work? Zero cost or obligation.

Best regards,
Shailesh Singh | Reflecter Technologies"""

# --- Signature Template ---
SIGNATURE_TEMPLATE = """\
Best regards,

Shailesh Singh
Reflecter Technologies | Custom Software & Growth Engineering
WhatsApp / Direct: +91 91731 08730
Portfolio: www.reflecter.in | Surat, Gujarat, India"""

# --- Clean Mobile HTML Wrapper ---
HTML_WRAPPER = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            font-size: 15px;
            color: #24292e;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        .container {{
            padding: 24px;
            max-width: 580px;
            margin: 0 auto;
        }}
        p {{
            margin-bottom: 1.1em;
        }}
        .signature {{
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #eaecef;
            color: #586069;
            font-size: 14px;
        }}
        .signature a {{
            color: #0366d6;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        {body_content}
    </div>
</body>
</html>"""
