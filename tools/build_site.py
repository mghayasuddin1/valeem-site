"""Build the Valeem homepage draft and the three programme/teacher pages from shared parts."""
import json, re, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from subjects import SUBJECTS
R = sys.argv[1]
T = '/home/claude/tools/'
B = 'https://www.valeem.com'
CSS = open(T + 'site.css').read() + open(T + 'site_extra.css').read()
ICONS = open(T + 'icons.svg').read().replace('  </defs>', '''    <symbol id="i-shield" viewBox="0 0 24 24"><path d="M12 3 4 6v6c0 4.5 3.4 8.300 8 9 4.600-.7 8-4.500 8-9V6z"/><path d="m9 12 2 2 4-4"/></symbol>
    <symbol id="i-file" viewBox="0 0 24 24"><path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><path d="M14 3v6h6M8 13h8M8 17h5"/></symbol>
    <symbol id="i-award" viewBox="0 0 24 24"><circle cx="12" cy="9" r="6"/><path d="m8.500 14-1.500 7 5-3 5 3-1.500-7"/></symbol>
    <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
    <symbol id="i-repeat" viewBox="0 0 24 24"><path d="M17 2l4 4-4 4M3 11V9a3 3 0 0 1 3-3h15M7 22l-4-4 4-4M21 13v2a3 3 0 0 1-3 3H3"/></symbol>
    <symbol id="i-lock" viewBox="0 0 24 24"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></symbol>
    <symbol id="i-invoice" viewBox="0 0 24 24"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/></symbol>
    <symbol id="i-sparkle" viewBox="0 0 24 24"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.500 2.500M15.500 15.500 18 18M18 6l-2.500 2.500M8.500 15.500 6 18"/></symbol>
  </defs>''')
JS = open(T + 'site.js').read()

def esc(s): return html.escape(s, quote=True)

# ---------- script: make page-agnostic ----------
js = JS
js = js.replace("var WA_TEXT = \"Hello, I'm interested in Valeem's classes. I would like to book a free demo.\";",
                "var WA_TEXT = document.body.getAttribute('data-wa-text') || \"Hello, I'm interested in Valeem's classes. I would like to book a free demo.\";\n  var LEAD = document.body.getAttribute('data-lead') || 'HOMEPAGE';")
js = js.replace("body.set('interests', 'HOMEPAGE: ' + form.elements.interests.value);", "body.set('interests', LEAD + ': ' + form.elements.interests.value);")
js = js.replace("check('prog', 'Please choose a programme.', !!f.interests.value);", "check('prog', 'Please choose an option.', !!f.interests.value);")
js = js.replace("'Hello, I would like to book a free demo class with Valeem.'", "(LEAD === 'TEACHER APPLICATION' ? 'Hello, I would like to apply to teach with Valeem.' : 'Hello, I would like to book a free demo class with Valeem.')")
a, b = js.index('  /* Banner carousel'), js.index('  /* Gallery strip arrows */')
js = js[:a] + '  if(document.getElementById(\'slides\')) (function(){\n' + js[a:b] + '  })();\n\n' + js[b:]
a = js.index('  /* Gallery strip arrows */'); f = js.index("  var form = $('#leadForm')", a); b = js.index('\n})();', f)
gal = js[a:f].replace("  var strip = $('#strip');", "  var strip = $('#strip');\n  if(strip){")
js = js[:a] + gal.rstrip() + "\n  }\n\n  if($('#leadForm')){\n" + js[f:b] + '\n  }' + r'''

  /* Infinity forms: count views and starts (the form itself sits on Infinity's site) */
  $all('iframe[data-infinity]').forEach(function(fr){
    var kind = fr.getAttribute('data-infinity'), seen = false, started = false;
    if('IntersectionObserver' in window){ new IntersectionObserver(function(en, ob){ if(en[0].isIntersecting && !seen){ seen = true; track('infinity_form_view', {form:kind}); ob.disconnect(); } }, {threshold:.3}).observe(fr); }
    window.addEventListener('blur', function(){ setTimeout(function(){ if(document.activeElement === fr && !started){ started = true; track('infinity_form_start', {form:kind}); } }, 0); });
  });''' + js[b:]
# 'still' is defined inside the carousel closure; define it globally for the gallery
js = js.replace("  /* Programme preselect", "  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n\n  /* Programme preselect")
js = js.replace("  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;\n  hero.style", "  hero.style")
js = js.replace("  /* Programme preselect", r'''  /* Location: the visitor's time zone tells us the country; Gulf families see a line for them */
  var GULF = {SA:['Saudi Arabia', 'https://www.valeem.com/online-tuition-saudi-arabia/', 'Riyadh, Saudi Arabia', 'Saudi time'], AE:['the UAE', 'https://www.valeem.com/online-tuition-uae/', 'Dubai, UAE', 'UAE time'], QA:['Qatar', '', 'Doha, Qatar', 'Qatar time'], KW:['Kuwait', '', 'Kuwait City, Kuwait', 'Kuwait time'], BH:['Bahrain', '', 'Manama, Bahrain', 'Bahrain time'], OM:['Oman', '', 'Muscat, Oman', 'Oman time']};
  var TZ = {'Asia/Riyadh':'SA', 'Asia/Dubai':'AE', 'Asia/Qatar':'QA', 'Asia/Kuwait':'KW', 'Asia/Bahrain':'BH', 'Asia/Muscat':'OM', 'Asia/Karachi':'PK'};
  try{
    var c = TZ[Intl.DateTimeFormat().resolvedOptions().timeZone];
    if(c){
      var g = GULF[c], bar = $('#geo'), city = $('#city'), here = document.body.getAttribute('data-country');
      document.documentElement.setAttribute('data-country', c);
      if(city && g) city.placeholder = 'e.g. ' + g[2];
      if(city && c === 'PK') city.placeholder = 'e.g. Karachi, Pakistan';
      if(g && bar && here !== c){
        $('#geoText').innerHTML = '<b>Families in ' + g[0] + ':</b> classes are scheduled after school, in ' + g[3] + '.';
        var l = $('#geoLink'); if(g[1]){ l.href = g[1]; l.textContent = 'Tuition in ' + g[0]; } else { l.remove(); }
        bar.hidden = false; track('geo_bar_shown', {country:c});
      }
    }
  }catch(e){}

  /* Programme preselect''')
assert "if($('#leadForm'))" in js and 'infinity_form_view' in js and 'LEAD + ' in js and "if(document.getElementById('slides'))" in js and 'if(strip){' in js and 'resolvedOptions' in js
SCRIPT = js

