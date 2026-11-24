(function(){var b=document.getElementById('mb'),n=document.getElementById('nav');
b.addEventListener('click',function(){var o=n.classList.toggle('o');b.setAttribute('aria-expanded',o)});
n.addEventListener('click',function(e){if(e.target.tagName=='A'){n.classList.remove('o');b.setAttribute('aria-expanded',false)}});
var fs='all',fb='all';
function apply(){document.querySelectorAll('.chip[data-f]').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f==fs)});
document.querySelectorAll('.chip[data-b]').forEach(function(x){x.setAttribute('aria-pressed',x.dataset.b==fb)});
document.querySelectorAll('.pc').forEach(function(c){c.hidden=!(fb=='all'||c.dataset.b==fb)});
document.querySelectorAll('.pg').forEach(function(p){var any=false;p.querySelectorAll('.grid').forEach(function(g){var v=g.querySelector('.pc:not([hidden])');g.hidden=!v;if(g.previousElementSibling)g.previousElementSibling.hidden=!v;if(v)any=true});p.hidden=!(any&&(fs=='all'||p.dataset.s==fs))})}
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){if(c.dataset.b)fb=c.dataset.b;else fs=c.dataset.f;apply()})});
document.querySelectorAll('.tl[data-b]').forEach(function(a){a.addEventListener('click',function(){fb=a.dataset.b;fs='all';apply()})});
var l=document.querySelector('.lang');if(l)l.addEventListener('click',function(){l.href=l.getAttribute('href').split('#')[0]+location.hash});
var s=document.querySelector('.slider');if(s){var hs=function(d){return d=='conditioner'?'conditioner-hero':d},ids=s.dataset.ids.split(','),nm=s.dataset.names.split('|'),fg=s.querySelectorAll('figure'),k=0,t;
window.addEventListener('load',function(){ids.forEach(function(d){new Image().src='/assets/img/'+hs(d)+'-480.webp'})});
function show(){fg.forEach(function(f,j){f.classList.add('f');setTimeout(function(){var q=(k+j)%ids.length,im=f.querySelector('img');im.src='/assets/img/'+hs(ids[q])+'-480.webp';im.alt=nm[q];f.classList.remove('f')},300)})}
function go(d){k=(k+d*3+ids.length)%ids.length;show()}
function stop(){clearInterval(t)}
function play(){stop();if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(1)},3000)}
s.querySelector('.pv').onclick=function(){go(-1)};s.querySelector('.nx').onclick=function(){go(1)};
s.addEventListener('mouseenter',stop);s.addEventListener('mouseleave',play);s.addEventListener('focusin',stop);s.addEventListener('focusout',play);play()}
var lb=document.getElementById('lb');if(lb){document.querySelectorAll('.zi').forEach(function(z){z.addEventListener('click',function(){var im=lb.querySelector('img');im.src=z.dataset.full;im.alt=z.dataset.alt;lb.showModal()})});
lb.addEventListener('click',function(e){if(e.target===lb||e.target.className=='x')lb.close()})}
})();
(function(){var ls=[].slice.call(document.querySelectorAll('#nav a[href^="#"]')),m={};ls.forEach(function(a){m[a.getAttribute('href').slice(1)]=a});
if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ls.forEach(function(a){a.removeAttribute('aria-current')});var a=m[e.target.id];if(a)a.setAttribute('aria-current','true')}})},{rootMargin:'-45% 0px -50% 0px'});
Object.keys(m).forEach(function(k){var s=document.getElementById(k);if(s)o.observe(s)})})();
