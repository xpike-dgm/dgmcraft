// DgmCraft kart -> kategori akisi + admin toggle + direkt komut sonuclari
const THEMES = [
  {a:'#1B2A33',b:'#0B0F0E',l:'rgba(148,184,205,.20)',dot:'#2FD35C'},
  {a:'#23301F',b:'#0B0F0E',l:'rgba(150,200,150,.18)',dot:'#34D399'},
  {a:'#2E2438',b:'#0B0F0E',l:'rgba(190,170,220,.18)',dot:'#C4B5FD'},
  {a:'#3A2A18',b:'#0B0F0E',l:'rgba(53,217,89,.22)',dot:'#2FD35C'},
  {a:'#1E3030',b:'#0B0F0E',l:'rgba(140,220,210,.18)',dot:'#2DD4BF'},
  {a:'#33202A',b:'#0B0F0E',l:'rgba(220,160,180,.16)',dot:'#FB7185'},
  {a:'#26334A',b:'#0B0F0E',l:'rgba(150,180,230,.20)',dot:'#93C5FD'},
  {a:'#2A2F1C',b:'#0B0F0E',l:'rgba(210,220,140,.16)',dot:'#A3E635'}
];
// OP / admin izni gerektiren kategoriler (kilavuz kullanim kuralina gore)
const ADMIN_IDS = [17,19,20,21,22,23,24,25,26,27,28];
const isAdminCat = id => ADMIN_IDS.includes(id);
// Kılavuz ASCII yazıldığı için arayüzde düzgün Türkçe gösterilen başlıklar
const TITLE_TR = {1:'DGM Craft Türkçe Kısayollar (Skript)', 28:'Admin ve Sunucu İşlemleri'};
const dispTitle = c => TITLE_TR[c.id] || c.title;
const shortCat = c => dispTitle(c).replace(/^DGM Craft /,'').replace(/\s*\(Skript\)$/,'');
const adminOn = () => localStorage.getItem('dgm_admin') === '1';
function setAdmin(v){ localStorage.setItem('dgm_admin', v ? '1' : '0'); }
function thumbSVG(t,i){
  const id='g'+i;
  return `<svg preserveAspectRatio="xMidYMid slice" viewBox="0 0 400 168">
  <defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="${t.a}"/><stop offset="1" stop-color="${t.b}"/></linearGradient></defs>
  <rect width="400" height="168" fill="url(#${id})"/>
  <g stroke="${t.l}" stroke-width="1">
  <path d="M-20 130 L120 60 L260 110 L420 40"/><path d="M-20 150 L120 80 L260 130 L420 60"/>
  <path d="M40 0 L40 168 M120 0 L120 168 M200 0 L200 168 M280 0 L280 168 M360 0 L360 168" opacity=".35"/>
  <rect x="52" y="52" width="26" height="26" fill="none"/><rect x="212" y="34" width="18" height="18" fill="none"/>
  <rect x="300" y="80" width="34" height="34" fill="none" opacity=".7"/></g>
  <circle cx="330" cy="36" r="5" fill="${t.dot}"/><circle cx="70" cy="120" r="3" fill="${t.dot}" opacity=".7"/>
  </svg>`;
}
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function getParam(n){return new URLSearchParams(location.search).get(n)}
// file:// + eski tarayici uyumlu kopyalama (clipboard API yoksa fallback)
function copyText(t, ok){
  const done = () => ok && ok();
  if(navigator.clipboard && window.isSecureContext !== false && navigator.clipboard.writeText){
    navigator.clipboard.writeText(t).then(done).catch(() => legacyCopy(t, done));
  } else legacyCopy(t, done);
}
function legacyCopy(t, done){
  var ok = false;
  try{
    const ta = document.createElement('textarea');
    ta.value = t; ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
    document.body.appendChild(ta); ta.select();
    try{ ta.setSelectionRange(0, ta.value.length); }catch(e){}
    ok = document.execCommand('copy');
    document.body.removeChild(ta);
  }catch(e){ ok = false; }
  if(!ok) copyManuel(t);
  done(!ok);
}
function copyManuel(t){
  var old = document.getElementById('copy-manuel');
  if(old) old.remove();
  var d = document.createElement('div');
  d.id = 'copy-manuel';
  d.style.cssText = 'position:fixed;left:50%;bottom:22px;transform:translateX(-50%);z-index:200;max-width:92vw;' +
    'background:#231309;border:1px solid #5a2b1a;color:#E8B4A0;border-radius:12px;padding:12px 16px;font-size:14px';
  d.innerHTML = 'Kopyalanamadı, seçili metni Ctrl+C ile al: <b></b>';
  d.querySelector('b').textContent = t;
  document.body.appendChild(d);
  var r = document.createRange(); r.selectNodeContents(d.querySelector('b'));
  var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  setTimeout(function(){ if(d.parentNode) d.parentNode.removeChild(d); }, 8000);
  d.onclick = function(){ if(d.parentNode) d.parentNode.removeChild(d); };
}
function trFold(s){
  return String(s||'')
    .replace(/İ/g,'i').replace(/I/g,'ı')
    .toLocaleLowerCase('tr')
    .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
    .replace(/ı/g,'i');
}
function norm(s){return trFold(s).trim().replace(/^\/+/, '').replace(/\s+/g,' ')}
function cmdText(k){return norm(k.k+' '+k.n+' '+k.o+' '+k.r+' '+k.d)}
function visibleCats(){ return window.DGM_DATA.filter(c => adminOn() || !isAdminCat(c.id)); }

