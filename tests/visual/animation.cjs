const {chromium}=require('playwright');
const {PNG}=require('pngjs');
const fs=require('node:fs');
const path=require('node:path');
const output=path.resolve(process.argv[2]||'tests/visual/evidence');
function difference(a,b){
  const first=PNG.sync.read(a),second=PNG.sync.read(b);
  if(first.width!==second.width||first.height!==second.height)throw Error('Different frame sizes');
  let changed=0;
  for(let i=0;i<first.data.length;i+=4){
    if(Math.abs(first.data[i]-second.data[i])+Math.abs(first.data[i+1]-second.data[i+1])+Math.abs(first.data[i+2]-second.data[i+2])>20) changed++;
  }
  return changed;
}
(async()=>{
  fs.mkdirSync(output,{recursive:true});
  const browser=await chromium.launch({headless:true});
  const results=[];
  try{
    for(const reduced of [false,true]){
      const context=await browser.newContext({viewport:{width:900,height:900},reducedMotion:reduced?'reduce':'no-preference'});
      const page=await context.newPage();
      for(const name of ['hero','activity','project-vorcen','project-ethan']){
        await page.goto('http://localhost:8765/preview/?theme=dark',{waitUntil:'networkidle'});
        await page.waitForFunction(()=>window.previewReady);
        // Select the real README <picture>/<img>, including its reduced-motion
        // source selection. Mobile is tested separately by the capture harness.
        const extension=name==='project-ethan'?'gif':'svg';
        const markup=await page.locator(`#readme img[src$="/${name}.${extension}"]`).evaluate(img=>img.parentElement.outerHTML);
        // Isolate this exact picture so offscreen throttling and loading the
        // preceding README sections cannot consume its one-shot animation.
        await page.setContent(`<body style="margin:0;background:#0d1117">${markup}</body>`);
        const image=page.locator('img');
        // A cached SVG image can share an already-completed animation timeline
        // with its prior use. A unique query reloads identical repository bytes.
        await image.evaluate(async img=>{
          const stamp=Date.now();
          img.parentElement.querySelectorAll('source').forEach(source=>{
            const url=new URL(source.srcset,location.href);url.searchParams.set('animationEvidence',stamp);source.srcset=url.href;
          });
          const url=new URL(img.src);url.searchParams.set('animationEvidence',stamp);img.src=url.href;
          await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
          await img.decode();
        });
        const staticSelected=await image.evaluate(img=>/-static\.(svg|png)$/.test(new URL(img.currentSrc).pathname));
        await page.waitForTimeout(100);
        const first=await image.screenshot({animations:'allow'});
        await page.waitForTimeout(4000);
        const second=await image.screenshot({animations:'allow'});
        const changedPixels=difference(first,second);
        const suffix=reduced?'reduced':'motion';
        fs.writeFileSync(path.join(output,`${name}-${suffix}-early.png`),first);
        fs.writeFileSync(path.join(output,`${name}-${suffix}-late.png`),second);
        results.push({asset:name,reducedMotion:reduced,staticSelected,changedPixels,passed:reduced?changedPixels===0&&staticSelected:changedPixels>100&&!staticSelected});
      }
      await context.close();
    }
  }finally{await browser.close();}
  fs.writeFileSync(path.join(output,'animation-report.json'),JSON.stringify({context:'SVG loaded in img; screenshots 4s apart',results},null,2)+'\n');
  console.log(JSON.stringify(results,null,2));
  if(results.some(result=>!result.passed))process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
