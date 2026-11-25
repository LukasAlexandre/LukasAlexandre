const {chromium}=require('playwright');
const fs=require('node:fs');
const path=require('node:path');
const output=path.resolve(process.argv[2]||'tests/visual/evidence');
(async()=>{
  const browser=await chromium.launch({headless:true});
  const results=[];
  try{
    for(const theme of ['dark','light'])for(const width of [375,1440]){
      const context=await browser.newContext({viewport:{width,height:900},colorScheme:theme,reducedMotion:'reduce'});
      const page=await context.newPage();
      await page.goto(`http://localhost:8765/preview/?theme=${theme}`,{waitUntil:'networkidle'});
      await page.waitForFunction(()=>window.previewReady);
      const assets=await page.locator('#readme img').evaluateAll(imgs=>imgs.map(img=>new URL(img.currentSrc).pathname));
      results.push({theme,width,assets,passed:assets.length>0&&assets.every(src=>src.includes(`/generated/${theme}/`)&&src.endsWith('-static.svg'))&&assets.some(src=>src.endsWith(width<600?'/hero-mobile-static.svg':'/hero-static.svg'))});
      await context.close();
    }
  }finally{await browser.close();}
  fs.mkdirSync(output,{recursive:true});
  fs.writeFileSync(path.join(output,'reduced-selection.json'),JSON.stringify(results,null,2)+'\n');
  console.log(JSON.stringify(results.map(({theme,width,assets,passed})=>({theme,width,images:assets.length,passed})),null,2));
  if(results.some(result=>!result.passed))process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
