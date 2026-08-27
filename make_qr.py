"""부스에 붙일 QR 과 A4 인쇄물을 만든다.

왜 오류정정 H 인가
    부스에서는 종이가 접히고, 손가락이 걸치고, 조명이 반사된다. H 는 코드의
    30% 가 가려져도 읽힌다. 주소가 짧아서(31자) H 를 써도 격자가 촘촘해지지
    않는다 — 멀리서도 잘 잡힌다.

다시 만들려면
    ./venv/bin/python make_qr.py
"""

import io
import os

import re

import segno

URL = "https://rayul0325.github.io/b02/"
HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = re.search(r'(@font-face\{font-family:"Gaegu".*?format\("woff2"\)\}\s*@font-face\{font-family:"Jua".*?format\("woff2"\)\})',
                  io.open(os.path.join(HERE, "index.html"), encoding="utf-8").read(), re.S).group(1)

qr = segno.make(URL, error="h")

# 1) 낱장 PNG — 다른 인쇄물에 끼워 넣을 때
png_path = os.path.join(HERE, "qr_b02.png")
qr.save(png_path, scale=24, border=4, dark="#071A26", light="#FFFFFF")

# 2) A4 인쇄물 — 브라우저에서 열어 그대로 인쇄한다
# segno 는 바이트로 쓴다. StringIO 를 주면 TypeError 가 난다(실측).
buf = io.BytesIO()
qr.save(buf, kind="svg", scale=10, border=0,
        dark="#071A26", light=None, svgclass=None, lineclass=None,
        xmldecl=False, svgns=True, omitsize=True)
svg = buf.getvalue().decode("utf-8")

DARK = """<!doctype html>
<meta charset="utf-8">
<title>부스 B02 · QR 인쇄물</title>
<style>
  /* 게임과 같은 정체성 — memgineering 「종이와 실」. 종이 위에 손으로 쓴 것처럼. */
  @page { size: A4 portrait; margin: 0; }
  *{ box-sizing:border-box; margin:0; padding:0 }
  __FONTS__
  :root{
    --paper:#f6f9fd; --surface:#ffffff;
    --ink:#101828; --ink-2:#667085; --ink-3:#5f6d80; --ink-ghost:#b9c4d6;
    --accent:#1769ff; --accent-press:#0b56e8; --signal:#ffd84a; --signal-ink:#171711;
    --font-display:"Gaegu",sans-serif; --font-title:"Jua",sans-serif;
    --font-body:-apple-system,BlinkMacSystemFont,"Pretendard","Apple SD Gothic Neo",sans-serif;
  }
  body{ font:400 16px/1.6 var(--font-body); -webkit-font-smoothing:antialiased; background:#e7ecef }
  .sheet{
    width:210mm; height:297mm; margin:0 auto; background:var(--paper); color:var(--ink);
    display:flex; flex-direction:column; padding:20mm 18mm 14mm; position:relative;
  }
  .head{ display:flex; align-items:center; gap:5mm }
  .chip{ font-family:var(--font-title); font-size:20pt; background:var(--signal);
         color:var(--signal-ink); padding:2.5mm 6mm; transform:rotate(-1.4deg) }
  .who{ font-family:var(--font-title); font-size:16pt; color:var(--ink-2) }

  h1{ margin:12mm 0 0; font-family:var(--font-display); font-weight:700; font-size:78pt;
      line-height:.9; -webkit-text-stroke:.022em currentColor; paint-order:fill stroke }
  h1 span{ display:block; color:var(--accent) }
  .lede{ margin:8mm 0 0; font-size:16pt; color:var(--ink-2); line-height:1.5 }

  .mid{ margin-top:auto; display:flex; align-items:center; gap:12mm }
  .qrbox{ flex:none; padding:5mm; background:var(--surface); border:.7mm solid var(--ink);
          transform:rotate(-.8deg); box-shadow:2mm 3mm 6mm -2mm rgba(18,22,41,.2) }
  .qrbox svg{ display:block; width:62mm; height:62mm }
  .cta b{ display:block; font-family:var(--font-display); font-weight:700; font-size:30pt;
          color:var(--accent-press); line-height:1.08;
          -webkit-text-stroke:.022em currentColor; paint-order:fill stroke }
  .cta p{ margin-top:5mm; font-size:13pt; color:var(--ink-2); line-height:1.5 }
  .cta .gift{ margin-top:6mm; padding:4mm 6mm; display:block; max-width:82mm;
              background:var(--signal); color:var(--signal-ink);
              font-family:var(--font-title); font-size:14pt; line-height:1.4;
              transform:rotate(-1.2deg) }
  .cta .gift b{ font-weight:400; box-shadow:inset 0 -.42em 0 rgba(23,23,17,.16) }
  .cta .url{ margin-top:5mm; font-family:var(--font-title); font-size:11pt; color:var(--ink-3) }

  .foot{ margin-top:auto; padding-top:6mm; border-top:.5mm dashed var(--ink-ghost);
         display:flex; justify-content:space-between; align-items:flex-end; gap:8mm }
  .foot .subject{ font-family:var(--font-title); font-size:13pt; color:var(--ink-2); line-height:1.5 }
  .foot .team{ font-size:9.5pt; color:var(--ink-3); text-align:right; line-height:1.6 }
  @media print{ body{ background:var(--paper) } .sheet{ margin:0 } }
</style>
<div class="sheet">
  <div class="head"><span class="chip">B02</span><span class="who">젤리피쉬</span></div>
  <h1>해파리<span>피하기</span></h1>
  <p class="lede">수온이 오를수록 해파리가 늘어납니다.<br>얼마나 버틸 수 있습니까.</p>
  <div class="mid">
    <div class="qrbox">__SVG__</div>
    <div class="cta">
      <b>폰 카메라로<br>찍으세요</b>
      <p>설치 없이 바로 열립니다.<br>관측 부표를 모으고 살아남으세요.</p>
      <p class="gift">투표하고 <b>B02</b>로 오시면 <b>젤리</b> 드려요</p>
      <p class="url">rayul0325.github.io/b02</p>
    </div>
  </div>
  <div class="foot">
    <p class="subject">해양열파로 동해안 해파리<br>대량 발생 위험을 예측</p>
    <p class="team">제9회 Ocean ICT Festival<br>김민아 · 강태영 · 장도건 · 황은성</p>
  </div>
</div>
"""

# 자리표시가 하나라도 남으면 CSS 파서가 그 줄을 선택자로 읽어 :root 를 통째로
# 날린다(실측: 색·서체가 전부 기본값이 됐다). 남았는지 확인하고 쓴다.
doc = DARK.replace("__FONTS__", FONTS).replace("__SVG__", svg)
for token in ("__FONTS__", "__SVG__"):
    assert token not in doc, "치환 안 된 자리표시가 남았다: %s" % token

path = os.path.join(HERE, "qr_print.html")
with io.open(path, "w", encoding="utf-8") as fh:
    fh.write(doc)
print("A4 인쇄물:", path)

print("주소     :", URL)
print("QR 격자  : %d x %d" % qr.symbol_size(scale=1, border=0))
print("낱장 PNG :", png_path)
print()
