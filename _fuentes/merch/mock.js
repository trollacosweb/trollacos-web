const { chromium } = require('playwright');const fs=require('fs');
const M='file:///home/claude/merch/';
const camiseta=(col,diseno,etq)=>`<svg viewBox="0 0 1000 1100" width="1000" height="1100" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".25"/><stop offset=".25" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient></defs>
<path d="M330 80 Q500 150 670 80 L900 190 L840 400 L760 370 L760 1040 Q500 1070 240 1040 L240 370 L160 400 L100 190Z" fill="${col}"/>
<path d="M330 80 Q500 150 670 80 L900 190 L840 400 L760 370 L760 1040 Q500 1070 240 1040 L240 370 L160 400 L100 190Z" fill="url(#s)"/>
<path d="M375 92 Q500 170 625 92" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="16"/>
<path d="M240 370 L240 560 M760 370 L760 560" stroke="#000" stroke-opacity=".15" stroke-width="6"/>
<image href="${M}${diseno}.png" x="305" y="230" width="390" height="468"/>
</svg>`;
const sudadera=(col,diseno)=>`<svg viewBox="0 0 1000 1100" width="1000" height="1100" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="s" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".3"/><stop offset=".25" stop-color="#000" stop-opacity="0"/><stop offset=".75" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient></defs>
<path d="M300 140 Q500 20 700 140 L860 230 L960 900 L860 930 L790 520 L780 1000 Q500 1040 220 1000 L210 520 L140 930 L40 900 L140 230Z" fill="${col}"/>
<path d="M300 140 Q500 20 700 140 L860 230 L960 900 L860 930 L790 520 L780 1000 Q500 1040 220 1000 L210 520 L140 930 L40 900 L140 230Z" fill="url(#s)"/>
<path d="M330 150 Q500 300 670 150 Q640 60 500 50 Q360 60 330 150Z" fill="#000" fill-opacity=".35"/>
<path d="M470 200 v150 M530 200 v150" stroke="#ddd" stroke-width="6"/><circle cx="470" cy="356" r="8" fill="#ddd"/><circle cx="530" cy="356" r="8" fill="#ddd"/>
<path d="M320 820 L680 820 L700 960 L300 960Z" fill="#000" fill-opacity=".18"/>
<rect x="220" y="975" width="560" height="35" fill="#000" fill-opacity=".25"/>
<image href="${M}${diseno}.png" x="330" y="400" width="340" height="408"/>
</svg>`;
const items=[['m1',camiseta('#141418','1-trollacos-clasico'),'CAMISETA · TROLLACOS CLÁSICO'],['m2',sudadera('#1a1f1c','2-expediente-trollaco'),'SUDADERA · EXPEDIENTE TROLLACO'],['m3',camiseta('#1b1012','3-trolloween'),'CAMISETA · TROLLOWEEN (EDICIÓN LIMITADA)']];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:3150,height:1260}});
const html=`<!doctype html><html><head><meta charset="utf-8"><style>@font-face{font-family:V;src:url(file:///home/claude/trollacos-web/fuentes/vt323.woff2)}
body{margin:0;background:linear-gradient(180deg,#e9e6f2,#cfcbe0);display:flex;gap:50px;padding:40px;font-family:V}
.c{background:#f4f2fa;border-radius:24px;padding:20px;box-shadow:0 10px 30px rgba(0,0,0,.15)}.c p{text-align:center;font-size:44px;margin:0;color:#2a1f50}</style></head><body>
${items.map(i=>`<div class="c">${i[1]}<p>${i[2]}</p></div>`).join('')}</body></html>`;
fs.writeFileSync('mock.html',html);await p.goto('file://'+__dirname+'/mock.html');await p.waitForTimeout(800);
await p.screenshot({path:'/tmp/claude-0/-home-claude/074a85cb-bf8f-5cf1-801a-ef5ae6c1a692/scratchpad/mockups.png'});await b.close();})();