// Toggle her iki sayfada da calisir
(function(){
  const t = document.getElementById('adminToggle');
  if(!t) return;
  t.checked = adminOn();
  t.addEventListener('change', () => { setAdmin(t.checked); location.reload(); });
})();

// ANA SAYFA
if(document.getElementById('grid')){
  const grid=document.getElementById('grid'), q=document.getElementById('q'),
        count=document.getElementById('count'), navCount=document.getElementById('navCount'),
        dWrap=document.getElementById('directWrap'), direct=document.getElementById('direct');
  const totalAll = window.DGM_DATA.reduce((a,c)=>a+c.cmds.length,0);
  const visCats = visibleCats();
  const totalVis = visCats.reduce((a,c)=>a+c.cmds.length,0);
  if(navCount) navCount.textContent = visCats.length+' kategori • '+totalVis+' komut'+(adminOn()?' • admin açık':'');
  function render(f=''){
    const F=norm(f);
    grid.innerHTML=''; direct.innerHTML='';
    let shown=0; const allHits=[];
    window.DGM_DATA.forEach((c,idx)=>{
      if(!adminOn() && isAdminCat(c.id)) return; // admin kapaliysa gizle
      const titleN=norm(c.title);
      let matches=[];
      if(F){
        const titleHit=titleN.includes(F);
        matches=c.cmds.filter(k=>cmdText(k).includes(F));
        matches.forEach(k=>allHits.push({cat:c,cmd:k}));
        if(!titleHit && matches.length===0) return;
      }
      shown++;
      const t=THEMES[idx%THEMES.length];
      const el=document.createElement('a');
      el.className='card';
      el.href='kategori.html?id='+c.id+(F?'&q='+encodeURIComponent(f.trim()):'');
      let sub='Komutları gör';
      if(F && matches.length>0) sub=matches.length+' eşleşme: '+matches.slice(0,3).map(m=>m.k).join(', ')+(matches.length>3?'…':'');
      else if(F) sub='Başlık eşleşti • Komutları gör';
      const adminBadge = isAdminCat(c.id) ? '<span class="badge-admin">ADMIN</span>' : '';
      el.innerHTML=`<div class="thumb">${thumbSVG(t,idx)}<span class="tag">${c.cmds.length} komut</span></div>
      <div class="card-body"><div><h3>${esc(dispTitle(c))}${adminBadge}</h3><small>${esc(sub)}</small></div><span class="arrow">→</span></div>`;
      grid.appendChild(el);
    });
    // Direkt komut sonuclari (en fazla 12)
    if(F && allHits.length){
      dWrap.style.display='block';
      allHits.slice(0,12).forEach(h=>{
        const a=document.createElement('a');
        a.className='direct-item';
        a.href='kategori.html?id='+h.cat.id+'&q='+encodeURIComponent(h.cmd.k);
        a.innerHTML=`<div class="di-main"><div class="di-top"><code>${esc(h.cmd.k)}</code><span class="di-cat">${esc(shortCat(h.cat))}</span></div><p class="di-desc">${esc(h.cmd.n||'')}</p></div><span class="go">Git →</span>`;
        direct.appendChild(a);
      });
      if(allHits.length>12){
        const more=document.createElement('div');
        more.className='empty'; more.textContent='+'+(allHits.length-12)+' komut daha var, aramanı daralt veya karta tıkla.';
        direct.appendChild(more);
      }
    } else dWrap.style.display='none';
    const base = adminOn() ? totalAll : totalVis;
    count.textContent = F ? (shown+' kategori • '+allHits.length+' direkt komut eşleşmesi') : (shown+' kategori • '+base+' komut'+(adminOn()?' (admin dahil)':' (admin gizli — sağdan açabilirsin)'));
    if(!shown && !(F&&allHits.length)) grid.innerHTML='<div class="empty">Sonuç yok. Admin kapalıysa sağdan açmayı dene.</div>';
  }
  q.addEventListener('input',e=>render(e.target.value));
  render();
}

