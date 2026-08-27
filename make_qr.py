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

import segno

URL = "https://rayul0325.github.io/b02/"
HERE = os.path.dirname(os.path.abspath(__file__))

qr = segno.make(URL, error="h")

# 1) 낱장 PNG — 다른 인쇄물에 끼워 넣을 때
png_path = os.path.join(HERE, "qr_b02.png")
qr.save(png_path, scale=24, border=4, dark="#0B2E4A", light="#FFFFFF")

# 2) A4 인쇄물 — 브라우저에서 열어 그대로 인쇄한다
# segno 는 바이트로 쓴다. StringIO 를 주면 TypeError 가 난다(실측).
buf = io.BytesIO()
qr.save(buf, kind="svg", scale=10, border=0,
        dark="#0B2E4A", light=None, svgclass=None, lineclass=None,
        xmldecl=False, svgns=True, omitsize=True)
svg = buf.getvalue().decode("utf-8")

html = """<!doctype html>
<meta charset="utf-8">
<title>부스 B02 · QR 인쇄물</title>
<style>
  @page { size: A4 portrait; margin: 0; }
  *{ box-sizing:border-box; margin:0; padding:0 }
  body{
    font:16px/1.6 -apple-system,BlinkMacSystemFont,"Pretendard",
         "Apple SD Gothic Neo","Malgun Gothic",sans-serif;
    -webkit-font-smoothing:antialiased;
    background:#E8EDF1;
  }
  .sheet{
    width:210mm; height:297mm; margin:0 auto; background:#fff;
    display:flex; flex-direction:column; align-items:center;
    padding:16mm 16mm 16mm; text-align:center;
    background:linear-gradient(180deg,#FFFFFF 62%,#F4FAFD 100%);
  }
  .badge{
    display:inline-block; padding:5mm 11mm; border-radius:999px;
    background:#0B2E4A; color:#fff;
    font-size:20pt; font-weight:800; letter-spacing:.06em;
  }
  h1{ margin:7mm 0 0; font-size:46pt; font-weight:800; letter-spacing:-.03em;
      color:#0B2E4A; line-height:1.05 }
  .sub{ margin:4mm 0 0; font-size:17pt; font-weight:600; color:#3E6C8C }
  .qrbox{
    margin:7mm 0 0; padding:6mm; background:#fff; border:1.2mm solid #0B2E4A;
    border-radius:6mm;
  }
  .qrbox svg{ display:block; width:74mm; height:74mm }
  .cta{ margin:6mm 0 0; font-size:23pt; font-weight:800; color:#C2410C }
  .cta small{ display:block; margin-top:2mm; font-size:14pt; font-weight:600; color:#7A5A2A }
  .rule{ width:60mm; height:.6mm; background:#CBD8E2; margin:6mm 0 }
  .team{ font-size:22pt; font-weight:800; color:#0B2E4A }
  .subject{ margin-top:3mm; font-size:14pt; font-weight:600; color:#4E6C82; line-height:1.5 }
  .foot{ margin-top:auto; padding-top:6mm; font-size:10.5pt; color:#8B95A1 }
  @media print{ body{background:#fff} .sheet{margin:0} }
</style>
<div class="sheet">
  <div class="badge">부스 B02</div>
  <h1>해파리<br>피하기</h1>
  <p class="sub">수온이 오를수록 해파리가 늘어납니다</p>

  <div class="qrbox">__SVG__</div>

  <p class="cta">폰 카메라로 찍으세요
    <small>30초 버틸 수 있나요? · 설치 없이 바로 열립니다</small></p>

  <div class="rule"></div>
  <div class="team">젤리피쉬</div>
  <p class="subject">해양열파로 동해안 해파리<br>대량 발생 위험을 예측</p>

  <p class="foot">제9회 Ocean ICT Festival · 김민아 · 강태영 · 장도건 · 황은성</p>
</div>
""".replace("__SVG__", svg)

html_path = os.path.join(HERE, "qr_print.html")
with io.open(html_path, "w", encoding="utf-8") as fh:
    fh.write(html)

print("주소     :", URL)
print("QR 격자  :", "%d x %d" % qr.symbol_size(scale=1, border=0))
print("낱장 PNG :", png_path)
print("A4 인쇄물:", html_path)
