# -*- coding: utf-8 -*-
import sys, os, json, html
sys.path.insert(0, os.path.dirname(__file__))
from kararlar_icerik import KARARLAR

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ONAY = "--onay" in sys.argv   # onaydan sonra: noindex kalkar
AY = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
WA_NO = "905064933573"
e = html.escape

def tarih_tr(iso):
    y, m, d = iso.split('-'); return f"{int(d)} {AY[int(m)-1]} {y}"

WA_SVG = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff"><path d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 001.8-1.3 2.2 2.2 0 00.2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
FOOTER = f'''<footer><div class="wrap">
  <span>© 2026 DESE Hukuk ve Danışmanlık · <a href="/">desehukuk.com</a> · <a href="/kvkk.html">KVKK Aydınlatma Metni</a> · <a href="/cerez-politikasi.html">Çerez Politikası</a></span>
  <span>Karar bülteni genel bilgilendirme amaçlıdır; belirli bir uyuşmazlığa ilişkin hukuki mütalaa niteliği taşımaz ve avukat-müvekkil ilişkisi kurmaz.</span>
</div></footer>
<a class="wa" href="https://wa.me/{WA_NO}?text=Merhaba%2C%20desehukuk.com%20%C3%BCzerinden%20ula%C5%9F%C4%B1yorum." target="_blank" rel="noopener" aria-label="WhatsApp ile yazın">{WA_SVG}</a>'''

HEAD = '''<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no">
{robots}<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/sayfa.css">
<link rel="stylesheet" href="/assets/araclar.css">'''
ROBOTS = '' if ONAY else '<meta name="robots" content="noindex, nofollow">\n'

# yayın tarihi gelmeden sayfa açılırsa bültene yönlendir (?onizleme ile atlanır)
KILIT = 'false' if ONAY else 'true'   # onay gelene kadar tarih gelse de gizli
GATE = '''<script>(function(){try{if(/[?&]onizleme/.test(location.search))return;var y=document.documentElement.getAttribute('data-yayin'),d=new Date(),t=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');if(%s||(y&&y>t))location.replace('/kararlar/');}catch(x){}})();</script>''' % KILIT

