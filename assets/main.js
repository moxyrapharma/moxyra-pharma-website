(function(){var b=document.getElementById('mb'),n=document.getElementById('nav');
b.addEventListener('click',function(){var o=n.classList.toggle('o');b.setAttribute('aria-expanded',o)});
n.addEventListener('click',function(e){if(e.target.tagName=='A'){n.classList.remove('o');b.setAttribute('aria-expanded',false)}});
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){
document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x==c)});
var f=c.dataset.f;document.querySelectorAll('.pg').forEach(function(p){p.hidden=!(f=='all'||p.dataset.s==f)})})});
var l=document.querySelector('.lang');if(l)l.addEventListener('click',function(){l.href=l.getAttribute('href').split('#')[0]+location.hash});
var s=document.querySelector('.slider');if(s){var ids=s.dataset.ids.split(','),nm=s.dataset.names.split('|'),fg=s.querySelectorAll('figure'),k=0,t;
window.addEventListener('load',function(){ids.forEach(function(d){new Image().src='/assets/img/'+d+'-480.webp'})});
function show(){fg.forEach(function(f,j){f.classList.add('f');setTimeout(function(){var q=(k+j)%ids.length,im=f.querySelector('img');im.src='/assets/img/'+ids[q]+'-480.webp';im.alt=nm[q];f.classList.remove('f')},300)})}
function go(d){k=(k+d*3+ids.length)%ids.length;show()}
function stop(){clearInterval(t)}
function play(){stop();if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(1)},2000)}
s.querySelector('.pv').onclick=function(){go(-1)};s.querySelector('.nx').onclick=function(){go(1)};
s.addEventListener('mouseenter',stop);s.addEventListener('mouseleave',play);s.addEventListener('focusin',stop);s.addEventListener('focusout',play);play()}
var lb=document.getElementById('lb');if(lb){document.querySelectorAll('.zi').forEach(function(z){z.addEventListener('click',function(){var im=lb.querySelector('img');im.src=z.dataset.full;im.alt=z.dataset.alt;lb.showModal()})});
lb.addEventListener('click',function(e){if(e.target===lb||e.target.className=='x')lb.close()})}
var f=document.getElementById('cf');if(f)f.addEventListener('submit',function(e){e.preventDefault();var s=f.querySelector('.fs'),b=f.querySelector('button'),d=new FormData(f);
if(d.get('_honey'))return;b.disabled=true;
fetch('https://formsubmit.co/ajax/info@moxyrapharma.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({name:d.get('n'),company:d.get('c'),email:d.get('e'),type:d.get('t'),message:d.get('m'),_subject:'Moxyra website enquiry',_replyto:d.get('e')})})
.then(function(r){return r.json()}).then(function(j){if(j.success===true||j.success==='true'){s.textContent=f.dataset.ok;f.reset()}else throw 0}).catch(function(){s.textContent=f.dataset.err}).finally(function(){b.disabled=false})})})();
