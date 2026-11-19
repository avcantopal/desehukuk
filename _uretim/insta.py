# -*- coding: utf-8 -*-
# Karar bülteni için Instagram görselleri (1080x1350). Kullanım: python3 insta.py [çıktı klasörü]
import sys, os, html, json, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from kararlar_icerik import KARARLAR
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "_uretim", "insta")
os.makedirs(OUT, exist_ok=True)
e = html.escape

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{font-family:Inter,sans-serif;background:#0a1830;color:#fff;overflow:hidden;position:relative}
.ph{position:absolute;left:0;top:0;width:1080px;height:640px;background-size:cover;background-position:center}
.ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,24,48,.88) 0%,rgba(10,24,48,.5) 32%,rgba(10,24,48,.62) 62%,#0a1830 100%)}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;right:-380px;bottom:-420px;background:radial-gradient(circle,rgba(214,180,131,.22),transparent 65%)}
.sec{position:absolute;right:46px;top:430px;font-family:"Crimson Text",serif;font-size:520px;line-height:1;color:rgba(214,180,131,.07)}
.frame{position:absolute;inset:34px;border:1.5px solid rgba(214,180,131,.45);pointer-events:none}
.top{position:absolute;left:84px;right:84px;top:84px;display:flex;justify-content:space-between;align-items:center}
.wm b{display:block;font-family:"Crimson Text",serif;font-weight:600;font-size:52px;letter-spacing:.34em;color:#e3c48f;line-height:1}
.wm small{display:block;margin-top:8px;font-size:15px;letter-spacing:.32em;color:rgba(233,211,160,.9);font-weight:500}
.chip{font-size:17px;font-weight:600;letter-spacing:.2em;color:#0f2240;background:linear-gradient(100deg,#d6b483,#f1dcae);padding:13px 22px;border-radius:999px}
.body{position:absolute;left:84px;right:84px;top:520px}
.alan{display:flex;align-items:center;gap:16px;font-size:20px;font-weight:600;letter-spacing:.24em;color:#d6b483;text-transform:uppercase}
.alan:before{content:"";width:56px;height:2px;background:#d6b483}
h1{font-family:"Crimson Text",serif;font-weight:600;color:#fff;line-height:1.12;margin-top:26px;letter-spacing:-.005em}
.kart{position:absolute;left:84px;right:84px;bottom:150px;background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(255,255,255,.04));border:1px solid rgba(214,180,131,.35);border-radius:22px;padding:28px 34px}
.kart .m{font-family:"Crimson Text",serif;font-size:31px;font-weight:600;color:#fff}
.kart .g{display:flex;gap:0;margin-top:16px}
.kart .g div{flex:1;border-left:1.5px solid rgba(214,180,131,.5);padding-left:18px}
.kart span{display:block;font-size:14px;letter-spacing:.2em;color:rgba(255,255,255,.6);font-weight:500}
.kart strong{display:block;font-size:25px;font-weight:600;margin-top:4px;font-variant-numeric:tabular-nums}
.alt{position:absolute;left:84px;right:84px;bottom:76px;display:flex;justify-content:space-between;align-items:center;font-size:20px;color:rgba(255,255,255,.75)}
.alt b{color:#e3c48f;font-weight:600;letter-spacing:.02em}
"""

def fs(t):
    n = len(t)
    return 86 if n < 70 else 78 if n < 95 else 72 if n < 120 else 66 if n < 150 else 60

for k in KARARLAR:
    kn = k['kunye']; mah = kn['mahkeme'].split(' (')[0]
    img = "file://" + os.path.join(ROOT, "assets", "img", k['img'])
    h = f"""<!DOCTYPE html><html lang="tr"><head><meta charset="UTF-8"><style>{CSS}</style></head><body>
<div class="ph" style="background-image:url('{img}')"></div><div class="glow"></div><div class="sec">§</div><div class="frame"></div>
<div class="top"><div class="wm"><b>DESE</b><small>HUKUK VE DANIŞMANLIK</small></div><div class="chip">KARAR BÜLTENİ</div></div>
<div class="body"><div class="alan">{e(k['alan'])}</div><h1 style="font-size:{fs(k['baslik'])}px">{e(k['baslik']).replace('3. kişi','3.&nbsp;kişi')}</h1></div>
<div class="kart"><div class="m">{e(mah)}</div><div class="g"><div><span>ESAS</span><strong>{kn['esas']}</strong></div><div><span>KARAR</span><strong>{kn['karar']}</strong></div><div><span>TARİH</span><strong>{kn['tarih']}</strong></div></div></div>
<div class="alt"><span>Değerlendirmenin tamamı</span><b>desehukuk.com/kararlar</b></div>
</body></html>"""
    hp = os.path.join(OUT, k['slug'] + ".html")
    open(hp, "w", encoding="utf-8").write(h)

js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1350}}}});
for(const s of {json.dumps([k['yayin']+'_'+k['slug'] for k in KARARLAR])}){{const slug=s.slice(11);await p.goto('file://{OUT}/'+slug+'.html');await p.waitForTimeout(300);
const ov=await p.evaluate(()=>{{const h=document.querySelector('h1').getBoundingClientRect(),k=document.querySelector('.kart').getBoundingClientRect();return k.top-h.bottom;}});
console.log(slug,'bosluk',Math.round(ov));await p.screenshot({{path:'{OUT}/'+s+'.png'}});}}await b.close();}})();"""
open(os.path.join(OUT, "_render.js"), "w").write(js)
subprocess.run(["node", os.path.join(OUT, "_render.js")], check=True)
for k in KARARLAR: os.remove(os.path.join(OUT, k['slug'] + ".html"))
os.remove(os.path.join(OUT, "_render.js"))
