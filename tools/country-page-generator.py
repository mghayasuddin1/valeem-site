import json, re, os, shutil, html as H
from PIL import Image, ImageOps
REPO='/home/claude/valeem-site'; U='/mnt/user-data/uploads/'
base=open(f'{REPO}/new-home/index.html').read()
HOME='https://www.valeem.com/'

C=[dict(
 slug='online-tuition-saudi-arabia', code='KSA', country='Saudi Arabia', demonym='Saudi Arabia',
 photo='9672c45d', box=(0.0,0.0,0.72,1.0),
 alt='A student giving a thumbs up during an online class at home',
 title='Online O Level, IGCSE and A Level Tuition in Saudi Arabia | Valeem',
 desc='One-to-one live online tuition for O Level, IGCSE and A Level students in Riyadh, Jeddah, Dammam and across Saudi Arabia. Classes in Saudi time. Book a free demo class.',
 h1='Online O Level, IGCSE and A Level Tuition for Families in <em>Saudi Arabia.</em>',
 lede='Valeem gives students across Saudi Arabia one-to-one live classes with trained subject teachers, scheduled in Saudi time around your child\'s school week. Many of our families live in the Kingdom, so we know the questions parents here ask.',
 cities=['Riyadh','Jeddah','Dammam','Al Khobar','Makkah','Madinah','Taif','Jubail'],
 tz='Arabia Standard Time (UTC+3)', tzshort='Saudi time',
 week='The Saudi school week runs Sunday to Thursday, with Friday and Saturday as the weekend. We agree class times with you around that week.',
 currency='SAR', wa="Hello, I'm in Saudi Arabia and interested in Valeem's online tuition. I would like to book a free demo class.",
 place='e.g. Riyadh, Saudi Arabia'),
 dict(
 slug='online-tuition-uae', code='UAE', country='the UAE', demonym='the UAE',
 photo='f54cd543', box=(0.0,0.0,0.85,1.0),
 alt='A student smiling while following an online lesson on her laptop',
 title='Online O Level, IGCSE and A Level Tuition in the UAE | Valeem',
 desc='One-to-one live online tuition for O Level, IGCSE and A Level students in Dubai, Abu Dhabi, Sharjah and across the UAE. Classes in UAE time. Book a free demo class.',
 h1='Online O Level, IGCSE and A Level Tuition for Families in <em>the UAE.</em>',
 lede='Valeem gives students across the UAE one-to-one live classes with trained subject teachers, scheduled in UAE time around your child\'s school week. No commute and no tuition-centre timetable: your child learns from home with a teacher matched to their subject.',
 cities=['Dubai','Abu Dhabi','Sharjah','Ajman','Al Ain','Ras Al Khaimah','Fujairah','Umm Al Quwain'],
 tz='Gulf Standard Time (UTC+4)', tzshort='UAE time',
 week='UAE schools run Monday to Friday, with a shorter Friday and the weekend on Saturday and Sunday. We agree class times with you around that week.',
 currency='AED', wa="Hello, I'm in the UAE and interested in Valeem's online tuition. I would like to book a free demo class.",
 place='e.g. Dubai, UAE')]

