// DgmCraft canli sayfa altyapisi (ortak)
// Sozlesme: tum istekler GORELI yoldan (/api/...), sabit IP/host yok.
// file:// uyumu: fetch patlarsa snapshot + cevrimdisi gosterilir, sayfa asla kilitlenmez.
window.Canli = (function(){
  function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}

  async function req(path, opt){
    opt = opt || {};
    var timeout = opt.timeout || 8000;
    var ctrl = null, timer = null;
    try{ if(window.AbortController){ ctrl = new AbortController(); } }catch(e){ ctrl = null; }
    var p = Promise.resolve().then(function(){
      if(location.protocol === 'file:') throw new Error('file');
      var fopt = { headers: { 'Accept': 'application/json' } };
      if(ctrl){ fopt.signal = ctrl.signal; }
      if(opt.method){
        fopt.method = opt.method;
        fopt.headers['Content-Type'] = 'application/json';
        fopt.body = JSON.stringify(opt.body || {});
      }
      return fetch(path, fopt);
    }).then(function(res){
      if(!res.ok) throw new Error('http ' + res.status);
      return res.json();
    });
    if(ctrl){
      var to = new Promise(function(_, rej){
        timer = setTimeout(function(){ try{ ctrl.abort(); }catch(e){} rej(new Error('zamanasimi')); }, timeout);
      });
      try{ var d = await Promise.race([p, to]); clearTimeout(timer); return { ok: true, data: d }; }
      catch(e){ clearTimeout(timer); return { ok: false, error: String(e && e.message || e) }; }
    }
    try{ var d2 = await p; return { ok: true, data: d2 }; }
    catch(e2){ return { ok: false, error: String(e2 && e2.message || e2) }; }
  }
  function get(path, timeout){ return req(path, { timeout: timeout || 8000 }); }
  function post(path, body, timeout){ return req(path, { method: 'POST', body: body, timeout: timeout || 8000 }); }

  // --- snapshot (son bilinen veri) ---
  function snapSave(key, data){
    try{ localStorage.setItem('dgm_snap_' + key, JSON.stringify({ zaman: Date.now(), data: data })); }catch(e){}
  }
  function snapLoad(key){
    try{
      var raw = localStorage.getItem('dgm_snap_' + key);
      if(!raw) return null;
      return JSON.parse(raw);
    }catch(e){ return null; }
  }
  function snapSaat(zaman){
    try{ var d = new Date(zaman); return ('0'+d.getHours()).slice(-2) + ':' + ('0'+d.getMinutes()).slice(-2); }
    catch(e){ return ''; }
  }

  // --- durum noktasi (sag ust, tum sayfalarda ayni yer) ---
  var dotEl = null;
  function ensureDot(){
    if(dotEl) return dotEl;
    dotEl = document.createElement('div');
    dotEl.id = 'canli-dot';
    dotEl.className = 'canli-dot off';
    dotEl.innerHTML = '<i></i><span>Bağlanıyor…</span>';
    document.body.appendChild(dotEl);
    return dotEl;
  }
  // durum: 'on' | 'orta' | 'off'
  function dot(durum, yazi){
    var el = ensureDot();
    el.className = 'canli-dot ' + durum;
    el.querySelector('span').textContent = yazi;
  }

  // --- admin toggle (mevcut davranisla ayni) ---
  function initAdmin(onChange){
    var t = document.getElementById('adminToggle');
    if(!t) return;
    try{ t.checked = (localStorage.getItem('dgm_admin') === '1'); }catch(e){}
    t.addEventListener('change', function(){
      try{ localStorage.setItem('dgm_admin', t.checked ? '1' : '0'); }catch(e){}
      if(onChange) onChange(t.checked); else location.reload();
    });
  }

  // --- tarayici bildirimi (izin yoksa sessizce kapanir) ---
  var notifIzin = null;
  function notifIste(){
    try{
      if(!('Notification' in window)) return;
      if(Notification.permission === 'granted'){ notifIzin = true; }
      else if(Notification.permission !== 'denied'){
        Notification.requestPermission().then(function(p){ notifIzin = (p === 'granted'); }).catch(function(){});
      }
    }catch(e){}
  }
  function notif(baslik, govde){
    try{
      if(notifIzin && 'Notification' in window && document.hidden){
        new Notification(baslik, { body: govde });
      }
    }catch(e){}
  }

  function saatStr(ts){
    try{
      var d = (ts instanceof Date) ? ts : new Date(ts);
      if(isNaN(d.getTime())) return String(ts || '');
      return ('0'+d.getHours()).slice(-2) + ':' + ('0'+d.getMinutes()).slice(-2) + ':' + ('0'+d.getSeconds()).slice(-2);
    }catch(e){ return String(ts || ''); }
  }
  function sureStr(dk){
    dk = Math.max(0, Math.floor(Number(dk) || 0));
    if(dk < 60) return dk + ' dk';
    if(dk < 1440) return Math.floor(dk / 60) + ' sa ' + (dk % 60) + ' dk';
    return Math.floor(dk / 1440) + ' gün ' + Math.floor((dk % 1440) / 60) + ' sa';
  }

  return { esc: esc, get: get, post: post, snapSave: snapSave, snapLoad: snapLoad,
           snapSaat: snapSaat, dot: dot, initAdmin: initAdmin,
           notifIste: notifIste, notif: notif, saatStr: saatStr, sureStr: sureStr };
})();