// KATEGORI SAYFASI
if(document.getElementById('cmdlist')){
  const id=parseInt(getParam('id')||'1',10);
  const c=window.DGM_DATA.find(x=>x.id===id)||window.DGM_DATA[0];
  const adminNote=document.getElementById('adminNote');
  if(isAdminCat(c.id) && !adminOn() && adminNote){
    adminNote.style.display='flex';
    document.getElementById('adminEnable').onclick=()=>{setAdmin(true);location.reload();};
  }
  document.getElementById('ctitle').innerHTML=esc(dispTitle(c))+(isAdminCat(c.id)?' <span class="badge-admin">ADMIN</span>':'');
  document.getElementById('cdesc').textContent=(c.desc||'Bu kategorinin komutları.')+' • '+c.cmds.length+' komut';
  document.title=dispTitle(c)+' • DgmCraft';
  const list=document.getElementById('cmdlist'), q=document.getElementById('cq');
  function render(f=''){
    const F=norm(f);
    list.innerHTML='';
    let n=0;
    c.cmds.forEach(k=>{
      if(F && !(cmdText(k).includes(F))) return;
      n++;
      const d=document.createElement('div'); d.className='cmd';
      d.innerHTML=`<div class="cmd-top"><code>${esc(k.k)}</code><button class="copy">Kopyala</button></div>
      ${k.n?`<p>${esc(k.n)}</p>`:''}
      <div class="meta">
      ${k.o?`<div><b>Örnek:</b> <code>${esc(k.o)}</code></div>`:''}
      ${k.r?`<div><b>Orijinal:</b> <code>${esc(k.r)}</code></div>`:''}
      ${k.d?`<div class="warn"><b>Dikkat:</b> ${esc(k.d)}</div>`:''}
      </div>`;
      d.querySelector('.copy').onclick=(e)=>{const b=e.target;copyText(k.k,(manuel)=>{if(!manuel){b.textContent='Kopyalandı!';setTimeout(()=>b.textContent='Kopyala',1200);}});};
      list.appendChild(d);
    });
    if(!n) list.innerHTML='<div class="empty">Bu kategoride sonuç yok.</div>';
  }
  q.addEventListener('input',e=>render(e.target.value));
  const preQ=getParam('q');
  if(preQ){q.value=preQ;render(preQ);}else{render();}
}
