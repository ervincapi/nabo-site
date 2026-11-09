#!/usr/bin/env python3
"""Render legal/*.html and 404.html with the site chrome.

The legal texts themselves are being prepared in six languages (Terms, Privacy Policy, Community
Guidelines, DPA, sub-processor list). Until they land, each page states plainly what it will cover
and how to reach us, so the App Store privacy URL and footer links resolve to real, styled pages.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · Nabo</title>
<meta name="description" content="{description}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#F7F6F2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0F1A17" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}assets/style.css">
<script>(function(){{try{{var t=localStorage.getItem('nabo-theme');if(t)document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body>
<header class="nav is-scrolled" id="nav">
  <div class="wrap">
    <a class="brand" href="{base}" aria-label="Nabo">
      <span class="mark" aria-hidden="true"><svg viewBox="0 0 64 64"><path d="M18 46V28l14-11 14 11v18H36V34h-8v12z" fill="currentColor"/></svg></span>
      Nabo
    </a>
    <nav class="nav-links" aria-label="Legal">
      <a href="{base}legal/terms.html">Terms</a>
      <a href="{base}legal/privacy.html">Privacy</a>
      <a href="{base}legal/guidelines.html">Guidelines</a>
    </nav>
    <div class="nav-right">
      <a class="btn btn-ghost btn-sm" href="{base}">← Back to nabo.al</a>
    </div>
  </div>
</header>
<main id="main">
"""

FOOT = """
</main>
<footer class="footer">
  <div class="wrap footer-bottom" style="margin-top:0;border-top:0;padding-top:0">
    <span>© 2026 Nabo · All rights reserved.</span>
    <span><a href="mailto:hello@nabo.al">hello@nabo.al</a></span>
  </div>
</footer>
<script src="{base}assets/site.js" defer></script>
</body>
</html>
"""

NOTICE = """<div class="notice"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg><span>{text}</span></div>"""