def sayfa(k):
    url = f"https://desehukuk.com/kararlar/{k['slug']}.html"
    kn = k['kunye']
    kaynak = f"https://mevzuat.adalet.gov.tr/ictihat/{kn['id']}"
    atif = f"{kn['mahkeme'].split(' (')[0]}, {kn['tarih']} tarihli, {kn['esas']} E., {kn['karar']} K."
    ld = {"@context":"https://schema.org","@type":"Article","headline":k['baslik'],"description":k['aciklama'],"inLanguage":"tr",
          "datePublished":k['yayin'],"image":f"https://desehukuk.com/assets/img/{k['img']}",
          "author":{"@type":"Organization","name":"DESE Hukuk ve Danışmanlık","url":"https://desehukuk.com/"},
          "publisher":{"@type":"Organization","name":"DESE Hukuk ve Danışmanlık","url":"https://desehukuk.com/"},
          "mainEntityOfPage":url}
    msg = f"Merhaba, desehukuk.com karar bülteninde \"{k['baslik']}\" kararını okudum. {k['wa'].capitalize()} konusunda görüşmek istiyorum."
    p = []
    p.append(f'''<!DOCTYPE html>
<html lang="tr" data-yayin="{k['yayin']}">
<head>
{HEAD.format(robots=ROBOTS)}
{GATE}
<title>{e(k['baslik'])} | DESE Hukuk</title>
<meta name="description" content="{e(k['aciklama'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(k['baslik'])}">
<meta property="og:description" content="{e(k['aciklama'])}">
<meta property="og:image" content="https://desehukuk.com/assets/img/{k['img']}">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="DESE Hukuk ve Danışmanlık">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://desehukuk.com/assets/img/{k['img']}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap">
  <a href="/" class="logo" aria-label="DESE Hukuk ve Danışmanlık"><span class="wm"><b>DESE</b><small>Hukuk ve Danışmanlık</small></span></a>
  <div class="hr"><a href="/kararlar/" class="back">← Karar bülteni</a></div>
</div></header>
<div id="prog" aria-hidden="true"></div>
<div class="hero photo"><div class="hbg" style="background-image:url(/assets/img/{k['img']});--fp:50% 50%;--fl:50%" aria-hidden="true"></div>
<div class="wrap">
  <div class="eyebrow">Karar Bülteni · {e(k['alan'])}</div>
  <h1>{e(k['baslik'])}</h1>
  <div class="meta">{e(kn['mahkeme'].split(' (')[0])}</div>
</div></div>
<article><div class="wrap">

<div class="kunye-kart">
<div class="ust">KARAR KÜNYESİ</div>
<h4>{e(kn['mahkeme'].split(' (')[0])}</h4>
<div class="g"><div><span>Esas</span><strong>{kn['esas']}</strong></div><div><span>Karar</span><strong>{kn['karar']}</strong></div><div><span>Tarih</span><strong>{kn['tarih']}</strong></div></div>
<div class="alt"><a href="{kaynak}" target="_blank" rel="noopener">Resmi metin ↗</a></div>
</div>

<h2>Olay</h2>''')
    for x in k['olay']: p.append(f"<p>{e(x)}</p>")
    p.append("<h2>Yargıtay ne dedi?</h2>")
    for x in k['alinti']: p.append(f"<blockquote>“{e(x)}”</blockquote>")
    p.append("<h2>Ne anlama geliyor?</h2>")
    for x in k['anlam']: p.append(f"<p>{e(x)}</p>")
    p.append('<div class="box"><h3>Dikkat edilmesi gerekenler</h3><ul>' + ''.join(f"<li>{e(x)}</li>" for x in k['dikkat']) + "</ul></div>")
    p.append(f'''<div class="cta">Benzer bir durumla karşı karşıyaysanız dosyanızı birlikte değerlendirelim.<br><a href="https://wa.me/{WA_NO}?text={_q(msg)}" target="_blank" rel="noopener">WhatsApp ile yazın</a></div>''')
    if k.get('ilgili'):
        p.append('<p class="areas-link">İlgili içerikler: ' + ' · '.join(f'<a href="{u}">{e(t)}</a>' for u, t in k['ilgili']) + ' · <a href="/kararlar/">Tüm kararlar</a></p>')
    p.append(f'''<p class="note">Kararın künyesi ve alıntılar Yargıtay'ın resmi içtihat metninden aynen aktarılmıştır; taraf bilgileri yer almamaktadır. Atıf: {e(atif)}. Bu yazı genel bilgilendirme amaçlıdır ve somut uyuşmazlıklar için hukuki mütalaa yerine geçmez.</p>
<p class="telif">© DESE Hukuk ve Danışmanlık. Bu yazının tamamı veya bir kısmı kaynak gösterilmeden kullanılamaz.</p>

</div></article>
{FOOTER}
<script>(function(){{var b=document.getElementById('prog');if(!b)return;function u(){{var a=document.querySelector('article');if(!a)return;var r=a.getBoundingClientRect(),h=a.offsetHeight-innerHeight,p=Math.min(1,Math.max(0,-r.top/(h>0?h:1)));b.style.transform='scaleX('+p+')';}}addEventListener('scroll',u,{{passive:true}});addEventListener('resize',u);u();}})();</script>
</body>
</html>
''')
    return "\n".join(p)

def _q(s):
    from urllib.parse import quote
    return quote(s, safe='')