for c in C:
    out=f"{REPO}/{c['slug']}"; os.makedirs(out+'/images',exist_ok=True)
    for f in ['valeem-logo.png','o-level.webp','a-level.webp','homeschool.webp']:
        shutil.copy(f'{REPO}/new-home/images/{f}', f'{out}/images/{f}')
    im=ImageOps.exif_transpose(Image.open(U+c['photo']+'-image.jpg')).convert('RGB'); W,Hh=im.size
    b=c['box']; im=im.crop((int(b[0]*W),int(b[1]*Hh),int(b[2]*W),int(b[3]*Hh)))
    im=im.resize((1100,round(im.height*1100/im.width)),Image.LANCZOS); im.save(f'{out}/images/hero.webp','WEBP',quality=78,method=6)
    hw,hh=im.size
    # share image
    sh=im.copy(); tr=1200/630; Wi,Hi=sh.size
    if Wi/Hi>tr: nw=int(Hi*tr); x=(Wi-nw)//2; sh=sh.crop((x,0,x+nw,Hi))
    else: nh=int(Wi/tr); y=int((Hi-nh)*0.3); sh=sh.crop((0,y,Wi,y+nh))
    sh=sh.resize((1200,630),Image.LANCZOS)
    logo=Image.open(f'{REPO}/new-home/images/valeem-logo.png').convert('RGBA'); badge=Image.new('RGBA',(300,120),(255,255,255,240)); l=logo.copy(); l.thumbnail((260,90)); badge.paste(l,((300-l.width)//2,(120-l.height)//2),l); sh.paste(badge,(40,40),badge); sh.save(f'{out}/images/share.jpg','JPEG',quality=82,optimize=True)

    s=base
    url=f"{HOME}{c['slug']}/"
    s=re.sub(r'<title>.*?</title>',f"<title>{c['title']}</title>",s)
    s=re.sub(r'<meta name="description" content="[^"]*">',f'<meta name="description" content="{c["desc"]}">',s)
    s=s.replace('<link rel="canonical" href="https://www.valeem.com/">',f'<link rel="canonical" href="{url}">')
    s=re.sub(r'\n<meta name="robots"[^\n]*','',s)
    s=s.replace('<meta property="og:url" content="https://www.valeem.com/">',f'<meta property="og:url" content="{url}">')
    s=re.sub(r'<meta property="og:title" content="[^"]*">',f'<meta property="og:title" content="{H.escape(c["title"])}">',s)
    s=re.sub(r'<meta property="og:description" content="[^"]*">',f'<meta property="og:description" content="{c["desc"]}">',s)
    s=s.replace('https://www.valeem.com/new-home/images/share.jpg',f'{url}images/share.jpg')
    s=re.sub(r'<script type="application/ld\+json">.*?</script>\n','',s,flags=re.S)

    faq=[
     (f"Do you offer online tuition for students in {c['country']}?", f"Yes. Valeem teaches students across {c['country']}, including {', '.join(c['cities'][:4])}, with live one-to-one online classes. All you need is a laptop or tablet and a stable internet connection."),
     ("Which levels and subjects do you teach?", "Valeem teaches Cambridge O Level, IGCSE and A Level subjects one-to-one. Tell us your child's subject, syllabus and exam session, and we will match a teacher who teaches that syllabus."),
     ("What time are the classes?", f"Classes are scheduled in {c['tzshort']}, {c['tz']}, at times agreed with you around your child's school timetable. {c['week']}"),
     ("Can my child try a class first?", "Yes. Every new student can take a free demo class with a matched teacher before you decide to enrol. If the teacher is not the right fit, we arrange another."),
     ("How much does it cost?", f"Fees depend on the level, the subject and how many classes a week your child takes. Your counsellor will share the current fees in {c['currency']} before the demo class, with no obligation to enrol."),
     ("Do you help homeschooled students?", "Yes. Valeem Homeschool Pathways is a structured online programme for homeschooled children aged 7 to 14, with guidance towards O Levels and A Levels. See the Homeschool Pathways page for details."),
    ]
    service={"@context":"https://schema.org","@type":"Service","name":f"Online O Level, IGCSE and A Level tuition in {c['country'].replace('the ','')}",
      "serviceType":"Online tutoring","url":url,
      "description":f"One-to-one live online tuition for Cambridge O Level, IGCSE and A Level students in {c['country']}, scheduled in {c['tzshort']}.",
      "provider":{"@type":"EducationalOrganization","name":"Valeem","url":HOME,"@id":HOME+"#org"},
      "areaServed":{"@type":"Country","name":c['country'].replace('the ','').replace('UAE','United Arab Emirates')}}
    faqld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}
    ld=''.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>\n' for o in (service,faqld))
    s=s.replace('</head>',ld+'</head>',1)

    # nav: anchors on this page + home
    s=s.replace('<a class="brand" href="#top" aria-label="Valeem home">','<a class="brand" href="https://www.valeem.com/" aria-label="Valeem home">')
    s=s.replace('<a href="#about">About</a>','<a href="#schedule">Timings</a>\n      <a href="#faqs">FAQs</a>')
    s=s.replace('<a class="logo" href="#top">','<a class="logo" href="https://www.valeem.com/">')

    # hero
    a=s.index('<section class="hero">'); b=s.index('<section id="programmes">')
    hero=s[a:b]
    hero=re.sub(r'<p class="kicker">.*?</p>',f'<p class="kicker">Live online tuition · {c["country"].replace("the ","")}</p>',hero,count=1)
    hero=re.sub(r'<h1>.*?</h1>',f'<h1>{c["h1"]}</h1>',hero,flags=re.S)
    hero=re.sub(r'<p class="lede">.*?</p>',f'<p class="lede">{c["lede"]}</p>',hero,count=1,flags=re.S)
    hero=re.sub(r'<li><b>14\+ countries</b>[^<]*</li>',f'<li><b>{c["tzshort"].split()[0]} time</b>classes in {c["tz"].split(" (")[0]}</li>',hero)
    hero=re.sub(r'<img src="images/hero.webp"[^>]*>',f'<img src="images/hero.webp" alt="{c["alt"]}" width="{hw}" height="{hh}" fetchpriority="high">',hero)
    s=s[:a]+hero+s[b:]

    # programmes: homeschool link absolute already; fine. Replace about section with cities + schedule
    a=s.index('<section id="about" class="wash">'); b=s.index('<section id="how">')
    chips=''.join(f'<li>{x}</li>' for x in c['cities'])
    sched=f'''<section id="schedule" class="wash">
  <div class="wrap split" style="align-items:start">
    <div class="head" style="margin-bottom:0">
      <p class="kicker">Timings and scheduling</p>
      <h2>Classes in {c["tzshort"].title() if False else c["tzshort"]}, Around Your Child's School Week.</h2>
      <p class="lede">Every class is booked in {c["tz"]}, so you never have to convert times. {c["week"]}</p>
      <p class="lede">Your counsellor agrees a regular timetable with you before classes begin, and you can raise changes with them as the term goes on.</p>
    </div>
    <div>
      <h3 style="margin-bottom:12px">Students across {c["country"]}</h3>
      <ul class="chips" style="margin-bottom:24px">{chips}<li>and everywhere else in {c["country"]}</li></ul>
      <div class="card">
        <h3>Fees</h3>
        <!-- PRICE GUIDANCE PLACEHOLDER: when Valeem confirms prices, replace this paragraph with
             "One-to-one classes from {c["currency"]} ___ per hour" and add "offers" to the Service JSON-LD in <head>. -->
        <p>Fees depend on the level, the subject and how many classes a week your child takes. Your counsellor shares the current fees in {c["currency"]} before the free demo class, and there is no obligation to enrol.</p>
      </div>
    </div>
  </div>
</section>

'''
    s=s[:a]+sched+s[b:]

    # remove gulf band and team section; add FAQ before #start
    a=s.index('<section id="gulf" class="pathway">'); b=s.index('<section id="start" class="wash">')
    det=''.join(f'<details><summary>{H.escape(q)}</summary><div class="a"><p>{H.escape(ans)}</p></div></details>\n' for q,ans in faq)
    det=det.replace('See the Homeschool Pathways page for details.','See the <a href="https://www.valeem.com/homeschool-pathways/">Homeschool Pathways</a> page for details.')
    faqsec=f'''<section id="faqs">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Questions from parents in {c["country"]}</p>
      <h2>Frequently Asked Questions.</h2>
    </div>
    <div class="faq">
{det}    </div>
  </div>
</section>

'''
    s=s[:a]+faqsec+s[b:]
    s=s.replace('placeholder="e.g. Riyadh, Saudi Arabia"',f'placeholder="{c["place"]}"')
    s=s.replace("var WA_TEXT = \"Hello, I'm interested in Valeem's online tuition. I would like to book a free demo class.\";","var WA_TEXT = "+json.dumps(c['wa'])+";")
    s=s.replace("body.set('interests', 'HOMEPAGE: ' + form.elements.interests.value);",f"body.set('interests', '{c['code']} PAGE: ' + form.elements.interests.value);")
    s=s.replace("sessionStorage.getItem('vhome_attr')","sessionStorage.getItem('vctry_attr')").replace("sessionStorage.setItem('vhome_attr'","sessionStorage.setItem('vctry_attr'")
    assert f"{c['code']} PAGE:" in s and c['wa'][:20] in s
    open(f'{out}/index.html','w').write(s)
    print(c['slug'], len(s))
