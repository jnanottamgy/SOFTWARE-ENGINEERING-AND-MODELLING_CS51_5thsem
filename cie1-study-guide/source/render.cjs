// Usage: node render.cjs <input.html> <output.pdf> [--cover]
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');

(async () => {
  const [input, output, ...rest] = process.argv.slice(2);
  const cover = rest.includes('--cover');
  const labelArg = rest.find(a => a.startsWith('--label='));
  const label = labelArg ? labelArg.slice(8) : 'CIE-1 Study Guide';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  const footer = `
    <div style="width:100%; padding:0 15mm; font-family:Carlito, 'DejaVu Sans', sans-serif; font-size:8pt; color:#8a93a6;
                display:flex; justify-content:space-between; align-items:center;">
      <span>Software Engineering &amp; Modelling (CS51) &nbsp;·&nbsp; ${label}</span>
      <span style="font-weight:600; color:#4b5468;"><span class="pageNumber"></span></span>
    </div>`;
  await page.pdf({
    path: output,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: false,
    margin: cover ? { top: '0', bottom: '0', left: '0', right: '0' }
                  : { top: '14mm', bottom: '16mm', left: '15mm', right: '15mm' },
    displayHeaderFooter: !cover,
    headerTemplate: '<span></span>',
    footerTemplate: cover ? '<span></span>' : footer,
    outline: !cover,
    tagged: true,
  });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
