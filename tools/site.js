<script>
(function(){
  var WHATSAPP_NUMBER = '923322636574';
  var LEAD_ENDPOINT   = 'https://script.google.com/macros/s/AKfycbw5O8zgbUlM1L16OP2LMHxirFEzaSJOI-p6-Abr2YTx-1TndikshseIqZIHTZYTjtY1/exec';
  var WA_TEXT = "Hello, I'm interested in Valeem's classes. I would like to book a free demo.";
  function waUrl(t){ return 'https://wa.me/' + WHATSAPP_NUMBER + '?text=' + encodeURIComponent(t || WA_TEXT); }
  function $(s,r){ return (r||document).querySelector(s); }
  function $all(s,r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); }
  window.dataLayer = window.dataLayer || [];
  function track(name, data){
    data = data || {};
    try{
      var ev = {event:name}; for(var k in data) ev[k] = data[k];
      window.dataLayer.push(ev);
      if(typeof window.gtag === 'function') window.gtag('event', name, data);
      if(typeof window.fbq === 'function'){
        if(name === 'demo_form_submit_success') window.fbq('track','Lead', data);
        else if(name === 'whatsapp_click') window.fbq('track','Contact', data);
        else window.fbq('trackCustom', name, data);
      }
    }catch(e){}
  }
  $all('[data-wa]').forEach(function(a){ a.href = waUrl(); a.addEventListener('click', function(){ track('whatsapp_click', {location:a.dataset.wa}); }); });
  $all('[data-cta]').forEach(function(a){ a.addEventListener('click', function(){ track('demo_cta_click', {location:a.dataset.cta}); }); });
  var nav = $('#nav'), mb = $('#menuBtn');
  mb.addEventListener('click', function(){ var o = nav.classList.toggle('open'); mb.setAttribute('aria-expanded', o); mb.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); });
  nav.addEventListener('click', function(e){ if(e.target.tagName === 'A'){ nav.classList.remove('open'); mb.setAttribute('aria-expanded','false'); } });
  var sticky = $('#sticky');
  if('IntersectionObserver' in window){ new IntersectionObserver(function(en){ sticky.style.visibility = en[0].isIntersecting ? 'hidden' : 'visible'; }, {threshold:.15}).observe($('#demo')); }
  $('#yr').textContent = new Date().getFullYear();

  /* Programme preselect from any CTA with data-prog */
  $all('[data-prog]').forEach(function(a){ a.addEventListener('click', function(){ var s = $('#prog'); if(s){ s.value = a.dataset.prog; } }); });

  /* Banner carousel: native swipe (scroll-snap), tabs, arrows, gentle autoplay */
  var hero = $('#hero'), track = $('#slides'), slides = $all('.slide'), tabs = $all('.tabs button'), cur = 0, timer = null, DUR = 7000;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  hero.style.setProperty('--dur', DUR + 'ms');
  function mark(i){
    cur = i;
    slides.forEach(function(s, k){ s.classList.toggle('on', k === i); s.setAttribute('aria-hidden', k === i ? 'false' : 'true'); $all('a', s).forEach(function(a){ a.tabIndex = k === i ? 0 : -1; }); });
    tabs.forEach(function(t, k){ t.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
  }
  function go(i, user){
    i = (i + slides.length) % slides.length;
    track.scrollTo({left: i * track.clientWidth, behavior: still ? 'auto' : 'smooth'});
    mark(i); if(user){ track_ev(i); restart(); }
  }
  function track_ev(i){ track('banner_slide', {slide: tabs[i].textContent}); }
  function restart(){
    clearInterval(timer); if(still || hero.classList.contains('paused')) return;
    tabs.forEach(function(t){ t.style.transition = 'none'; }); void hero.offsetWidth; tabs.forEach(function(t){ t.style.transition = ''; });
    var sel = tabs[cur]; sel.setAttribute('aria-selected','false'); void sel.offsetWidth; sel.setAttribute('aria-selected','true');
    timer = setInterval(function(){ go(cur + 1); }, DUR);
  }
  tabs.forEach(function(t, k){ t.addEventListener('click', function(){ go(k, true); }); });
  $('#prev').addEventListener('click', function(){ go(cur - 1, true); });
  $('#next').addEventListener('click', function(){ go(cur + 1, true); });
  var st; track.addEventListener('scroll', function(){ clearTimeout(st); st = setTimeout(function(){ var i = Math.round(track.scrollLeft / track.clientWidth); if(i !== cur){ mark(i); track_ev(i); restart(); } }, 90); }, {passive:true});
  function pause(){ hero.classList.add('paused'); clearInterval(timer); }
  function resume(){ hero.classList.remove('paused'); restart(); }
  hero.addEventListener('mouseenter', pause); hero.addEventListener('mouseleave', resume);
  hero.addEventListener('focusin', pause); hero.addEventListener('focusout', resume);
  track.addEventListener('touchstart', pause, {passive:true}); track.addEventListener('touchend', function(){ setTimeout(resume, 4000); }, {passive:true});
  document.addEventListener('visibilitychange', function(){ document.hidden ? clearInterval(timer) : restart(); });
  window.addEventListener('resize', function(){ track.scrollLeft = cur * track.clientWidth; });
  hero.addEventListener('keydown', function(e){ if(e.key === 'ArrowRight'){ go(cur + 1, true); } else if(e.key === 'ArrowLeft'){ go(cur - 1, true); } });
  mark(0); if(still){ hero.classList.add('paused'); } else { restart(); }

  /* Gallery strip arrows */
  var strip = $('#strip');
  function step(d){ strip.scrollBy({left: d * Math.max(320, strip.clientWidth * 0.6), behavior: still ? 'auto' : 'smooth'}); }
  $('#gPrev').addEventListener('click', function(){ step(-1); });
  $('#gNext').addEventListener('click', function(){ step(1); });

  var form = $('#leadForm'), KEYS = ['utm_source','utm_medium','utm_campaign','utm_content','utm_term'], attr = {};
  try{ attr = JSON.parse(sessionStorage.getItem('vhome_attr') || '{}'); }catch(e){}
  try{
    var qs = new URLSearchParams(location.search), found = false;
    KEYS.forEach(function(k){ if(qs.get(k)){ attr[k] = qs.get(k); found = true; } });
    if(!attr.landing_page || found) attr.landing_page = location.href.split('#')[0];
    if(attr.referrer === undefined) attr.referrer = document.referrer || '';
    sessionStorage.setItem('vhome_attr', JSON.stringify(attr));
  }catch(e){}
  KEYS.concat(['landing_page','referrer']).forEach(function(k){ if(form.elements[k]) form.elements[k].value = attr[k] || ''; });

  var started = false;
  form.addEventListener('focusin', function(){ if(!started){ started = true; track('demo_form_start'); } });
  function setErr(id, msg){
    var el = $('#'+id), er = $('#'+id+'-err');
    if(er) er.textContent = msg || '';
    if(el){ if(msg){ el.setAttribute('aria-invalid','true'); el.setAttribute('aria-describedby', id+'-err'); } else el.removeAttribute('aria-invalid'); }
    return !msg;
  }
  function validate(){
    var ok = true, first = null, f = form.elements;
    function check(id, msg, test){ if(!setErr(id, test ? '' : msg)){ ok = false; first = first || $('#'+id); } }
    check('pname', 'Please enter your name.', f.parent_name.value.trim().length > 1);
    check('phone', 'Please enter a phone or WhatsApp number we can reach you on.', f.phone.value.replace(/\D/g,'').length >= 7);
    check('email', 'That email address does not look right. Check it, or leave it blank.', !f.email.value.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.email.value.trim()));
    check('city', 'Please tell us your city and country.', f.city_country.value.trim().length > 1);
    check('prog', 'Please choose a programme.', !!f.interests.value);
    check('consent', 'Please tick the box so we can contact you about your enquiry.', f.consent.checked);
    if(first) first.focus();
    return ok;
  }
  function summary(){
    var f = form.elements, l = ['Hello, I would like to book a free demo class with Valeem.', '', 'Name: ' + f.parent_name.value.trim(), 'City/country: ' + f.city_country.value.trim(), 'Programme: ' + f.interests.value];
    if(f.background.value.trim()) l.push('Subject/class: ' + f.background.value.trim());
    if(f.message.value.trim()) l.push('Message: ' + f.message.value.trim());
    return l.join('\n');
  }
  function showFail(text){
    var m = $('#formMsg'); m.hidden = false; m.textContent = text + ' ';
    var a = document.createElement('a'); a.href = waUrl(summary()); a.target = '_blank'; a.rel = 'noopener'; a.textContent = 'Send your request on WhatsApp instead'; m.appendChild(a);
  }
  form.addEventListener('submit', function(e){
    e.preventDefault(); $('#formMsg').hidden = true;
    if(form.elements.website.value) return;
    if(!validate()){ track('demo_form_error'); return; }
    track('demo_form_submit');
    var btn = $('#submitBtn'), label = btn.textContent; btn.disabled = true; btn.textContent = 'Sending…';
    var body = new URLSearchParams(new FormData(form)); body.delete('website');
    body.set('interests', 'HOMEPAGE: ' + form.elements.interests.value);
    body.append('submitted_at', new Date().toISOString());
    fetch(LEAD_ENDPOINT, {method:'POST', mode:'no-cors', body:body}).then(function(){
      form.hidden = true; var t = $('#thanks'); t.hidden = false; t.focus();
      track('demo_form_submit_success', {programme: form.elements.interests.value});
    }).catch(function(){
      btn.disabled = false; btn.textContent = label;
      showFail('We could not send your request just now. Please try again in a moment.');
      track('demo_form_error', {type:'network'});
    });
  });
})();
</script>