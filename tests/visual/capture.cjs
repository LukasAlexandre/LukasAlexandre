/* Real Chromium evidence using the exact README SVG image assets.
 * NODE_PATH may point at the bundled node_modules; no npm install is needed.
 * Usage: node tests/visual/capture.cjs [output-directory]
 */
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = process.env.PREVIEW_URL || 'http://localhost:8765/preview/';
const output = path.resolve(process.argv[2] || 'tests/visual/evidence');
const sizes = [[1920,1080],[1440,900],[1280,720],[768,1024],[390,844],[375,812]];

(async () => {
  fs.mkdirSync(output,{recursive:true});
  const browser = await chromium.launch({headless:true});
  const report = {testedAt:new Date().toISOString(),base,platform:'Local Chromium; GitHub remote platform not tested',results:[],animation:[],reducedMotion:[],failures:[]};
  try {
    for (const theme of ['dark','light']) for (const [width,height] of sizes) {
      const context = await browser.newContext({viewport:{width,height},colorScheme:theme,deviceScaleFactor:1});
      const page = await context.newPage();
      const errors=[];
      page.on('pageerror',error => errors.push(error.message));
      page.on('response',response => { if(response.status()>=400) errors.push(`${response.status()} ${response.url()}`); });
      await page.goto(`${base}?theme=${theme}`,{waitUntil:'networkidle'});
      await page.waitForFunction(() => window.previewReady || window.previewError);
      assert.equal(await page.evaluate(() => window.previewError || null),null);
      await page.locator('#readme img').evaluateAll(async imgs => { await Promise.all(imgs.map(img=>img.decode())); });
      await page.waitForTimeout(7000);
      await page.locator('#readme img[src*="/activity.svg"]').scrollIntoViewIfNeeded();
      await page.waitForTimeout(2600);
      // Chromium can throttle SVG animation while an <img> is offscreen.
      // Visit the whole README before the full-page screenshot.
      await page.evaluate(async () => {
        for (let y=0;y<document.documentElement.scrollHeight;y+=innerHeight*.75) {
          scrollTo(0,y); await new Promise(resolve=>setTimeout(resolve,120));
        }
      });
      await page.waitForTimeout(3200);
      await page.evaluate(() => scrollTo(0,0));
      const layout = await page.evaluate(() => {
        const article=document.querySelector('#readme'), box=article.getBoundingClientRect();
        return {
          pageWidth:document.documentElement.scrollWidth,viewport:innerWidth,
          articleWidth:box.width,articleScrollWidth:article.scrollWidth,
          images:[...article.querySelectorAll('img')].map(img=>({src:new URL(img.currentSrc).pathname,alt:img.alt,left:img.getBoundingClientRect().left,top:img.getBoundingClientRect().top,width:img.getBoundingClientRect().width,height:img.getBoundingClientRect().height,naturalWidth:img.naturalWidth,complete:img.complete})),
          theme:document.documentElement.dataset.colorMode,
          transferredBytes:performance.getEntriesByType('resource').reduce((sum,item)=>sum+item.transferSize,0),
          domContentLoadedMs:performance.getEntriesByType('navigation')[0].domContentLoadedEventEnd,
        };
      });
      const filename=`${theme}-${width}x${height}.png`;
      await page.screenshot({path:path.join(output,filename),fullPage:true,animations:'allow'});
      if(layout.pageWidth>width) report.failures.push(`${theme}/${width}: page overflow ${layout.pageWidth}`);
      if(layout.articleScrollWidth>Math.ceil(layout.articleWidth)+1) report.failures.push(`${theme}/${width}: README overflow`);
      if(layout.images.some(img=>!img.complete || !img.naturalWidth || !img.alt)) report.failures.push(`${theme}/${width}: broken or inaccessible image`);
      if(layout.images.some(img=>!img.src.includes(`/generated/${theme}/`))) report.failures.push(`${theme}/${width}: mismatched asset theme`);
      const projects=layout.images.filter(img=>img.src.includes('/project-'));
      if(projects.length!==5 || Math.abs(projects[0].top-projects[1].top)>1 || projects.slice(2).some(img=>Math.abs(img.top-projects[2].top)>1) || projects[0].width<projects[2].width*1.45) report.failures.push(`${theme}/${width}: Bento row structure or featured emphasis mismatch`);
      if(errors.length) report.failures.push(...errors);
      report.results.push({theme,width,height,filename,...layout,errors});
      await context.close();
    }
    // Direct SVG documents give access to the internal animation tree. Each SVG
    // is separately decoded as <img> above; this check verifies its motion rules.
    const context=await browser.newContext({viewport:{width:1000,height:900}});
    const page=await context.newPage();
    const files=fs.readdirSync(path.resolve('generated/dark')).filter(file=>file.endsWith('.svg'));
    for(const file of files){
      const url=new URL(`/generated/dark/${file}`,base).href;
      await page.emulateMedia({reducedMotion:'no-preference'});
      await page.goto(url,{waitUntil:'load'});
      const normal=await page.evaluate(()=>({xmlError:!!document.querySelector('parsererror'),animations:document.getAnimations().length,smil:document.querySelectorAll('animate,animateTransform,animateMotion').length,title:document.querySelector('title')?.textContent,desc:document.querySelector('desc')?.textContent}));
      report.animation.push({file,...normal});
      if(normal.xmlError||!normal.title||!normal.desc) report.failures.push(`${file}: XML/title/desc failure`);
      await page.emulateMedia({reducedMotion:'reduce'});
      await page.reload({waitUntil:'load'});
      const reduced=await page.evaluate(()=>({animations:document.getAnimations().length,hiddenText:[...document.querySelectorAll('text')].filter(el=>getComputedStyle(el).opacity==='0'||getComputedStyle(el).visibility==='hidden').length}));
      report.reducedMotion.push({file,...reduced});
      if(reduced.animations!==0||reduced.hiddenText!==0) report.failures.push(`${file}: reduced-motion content hidden or active animation`);
    }
    await context.close();
    fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({screenshots:report.results.length,svgAnimationChecks:report.animation.length,failures:report.failures,report:path.join(output,'report.json')},null,2));
    if(report.failures.length) process.exitCode=1;
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1});
