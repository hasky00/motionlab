const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
function studio(reduced=false){
 const nodes={}; for(const id of ['preview','play','restart','speed','timeline','status']) nodes[id]={disabled:true,value:id==='speed'?'1':'0',events:{},addEventListener(k,f){this.events[k]=f},setAttribute(){}};
 let draws=0, next, sheet;
 nodes.preview.getContext=()=>({drawImage(){draws++}});
 const doc={hidden:false,querySelector:s=>nodes[s.slice(1)],addEventListener(){}};
 vm.runInNewContext(fs.readFileSync('web/app.js','utf8'),{document:doc,matchMedia:()=>({matches:reduced,addEventListener(){}}),Image:class{constructor(){sheet=this}},requestAnimationFrame:f=>next=f});
 sheet.onload();
 return {nodes,tick:n=>next(n),draws:()=>draws};
}
test('autoplay, pause, play, speed, seek and restart',()=>{
 const s=studio(); const n=s.nodes;
 assert.equal(n.play.textContent,'Pause'); assert.equal(n.play.disabled,false);
 s.tick(0);s.tick(60);assert.equal(n.timeline.value,1);
 n.play.events.click();s.tick(120);s.tick(180);assert.equal(n.timeline.value,1);
 n.play.events.click();n.speed.value='2';s.tick(200);s.tick(260);assert.equal(n.timeline.value,3);
 n.timeline.value='20';n.timeline.events.input();assert.equal(n.play.textContent,'Play');
 n.restart.events.click();assert.equal(n.timeline.value,0);
 assert(s.draws()>3);
});
test('reduced motion starts paused',()=>assert.equal(studio(true).nodes.play.textContent,'Play'));
