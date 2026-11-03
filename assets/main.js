(function(){var b=document.getElementById('mb'),n=document.getElementById('nav');
b.addEventListener('click',function(){var o=n.classList.toggle('o');b.setAttribute('aria-expanded',o)});
n.addEventListener('click',function(e){if(e.target.tagName=='A'){n.classList.remove('o');b.setAttribute('aria-expanded',false)}});
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){
document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x==c)});
var f=c.dataset.f;document.querySelectorAll('.pc').forEach(function(p){p.hidden=!(f=='all'||p.dataset.s==f)})})});
var l=document.querySelector('.lang');if(l)l.addEventListener('click',function(){l.href=l.getAttribute('href').split('#')[0]+location.hash});
var s=document.querySelector('.slider');if(s){var sl=s.querySelectorAll('.sl'),k=0,t,cnt=s.querySelector('.cnt'),cap=s.querySelector('.cap');
function go(j){sl[k].classList.remove('on');k=(j+sl.length)%sl.length;sl[k].classList.add('on');cnt.textContent=(k+1)+' / '+sl.length;cap.textContent=sl[k].dataset.n}
function play(){stop();if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(k+1)},3500)}
function stop(){clearInterval(t)}
s.querySelector('.pv').onclick=function(){go(k-1)};s.querySelector('.nx').onclick=function(){go(k+1)};
s.addEventListener('mouseenter',stop);s.addEventListener('mouseleave',play);s.addEventListener('focusin',stop);s.addEventListener('focusout',play);play()}
var f=document.getElementById('cf');if(f)f.addEventListener('submit',function(e){e.preventDefault();var s=f.querySelector('.fs'),b=f.querySelector('button'),d=new FormData(f);
if(d.get('_honey'))return;b.disabled=true;
fetch('https://formsubmit.co/ajax/info@moxyrapharma.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({name:d.get('n'),company:d.get('c'),email:d.get('e'),type:d.get('t'),message:d.get('m'),_subject:'Moxyra website enquiry',_replyto:d.get('e')})})
.then(function(r){return r.json()}).then(function(j){if(j.success===true||j.success==='true'){s.textContent=f.dataset.ok;f.reset()}else throw 0}).catch(function(){s.textContent=f.dataset.err}).finally(function(){b.disabled=false})})})();
