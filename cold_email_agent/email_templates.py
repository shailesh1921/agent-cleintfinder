# email_templates.py

TEXTILE_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for textile and garment manufacturing, customers searching online currently have no direct portal to browse your collection, check availability, or place inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your brand, with zero cost and no obligation.

{cta}

{signature}"""

CLINIC_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for your medical services, patients searching online currently have no direct portal to book appointments or check availability after hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your clinic, with zero cost and no obligation.

{cta}

{signature}"""

RETAIL_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for retail, customers searching online currently have no direct portal to browse your collection, check availability, or place inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your brand, with zero cost and no obligation.

{cta}

{signature}"""

DIAMOND_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for diamond and jewellery, buyers searching online currently have no direct portal to browse your collection, check availability, or place inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your brand, with zero cost and no obligation.

{cta}

{signature}"""

MANUFACTURING_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for manufacturing, clients searching online currently have no direct portal to browse your products, check availability, or place inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your brand, with zero cost and no obligation.

{cta}

{signature}"""

DEFAULT_TEMPLATE = """\
Dear {contact_person},

I noticed that while {business_name} has a strong reputation in {area} for {industry_product}, customers searching online currently have no direct portal to browse your offerings, check availability, or place inquiries after business hours.

At Reflecter Technologies, {proof_line}

We would love to design a 100% free interactive prototype/demo website tailored specifically for {business_name} — so you can see exactly how a modern digital presence would look for your brand, with zero cost and no obligation.

{cta}

{signature}"""

FOLLOWUP_1_TEMPLATE = """\
Hi {contact_person},

Just floating this to the top of your inbox. Did you get a chance to see my previous email about {business_name}?

I'd still love to send over that 2-minute preview link for a free demo website. No pressure and absolutely zero cost involved.

{cta}

{signature}"""

FOLLOWUP_2_TEMPLATE = """\
Hi {contact_person},

I know how busy running {business_name} must be, so I'll keep this brief. 

We specialize in helping businesses like yours in {city} establish a powerful digital presence without the usual hassle or high upfront costs. 

Could I just send you a quick preview link of what we can do for you?

{signature}"""

FINAL_NUDGE_TEMPLATE = """\
Hi {contact_person},

This will be my last email, but I didn't want to close the loop without trying one more time.

If building a digital portal for {business_name} is on your radar anytime soon, please feel free to reach out. We've helped many others in {area} and would love to do the same for you.

Best wishes for the season,

{signature}"""

WHATSAPP_TEXTILE_TEMPLATE = """\
Namaste {contact_person} ji,

Main Reflecter Technologies se baat kar raha hoon. Humne dekha ki {business_name} {area} mein kaafi well-known hai, par online inquiries ke liye aapka koi direct portal nahi hai.

Humne haal hi mein Surat ke ek textile manufacturer ke liye ERP aur order tracking system banaya tha, jisse unka manual kaam aur dispatch delays 40% tak kam ho gaya.

Kya main aapko ek 2-minute ka free demo link bhejoon jisme aap dekh sakein ki aapke brand ke liye ek modern digital presence kaisa lagega? Koi cost ya obligation nahi hai.

Agar theek lage toh bas 'Yes' reply kar dijiye."""

WHATSAPP_CLINIC_TEMPLATE = """\
Namaste {contact_person} ji,

Main Reflecter Technologies se baat kar raha hoon. Humne dekha ki {business_name} clinic {area} mein kaafi well-known hai, par online appointments ke liye patients ke paas koi direct portal nahi hai.

Humne haal hi mein ek local clinic ke liye WhatsApp automated appointment alerts aur billing set up kiya tha, jisse front-desk ka kaafi time bach raha hai.

Kya main aapko ek 2-minute ka free demo link bhejoon jisme aap dekh sakein ki aapke clinic ke liye ek modern booking system kaisa lagega? Koi cost ya obligation nahi hai.

Agar theek lage toh bas 'Yes' reply kar dijiye."""

SIGNATURE_TEMPLATE = """\
Best regards,

Shailesh Singh
Reflecter Technologies | Surat, Gujarat
Phone: +91 91731 08730 | WhatsApp: +91 91731 08730
Portfolio: www.reflecter.in"""

HTML_WRAPPER = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 16px;
            color: #333333;
            line-height: 1.5;
            margin: 0;
            padding: 0;
        }}
        .container {{
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
        }}
        p {{
            margin-bottom: 1em;
        }}
        .signature {{
            margin-top: 2em;
        }}
        .signature a {{
            color: #0066cc;
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
