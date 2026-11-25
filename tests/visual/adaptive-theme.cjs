const {chromium}=require('playwright');
const {PNG}=require('pngjs');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const output=path.resolve(process.argv[2]||'tests/visual/evidence');
(async()=>{const browser=await chromium.launch();const results=[];try{
 for(const theme of ['dark','light'])for(const mobile of [false,true])for(const name of ['hero','activity','project-ethan']){
  const p=await browser.newPage({viewport:{width:1000,height:1000},colorScheme:theme==='dark'?'light':'dark',reducedMotion:'reduce'});
  await p.goto('http://localhost:8765/preview/');
  const stem=name+(mobile?'-mobile':'')+'-static';const ext=name==='project-ethan'?'png':'svg';
  const width=name==='project-ethan'?(mobile?174:352):(mobile?360:720);
  await p.setContent(`<html style="color-scheme:${theme}"><body style="margin:0"><img width="${width}" src="http://localhost:8765/generated/adaptive/${stem}.svg"></body></html>`);
  await p.locator('img').evaluate(i=>i.decode());const a=PNG.sync.read(await p.locator('img').screenshot());
  await p.locator('img').evaluate((i,url)=>{i.src=url;return i.decode()},`http://localhost:8765/generated/${theme}/${stem}.${ext}`);
  const z=PNG.sync.read(await p.locator('img').screenshot());assert.equal(a.data.length,z.data.length);
  let difference=0;for(let i=0;i<a.data.length;i++)difference+=Math.abs(a.data[i]-z.data[i]);
  const mean=difference/a.data.length;results.push({theme,mobile,name,meanAbsoluteChannelError:mean,passed:mean<.1});await p.close();
 }
}finally{await browser.close()}fs.mkdirSync(output,{recursive:true});fs.writeFileSync(path.join(output,'adaptive-theme-pixels.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results,null,2));if(results.some(r=>!r.passed))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