PAGES = {
    "terms": dict(
        title="Terms of service",
        description="Terms of service for Nabo, the private community app for one apartment building.",
        meta="Draft · applies to the pilot programme · last updated 9 November 2026",
        notice="The full terms in Albanian, English, French, Italian, German and Spanish are being finalised. Until they are published, pilot buildings are covered by the pilot agreement signed with their property manager, together with the summary below.",
        body="""
<h2>What Nabo is</h2>
<p>Nabo is a private community service for a single apartment building, provided to the building through its property manager or certified administrator (the <strong>customer</strong>). Residents use Nabo free of charge, once approved by the customer.</p>
<h2>Accounts</h2>
<p>You sign in with your email address; there is no password. You must be at least 16 years old. You are responsible for keeping your email account secure and for everything posted from your account. You can see your active devices and sign them out in the app.</p>
<h2>Your content</h2>
<p>You keep ownership of what you post. You grant Nabo the licence needed to store, display and, at your request, translate it for the other members of your building. Content never leaves the building it was posted in. You agree to follow the <a href="guidelines.html">community guidelines</a>; content that breaks them can be hidden or removed, and you can appeal every decision.</p>
<h2>Lending and borrowing</h2>
<p>The lend &amp; borrow board connects neighbours; Nabo is not a party to any loan, and no payments or deposits are handled in the app. Lenders decide who borrows and remain responsible for their items.</p>
<h2>Billing</h2>
<p>Residents never pay. The customer pays a flat monthly fee per building after a 60-day free pilot, billed on the web by card or SEPA direct debit, and may cancel at any time at the end of a billing period. There are no in-app purchases.</p>
<h2>Ending your use</h2>
<p>You can delete your account from the app at any time. When you move out, the customer deactivates your membership and your access ends immediately; your posts remain visible to the building unless you delete them first.</p>
<h2>Liability and law</h2>
<p>Nabo is provided with reasonable care but without warranty of uninterrupted availability. To the extent permitted by law, liability is limited to the fees paid by the customer for the building in the preceding twelve months. Mandatory consumer rights in your country are not affected.</p>
<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:hello@nabo.al">hello@nabo.al</a>.</p>
""",
    ),
    "privacy": dict(
        title="Privacy policy",
        description="How Nabo handles personal data: what we collect, why, where it is stored, and your rights.",
        meta="Draft · last updated 9 November 2026",
        notice="The full privacy policy in six languages, the data processing agreement for buildings and the sub-processor list are being finalised. The summary below describes how Nabo already works.",
        body="""
<h2>Who is responsible</h2>
<p>For a building's community, the property manager or administrator is the data controller and Nabo acts as the processor under a data processing agreement. For your account itself (email address, sessions, language), Nabo is the controller.</p>
<h2>What we collect</h2>
<ul>
<li><strong>Account:</strong> email address, display name, preferred language, devices and sessions.</li>
<li><strong>Membership:</strong> building, unit and role, as confirmed by the building's manager.</li>
<li><strong>Content:</strong> posts, comments, reactions, events, listings and messages you create, and any images you attach.</li>
<li><strong>Delivery:</strong> for announcements, whether each recipient received, opened and acknowledged them. Managers need this to prove that notices reached residents.</li>
<li><strong>Technical:</strong> crash reports and anonymous usage statistics, with IP addresses truncated.</li>
</ul>
<h2>What we do not do</h2>
<p>No advertising, no selling or sharing of data for marketing, no tracking across other apps or sites, no reading of your messages for anything other than delivering them and acting on reports you or others make.</p>
<h2>Where data lives</h2>
<p>All data is stored in Frankfurt, Germany, in the European Union. Transactional emails are sent by an email provider; post translations are produced on demand by a translation provider that does not retain the text. A full sub-processor list will be published here.</p>
<h2>How long we keep it</h2>
<p>Content stays while your building uses Nabo. Delivery logs for official notices are kept for the period required by the building's country. When a building leaves Nabo, its data is deleted within 90 days. Deleting your account removes your personal data and anonymises your past posts.</p>
<h2>Your rights</h2>
<p>You can export everything you have posted and delete your account directly in the app. You can also ask us to access, correct, restrict or object to processing of your data, and you have the right to complain to your national data protection authority.</p>
<h2>Age</h2>
<p>Nabo is for people aged 16 and over.</p>
<h2>Contact</h2>
<p>Privacy questions and requests: <a href="mailto:hello@nabo.al">hello@nabo.al</a>.</p>
""",
    ),
    "guidelines": dict(
        title="Community guidelines",
        description="The few rules that keep a Nabo building friendly, useful and safe.",
        meta="Applies to every building · last updated 9 November 2026",
        notice="These guidelines are shown to every resident before their first post, in the six languages Nabo supports.",
        body="""
<h2>Be a good neighbour</h2>
<p>Write the way you would talk in the stairwell. Disagree with ideas, not people. Assume good intent; most problems in a building are misunderstandings.</p>
<h2>Keep it about the building</h2>
<p>Questions, notices, recommendations, lost and found, events, things to lend or give away. Not politics, not national news, not advertising for businesses outside the building.</p>
<h2>Respect privacy</h2>
<p>Do not post other people's phone numbers, photos, or details about who is away from home. Do not photograph neighbours or their doors without asking. What is said in the building stays in the building.</p>
<h2>No harassment, no discrimination</h2>
<p>No insults, threats, or content that targets anyone for who they are. Repeated unwanted contact is harassment, even when each message seems harmless.</p>
<h2>No scams, no sales</h2>
<p>The lend &amp; borrow board is for lending and giving, not selling. Never ask for payments or deposits. Report anything that looks like a scam.</p>
<h2>Reporting and moderation</h2>
<p>Every post, comment and message has a report button. Reports go to your building's moderators; content with three independent reports is hidden automatically pending review. Unresolved reports escalate to Nabo within 24 hours. Every decision comes with a reason, and you can appeal it.</p>
<h2>Managers and moderators</h2>
<p>Managers and moderators follow the same rules and are held to a higher standard. They may pin, hide or remove content and deactivate memberships, and each action is logged.</p>
<h2>Contact</h2>
<p>Something urgent or sensitive? Write to <a href="mailto:hello@nabo.al">hello@nabo.al</a>.</p>
""",
    ),
}


def page(slug: str, spec: dict) -> str:
    base = "../"
    html = HEAD.format(title=spec["title"], description=spec["description"], robots="index,follow", base=base)
    html += f"""<section class="doc"><div class="wrap">
<h1 class="display">{spec['title']}</h1>
<p class="meta">{spec['meta']}</p>
{NOTICE.format(text=spec['notice'])}
{spec['body']}
</div></section>"""
    html += FOOT.format(base=base)
    return html


def not_found() -> str:
    # Served for any path, so resolve assets from the site root — which is /nabo-site/ on the GitHub Pages preview.
    base = ""
    html = HEAD.format(title="Page not found", description="This page does not exist.", robots="noindex", base=base)
    html = html.replace(
        "<meta charset=\"utf-8\">",
        "<meta charset=\"utf-8\">\n<script>document.write('<base href=\"' + (location.pathname.indexOf('/nabo-site/') === 0 ? '/nabo-site/' : '/') + '\">');</script>",
        1,
    )
    html += """<section class="nf"><div class="wrap">
<span class="eyebrow">404</span>
<h1 class="display">Wrong <em>door.</em></h1>
<p class="lede" style="text-align:center">This page is not in the building. Try the entrance.</p>
<a class="btn btn-primary" href="/">Back to nabo.al</a>
</div></section>"""
    html += FOOT.format(base=base)
    return html


if __name__ == "__main__":
    (ROOT / "legal").mkdir(exist_ok=True)
    for slug, spec in PAGES.items():
        (ROOT / "legal" / f"{slug}.html").write_text(page(slug, spec), encoding="utf-8")
        print(f"wrote legal/{slug}.html")
    (ROOT / "404.html").write_text(not_found(), encoding="utf-8")
    print("wrote 404.html")
