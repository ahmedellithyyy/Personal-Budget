# Agro Green website rebuild: brief

Status: paused before any generation. Built with the `10k-websites` skill (re-upload the zip in the new session).
Blocker: the Higgsfield connector in the first session was read-only (balance, models, past generations). No generate, upload or cost-preflight tools.

## Decisions made by the owner
- Audience and single call to action: UK and EU importers (supermarket and wholesale buyers). One enquiry form: request a quote.
- Feeling: premium and fresh. Warm Egyptian light, sand soil, rich produce colour.
- Files live in this folder on branch `claude/new-session-oxif67`. Never merge to main. Move to its own repo later.
- Hero video route: wait for a Higgsfield connector that can generate.

## Facts from the old site (agrogreen.co.uk, read 2026-11-16)
- Growers, packers and exporters of fresh produce from Egypt. Established 2018, paid-up capital EGP 10 million.
- 5,000 acres, sand soil. Produce available 10 months of the year, including January to March.
- Products and export seasons:
  - Sweet potato, organic and conventional, grown from tissue culture: 1 July to 1 March.
  - Dry onions, red and brown: 1 May to end of July.
  - Green beans: 1 September to end of March.
- Certifications named: Global Gap, Food Expert, Sedex. Eight certificate images in `source-assets/certificate/`.
- Cold chain claim: products kept at or below 14 degrees Celsius through the supply chain. Shipping by air and sea.
- Team has over 20 years of experience exporting to the European market.
- Offices: 190 El Hegaz St, Heliopolis, Cairo, (002 02) 21809236. 2 Buckden Close, London SE12 8AB, (+44) 7850086554. info@agrogreen.co.uk
- Founders listed: Ahmed Abdelrahman (Managing Director), Adel Ellithy (Managing Partner), Ayman Elshewy (CFO), Ibrahim Elsedawy (B.D Director).
- Values: integrity, accountability, empowerment, innovation.
- Pages: Home, About, Products (Sweet Potato, Onions, Beans), Operations (packing, exporting), Careers, Contact.

## Faults on the old site to fix
- Browser title says "Green Agro"; the company is Agro Green.
- Placeholder phone number `+555-123-2323` in the header.
- Facebook link points to another company's page (GoldenshutterEg).
- Leftover template text in Arabic for an unrelated brand ("Smile Home").
- Second email domain `info@GreenAgro.com` and a third address in Nasr City that conflict with the contact page.
- Operations page opens with an email confidentiality disclaimer.
- Onion page is titled "Spring Onion" and describes dry onions.
- No meta description, footer copyright 2019, credited to the template vendor.
- Careers CV upload and contact form have no confirmed destination.

## Open questions for the owner
- Are all eight certificates current? Certificate numbers and expiry dates would sit well beside the logos.
- Pack formats, sizes and grades per product. Buyers ask for these first.
- Named customers or supermarkets that can be shown.
- Where enquiry form submissions should land.

## Source assets
`source-assets/` holds the 67 images from the old site. Logo is 624x206 PNG. Best large photo is `slider/slider-1.jpg` at 2400x1200. Team photos are 149x149 and too small to reuse.
