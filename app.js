const form=document.getElementById('uploadForm'), input=document.getElementById('project');
const filename=document.getElementById('filename'), errorBox=document.getElementById('error');
const results=document.getElementById('results'), rows=document.getElementById('rows'), details=document.getElementById('details');
let latest=null;
input.addEventListener('change',()=>filename.textContent=input.files[0]?.name||'Python repository packaged as .zip');
form.addEventListener('submit',async e=>{
 e.preventDefault(); errorBox.classList.add('hidden'); results.classList.add('hidden');
 const btn=document.getElementById('submitBtn'); btn.disabled=true; btn.textContent='Analyzing…';
 try{
  const data=new FormData(form); const response=await fetch('/api/analyze',{method:'POST',body:data});
  const payload=await response.json(); if(!response.ok) throw new Error(payload.error||'Analysis failed');
  latest=payload; render(payload);
 }catch(err){errorBox.textContent=err.message;errorBox.classList.remove('hidden')}
 finally{btn.disabled=false;btn.textContent='Analyze repository →'}
});
function render(data){
 const s=data.summary;
 document.getElementById('files').textContent=s.files_scanned;
 document.getElementById('avg').textContent=s.average_risk+'/100';
 document.getElementById('high').textContent=s.high_risk;
 document.getElementById('lines').textContent=s.total_lines.toLocaleString();
 rows.innerHTML=''; details.innerHTML='';
 data.files.forEach((f,i)=>{
  const tr=document.createElement('tr');
  tr.innerHTML=`<td>${escapeHtml(f.path)}</td><td>${f.risk}</td><td>${f.complexity}</td><td>${f.lines}</td><td><span class="severity ${f.severity}">${f.severity}</span></td>`;
  tr.addEventListener('click',()=>showDetail(f)); rows.appendChild(tr);
  if(i===0) showDetail(f);
 });
 document.getElementById('notice').textContent=data.notice;
 results.classList.remove('hidden');
}
function showDetail(f){
 details.innerHTML=`<h3>${escapeHtml(f.path)} <span class="severity ${f.severity}">${f.severity} risk</span></h3>
 <p>Risk score: <b>${f.risk}/100</b> · Complexity: ${f.complexity} · Functions: ${f.functions} · Classes: ${f.classes} · Duplicate lines: ${f.duplicates}</p>
 <b>Detected indicators</b><ul>${(f.smells.length?f.smells:['No major indicators detected']).map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul>
 <b>Suggested actions</b><ul>${f.recommendations.map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul>`;
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
document.getElementById('download').addEventListener('click',()=>{
 if(!latest)return; const blob=new Blob([JSON.stringify(latest,null,2)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='technical-debt-report.json';a.click();URL.revokeObjectURL(a.href);
});
