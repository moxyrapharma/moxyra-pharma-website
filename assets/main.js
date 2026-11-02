
(function(){var b=document.getElementById('mb'),n=document.getElementById('nav');
b.addEventListener('click',function(){var o=n.classList.toggle('o');b.setAttribute('aria-expanded',o)});
n.addEventListener('click',function(e){if(e.target.tagName=='A'){n.classList.remove('o');b.setAttribute('aria-expanded',false)}});
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){
document.querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',x==c)});
var f=c.dataset.f;document.querySelectorAll('.pc').forEach(function(p){p.hidden=!(f=='all'||p.dataset.s==f)})})});
var l=document.querySelector('.lang');if(l)l.addEventListener('click',function(){l.href=l.getAttribute('href').split('#')[0]+location.hash});
var f=document.getElementById('cf');if(f)f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f);
var body='Name: '+d.get('n')+'\nCompany: '+d.get('c')+'\nEmail: '+d.get('e')+'\nType: '+d.get('t')+'\n\n'+d.get('m');
location.href='mailto:info@moxyrapharma.com?subject='+encodeURIComponent('Partnership enquiry - '+d.get('c'))+'&body='+encodeURIComponent(body)})})();