# ---------- shared parts ----------
def head(title, desc, canonical, og_title, og_desc, og_img, jsonld, preload='', noindex=False):
    s = ['<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">',
         open(T + 'gtag.html').read(), open(T + 'pixel.html').read(),
         f'<title>{title}</title>', f'<meta name="description" content="{esc(desc)}">', f'<link rel="canonical" href="{canonical}">']
    if noindex: s.append('<meta name="robots" content="noindex, follow"><!-- REMOVE this robots line when this page becomes the real homepage -->')
    s += ['<meta property="og:type" content="website">', '<meta property="og:site_name" content="Valeem">',
          f'<meta property="og:title" content="{esc(og_title)}">', f'<meta property="og:description" content="{esc(og_desc)}">',
          f'<meta property="og:url" content="{canonical}">', f'<meta property="og:image" content="{og_img}">',
          '<meta name="twitter:card" content="summary_large_image">', preload,
          '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
          '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">',
          '<style>' + CSS + '</style>']
    s += ['<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + '</script>' for j in jsonld]
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + '\n'.join(x for x in s if x) + '\n</head>\n'

NAV = [('Online Tuition', B + '/online-tuition/', 'tuition'), ('Skills &amp; Courses', B + '/skills-courses/', 'skills'),
       ('Homeschool Pathways', B + '/homeschool-pathways/', 'homeschool'), ('Teach With Us', B + '/teach-at-valeem/', 'teach'),
       ('About Us', B + '/mod/page/view.php?id=2', 'about'), ('Contact', '#contact', 'contact'), ('Log In', B + '/login/index.php', 'login')]
def header(active, cta='Book a Free Demo', cta_href='#demo', home_href=B + '/'):
    links = '\n'.join(f'      <a href="{h}"' + (' aria-current="page"' if k == active else '') + f'>{t}</a>' for t, h, k in NAV)
    return f'''<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{home_href}" aria-label="Valeem home"><img src="images/valeem-logo.png" alt="Valeem" width="132" height="48"></a>
    <nav class="nav" id="nav" aria-label="Main">
{links}
    </nav>
    <a class="btn btn-primary" href="{cta_href}" data-cta="nav">{cta}</a>
    <button class="menu-btn" id="menuBtn" aria-controls="nav" aria-expanded="false" aria-label="Open menu"><svg class="icon"><use href="#i-menu"/></svg></button>
  </div>
</header>
<div class="geo" id="geo" hidden><div class="wrap"><span id="geoText"></span><a id="geoLink" href="#"></a></div></div>
'''

FOOTER = f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="logo" href="{B}/"><img src="images/valeem-logo.png" alt="Valeem" width="121" height="44"></a>
        <p>Live online tuition, skills courses and a structured homeschool pathway. Teaching online since 2019.</p>
      </div>
      <div><h4>Programmes</h4><ul>
        <li><a href="{B}/online-tuition/">Online Tuition</a></li>
        <li><a href="{B}/skills-courses/">Skills &amp; Courses</a></li>
        <li><a href="{B}/homeschool-pathways/">Homeschool Pathways</a></li>
        <li><a href="{B}/online-tuition-saudi-arabia/">Tuition in Saudi Arabia</a></li>
        <li><a href="{B}/online-tuition-uae/">Tuition in the UAE</a></li>
      </ul></div>
      <div><h4>Valeem</h4><ul>
        <li><a href="{B}/mod/page/view.php?id=2">About us</a></li>
        <li><a href="{B}/teach-at-valeem/">Teach with Valeem</a></li>
        <li><a href="{B}/blog/">Blog</a></li>
        <li><a href="{B}/login/index.php">Student log in</a></li>
        <li><a href="{B}/mod/page/view.php?id=3">Terms &amp; Conditions</a></li>
        <li><a href="{B}/mod/page/view.php?id=4">Privacy Policy</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:contact@valeem.com">contact@valeem.com</a></li>
        <li><a href="tel:+923322636574">+92 332 2636574</a></li>
        <li><a data-wa="footer" href="#" target="_blank" rel="noopener">WhatsApp us</a></li>
        <li><a href="https://www.facebook.com/studyatvaleem" rel="noopener">Facebook</a> · <a href="https://www.instagram.com/valeemonline" rel="noopener">Instagram</a> · <a href="https://www.youtube.com/@ValeemOnline" rel="noopener">YouTube</a> · <a href="https://www.linkedin.com/company/valeem-online" rel="noopener">LinkedIn</a></li>
      </ul></div>
    </div>
    <div class="legal"><span>© <span id="yr">2026</span> Valeem. All Rights Reserved by E-Resource Center (Pvt) Ltd.</span></div>
  </div>
</footer>
'''
def sticky(label='Book a Free Demo'):
    return f'''<div class="sticky" id="sticky">
  <a class="btn btn-primary" href="#demo" data-cta="sticky">{label}</a>
  <a class="btn wa" data-wa="sticky" href="#" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp"><svg class="icon"><use href="#i-wa"/></svg></a>
</div>
'''

def page(head_html, body_attrs, active, main, cta='Book a Free Demo', sticky_label='Book a Free Demo'):
    return (head_html + f'<body{body_attrs}>\n\n' + ICONS + '\n\n' + header(active, cta) + '\n<main id="top">\n' + main +
            '\n</main>\n\n' + FOOTER + '\n' + sticky(sticky_label) + '\n' + SCRIPT + '\n</body>\n</html>\n')

# ---------- shared sections ----------
CHECKS = [('i-file', 'Application', 'Teachers apply and share their subjects, levels and teaching background.'),
          ('i-award', 'Proven grades', 'They must prove an A or B grade in the subject they teach, at O Level, IGCSE or A Level.'),
          ('i-chat', 'One-to-one interview', 'Our team checks subject knowledge, academic depth and how clearly and confidently they teach.'),
          ('i-sparkle', 'Onboarding and training', 'Training on managing student and parent expectations, using AI, presentations and running live classes.')]
def vet_section(kicker='How we choose teachers', title='Every Teacher Passes Four Checks.', lede='Fewer teachers make it through, so your child learns from someone who knows the subject and can teach it.', foot=True, sid='teachers'):
    lis = '\n'.join(f'      <li><span class="dot"><svg class="icon"><use href="#{i}"/></svg></span><b>{t}</b><span>{d}</span></li>' for i, t, d in CHECKS)
    f = f'''
    <div class="vet-foot">
      <p>A teacher who isn't the right fit for your child? We arrange another.</p>
      <a href="{B}/teach-at-valeem/">Are you a teacher? Apply to teach</a>
    </div>''' if foot else ''
    return f'''<section id="{sid}" class="vet">
  <div class="wrap">
    <div class="head">
      <p class="kicker">{kicker}</p>
      <h2>{title}</h2>
      <p class="lede">{lede}</p>
    </div>
    <ol class="checks" aria-label="Teacher selection process">
{lis}
    </ol>{f}
  </div>
</section>
'''

FACTORS = [('i-cap', 'Grade or level', 'Grade 5 to A Level'), ('i-repeat', 'Classes per week', 'How often your child learns'),
           ('i-clock', 'Class length', 'Minutes per class'), ('i-lock', 'Fixed time slot', 'A time reserved only for your child'),
           ('i-calendar', 'Number of months', 'Longer plans cost less per month')]
def fees_section(sid='fees', wash=True, kicker='How fees work', title='One Monthly Fee, Built Around Your Child.',
                 lede='Tuition is a monthly plan. Your counsellor shares the fee after the free demo, based on five things.', extra=''):
    lis = '\n'.join(f'      <li><span class="badge"><svg class="icon"><use href="#{i}"/></svg></span><div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in FACTORS)
    return f'''<section id="{sid}"{' class="wash"' if wash else ''}>
  <div class="wrap fees-grid">
    <div class="head" style="margin-bottom:0">
      <p class="kicker">{kicker}</p>
      <h2>{title}</h2>
      <p class="lede">{lede}</p>
      {extra}
      <div class="cta-row" style="margin-top:6px"><a class="btn btn-primary" href="#demo" data-cta="fees">Get Your Fee After a Free Demo</a></div>
    </div>
    <ul class="factors">
{lis}
      <li class="wide"><span class="badge"><svg class="icon"><use href="#i-invoice"/></svg></span><div><b>Invoiced monthly</b><span>Your plan renews each month with an invoice. Many families pay from a Saudi or Pakistani bank account.</span></div></li>
    </ul>
  </div>
</section>
'''

STEPS = [('i-chat', 'Tell us what you need', 'Level, subject or course, and your goals.'),
         ('i-play', 'Free demo at your time', 'A live trial class, scheduled around your timings.'),
         ('i-user', 'We match the teacher', 'A vetted teacher who suits your child and timetable.'),
         ('i-invoice', 'Monthly plan and invoice', 'Once you are happy, we share the plan and first invoice.'),
         ('i-check', 'Classes continue', 'Learning continues month to month, with progress you can follow.')]
def timeline():
    return '<ol class="timeline">\n' + '\n'.join(f'        <li><span class="t-ic"><svg class="icon"><use href="#{i}"/></svg></span><div><b>{t}</b><span>{d}</span></div></li>' for i, t, d in STEPS) + '\n      </ol>'

def form_section(options, kicker='Contact us', title='Book a Free Demo Class.', lede='Tell us what you need. A counsellor will call you to arrange a demo with a suitable teacher.',
                 form_title='Request your free demo', submit='Book a Free Demo Class', teacher=False, wash=False, infinity=True):
    opts = []
    for o in options:
        if isinstance(o, tuple):
            opts.append(f'<optgroup label="{esc(o[0])}">' + ''.join(f'<option>{esc(x)}</option>' for x in o[1]) + '</optgroup>')
        else:
            opts.append(f'<option>{esc(o)}</option>')
    if teacher:
        lab = dict(name='Full name', prog='Level you want to teach', bg='Subjects you want to teach', bgph='e.g. O Level Physics and Chemistry',
                   msg='Your grades and teaching experience', msgph='e.g. A in O Level Physics, 3 years of online tutoring.', legend2='Your teaching', city='City and country',
                   consent='I agree that Valeem may contact me by phone, WhatsApp or email about my application.',
                   thanks_h='Thank you. We have received your application.', thanks_p='Our team reviews every application. If your profile fits, we will contact you to arrange the next step.')
    else:
        lab = dict(name='Parent or student name', prog='Programme', bg='Subject, course or class <small>(optional)</small>', bgph='e.g. O Level Physics, Grade 10',
                   msg='Anything else? <small>(optional)</small>', msgph='Goals, preferred timings, or anything we should know.', legend2='What do you need?', city='City and country',
                   consent='I agree that Valeem may contact me by phone, WhatsApp or email about this enquiry.',
                   thanks_h="Thank you. We've received your request.", thanks_p='A Valeem counsellor will contact you shortly to understand what you need and arrange a free demo.')
    side = '' if teacher else f'''
      <ul class="contact-list">
        <li><a data-wa="contact" href="#" target="_blank" rel="noopener"><span class="badge"><svg class="icon"><use href="#i-wa"/></svg></span>WhatsApp +92 332 2636574</a></li>
        <li><a href="mailto:contact@valeem.com"><span class="badge"><svg class="icon"><use href="#i-mail"/></svg></span>contact@valeem.com</a></li>
        <li><a href="tel:+923322636574"><span class="badge"><svg class="icon"><use href="#i-phone"/></svg></span>Call +92 332 2636574</a></li>
      </ul>'''
    if teacher:
        side = '''
      <ul class="ticks" style="grid-template-columns:1fr;margin-top:24px">
        <li><svg class="icon"><use href="#i-check"/></svg>An A or B grade in the subject you teach</li>
        <li><svg class="icon"><use href="#i-check"/></svg>Confident speaking and explaining</li>
        <li><svg class="icon"><use href="#i-check"/></svg>Ready to teach live online</li>
      </ul>'''
    if infinity:
        fid, h = (INF_TEACHER, 2350) if teacher else (INF_STUDENT, 980)
        kind = 'teacher' if teacher else 'student'
        card = f'''    <div class="form-card embed" id="demo">
      <iframe data-infinity="{kind}" src="https://app.startinfinity.com/form/{fid}" title="{esc(form_title)}" loading="lazy" class="inf inf-{kind}"></iframe>
      <p class="form-alt">Form not loading? <a href="https://app.startinfinity.com/form/{fid}" target="_blank" rel="noopener" data-cta="infinity-open">Open it in a new tab</a> or <a data-wa="form" href="#" target="_blank" rel="noopener">WhatsApp us</a>.</p>
    </div>'''
        return f'''<section id="start"{' class="wash"' if wash else ''}>
  <div class="wrap start-grid" id="contact">
    <div>
      <div class="head" style="margin-bottom:0">
        <p class="kicker">{kicker}</p>
        <h2>{title}</h2>
        <p class="lede">{lede}</p>
      </div>{side}
    </div>
{card}
  </div>
</section>
'''
    return f'''<section id="start"{' class="wash"' if wash else ''}>
  <div class="wrap start-grid" id="contact">
    <div>
      <div class="head" style="margin-bottom:0">
        <p class="kicker">{kicker}</p>
        <h2>{title}</h2>
        <p class="lede">{lede}</p>
      </div>{side}
    </div>
    <div class="form-card" id="demo">
      <form id="leadForm" novalidate>
        <h3>{form_title}</h3>
        <p>It takes about a minute.</p>
        <fieldset>
          <legend>Your details</legend>
          <div class="f"><label for="pname">{lab['name']}</label><input type="text" id="pname" name="parent_name" autocomplete="name" required><span class="err" id="pname-err"></span></div>
          <div class="f"><label for="phone">WhatsApp or contact number</label><input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" placeholder="Include country code" required><span class="err" id="phone-err"></span></div>
          <div class="f"><label for="email">Email address <small>(optional)</small></label><input type="email" id="email" name="email" autocomplete="email"><span class="err" id="email-err"></span></div>
          <div class="f"><label for="city">{lab['city']}</label><input type="text" id="city" name="city_country" placeholder="e.g. Riyadh, Saudi Arabia" required><span class="err" id="city-err"></span></div>
        </fieldset>
        <fieldset>
          <legend>{lab['legend2']}</legend>
          <div class="f"><label for="prog">{lab['prog']}</label>
            <select id="prog" name="interests" required>
              <option value="">Select</option>
              {''.join(opts)}
            </select><span class="err" id="prog-err"></span></div>
          <div class="f"><label for="bg">{lab['bg']}</label><input type="text" id="bg" name="background" placeholder="{lab['bgph']}"></div>
          <div class="f full"><label for="msg">{lab['msg']}</label><textarea id="msg" name="message" placeholder="{lab['msgph']}"></textarea></div>
        </fieldset>
        <label class="consent" for="consent"><input type="checkbox" id="consent" name="consent" required><span>{lab['consent']}</span></label>
        <span class="err" id="consent-err"></span>
        <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="utm_term">
        <input type="hidden" name="landing_page"><input type="hidden" name="referrer">
        <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
        <button class="btn btn-primary" type="submit" id="submitBtn">{submit}</button>
        <div class="form-msg" id="formMsg" role="alert" hidden></div>
        <p class="form-alt">Prefer to talk now? <a data-wa="form" href="#" target="_blank" rel="noopener">Chat with us on WhatsApp</a></p>
      </form>
      <div class="thanks" id="thanks" role="status" tabindex="-1" hidden>
        <span class="tick"><svg class="icon" style="width:32px;height:32px"><use href="#i-check"/></svg></span>
        <h3>{lab['thanks_h']}</h3>
        <p>{lab['thanks_p']}</p>
        <a class="btn btn-ghost" data-wa="thanks" href="#" target="_blank" rel="noopener"><svg class="icon"><use href="#i-wa"/></svg>Message us on WhatsApp</a>
      </div>
    </div>
  </div>
</section>
'''

def faq(groups, title='Questions Parents and Students Ask.', wash=True):
    out = []
    for g, qs in groups:
        if g: out.append(f'      <h3>{esc(g)}</h3>')
        for q, a, *link in qs:
            ah = esc(a)
            if link: ah = ah.replace(esc(link[0][0]), f'<a href="{link[0][1]}">{esc(link[0][0])}</a>')
            out.append(f'      <details><summary>{esc(q)}</summary><div class="a"><p>{ah}</p></div></details>')
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for _, qs in groups for q, a, *_ in qs]}
    sec = f'''<section id="faqs"{' class="wash"' if wash else ''}>
  <div class="wrap">
    <div class="head">
      <p class="kicker">FAQs</p>
      <h2>{title}</h2>
    </div>
    <div class="faq">
{chr(10).join(out)}
    </div>
  </div>
</section>
'''
    return sec, ld


# ---------- testimonials (published on the previous valeem.com homepage) ----------
TESTIMONIALS = [
 ("Valeem has been a blessing for our O Level preparation. We found a tutor who understood our child's needs and progress improved within weeks!", "Parent from Jeddah", "Saudi Arabia · O Level tuition"),
 ("My name is Fatima Shah, I live in Dammam, Saudi Arabia. I am an A Level student and a private candidate studying at Valeem. I was struggling to find teachers, I kept looking for online courses but was hopeless at some point when my friend told me about Valeem. I immediately contacted them and had my demo classes. It's great to see such wonderful, talented, passionate and committed teachers there.", "Fatima Shah", "A Level private candidate, Dammam"),
 ("My sessions with Sir Murtaza Farooq have been very encouraging. He is a great teacher. He is always very well prepared for the class, which helps a lot! Sir Murtaza always keeps a check on his students, whether they're doing their work or not. Overall, he is a good teacher and I would recommend him.", "Shireen Khan", "O Level student"),
 ("Ms. Javeria is a brilliant teacher with a very professional method of teaching. She has full grip on her subjects. Wajih is now settled with her. Initially he had some challenges but now, Alhamdulillah, he has adjusted. Thank you Valeem.", "Mr & Mrs Imran Ansari", "Parents, online tuition"),
]
def testimonials(wash=False, title='What Parents and Students Say.'):
    cards = '\n'.join(f'      <figure class="quote"><svg class="icon q" aria-hidden="true"><use href="#i-chat"/></svg><blockquote>{esc(q)}</blockquote><figcaption><b>{esc(n)}</b><span>{esc(w)}</span></figcaption></figure>' for q, n, w in TESTIMONIALS)
    cls = ' class="wash"' if wash else ''
    return (f'<section id="testimonials"{cls}>\n  <div class="wrap">\n    <div class="head">\n      <p class="kicker">In their words</p>\n      <h2>{title}</h2>\n'
            '      <p class="lede">From families and students who learn with Valeem, many of them in Saudi Arabia.</p>\n    </div>\n'
            f'    <div class="quotes">\n{cards}\n    </div>\n  </div>\n</section>\n')

INF_STUDENT = 'iwRmYUkbwrC'
INF_TEACHER = 'f5ff3893-4c5c-4b7b-82c1-f4bca5817094'
ORG = {"@type": "EducationalOrganization", "@id": B + "/#org", "name": "Valeem", "url": B + "/"}
def crumbs_ld(name, url):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Valeem", "item": B + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": url}]}
def page_hero(crumb, kicker, h1, lede, ctas, pills, img, alt):
    p = ''.join(f'<li><svg class="icon"><use href="#{i}"/></svg>{t}</li>' for i, t in pills)
    return f'''<section class="page-hero">
  <div class="wrap ph-grid">
    <div class="ph-copy">
      <p class="crumbs"><a href="{B}/">Home</a> / {crumb}</p>
      <p class="kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p class="lede">{lede}</p>
      <div class="cta-row">{ctas}</div>
      <ul class="pills">{p}</ul>
    </div>
    <figure class="photo"><img src="images/{img}" alt="{alt}" width="1100" height="935" fetchpriority="high"></figure>
  </div>
</section>
'''
WA_BTN = '<a class="btn btn-ghost" data-wa="hero" href="#" target="_blank" rel="noopener"><svg class="icon"><use href="#i-wa"/></svg>WhatsApp Us</a>'

# =====================================================================
# HOMEPAGE
# =====================================================================
home_src = open(T + 'home_body.html').read()
main = home_src[home_src.index('<main id="top">') + len('<main id="top">'):home_src.index('</main>')]
def rep(a, b, n=1):
    global main
    assert main.count(a) == n, (a[:70], main.count(a)); main = main.replace(a, b)
rep('<a class="btn btn-ghost on-dark" href="#tuition">Explore Online Tuition</a>', f'<a class="btn btn-ghost on-dark" href="{B}/online-tuition/">Explore Online Tuition</a>')
rep('<a class="btn btn-ghost on-dark" href="#skills">See All Courses</a>', f'<a class="btn btn-ghost on-dark" href="{B}/skills-courses/">See All Courses</a>')
rep('<a class="more" href="#tuition">Explore Online Tuition</a>', f'<a class="more" href="{B}/online-tuition/">Explore Online Tuition</a>')
rep('<a class="more" href="#skills">See All Courses</a>', f'<a class="more" href="{B}/skills-courses/">See All Courses</a>')
rep('''      <a class="btn btn-accent" href="#demo" data-cta="tuition" data-prog="Online Tuition: IGCSE, O Level or A Level">Book a Free Demo</a>''',
    f'''      <div class="cta-row"><a class="btn btn-accent" href="#demo" data-cta="tuition" data-prog="Online Tuition: IGCSE, O Level or A Level">Book a Free Demo</a><a class="btn btn-ghost on-dark" href="{B}/online-tuition/">Tuition Details</a></div>''')
rep('<!-- 6. ABOUT -->', vet_section(title='Every Valeem Teacher Passes Four Checks.') + '\n<!-- 6. ABOUT -->')
rep('<figure class="photo"><img src="images/g3.webp" alt="Two students working through a coding exercise together" width="747" height="560" loading="lazy" style="object-position:50% 40%"></figure>',
    '<figure class="photo"><img src="images/skills.webp" alt="Two boys working through a coding exercise on a laptop" width="900" height="945" loading="lazy"></figure>')
rep('''        <a class="btn btn-ghost" data-wa="skills" href="#" target="_blank" rel="noopener"><svg class="icon"><use href="#i-wa"/></svg>WhatsApp Us</a>''',
    f'''        <a class="btn btn-ghost" href="{B}/skills-courses/">See All Courses</a>''')
rep('with our largest community of families in the Middle East.', 'and 70% of our families live in the Middle East, most of them in Saudi Arabia.')
rep('<figure class="photo"><img src="images/g3.webp" alt="Two students working together on a laptop" width="747" height="560" loading="lazy"></figure>',
    '<figure class="photo"><img src="images/g8.webp" alt="A student smiling during an evening class on her laptop" width="420" height="560" loading="lazy"></figure>')
rep('''      <li><b>Tell us what you need</b><span>Level, subject or course, and your goals.</span></li>
      <li><b>Speak to a counsellor</b><span>We match a suitable teacher.</span></li>
      <li><b>Take a free demo</b><span>Meet the teacher before you commit.</span></li>
      <li><b>Start learning</b><span>Agree a timetable and follow progress.</span></li>''',
    '''      <li><b>Tell us what you need</b><span>Level, subject or course, and your goals.</span></li>
      <li><b>Free demo at your time</b><span>A live trial class, scheduled around you.</span></li>
      <li><b>We match the teacher</b><span>A vetted teacher who suits your child.</span></li>
      <li><b>Monthly plan and invoice</b><span>Once you are happy, classes continue month to month.</span></li>''')
rep('<!-- 9. WHY VALEEM -->', fees_section(wash=False, lede='Tuition is a monthly plan. Your counsellor shares the fee after the free demo, based on five things.') + '\n<!-- 9. WHY VALEEM -->')
rep('<section id="why">', '<section id="why" class="wash">')
rep('<h3>Trained subject teachers</h3><p>Selected for their subject and trained to teach live online.</p>', '<h3>Vetted subject teachers</h3><p>Proven A or B grades, interviewed and trained.</p>')
rep('<section id="team" class="wash">', '<section id="team">')
rep('<img src="images/teach-1.webp" alt="A Valeem educator teaching on her laptop" width="700" height="805" loading="lazy">', '<img src="images/teach-1.webp" alt="A Valeem teacher explaining a concept during a live class" width="700" height="805" loading="lazy">')
rep('<img src="images/teach-2.webp" alt="A Valeem educator smiling during an online lesson" width="700" height="805" loading="lazy">', '<img src="images/teach-2.webp" alt="A Valeem teacher preparing a lesson on her laptop" width="700" height="805" loading="lazy">')
rep('<p class="lede">Join 650+ educators teaching students in 14+ countries. We train you on our platform and match you with students who need your subject.</p>',
    '<p class="lede">Join 650+ educators teaching students in 14+ countries. If you hold an A or B grade in your subject and love explaining it, we will train you and match you with students.</p>')
rep(f'<div class="cta-row"><a class="btn btn-ghost" href="https://www.valeem.com/mod/page/view.php?id=21">Become a Teacher</a></div>',
    f'<div class="cta-row"><a class="btn btn-primary" href="{B}/teach-at-valeem/">Apply to Teach</a><a class="btn btn-ghost" href="{B}/teach-at-valeem/#process">See the Selection Process</a></div>')
a_ = main.index('<!-- 11. CONTACT'); b_ = main.index('<!-- 12. FAQS -->')
main = main[:a_] + testimonials() + '\n<!-- 11. CONTACT: Infinity free-trial form -->\n' + form_section([], title='Book a Free Trial Class.', lede='Tell us what you need. A counsellor will call you to arrange a free trial class with a suitable teacher.', form_title='Register for a free trial lesson', wash=True) + '\n' + main[b_:]
home_faq = [
 ("General", [
  ("What is Valeem?", "Valeem is an online education company, teaching live since 2019. It offers Online Tuition for IGCSE, O Level and A Level, Skills & Courses such as coding, IELTS, English and Quran, and Homeschool Pathways for homeschooled children aged 7 to 14. Over 650 vetted educators teach students in more than 14 countries."),
  ("Do you teach students in Saudi Arabia and the Gulf?", "Yes. About 70% of our families live in the Middle East, most of them in Saudi Arabia. Classes are scheduled after school, in your time zone."),
  ("How are Valeem teachers selected?", "Every teacher passes four checks: an application, proof of an A or B grade in the subject they teach, a one-to-one interview, and onboarding and training before they teach."),
 ]),
 ("Online Tuition", [
  ("Which levels does Valeem teach?", "One-to-one live tuition for IGCSE, O Level and A Level students, usually from Grade 8 upwards. We also support younger students from Grade 5 with English, Maths and homework."),
  ("How much does online tuition cost?", "Tuition is a monthly plan. The fee depends on the grade, the number of months, classes per week, class length and whether you want a fixed time slot. A counsellor shares the fee after the free demo."),
  ("How does payment work?", "Once you are happy with the demo and the teacher, we send a monthly invoice and the plan renews each month. Many families pay from a Saudi or Pakistani bank account."),
 ]),
 ("Skills & Homeschool", [
  ("What skills courses do you offer?", "Coding (Scratch for young learners; Python, SQL and Power BI for teens and adults), IELTS preparation, English improvement, language classes (English, Urdu, Arabic, Chinese and German) and Quran classes."),
  ("What is Homeschool Pathways?", "A structured online programme for homeschooled children aged 7 to 14, with three learning stages and guidance towards O Level and A Level. Full details and fees are on the Homeschool Pathways page.", ("Homeschool Pathways page", B + "/homeschool-pathways/")),
 ]),
 ("Getting started", [
  ("Is there a free demo class?", "Yes. Your child takes a free live demo at a time that suits you. If a teacher is not the right fit later, we arrange another."),
  ("How do I get started?", "Fill in the form on this page or message us on WhatsApp at +92 332 2636574. A counsellor will call you, understand what you need and arrange a free demo."),
 ]),
]
fs, home_faq_ld = faq(home_faq)
a = main.index('<!-- 12. FAQS -->'); main = main[:a] + '<!-- 12. FAQS -->\n' + fs
cur = open(R + '/new-home/index.html').read()
lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', cur, re.S)
org = json.loads(lds[0]); site = json.loads(lds[1])
org['description'] = "Valeem offers live online education: one-to-one Online Tuition for IGCSE, O Level and A Level, Skills & Courses including coding, IELTS, English and Quran, and Homeschool Pathways for homeschooled children aged 7 to 14. Most of its families live in Saudi Arabia and the Gulf."
cats = org['hasOfferCatalog']['itemListElement']
cats[0]['url'] = B + '/online-tuition/'; cats[1]['url'] = B + '/skills-courses/'; cats[2]['url'] = B + '/homeschool-pathways/'
h = head('Valeem | Online Tuition for IGCSE, O &amp; A Level, Coding Courses and Homeschool',
         'Live one-to-one online tuition for IGCSE, O Level and A Level with vetted teachers, plus coding, IELTS, English and Quran courses and Homeschool Pathways. Trusted by families in Saudi Arabia and the Gulf. Book a free demo.',
         B + '/', 'Valeem | Live Online Tuition, Skills Courses and Homeschool Pathways',
         'One-to-one tuition for IGCSE, O Level and A Level with vetted teachers, coding and IELTS courses, and a structured homeschool pathway. Book a free demo.',
         B + '/new-home/images/share.jpg', [org, site, home_faq_ld],
         '<link rel="preload" as="image" href="images/slide-tuition.webp" media="(min-width:761px)">\n<link rel="preload" as="image" href="images/slide-tuition-m.webp" media="(max-width:760px)">', noindex=True)
home = page(h, ' data-lead="HOMEPAGE"', '', main)
home = home.replace(f'<a class="brand" href="{B}/"', '<a class="brand" href="#top"')
open(R + '/new-home/index.html', 'w').write(home)

# =====================================================================
# ONLINE TUITION
# =====================================================================
url = B + '/online-tuition/'
def subj_links(exclude=None):
    out = []
    for lvl in ('O Level', 'IGCSE', 'A Level'):
        items = ''.join(f'<li><a href="{B}/online-tuition/{sl}/">{lv} {nm} <small>{cd}</small></a></li>' for sl, lv, nm, cd, *_ in SUBJECTS if lv == lvl and sl != exclude)
        if items: out.append(f'      <h3 class="subj-h">{lvl}</h3>\n      <ul class="subj">{items}</ul>')
    return '\n'.join(out)
SUBJ_SECTION = f'''<section id="subjects">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Popular subjects</p>
      <h2>Find Your Subject and Syllabus Code.</h2>
      <p class="lede">These are the subjects families ask for most. We teach every IGCSE, O Level and A Level subject, so ask us if yours isn't listed.</p>
    </div>
{subj_links()}
  </div>
</section>

'''
tq = [
 ("", [
  ("Which levels does Valeem teach?", "IGCSE, O Level and A Level (AS and A2), usually from Grade 8 upwards. We also teach younger students from Grade 5 in English and Maths, and help with homework."),
  ("Which subjects can my child study?", "All subjects offered for IGCSE, O Level and A Level in schools in Pakistan and Saudi Arabia. We match a teacher who holds an A or B grade in that subject and has passed our interview and training."),
  ("Are classes one-to-one?", "Yes. Every Online Tuition class is live and one-to-one, so the teacher follows your child's syllabus, pace and goals."),
  ("How much does online tuition cost?", "Tuition is a monthly plan. The fee depends on the grade, the number of months, classes per week, class length and whether you want a fixed time slot. A counsellor shares the fee after the free demo."),
  ("How do we pay?", "We send a monthly invoice and the plan renews each month. Many families pay from a Saudi or Pakistani bank account."),
  ("What time are classes for families in Saudi Arabia?", "Classes are scheduled after school in Saudi time (AST, UTC+3), at times that suit your child.", ("Saudi time", B + "/online-tuition-saudi-arabia/")),
  ("Can my child try a class first?", "Yes. The first class is a free live demo at your time. If the teacher isn't the right fit later, we arrange another."),
  ("How are teachers selected?", "Every teacher passes four checks: an application, proof of an A or B grade in the subject they teach, a one-to-one interview, and onboarding and training."),
 ])]
fs, ld = faq(tq, title='Online Tuition: Your Questions Answered.')
service = {"@context": "https://schema.org", "@type": "Service", "name": "Online Tuition for IGCSE, O Level and A Level", "serviceType": "Online tutoring",
  "description": "Live one-to-one online tuition for IGCSE, O Level and A Level, plus English, Maths and homework support from Grade 5. Vetted teachers, free demo, monthly plans.",
  "url": url, "provider": ORG, "areaServed": [{"@type": "Country", "name": n} for n in ["Saudi Arabia", "United Arab Emirates", "Qatar", "Kuwait", "Bahrain", "Oman", "Pakistan"]],
  "audience": {"@type": "EducationalAudience", "educationalRole": "student"}}
main = page_hero('Online Tuition', 'Online Tuition · IGCSE · O Level · A Level', 'Live One-to-One Tuition for IGCSE, O Level and <em>A Level.</em>',
  'A vetted subject teacher, classes at your time, and a plan for your child, from Grade 5 to A Level.',
  '<a class="btn btn-primary" href="#demo" data-cta="hero" data-prog="Online Tuition: IGCSE, O Level or A Level">Book a Free Demo</a>' + WA_BTN,
  [('i-user', 'One-to-one'), ('i-play', 'Free demo'), ('i-globe', 'Gulf time zones')], 'hero.webp', 'A student giving a thumbs up beside her laptop during an online class') + f'''
<section class="numbers" aria-label="Online Tuition in numbers" style="margin-top:0;padding-top:0">
  <div class="wrap">
    <ul>
      <li><span class="badge"><svg class="icon"><use href="#i-live"/></svg></span><div><b>1:1</b><span>live classes</span></div></li>
      <li><span class="badge"><svg class="icon"><use href="#i-users"/></svg></span><div><b>650+</b><span>vetted educators</span></div></li>
      <li><span class="badge"><svg class="icon"><use href="#i-globe"/></svg></span><div><b>70%</b><span>families in the Gulf</span></div></li>
      <li><span class="badge"><svg class="icon"><use href="#i-calendar"/></svg></span><div><b>Since 2019</b><span>teaching online</span></div></li>
    </ul>
  </div>
</section>

<section id="levels">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Levels we teach</p>
      <h2>A Teacher for Every Step, From Grade 5 to A Level.</h2>
      <p class="lede">Every subject taught for IGCSE, O Level and A Level in schools in Pakistan and Saudi Arabia.</p>
    </div>
    <ol class="ladder light" aria-label="Online tuition levels">
      <li><span class="ic"><svg class="icon"><use href="#i-book"/></svg></span><i>Grades 5–7</i><b>Strong Basics</b><span>English, Maths and homework support.</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-compass"/></svg></span><i>Grade 8</i><b>Getting Ready</b><span>Foundations for IGCSE and O Level subjects.</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-cap"/></svg></span><i>Grades 9–11</i><b>IGCSE &amp; O Level</b><span>Full syllabus, past papers and exam technique.</span><span class="core">Most popular</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-route"/></svg></span><i>AS &amp; A2</i><b>A Level</b><span>Subject specialists for the step up.</span></li>
    </ol>
  </div>
</section>

{SUBJ_SECTION}<section id="classes" class="wash">
  <div class="wrap feat">
    <figure class="photo"><img src="images/levels.webp" alt="A student smiling at his laptop during a live lesson" width="900" height="945" loading="lazy"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">Inside every class</p>
        <h2>One Teacher, One Student, One Plan.</h2>
      </div>
      <ul class="feature-list">
        <li><span class="badge"><svg class="icon"><use href="#i-live"/></svg></span><div><h3>Live and one-to-one</h3><p>Your child's own teacher, full attention, real questions.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-book"/></svg></span><div><h3>Follows your syllabus</h3><p>Built around your child's board, school topics and gaps.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-clip"/></svg></span><div><h3>Past papers and exam technique</h3><p>Practice that prepares your child for the real exam.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-chart"/></svg></span><div><h3>Progress you can follow</h3><p>Classes and resources on our learning platform.</p></div></li>
      </ul>
    </div>
  </div>
</section>

''' + vet_section(title='Every Tuition Teacher Passes Four Checks.') + f'''
<section id="gulf" class="gulf">
  <div class="wrap feat rev">
    <figure class="photo"><img src="images/evening.webp" alt="A student smiling during an evening online class" width="1000" height="800" loading="lazy"></figure>
    <div class="head" style="margin-bottom:0">
      <p class="kicker">For families in Saudi Arabia and the Gulf</p>
      <h2>Tuition That Fits Your Family's Day.</h2>
      <div class="stat-big"><b>70%</b><span>of our families live in the Middle East, most of them in Saudi Arabia.</span></div>
      <ul class="ticks" style="grid-template-columns:1fr;margin-top:8px">
        <li><svg class="icon"><use href="#i-check"/></svg>Classes after school, in your time zone</li>
        <li><svg class="icon"><use href="#i-check"/></svg>Teachers who know IGCSE, O Level and A Level boards</li>
        <li><svg class="icon"><use href="#i-check"/></svg>Pay from a Saudi or Pakistani bank account</li>
      </ul>
      <ul class="places">
        <li><a href="{B}/online-tuition-saudi-arabia/">Saudi Arabia</a></li><li><a href="{B}/online-tuition-uae/">UAE</a></li><li>Qatar</li><li>Kuwait</li><li>Bahrain</li><li>Oman</li><li>Pakistan</li>
      </ul>
    </div>
  </div>
</section>

''' + fees_section() + f'''
<section id="process">
  <div class="wrap feat">
    <figure class="photo"><img src="images/counsellor.webp" alt="A Valeem counsellor holding a laptop" width="800" height="880" loading="lazy" style="object-position:50% 25%"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">How to start</p>
        <h2>From Free Demo to Monthly Plan.</h2>
      </div>
      {timeline()}
    </div>
  </div>
</section>

''' + testimonials() + form_section([('Online Tuition', ['Online Tuition: IGCSE, O Level or A Level', 'Online Tuition: Grades 5–8']), 'Not sure yet'], wash=True) + fs
h = head('Online Tuition for IGCSE, O Level and A Level | Valeem',
  'Live one-to-one online tuition for IGCSE, O Level and A Level with vetted teachers who hold A or B grades. Classes in Saudi and Gulf time zones, free demo, monthly plans.',
  url, 'Online Tuition for IGCSE, O Level and A Level | Valeem', 'Vetted one-to-one teachers, classes in your time zone, a free demo and monthly plans.',
  url + 'images/hero.webp', [service, ld, crumbs_ld('Online Tuition', url)])
open(R + '/online-tuition/index.html', 'w').write(page(h, ' data-lead="TUITION PAGE"', 'tuition', main))

# =====================================================================
# SKILLS & COURSES
# =====================================================================
url = B + '/skills-courses/'
sq = [("", [
  ("What coding courses does Valeem offer?", "Scratch for young learners, and Python, SQL and Power BI for teenagers and adults. Classes are live with a Valeem teacher."),
  ("What age can my child start coding?", "Young learners start with Scratch, a visual way to learn coding. Tell us your child's age and we will suggest the right starting point."),
  ("Do you offer IELTS preparation?", "Yes. IELTS preparation is taught live for teenagers and adults, alongside English improvement classes."),
  ("Which languages do you teach?", "English, Urdu, Arabic, Chinese and German, for children and adults, from beginner level upwards."),
  ("Do you offer Quran classes?", "Yes. Live online Quran classes are available for children and adults."),
  ("How are courses priced?", "Courses are billed monthly. The fee depends on the course, classes per week and class length, and is shared after a free demo."),
])]
fs, ld = faq(sq, title='Skills &amp; Courses: Your Questions Answered.')
offer = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Valeem Skills & Courses", "url": url, "itemListElement": [
  {"@type": "Course", "name": n, "description": d, "provider": ORG, "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online"}} for n, d in [
   ("Scratch coding for young learners", "Live online Scratch coding classes for children."),
   ("Python", "Live online Python programming classes for teenagers and adults."),
   ("SQL", "Live online SQL classes for teenagers and adults."),
   ("Power BI", "Live online Power BI data visualisation classes for adults."),
   ("IELTS preparation", "Live online IELTS preparation."),
   ("English improvement", "Live online classes to improve spoken and written English."),
   ("Quran classes", "Live online Quran classes for children and adults.")]]}
def ccard(img, alt, who, h3, p, chips, prog, tone='var(--orange)'):
    ch = ''.join(f'<li>{c}</li>' for c in chips)
    return f'''      <article class="course" style="--tone:{tone}">
        <figure class="photo"><img src="images/{img}" alt="{alt}" width="800" height="880" loading="lazy"></figure>
        <div class="course-body">
          <p class="who">{who}</p>
          <h3>{h3}</h3>
          <p>{p}</p>
          <ul class="chips">{ch}</ul>
          <a class="more" href="#demo" data-cta="course" data-prog="{prog}" style="margin-top:auto">Ask about this course</a>
        </div>
      </article>'''
main = page_hero('Skills &amp; Courses', 'Skills &amp; Courses · Children and adults', 'Coding, IELTS, English and Quran, <em>Taught Live.</em>',
  'Practical courses with vetted Valeem teachers, for young learners, teens and working adults.',
  '<a class="btn btn-primary" href="#demo" data-cta="hero" data-prog="Skills &amp; Courses: Coding">Ask About a Course</a>' + WA_BTN,
  [('i-code', 'Coding'), ('i-chat', 'IELTS and English'), ('i-book', 'Quran')], 'hero.webp', 'Two boys working through a coding exercise on a laptop') + f'''
<section id="courses">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Our courses</p>
      <h2>Four Ways to Build a Skill.</h2>
      <p class="lede">Every course is live, with a teacher who checks understanding as you go.</p>
    </div>
    <div class="courses">
{ccard('kids.webp', 'A young learner in headphones giving a thumbs up at his laptop', 'Young learners', 'Coding for Kids', 'Children learn to think like coders with Scratch, building games and stories step by step.', ['Scratch', 'Logic', 'Problem solving'], 'Skills &amp; Courses: Coding')}
{ccard('adults.webp', 'An adult learner working through a data exercise on his laptop', 'Teens and adults', 'Coding and Data', 'Job-ready skills for students and working adults, from first lines of code to dashboards.', ['Python', 'SQL', 'Power BI'], 'Skills &amp; Courses: Coding', 'var(--plum)')}
{ccard('english.webp', 'A student smiling while practising English on her laptop', 'Teens and adults', 'Languages and IELTS', 'Prepare for IELTS, speak and write with confidence, or learn a new language.', ['IELTS', 'English', 'Urdu', 'Arabic', 'Chinese', 'German'], 'Skills &amp; Courses: IELTS, English or languages', '#a784c7')}
      <article class="course solid">
        <div class="course-body">
          <span class="big-ic"><svg class="icon" style="width:28px;height:28px"><use href="#i-book"/></svg></span>
          <p class="who">Children and adults</p>
          <h3>Quran Classes</h3>
          <p>Live one-to-one Quran classes with a patient teacher, at times that suit your family.</p>
          <ul class="chips"><li>Quran classes</li><li>Flexible timings</li></ul>
          <a class="btn btn-accent" href="#demo" data-cta="course" data-prog="Skills &amp; Courses: Quran" style="margin-top:auto;align-self:flex-start">Ask About Quran Classes</a>
        </div>
      </article>
    </div>
  </div>
</section>

<section id="who" class="wash">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Who it's for</p>
      <h2>Courses for Every Stage of Life.</h2>
    </div>
    <div class="audience">
      <div><h3>Children</h3><p>Scratch coding, English and Quran, taught patiently and live.</p></div>
      <div><h3>Teenagers</h3><p>Python, IELTS and English to get ahead of school and university.</p></div>
      <div><h3>Working adults</h3><p>SQL, Power BI, Python and IELTS for your career or a move abroad.</p></div>
    </div>
  </div>
</section>

''' + vet_section(title='Every Course Teacher Passes Four Checks.', lede='The same selection process as our tuition teachers: proven grades, an interview and training before the first class.') + f'''
<section id="process">
  <div class="wrap feat">
    <figure class="photo"><img src="images/adults.webp" alt="An adult learner typing on a laptop" width="800" height="880" loading="lazy"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">How to start</p>
        <h2>From Free Demo to Your First Course.</h2>
      </div>
      {timeline()}
    </div>
  </div>
</section>

''' + form_section([('Skills &amp; Courses', ['Skills & Courses: Coding', 'Skills & Courses: IELTS, English or languages', 'Skills & Courses: Quran']), 'Not sure yet'],
                   title='Ask About a Course.', lede='Tell us the course and your level. A counsellor will call you to arrange a free demo.', form_title='Ask about a course', submit='Ask About a Course', wash=True).replace('Skills &amp;amp; Courses', 'Skills &amp; Courses') + fs
h = head('Coding, IELTS, English and Quran Classes Online | Valeem Skills &amp; Courses',
  'Live online courses with vetted teachers: Scratch coding for kids, Python, SQL and Power BI for teens and adults, IELTS, English, language and Quran classes. Free demo.',
  url, 'Valeem Skills & Courses: Coding, IELTS, English and Quran', 'Live courses for children, teens and adults with vetted Valeem teachers. Free demo.',
  url + 'images/hero.webp', [offer, ld, crumbs_ld('Skills & Courses', url)])
open(R + '/skills-courses/index.html', 'w').write(page(h, ' data-lead="SKILLS PAGE" data-wa-text="Hello, I\'m interested in a Valeem course. I would like to book a free demo."', 'skills', main, cta='Ask About a Course', sticky_label='Ask About a Course'))

# =====================================================================
# TEACH WITH VALEEM
# =====================================================================
url = B + '/teach-at-valeem/'
eq = [("", [
  ("What do I need to teach with Valeem?", "An A or B grade in the subject you want to teach, at O Level, IGCSE or A Level, confident spoken English, and the ability to teach live online."),
  ("What is the selection process?", "Four steps: you apply, you share proof of your subject grades, you have a one-to-one interview with our team, and you complete onboarding and training before your first class."),
  ("What does the training cover?", "Managing student and parent expectations, using AI in your teaching, building presentations and running live classes on our platform."),
  ("Can I teach from anywhere?", "Yes. All classes are live online. Our students are in 14+ countries, most of them in Saudi Arabia and the Gulf."),
  ("What can I teach?", "IGCSE, O Level and A Level subjects, younger students from Grade 5, skills courses such as coding and IELTS, and Homeschool Pathways."),
])]
fs, ld = faq(eq, title='Teaching With Valeem: Your Questions Answered.')
job = {"@context": "https://schema.org", "@type": "WebPage", "name": "Teach with Valeem", "url": url, "about": ORG,
  "description": "Apply to teach IGCSE, O Level, A Level and skills courses live online with Valeem. Four-step selection: application, proven grades, interview, training."}
main = page_hero('Teach With Valeem', 'Teach with Valeem', 'Teach Students Across 14+ Countries, <em>From Home.</em>',
  'Join 650+ educators teaching IGCSE, O Level, A Level and skills courses live online.',
  '<a class="btn btn-primary" href="#demo" data-cta="hero">Apply to Teach</a><a class="btn btn-ghost" href="#process">See the Selection Process</a>',
  [('i-globe', 'Teach online'), ('i-users', '650+ educators'), ('i-sparkle', 'Training included')], 'hero.webp', 'A Valeem teacher explaining a concept during a live class') + f'''
<section id="why-teach">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Why teach with us</p>
      <h2>Do What You Do Best. We Handle the Rest.</h2>
    </div>
    <div class="cards">
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-globe"/></svg></span><h3>Teach from anywhere</h3><p>Live online classes with students in 14+ countries.</p></article>
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-users"/></svg></span><h3>Students matched to you</h3><p>We match you with students who need your subject.</p></article>
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-repeat"/></svg></span><h3>Long-term students</h3><p>Families learn on monthly plans that continue month to month.</p></article>
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-sparkle"/></svg></span><h3>Training that grows you</h3><p>AI tools, presentations and live-class skills.</p></article>
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-chat"/></svg></span><h3>A team behind you</h3><p>Counsellors handle scheduling, parents and invoicing.</p></article>
      <article class="card"><span class="badge"><svg class="icon"><use href="#i-cap"/></svg></span><h3>Many levels</h3><p>Grade 5 to A Level, skills courses and Homeschool Pathways.</p></article>
    </div>
  </div>
</section>

''' + vet_section(kicker='The selection process', title='Four Steps to Your First Class.', lede='Our process is strict, so families trust every Valeem teacher. Here is what to expect.', foot=False, sid='process') + f'''
<section id="training" class="wash">
  <div class="wrap feat">
    <figure class="photo"><img src="images/training.webp" alt="A Valeem trainer holding a laptop" width="800" height="880" loading="lazy" style="object-position:50% 25%"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">Onboarding and training</p>
        <h2>Ready for Your First Class, and Every One After.</h2>
      </div>
      <ul class="feature-list">
        <li><span class="badge"><svg class="icon"><use href="#i-users"/></svg></span><div><h3>Students and parents</h3><p>Set clear goals and manage expectations from the start.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-sparkle"/></svg></span><div><h3>AI in your teaching</h3><p>Use AI tools to plan, explain and practise.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-grid"/></svg></span><div><h3>Presentations</h3><p>Clear visual lessons that keep students engaged.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-live"/></svg></span><div><h3>Live classes</h3><p>Run smooth one-to-one classes on our platform.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section id="team-photos">
  <div class="wrap team">
    <div class="head" style="margin-bottom:0">
      <p class="kicker">Our educators</p>
      <h2>Join 650+ Valeem Educators.</h2>
      <p class="lede">Subject specialists, coders, English and Quran teachers, teaching families across the Gulf, Pakistan and beyond.</p>
      <div class="cta-row"><a class="btn btn-primary" href="#demo" data-cta="team">Apply to Teach</a></div>
    </div>
    <div class="team-photos">
      <figure class="photo"><img src="images/teacher-2.webp" alt="A Valeem teacher preparing a lesson on her laptop" width="800" height="880" loading="lazy"></figure>
      <figure class="photo"><img src="images/teacher-3.webp" alt="A Valeem teacher smiling at his laptop" width="800" height="880" loading="lazy"></figure>
    </div>
  </div>
</section>

''' + form_section(['O Level or IGCSE', 'A Level', 'Grades 5–8', 'Skills courses (coding, IELTS, English, languages, Quran)', 'Homeschool Pathways'],
                   kicker='Apply to teach', title='Start Your Application.', lede='Fill in the Valeem Instructor Registration Form. If your profile fits, our team will contact you for the next step.',
                   form_title='Teacher application', submit='Send My Application', teacher=True, wash=True) + fs
h = head('Teach With Valeem | Online Teaching Jobs for IGCSE, O Level and A Level Teachers',
  'Apply to teach IGCSE, O Level, A Level, coding, IELTS and Quran live online with Valeem. Four-step selection: application, proven A or B grades, interview and training.',
  url, 'Teach With Valeem', 'Join 650+ educators teaching students in 14+ countries. Apply in a minute.',
  url + 'images/hero.webp', [job, ld, crumbs_ld('Teach With Valeem', url)])
open(R + '/teach-at-valeem/index.html', 'w').write(page(h, ' data-lead="TEACHER APPLICATION" data-wa-text="Hello, I would like to apply to teach with Valeem."', 'teach', main, cta='Apply to Teach', sticky_label='Apply to Teach'))
print('built 4 pages')