def index():
    veri = [{"slug":k['slug'],"alan":k['alan'],"baslik":k['baslik'],"ozet":k['aciklama'],"yayin":k['yayin'],
             "mahkeme":k['kunye']['mahkeme'].split(' (')[0],"tarih":k['kunye']['tarih']} for k in KARARLAR]
    return f'''<!DOCTYPE html>
<html lang="tr">
<head>
{HEAD.format(robots=ROBOTS)}
<title>Karar Bülteni: Yargıtay'ın Yerleşik Kararları | DESE Hukuk</title>
<meta name="description" content="Kira, iş, aile, miras, tazminat ve ceza hukukunda vatandaşı doğrudan ilgilendiren yerleşik Yargıtay kararları; sade özet ve değerlendirmeyle.">
<link rel="canonical" href="https://desehukuk.com/kararlar/">
<meta property="og:type" content="website">
<meta property="og:url" content="https://desehukuk.com/kararlar/">
<meta property="og:title" content="Karar Bülteni | DESE Hukuk">
<meta property="og:description" content="Vatandaşı doğrudan ilgilendiren yerleşik Yargıtay kararları, sade dille.">
<meta property="og:image" content="https://desehukuk.com/assets/img/mahkeme-terazi.jpg">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="DESE Hukuk ve Danışmanlık">
</head>
<body>
<header><div class="wrap">
  <a href="/" class="logo" aria-label="DESE Hukuk ve Danışmanlık"><span class="wm"><b>DESE</b><small>Hukuk ve Danışmanlık</small></span></a>
  <div class="hr"><a href="/" class="back">← Ana sayfa</a></div>
</div></header>
<div class="hero"><div class="wrap">
  <div class="eyebrow">Karar Bülteni</div>
  <h1>Yargıtay'ın Yerleşik Kararları</h1>
  <div class="meta">Vatandaşı doğrudan ilgilendiren kararlar, sade özet ve değerlendirmeyle</div>
</div></div>
<main class="tool"><div class="wrap">
<div class="filtre" id="filtre"></div>
<div class="tools kl" id="liste"></div>
<p class="disc">Kararların künyeleri ve alıntıları Yargıtay'ın resmi içtihat metinlerinden alınmıştır. Bülten genel bilgilendirme amaçlıdır; somut durumunuz için bizimle iletişime geçebilirsiniz.</p>
</div></main>
{FOOTER}
<script>
(function(){{
  var V={json.dumps(veri, ensure_ascii=False)};
  var AY={json.dumps(AY, ensure_ascii=False)};
  var on=/[?&]onizleme/.test(location.search), d=new Date(), t=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
  var L=V.filter(function(k){{return on||(!{KILIT}&&k.yayin<=t);}}).sort(function(a,b){{return a.yayin<b.yayin?1:-1;}});
  function tr(iso){{var p=iso.split('-');return (+p[2])+' '+AY[+p[1]-1]+' '+p[0];}}
  var alanlar=['Tümü'];L.forEach(function(k){{if(alanlar.indexOf(k.alan)<0)alanlar.push(k.alan);}});
  var secili='Tümü';
  function ciz(){{
    var h='';L.filter(function(k){{return secili==='Tümü'||k.alan===secili;}}).forEach(function(k){{
      h+='<a class="tcard" href="/kararlar/'+k.slug+'.html'+(on?'?onizleme':'')+'"><span>'+k.alan+'</span><b>'+k.baslik+'</b><em>'+k.mahkeme+'</em></a>';
    }});
    document.getElementById('liste').innerHTML=h||'<p>İlk kararlar çok yakında burada.</p>';
    document.getElementById('filtre').innerHTML=alanlar.length>2?alanlar.map(function(a){{return '<button type="button" class="'+(a===secili?'on':'')+'" data-a="'+a+'">'+a+'</button>';}}).join(''):'';
  }}
  document.getElementById('filtre').addEventListener('click',function(ev){{var a=ev.target.getAttribute('data-a');if(a){{secili=a;ciz();}}}});
  ciz();
}})();
</script>
</body>
</html>
'''

for k in KARARLAR:
    open(f"{ROOT}/kararlar/{k['slug']}.html", "w", encoding="utf-8").write(sayfa(k))
open(f"{ROOT}/kararlar/index.html", "w", encoding="utf-8").write(index())
print("ok", len(KARARLAR), "ONAY" if ONAY else "ONIZLEME")
