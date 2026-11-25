const {chromium}=require('playwright');
const {PNG}=require('pngjs');
const fs=require('fs'),path=require('path');
const output=path.resolve(process.argv[2]||'tests/visual/evidence');
(async()=>{
 const b=await chromium.launch({headless:true});const results=[];
 for(const theme of ['dark','light'])for(const width of [375,1440]){
  const p=await b.newPage({viewport:{width,height:900},colorScheme:theme});
  await p.goto(`http://localhost:8765/preview/?theme=${theme}`,{waitUntil:'networkidle'});
  await p.waitForFunction(()=>window.previewReady);
  const selector='#readme img[src$="/project-ethan.gif"]';
  const primary=await p.locator(selector).evaluate(img=>({src:img.currentSrc,width:img.naturalWidth,height:img.naturalHeight}));
  await p.locator(selector).evaluate(async img=>{img.parentElement.querySelectorAll('source[type="image/webp"]').forEach(s=>s.remove());await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));await img.decode()});
  const fallback=await p.locator(selector).evaluate(img=>({src:img.currentSrc,complete:img.complete,width:img.naturalWidth,height:img.naturalHeight}));
  results.push({theme,width,primary,fallback,passed:primary.src.endsWith('.webp')&&fallback.src.endsWith('.gif')&&fallback.complete&&primary.width===fallback.width&&primary.height===fallback.height});
  await p.close();
 }
 await b.close();fs.mkdirSync(output,{recursive:true});fs.writeFileSync(path.join(output,'media-fallback.json'),JSON.stringify(results,null,2));
 console.log(JSON.stringify(results.map(r=>({theme:r.theme,width:r.width,passed:r.passed})),null,2));if(results.some(r=>!r.passed))process.exitCode=1;
})();
