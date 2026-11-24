"""Build subject pages, the Saudi Arabia and UAE pages and the private-candidate guide, reusing the shared parts of build_site.py."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'build_site.py')).read()
cut = src.index('# =====================================================================\n# HOMEPAGE')
lib_end = src.index("tq = [", src.index("url = B + '/online-tuition/'"))
# shared parts, plus subj_links() from the Online Tuition block
exec(src[:cut] + src[src.index("url = B + '/online-tuition/'"):lib_end])
R = sys.argv[1]

def absimg(html_, folder):
    return html_.replace('src="images/', f'src="/{folder}/images/')

def write(path, html_):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w').write(html_)

GULF_PILLS = [('i-user', 'One-to-one'), ('i-play', 'Free demo'), ('i-globe', 'Gulf time zones')]
TICK = '<svg class="icon"><use href="#i-check"/></svg>'

# =====================================================================
# SUBJECT PAGES  /online-tuition/<slug>/
# =====================================================================
for slug, lvl, name, code, focus, topics, hard in SUBJECTS:
    full = f'{lvl} {name}'
    url = f'{B}/online-tuition/{slug}/'
    lvl_full = {'O Level': 'Cambridge O Level', 'IGCSE': 'Cambridge IGCSE', 'A Level': 'Cambridge International AS & A Level'}[lvl]
    q = [("", [
        (f"Do you offer one-to-one {full} tuition online?", f"Yes. Valeem teaches {lvl_full} {name} ({code}) live and one-to-one online. Your child's teacher holds an A or B grade in {name} and has passed our interview and training."),
        (f"What does {full} {code} tuition cover?", f"The full {name} {code} syllabus: " + ', '.join(t.lower() if i else t for i, t in enumerate(topics[:-1])) + f" and {topics[-1].lower()}, with past-paper practice and exam technique."),
        (f"Which {full} topics do students find hardest?", f"Most students we teach need extra help with {hard}. The teacher finds your child's gaps in the free demo and builds the plan around them."),
        ("Do you teach the latest syllabus?", f"Yes. Teachers follow the {name} {code} syllabus for your child's exam year, including any changes Cambridge has announced, and use past papers from recent series."),
        (f"How much is {full} tuition?", "Tuition is a monthly plan. The fee depends on the grade, the number of months, classes per week, class length and whether you want a fixed time slot. A counsellor shares the fee after the free demo."),
        ("Can students in Saudi Arabia and the Gulf join?", "Yes. About 70% of our families live in the Middle East, most of them in Saudi Arabia. Classes are scheduled after school in your time zone."),
    ])]
    fs, ld = faq(q, title=f'{full} {code}: Your Questions Answered.')
    course = {"@context": "https://schema.org", "@type": "Course", "name": f"{full} {name if False else ''}".strip() + f" {code} online tuition".replace(f'{full}  ', f'{full} '),
              "courseCode": code, "description": f"Live one-to-one online tuition for {lvl_full} {name} ({code}) with a vetted teacher. Free demo, monthly plans.",
              "url": url, "provider": ORG, "educationalLevel": lvl,
              "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online", "courseWorkload": "Live one-to-one classes, scheduled by arrangement"},
              "offers": {"@type": "Offer", "category": "Paid", "description": "Monthly plan; fee shared after a free demo class."}}
    course["name"] = f"{full} {code} online tuition"
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Valeem", "item": B + "/"},
        {"@type": "ListItem", "position": 2, "name": "Online Tuition", "item": B + "/online-tuition/"},
        {"@type": "ListItem", "position": 3, "name": f"{full} {code}", "item": url}]}
    tlis = '\n'.join(f'        <li>{TICK}{t}</li>' for t in topics)
    prog = 'Online Tuition: A Level' if lvl == 'A Level' else 'Online Tuition: IGCSE or O Level'
    main = page_hero(f'<a href="{B}/online-tuition/">Online Tuition</a> / {full} {code}', f'Online Tuition · {lvl} · Syllabus {code}',
        f'{full} {code} Tuition, <em>Live and One-to-One.</em>',
        f'{focus} A vetted {name} teacher, classes at your time, and a free demo before you decide.',
        f'<a class="btn btn-primary" href="#demo" data-cta="hero" data-prog="{prog}">Book a Free {name} Demo</a>' + WA_BTN,
        GULF_PILLS, 'levels.webp', f'A student smiling at his laptop during a live {name} lesson') + f'''
<section id="syllabus">
  <div class="wrap">
    <div class="head">
      <p class="kicker">What we cover</p>
      <h2>The Full {name} {code} Syllabus.</h2>
      <p class="lede">Your child's teacher works through every topic area, in the order that suits their school, and fills gaps along the way.</p>
    </div>
    <ul class="topics">
{tlis}
    </ul>
    <p class="note">Topic areas follow the {lvl_full} {name} {code} syllabus. We always teach the version for your child's exam year.</p>
  </div>
</section>

<section id="classes" class="wash">
  <div class="wrap feat">
    <figure class="photo"><img src="images/evening.webp" alt="A student smiling during an evening online {name} class" width="1000" height="800" loading="lazy"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">How the classes work</p>
        <h2>Built Around Where Your Child Loses Marks.</h2>
        <p class="lede">Most students we teach in {full} need help with {hard}.</p>
      </div>
      <ul class="feature-list">
        <li><span class="badge"><svg class="icon"><use href="#i-live"/></svg></span><div><h3>Concepts, explained properly</h3><p>Live one-to-one, so your child can ask until it makes sense.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-clip"/></svg></span><div><h3>Past papers and mark schemes</h3><p>Questions from recent {code} papers, marked the way examiners mark them.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-calendar"/></svg></span><div><h3>A plan to the exam</h3><p>A timetable that covers the syllabus and leaves time for revision.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-chart"/></svg></span><div><h3>Progress you can follow</h3><p>Classes and resources on our learning platform, with updates for parents.</p></div></li>
      </ul>
    </div>
  </div>
</section>

''' + vet_section(title=f'Every {name} Teacher Passes Four Checks.') + fees_section() + form_section([], title=f'Book a Free {full} Demo.', lede=f'Tell us your child\'s level and where they need help in {name}. A counsellor will call you to arrange a free demo with a {name} teacher.', form_title='Register for a free trial lesson', wash=False) + fs + f'''
<section id="more-subjects" class="wash">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Other subjects</p>
      <h2>Need Help in Another Subject?</h2>
      <p class="lede">We teach every IGCSE, O Level and A Level subject. <a href="{B}/online-tuition/">See Online Tuition</a>.</p>
    </div>
{subj_links(slug)}
  </div>
</section>
'''
    h = head(f'{full} {code} Online Tuition | One-to-One Tutor | Valeem',
             f'Live one-to-one {full} ({code}) tuition online with a vetted teacher. Full syllabus, past papers and exam technique. Classes in Pakistan, Saudi and Gulf time zones. Free demo.',
             url, f'{full} {code} Online Tuition | Valeem', f'One-to-one {full} {code} classes with a vetted teacher. Free demo, monthly plans.',
             B + '/online-tuition/images/levels.webp', [course, ld, crumbs])
    wa = f"Hello, I would like a free demo for {full} ({code})."
    html_ = page(h, f' data-lead="SUBJECT {full} {code}" data-wa-text="{esc(wa)}"', 'tuition', main)
    write(f'{R}/online-tuition/{slug}/index.html', absimg(html_, 'online-tuition'))

# =====================================================================
# COUNTRY PAGES  (same URLs as before)
# =====================================================================
COUNTRIES = {
 'SA': dict(folder='online-tuition-saudi-arabia', name='Saudi Arabia', the='Saudi Arabia', adj='Saudi', tz='Saudi time (AST, UTC+3)', short='Saudi time',
            week='The Saudi school week runs Sunday to Thursday, with Friday and Saturday as the weekend.',
            cities=['Riyadh', 'Jeddah', 'Dammam', 'Al Khobar', 'Makkah', 'Madinah', 'Taif', 'Jubail', 'Abha', 'Tabuk'],
            stat='70%', statline='of our families live in the Middle East, most of them in Saudi Arabia.',
            pay='Many families pay from a Saudi or Pakistani bank account.',
            schools='international and Pakistani curriculum schools in the Kingdom', lead='SAUDI PAGE'),
 'AE': dict(folder='online-tuition-uae', name='the UAE', the='the UAE', adj='UAE', tz='UAE time (GST, UTC+4)', short='UAE time',
            week='UAE schools run Monday to Friday, with a shorter Friday, and the weekend on Saturday and Sunday.',
            cities=['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman', 'Al Ain', 'Ras Al Khaimah', 'Fujairah'],
            stat='70%', statline='of our families live in the Middle East, including many in the UAE.',
            pay='Families pay by monthly invoice, from a UAE or Pakistani bank account.',
            schools='British, international and Pakistani curriculum schools across the Emirates', lead='UAE PAGE'),
}
for cc, c in COUNTRIES.items():
    url = f"{B}/{c['folder']}/"
    q = [("", [
        (f"Do you offer online O Level, IGCSE and A Level tuition in {c['the']}?", f"Yes. Valeem teaches students across {c['the']} live and one-to-one online, for IGCSE, O Level and A Level, and younger students from Grade 5. Every teacher holds an A or B grade in their subject."),
        (f"What time are classes for families in {c['the']}?", f"Every class is booked in {c['tz']}, after school or at weekends. {c['week']}"),
        ("Which subjects do you teach?", "Every subject offered for IGCSE, O Level and A Level, including Mathematics, Additional Mathematics, Physics, Chemistry, Biology, Economics, English Language and Pakistan Studies.", ("Pakistan Studies", B + "/online-tuition/igcse-pakistan-studies-0448/")),
        ("How much does tuition cost?", f"Tuition is a monthly plan. The fee depends on the grade, the number of months, classes per week, class length and whether you want a fixed time slot. A counsellor shares the fee after the free demo. {c['pay']}"),
        ("Can my child try a class first?", "Yes. The first class is a free live demo at your time. If the teacher isn't the right fit later, we arrange another."),
    ] + ([("Can my child sit O Level or IGCSE exams as a private candidate in Saudi Arabia?", "Yes. In Saudi Arabia, private candidates usually register for Cambridge exams through the British Council. Our private candidate guide explains the steps, and Valeem prepares students for the exams.", ("private candidate guide", B + "/online-tuition-saudi-arabia/private-candidate-guide/"))] if cc == 'SA' else []))]
    fs, ld = faq(q, title=f'Tuition in {c["name"][0].upper() + c["name"][1:]}: Your Questions Answered.')
    service = {"@context": "https://schema.org", "@type": "Service", "name": f"Online tuition in {c['the']}", "serviceType": "Online tutoring",
               "description": f"Live one-to-one online tuition for IGCSE, O Level and A Level for families in {c['the']}, in {c['short']}.",
               "url": url, "provider": ORG, "areaServed": {"@type": "Country", "name": 'Saudi Arabia' if cc == 'SA' else 'United Arab Emirates'}}
    cities = ''.join(f'<li>{x}</li>' for x in c['cities'])
    guide = f'''
<section id="private-candidates">
  <div class="wrap feat rev">
    <figure class="photo"><img src="images/a-level.webp" alt="A student revising for her exams at home" width="900" height="945" loading="lazy"></figure>
    <div class="head" style="margin-bottom:0">
      <p class="kicker">Sitting exams in Saudi Arabia</p>
      <h2>Taking O Levels or IGCSEs as a Private Candidate?</h2>
      <p class="lede">Many of our students sit Cambridge exams privately, through the British Council in Saudi Arabia. We prepare them for the syllabus and the exam, and help families plan the timeline.</p>
      <div class="cta-row"><a class="btn btn-ghost" href="{B}/online-tuition-saudi-arabia/private-candidate-guide/">Read the Private Candidate Guide</a></div>
    </div>
  </div>
</section>
''' if cc == 'SA' else ''
    main = page_hero(f'Tuition in {c["the"]}', f'Online Tuition · {c["adj"]} families', f'O Level, IGCSE and A Level Tuition in {c["name"][0].upper() + c["name"][1:]}, <em>in {c["short"]}.</em>',
        f"One-to-one live classes with vetted teachers, scheduled after school in {c['tz']}.",
        '<a class="btn btn-primary" href="#demo" data-cta="hero" data-prog="Online Tuition: IGCSE, O Level or A Level">Book a Free Demo</a>' + WA_BTN,
        [('i-user', 'One-to-one'), ('i-play', 'Free demo'), ('i-clock', c['short'])], 'hero.webp', 'A student giving a thumbs up beside her laptop during an online class') + f'''
<section id="timings" class="gulf">
  <div class="wrap feat">
    <figure class="photo"><img src="images/o-level.webp" alt="A student in an online class at home in the evening" width="900" height="945" loading="lazy"></figure>
    <div class="head" style="margin-bottom:0">
      <p class="kicker">Built for families in {c['the']}</p>
      <h2>Classes That Fit Your Child's School Week.</h2>
      <div class="stat-big"><b>{c['stat']}</b><span>{c['statline']}</span></div>
      <ul class="ticks" style="grid-template-columns:1fr;margin-top:8px">
        <li>{TICK}Every class booked in {c['tz']}, so you never convert times</li>
        <li>{TICK}{c['week']}</li>
        <li>{TICK}Teachers who know the boards used by {c['schools']}</li>
        <li>{TICK}{c['pay']}</li>
      </ul>
      <ul class="places">{cities}<li>and everywhere else in {c['the']}</li></ul>
    </div>
  </div>
</section>

<section id="levels" class="wash">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Levels we teach</p>
      <h2>From Grade 5 to A Level.</h2>
    </div>
    <ol class="ladder light" aria-label="Online tuition levels">
      <li><span class="ic"><svg class="icon"><use href="#i-book"/></svg></span><i>Grades 5–7</i><b>Strong Basics</b><span>English, Maths and homework support.</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-compass"/></svg></span><i>Grade 8</i><b>Getting Ready</b><span>Foundations for IGCSE and O Level subjects.</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-cap"/></svg></span><i>Grades 9–11</i><b>IGCSE &amp; O Level</b><span>Full syllabus, past papers and exam technique.</span><span class="core">Most popular</span></li>
      <li><span class="ic"><svg class="icon"><use href="#i-route"/></svg></span><i>AS &amp; A2</i><b>A Level</b><span>Subject specialists for the step up.</span></li>
    </ol>
  </div>
</section>

<section id="subjects">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Popular subjects</p>
      <h2>Find Your Subject and Syllabus Code.</h2>
      <p class="lede">We teach every IGCSE, O Level and A Level subject. These are the ones families in {c['the']} ask for most.</p>
    </div>
{subj_links()}
  </div>
</section>
''' + guide + vet_section(title='Every Teacher Passes Four Checks.') + fees_section() + f'''
<section id="process">
  <div class="wrap feat">
    <figure class="photo"><img src="images/homeschool.webp" alt="A parent and child at a laptop" width="900" height="945" loading="lazy"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">How to start</p>
        <h2>From Free Demo to Monthly Plan.</h2>
      </div>
      {timeline()}
    </div>
  </div>
</section>

''' + form_section([], title='Book a Free Demo Class.', lede=f'Tell us what your child needs. A counsellor will call you to arrange a free demo in {c["short"]}.', form_title='Register for a free trial lesson', wash=True) + fs
    h = head(f'Online O Level, IGCSE and A Level Tuition in {c["name"][0].upper() + c["name"][1:]} | Valeem',
             f'Live one-to-one online tuition for O Level, IGCSE and A Level for families in {c["the"]}. Vetted teachers, classes in {c["short"]}, free demo, monthly plans.',
             url, f'Online Tuition in {c["the"]} | Valeem', f'One-to-one IGCSE, O Level and A Level classes in {c["short"]}. Free demo.',
             url + 'images/share.jpg', [service, ld, crumbs_ld(f'Tuition in {c["the"]}', url)])
    html_ = page(h, f' data-lead="{c["lead"]}" data-country="{cc}"', 'tuition', main)
    write(f"{R}/{c['folder']}/index.html", html_)

# =====================================================================
# PRIVATE CANDIDATE GUIDE (Saudi Arabia)
# =====================================================================
url = f'{B}/online-tuition-saudi-arabia/private-candidate-guide/'
q = [("", [
    ("Can my child sit O Level or IGCSE exams privately in Saudi Arabia?", "Yes. Students who can't enter through their school can register as private candidates. In Saudi Arabia this is usually done through the British Council, which registers private candidates for Cambridge, Pearson Edexcel and OxfordAQA exams."),
    ("When are the Cambridge exams?", "Cambridge IGCSE, O Level and AS & A Level exams are held in two main series each year: May/June and October/November. Registration closes months before each series, so plan early."),
    ("What documents are needed to register?", "A valid passport or national ID (Iqama for residents). If the candidate is under 18, a parent or guardian completes the registration. Check the British Council Saudi Arabia website for the current requirements and fees."),
    ("Does Valeem register students for exams?", "No. Families register directly with the British Council. Valeem prepares the student: we teach the syllabus, practise past papers and plan the timeline to the exam series."),
    ("Can a homeschooled child take O Levels?", "Yes. Many homeschooled children sit O Levels or IGCSEs as private candidates. Our Homeschool Pathways programme prepares younger children for that step.", ("Homeschool Pathways", B + "/homeschool-pathways/")),
])]
fs, ld = faq(q, title='Private Candidates: Your Questions Answered.')
article = {"@context": "https://schema.org", "@type": "Article", "headline": "Sitting O Level, IGCSE or A Level exams as a private candidate in Saudi Arabia",
           "description": "How families in Saudi Arabia register children as private candidates for Cambridge O Level, IGCSE and A Level exams, and how to prepare.",
           "url": url, "author": ORG, "publisher": ORG, "dateModified": "2026-11-24", "inLanguage": "en"}
crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Valeem", "item": B + "/"},
    {"@type": "ListItem", "position": 2, "name": "Tuition in Saudi Arabia", "item": B + "/online-tuition-saudi-arabia/"},
    {"@type": "ListItem", "position": 3, "name": "Private candidate guide", "item": url}]}
main = page_hero(f'<a href="{B}/online-tuition-saudi-arabia/">Tuition in Saudi Arabia</a> / Private candidate guide', 'Guide · Families in Saudi Arabia',
    'Sitting O Levels, IGCSEs or A Levels as a <em>Private Candidate in Saudi Arabia.</em>',
    'If your child isn\'t entered through a school, they can still sit Cambridge exams. Here is how it works, and how to prepare.',
    '<a class="btn btn-primary" href="#demo" data-cta="hero" data-prog="Online Tuition: IGCSE, O Level or A Level">Book a Free Demo</a>' + WA_BTN,
    [('i-file', 'Register privately'), ('i-calendar', 'Two exam series'), ('i-user', '1:1 preparation')], 'a-level.webp', 'A student revising for her exams at home') + f'''
<section id="steps">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Step by step</p>
      <h2>From Choosing Subjects to Exam Day.</h2>
      <p class="lede">Dates, fees and rules change every series. Always confirm them with the British Council in Saudi Arabia before you register.</p>
    </div>
    <ol class="steps-plain">
      <li><b>Choose the qualification and subjects</b>Decide between O Level and IGCSE (or AS and A Level), and check the syllabus code for each subject, for example O Level Mathematics 4024 or IGCSE Pakistan Studies 0448.</li>
      <li><b>Pick the exam series</b>Cambridge exams run in May/June and October/November. Work back from the series to make sure there is enough time to finish the syllabus and practise past papers.</li>
      <li><b>Register with the British Council</b>Register online as a private candidate during the registration window, with a valid passport or Iqama. A parent or guardian registers candidates under 18.</li>
      <li><b>Pay the exam fees</b>The British Council lists the fees for each subject. Registration isn't complete until payment is received, and late entries cost more.</li>
      <li><b>Prepare with a plan</b>Cover the full syllabus, then switch to timed past papers. Science subjects may include practical papers, so plan for those too.</li>
      <li><b>Exam day and results</b>The British Council confirms the exam venue and timetable. Results are released by Cambridge after each series.</li>
    </ol>
    <p class="note">Official information: <a href="https://saudiarabia.britishcouncil.org/en/exam/igcse-school/register/private" rel="noopener">British Council Saudi Arabia, private candidate registration</a>.</p>
  </div>
</section>

<section id="prepare" class="wash">
  <div class="wrap feat">
    <figure class="photo"><img src="images/o-level.webp" alt="A student in a live online class" width="900" height="945" loading="lazy"></figure>
    <div>
      <div class="head" style="margin-bottom:24px">
        <p class="kicker">How Valeem helps</p>
        <h2>Private Candidates Need a Teacher and a Plan.</h2>
        <p class="lede">Without a school timetable, it's easy to fall behind. A one-to-one teacher keeps your child on track to the exam series.</p>
      </div>
      <ul class="feature-list">
        <li><span class="badge"><svg class="icon"><use href="#i-calendar"/></svg></span><div><h3>A timeline to the series</h3><p>Syllabus first, then past papers, with time for revision.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-user"/></svg></span><div><h3>A vetted subject teacher</h3><p>A or B grade in the subject, interviewed and trained.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-clock"/></svg></span><div><h3>Classes in Saudi time</h3><p>Booked in AST (UTC+3), around your family's week.</p></div></li>
        <li><span class="badge"><svg class="icon"><use href="#i-clip"/></svg></span><div><h3>Exam-style practice</h3><p>Past papers marked the way examiners mark them.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section id="subjects">
  <div class="wrap">
    <div class="head">
      <p class="kicker">Popular subjects</p>
      <h2>Subjects Private Candidates Choose Most.</h2>
    </div>
{subj_links()}
  </div>
</section>

''' + form_section([], title='Plan Your Child\'s Exams With Us.', lede='Tell us the subjects and the exam series. A counsellor will call you to arrange a free demo and a study plan.', form_title='Register for a free trial lesson', wash=True) + fs
h = head('O Level and IGCSE as a Private Candidate in Saudi Arabia | Valeem Guide',
         'How to sit Cambridge O Level, IGCSE and A Level exams as a private candidate in Saudi Arabia: subjects, exam series, British Council registration and how to prepare.',
         url, 'Private Candidate Guide: Saudi Arabia | Valeem', 'Sitting O Levels or IGCSEs privately in Saudi Arabia, step by step.',
         B + '/online-tuition-saudi-arabia/images/share.jpg', [article, ld, crumbs])
html_ = page(h, ' data-lead="SAUDI PRIVATE CANDIDATE GUIDE" data-country="SA"', 'tuition', main)
write(f'{R}/online-tuition-saudi-arabia/private-candidate-guide/index.html', absimg(html_, 'online-tuition-saudi-arabia'))
print('built', len(SUBJECTS), 'subject pages, 2 country pages, 1 guide')
