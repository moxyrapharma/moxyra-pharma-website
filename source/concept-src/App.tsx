import React, { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { products, ingLabel, type L, type Product } from './data';
import logo from './photos/logo.png';
import bUry from './photos/brand-uryhip.webp';
import bMox from './photos/brand-moxygain.webp';
import bWel from './photos/brand-wellness.webp';

type Sec = 'available' | 'licensed' | 'supp';
const secOf = (p: Product): Sec => (p.brand === 'MOXYRA WELLNESS' ? 'supp' : p.status === 'available' ? 'available' : 'licensed');
const goTo = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });

const HERO_SETS = Math.ceil(products.length / 3);
const SITE = 'https://moxyrapharma.com';
const WA = '201099688827';

const T = {
  nav: [
    ['about', { en: 'About', ar: 'عن الشركة' }],
    ['brands', { en: 'Brands', ar: 'العلامات' }],
    ['products', { en: 'Products', ar: 'المنتجات' }],
    ['quality', { en: 'Quality', ar: 'الجودة' }],
    ['partners', { en: 'Partnerships', ar: 'الشراكات' }],
  ] as [string, L][],
  eyebrow: { en: 'Egyptian healthcare & beauty company', ar: 'شركة مصرية للرعاية الصحية والتجميل' },
  h1: { en: 'Where innovation meets healthcare.', ar: 'حيث يلتقي الابتكار بالرعاية الصحية' },
  lead: { en: 'Skin care, hair care and wellness brands made in Egypt through qualified manufacturing partners, with clear product information for pharmacies, chains and distributors.', ar: 'علامات للعناية بالبشرة والشعر والصحة العامة، صُنعت في مصر لدى شركاء تصنيع مؤهلين، مع معلومات واضحة عن كل منتج للصيدليات والسلاسل والموزعين.' },
  cta1: { en: 'Explore our portfolio', ar: 'استكشف منتجاتنا' },
  cta2: { en: 'Become a partner', ar: 'كن شريكاً' },
  tag: { en: 'Quality-focused. Partnership-driven. Future-ready.', ar: 'الجودة نهجنا، والشراكة طريقنا، والمستقبل وجهتنا.' },
  statL: {
    all: { en: 'Products in our portfolio', ar: 'منتجًا في محفظتنا' },
    available: { en: 'Commercially available', ar: 'منتجات مطروحة تجاريًا' },
    licensed: { en: 'Licensed, not yet manufactured', ar: 'مرخّصة ولم تُصنَّع بعد' },
    supp: { en: 'Dietary supplements', ar: 'مكملات غذائية' },
  } as Record<string, L>,
  secs: {
    available: { t: { en: 'Commercially available', ar: 'مطروح تجارياً' }, s: { en: 'On the market today.', ar: 'منتجات متاحة في السوق الآن.' }, badge: { en: 'Commercially available', ar: 'مطروح تجارياً' } },
    licensed: { t: { en: 'Licensed, not yet manufactured', ar: 'مرخّص ولم يُصنَّع بعد' }, s: { en: 'Approved products that are not yet in production.', ar: 'منتجات مرخّصة لم يبدأ تصنيعها بعد.' }, badge: { en: 'Licensed, not yet manufactured', ar: 'مرخّص ولم يُصنَّع بعد' } },
    supp: { t: { en: 'Dietary supplements', ar: 'المكملات الغذائية' }, s: { en: 'Dietary Supplements for a Healthy Life. Each product shows its own status.', ar: 'مكملات غذائية للحياة الصحية. لكل منتج حالته الظاهرة عليه.' }, badge: { en: 'Licensed / approved', ar: 'مرخّص / معتمد' } },
  } as Record<Sec, { t: L; s: L; badge: L }>,
  tapHint: { en: 'Tap a card to open it', ar: 'اضغط على أي مربع لفتحه' },
  aboutH: { en: "Building today's healthcare solutions for tomorrow's healthcare vision.", ar: 'نبني حلول اليوم لرؤية صحية أفضل للغد.' },
  aboutP: { en: 'Moxyra Pharma is an Egyptian healthcare and beauty company. We develop proprietary brands in cosmeceuticals, skin care, hair care and nutrition & wellness, turning real market needs into distinctive products. Our products are made through qualified manufacturing partners. Expanding toward broader healthcare and pharmaceutical development is a medium to long-term ambition, not a current manufacturing activity.', ar: 'موكسيرا فارما شركة مصرية للرعاية الصحية والتجميل. نطوّر علامات تجارية خاصة في مستحضرات التجميل العلاجية والعناية بالبشرة والشعر والمكملات الغذائية، ونحوّل احتياجات السوق الحقيقية إلى منتجات مميزة. تُصنَّع منتجاتنا لدى شركاء تصنيع مؤهلين. أما التوسع نحو مجالات صحية ودوائية أوسع فهو هدف على المدى المتوسط إلى البعيد، وليس نشاط تصنيع قائماً اليوم.' },
  values: [
    [{ en: 'Innovation', ar: 'الابتكار' }, { en: 'Consumer-led formulation design', ar: 'تصميم تركيبات ينطلق من احتياجات المستهلك' }],
    [{ en: 'Quality first', ar: 'الجودة أولاً' }, { en: 'Quality-focused manufacturing through qualified partners', ar: 'تصنيع يهتم بالجودة لدى شركاء مؤهلين' }],
    [{ en: 'Partnership', ar: 'الشراكة' }, { en: 'Long-term cooperation over one-off transactions', ar: 'تعاون طويل الأمد بدلاً من الصفقات العابرة' }],
  ] as [L, L][],
  vision: [
    { en: 'Our vision', ar: 'رؤيتنا' },
    { en: 'To build a trusted Egyptian healthcare and beauty company with a growing portfolio of distinctive brands, expanding across local and international markets while developing toward broader healthcare opportunities.', ar: 'أن نكون شركة مصرية موثوقة في الرعاية الصحية والتجميل، بمحفظة متنامية من العلامات المميزة، نتوسع في الأسواق المحلية والدولية ونتطور نحو فرص صحية أوسع.' },
  ] as L[],
  mission: [
    { en: 'Our mission', ar: 'رسالتنا' },
    { en: 'To develop high-quality healthcare and beauty products that answer real consumer and market needs, build sustainable partnerships, and keep expanding our portfolio through innovation and responsible business development.', ar: 'تطوير منتجات صحية وتجميلية عالية الجودة تلبّي احتياجات المستهلك والسوق، وبناء شراكات مستدامة، وتوسيع محفظتنا بالابتكار والتطوير المسؤول لأعمالنا.' },
  ] as L[],
  whatH: { en: 'What we do', ar: 'مجالات عملنا' },
  what: [
    [{ en: 'Cosmeceuticals & dermatological care', ar: 'مستحضرات التجميل العلاجية والعناية بالبشرة' }, { en: 'Specialized skin care under proprietary brands.', ar: 'منتجات متخصصة للعناية بالبشرة تحت علاماتنا الخاصة.' }],
    [{ en: 'Hair & scalp care', ar: 'العناية بالشعر وفروة الرأس' }, { en: 'Solutions for different hair and scalp needs.', ar: 'حلول تناسب احتياجات الشعر وفروة الرأس المختلفة.' }],
    [{ en: 'Nutrition & Wellness', ar: 'التغذية والصحة العامة' }, { en: "Dietary supplements, subject to each product's regulatory and commercial status.", ar: 'مكملات غذائية، وفق الوضع التنظيمي والتجاري لكل منتج.' }],
    [{ en: 'Product development & proprietary brands', ar: 'تطوير المنتجات والعلامات الخاصة' }, { en: 'Distinctive products and consumer healthcare brands.', ar: 'منتجات مميزة وعلامات خاصة في الرعاية الصحية والتجميل.' }],
    [{ en: 'Pharmacy & distribution partnerships', ar: 'شراكات الصيدليات والتوزيع' }, { en: 'Relationships with pharmacies, chains, distributors and wholesalers.', ar: 'علاقات مع الصيدليات والسلاسل والموزعين وتجار الجملة.' }],
    [{ en: 'Professional & commercial support', ar: 'الدعم المهني والتجاري' }, { en: 'Product awareness, education and professional communication.', ar: 'التعريف بالمنتجات والتثقيف والتواصل المهني.' }],
    [{ en: 'Contract manufacturing & private label', ar: 'التصنيع للغير والعلامات الخاصة' }, { en: 'Explored through qualified partners, subject to technical and commercial arrangements.', ar: 'نستكشفها مع شركاء تصنيع مؤهلين، وفق الاتفاقيات الفنية والتجارية.' }],
    [{ en: 'Future healthcare development', ar: 'التطوير الصحي المستقبلي' }, { en: 'A long-term ambition toward broader healthcare and pharmaceutical products.', ar: 'هدف بعيد المدى للتوسع نحو منتجات صحية ودوائية أوسع.' }],
  ] as [L, L][],
  brandsH: { en: 'Our brands', ar: 'علاماتنا' },
  brands: [
    { key: 'URYHIP', img: bUry, a: { en: 'Advanced emollient skin care', ar: 'عناية متقدمة بالبشرة بكريمات ومرطّبات ملطّفة' }, b: { en: 'Body, face and cleansing care', ar: 'عناية بالجسم والوجه والتنظيف' }, tone: 'rose' },
    { key: 'MOXYGAIN', img: bMox, a: { en: 'Hair care & specialized scalp care', ar: 'العناية بالشعر وفروة الرأس' }, b: { en: 'Intensa repair line and scalp care line', ar: 'مجموعة Intensa للترميم ومجموعة العناية بفروة الرأس' }, tone: 'violet' },
    { key: 'MOXYRA WELLNESS', img: bWel, a: { en: 'Wellness & dietary supplements', ar: 'الصحة العامة والمكملات الغذائية' }, b: { en: 'Dietary Supplements for a Healthy Life', ar: 'مكملات غذائية للحياة الصحية' }, tone: 'teal' },
  ] as { key: Product['brand']; img: string; a: L; b: L; tone: string }[],
  explore: { en: 'Explore products', ar: 'استكشف المنتجات' },
  prodH: { en: 'Product portfolio', ar: 'منتجاتنا' },
  prodSub: { en: 'Every product carries its own status.', ar: 'لكل منتج حالته الظاهرة عليه.' },
  fAll: { en: 'All', ar: 'الكل' },
  fAvail: { en: 'Commercially available', ar: 'مطروح تجارياً' },
  fLic: { en: 'Licensed / approved', ar: 'مرخّص / معتمد' },
  fBrands: { en: 'All brands', ar: 'كل البراندات' },
  stAvail: { en: 'Commercially available', ar: 'مطروح تجارياً' },
  stLic: { en: 'Licensed / approved', ar: 'مرخّص / معتمد' },
  details: { en: 'Product details', ar: 'تفاصيل المنتج' },
  close: { en: 'Close', ar: 'إغلاق' },
  dlExport: { en: 'Download export company profile (PDF)', ar: 'حمّل الملف التعريفي للتصدير (PDF)' },
  dlEgypt: { en: 'Download Egypt company profile (PDF)', ar: 'حمّل الملف التعريفي للسوق المصري (PDF)' },
  qualH: { en: 'Product development & quality', ar: 'تطوير المنتجات والجودة' },
  qualP: { en: 'Moxyra focuses on product concepts, formulation development, brand development, portfolio expansion and manufacturing coordination. Our products are manufactured through qualified manufacturing partners.', ar: 'نركّز على أفكار المنتجات وتطوير التركيبات وبناء العلامات وتوسيع المحفظة وتنسيق التصنيع. وتُصنَّع منتجاتنا لدى شركاء تصنيع مؤهلين.' },
  certH: { en: 'Certifications held by our manufacturing partners', ar: 'شهادات يحملها شركاء التصنيع' },
  certs: [['GMP', { en: 'Good Manufacturing Practices', ar: 'ممارسات التصنيع الجيد' }], ['ISO 9001', { en: 'Quality management systems', ar: 'نظام إدارة الجودة' }], ['ISO 22716', { en: 'Cosmetics GMP', ar: 'ممارسات التصنيع الجيد لمستحضرات التجميل' }]] as [string, L][],
  certHeld: { en: 'Held by our manufacturing partners', ar: 'يحملها شركاء التصنيع لدينا' },
  growH: { en: 'How we grow', ar: 'كيف ننمو' },
  grow: [
    { en: 'Identify market needs', ar: 'تحديد احتياجات السوق' }, { en: 'Develop relevant products', ar: 'تطوير منتجات مناسبة' }, { en: 'Build distinctive brands', ar: 'بناء علامات مميزة' }, { en: 'Educate and support partners', ar: 'تثقيف الشركاء ودعمهم' }, { en: 'Develop sustainable distribution', ar: 'بناء توزيع مستدام' }, { en: 'Monitor performance and opportunities', ar: 'متابعة الأداء والفرص' }, { en: 'Expand portfolio and partnerships', ar: 'توسيع المحفظة والشراكات' },
  ] as L[],
  whyH: { en: 'Why partner with Moxyra', ar: 'لماذا الشراكة مع موكسيرا' },
  why: [
    { en: 'Distinctive proprietary brands', ar: 'علامات خاصة مميزة' }, { en: 'Market-oriented product development', ar: 'تطوير منتجات يلبّي احتياجات السوق' }, { en: 'A growing, diversified portfolio', ar: 'محفظة متنامية ومتنوعة' }, { en: 'Qualified manufacturing partnerships', ar: 'شراكات تصنيع مؤهلة' }, { en: 'Flexible commercial cooperation', ar: 'تعاون تجاري مرن' }, { en: 'Understanding of local and international market needs', ar: 'فهم لاحتياجات الأسواق المحلية والدولية' }, { en: 'Product education and professional support', ar: 'تثقيف بالمنتجات ودعم مهني' }, { en: 'Long-term growth ambitions', ar: 'طموح للنمو على المدى الطويل' },
  ] as L[],
  localH: { en: 'Local market partnerships', ar: 'الشراكات في السوق المحلي' },
  localP: { en: 'We have established cooperation with many pharmacies and major pharmacy chains across a number of Egyptian governorates, and we are building broader distribution partnerships. We engage healthcare professionals through scientific communication and product education.', ar: 'لدينا تعاون قائم مع العديد من الصيدليات وسلاسل صيدليات كبرى في عدد من المحافظات المصرية، ونعمل على بناء شراكات توزيع أوسع. ونتواصل مع متخصصي الرعاية الصحية من خلال التواصل العلمي والتثقيف بالمنتجات.' },
  local: [{ en: 'Pharmacy chains', ar: 'سلاسل الصيدليات' }, { en: 'Independent pharmacies', ar: 'الصيدليات المستقلة' }, { en: 'Pharmaceutical distributors', ar: 'موزعو الأدوية' }, { en: 'Distribution warehouses & wholesalers', ar: 'مخازن التوزيع وتجار الجملة' }, { en: 'Healthcare professionals', ar: 'متخصصو الرعاية الصحية' }] as L[],
  intlH: { en: 'International business partnerships', ar: 'الشراكات الدولية' },
  intlP: { en: 'URYHIP is commercialized in Saudi Arabia through a local distribution partner. We welcome importers, distributors, brand owners and manufacturing partners. Commercial and product documentation is available on request.', ar: 'تُسوَّق علامة URYHIP في المملكة العربية السعودية عبر شريك توزيع محلي. نرحّب بالمستوردين والموزعين وأصحاب العلامات التجارية وشركاء التصنيع. تتوفر المعلومات التجارية ومعلومات المنتجات عند الطلب.' },
  intl: [{ en: 'Importers & wholesalers', ar: 'المستوردون وتجار الجملة' }, { en: 'International distributors', ar: 'الموزعون الدوليون' }, { en: 'Healthcare & beauty companies', ar: 'شركات الرعاية الصحية والتجميل' }, { en: 'Private-label clients', ar: 'عملاء العلامات الخاصة' }, { en: 'Contract manufacturing partners', ar: 'شركاء التصنيع للغير' }, { en: 'Strategic business partners', ar: 'شركاء أعمال استراتيجيون' }] as L[],
  intlCta: { en: 'Discuss distribution opportunities', ar: 'ناقش فرص التوزيع معنا' },
  contactH: { en: "Let's build together.", ar: 'لنبنِ معاً.' },
  contactP: { en: 'Reach us by email or WhatsApp and tell us who you are and what you are looking for.', ar: 'تواصل معنا عبر البريد أو واتساب، وعرّفنا بنفسك وبم تبحث عنه.' },
  email: { en: 'Email', ar: 'البريد' }, phone: { en: 'Phone / WhatsApp', ar: 'الهاتف / واتساب' }, hq: { en: 'Headquarters', ar: 'المقر' },
  hqV: { en: 'Alexandria, Egypt', ar: 'الإسكندرية، مصر' },
  formH: { en: 'Partnership and company profile request', ar: 'طلب شراكة أو ملف تعريفي' },
  formP: { en: 'Choose what you need. Pricing and trade terms are shared directly with qualified partners, not published on this site.', ar: 'اختر ما تحتاجه. نشارك الأسعار وشروط التعامل مباشرةً مع الشركاء المؤهلين ولا ننشرها على الموقع.' },
  fName: { en: 'Your name', ar: 'الاسم' }, fCo: { en: 'Company / pharmacy', ar: 'الشركة / الصيدلية' }, fCity: { en: 'City and country', ar: 'المدينة والدولة' },
  fWho: { en: 'I am a…', ar: 'أنا…' }, fNeed: { en: 'I need…', ar: 'أحتاج…' }, fNotes: { en: 'Notes (optional)', ar: 'ملاحظات (اختياري)' },
  who: [{ en: 'Pharmacy / pharmacy chain', ar: 'صيدلية / سلسلة صيدليات' }, { en: 'Distributor / wholesaler', ar: 'موزع / تاجر جملة' }, { en: 'International importer', ar: 'مستورد دولي' }, { en: 'Private label / contract manufacturing', ar: 'علامة خاصة / تصنيع للغير' }, { en: 'Other', ar: 'أخرى' }] as L[],
  need: [{ en: 'Egypt company profile', ar: 'الملف التعريفي للسوق المصري' }, { en: 'Export company profile', ar: 'الملف التعريفي للتصدير' }, { en: 'Price list', ar: 'قائمة الأسعار' }, { en: 'Partnership / distribution discussion', ar: 'مناقشة شراكة أو توزيع' }, { en: 'Product information', ar: 'معلومات عن منتج' }] as L[],
  send: { en: 'Send on WhatsApp', ar: 'أرسل عبر واتساب' },
  note: { en: 'Nothing is stored by this site. The button opens WhatsApp with the message ready for you to review and send.', ar: 'لا يحفظ الموقع أي بيانات. الزر يفتح واتساب برسالة جاهزة لتراجعها وترسلها.' },
  foot: { en: '© 2026 Moxyra Pharma. All rights reserved.', ar: '© 2026 موكسيرا فارما. جميع الحقوق محفوظة.' },
  concept: { en: 'Design concept preview. Same content as the live site, new design.', ar: 'معاينة تصور تصميم. نفس محتوى الموقع الحالي بتصميم جديد.' },
};

export function App() {
  const [lang, setLang] = useState<'en' | 'ar'>(typeof location !== 'undefined' && location.pathname.indexOf('/ar') === 0 ? 'ar' : 'en');
  const [openVal, setOpenVal] = useState<number | null>(null);
  const [openWhat, setOpenWhat] = useState<number | null>(null);
  const [pickWhy, setPickWhy] = useState<number | null>(null);
  const [brand, setBrand] = useState<'all' | Product['brand']>('all');
  const [open, setOpenRaw] = useState<Product | null>(null);
  const [openY, setOpenY] = useState(0);
  const [boxTop, setBoxTop] = useState(0);
  const [vis, setVis] = useState({ t: 0, h: 700 });
  const [heroSet, setHeroSet] = useState(0);
  const [ready, setReady] = useState(false);
  const [pickLoc, setPickLoc] = useState<string | null>(null);
  const [pickPath, setPickPath] = useState<string | null>(null);
  const togglePath = (k: string) => (e: React.MouseEvent) => { if ((e.target as HTMLElement).closest('a,button')) return; setPickPath(pickPath === k ? null : k); };
  const [pickCert, setPickCert] = useState<number | null>(null);
  const [pickGrow, setPickGrow] = useState<number | null>(null);
  const rootRef = useRef<HTMLDivElement>(null);
  const boxRef = useRef<HTMLDivElement>(null);
  const setOpen = (p: Product | null, el?: HTMLElement) => {
    if (p && el && rootRef.current) {
      const r = el.getBoundingClientRect(); const rr = rootRef.current.getBoundingClientRect();
      setOpenY(r.top - rr.top + r.height / 2);
    }
    setOpenRaw(p);
  };
  useEffect(() => {
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const t = setInterval(() => setHeroSet((s) => (s + 1) % HERO_SETS), 2000);
    return () => clearInterval(t);
  }, []);
  useEffect(() => {
    if (!open) return;
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpenRaw(null); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  }, [open]);
  useEffect(() => {
    setReady(false);
    if (!open || !rootRef.current) return;
    if (typeof IntersectionObserver === 'undefined') { setReady(true); return; }
    const inFrame = window.self !== window.top;
    const io = new IntersectionObserver((es) => {
      const e = es[es.length - 1]; const ir = e.intersectionRect; const br = e.boundingClientRect;
      if (ir.height > 0) {
        const bar = inFrame ? 72 : 0;
        setVis({ t: ir.top - br.top + bar, h: Math.max(240, ir.height - bar) });
      }
      io.disconnect();
      setReady(true);
    });
    io.observe(rootRef.current);
    const fb = setTimeout(() => setReady(true), 400);
    return () => { io.disconnect(); clearTimeout(fb); };
  }, [open]);
  const maxH = Math.max(220, Math.min(vis.h - 24, 640));
  useLayoutEffect(() => {
    if (!open || !boxRef.current || !rootRef.current) return;
    const h = boxRef.current.offsetHeight; const H = rootRef.current.offsetHeight;
    const lo = vis.t + 12; const hi = Math.min(vis.t + vis.h - h - 12, H - h - 12);
    setBoxTop(Math.max(12, Math.min(Math.max(openY - h / 2, lo), Math.max(hi, lo))));
  }, [open, openY, lang, vis, maxH]);
  const [form, setForm] = useState({ name: '', co: '', city: '', who: 0, need: 0, notes: '' });
  const x = (l: L) => l[lang];
  const inBrand = (p: Product) => brand === 'all' || p.brand === brand;
  const secKeys: Sec[] = ['available', 'licensed', 'supp'];
  const secItems = (k: Sec) => products.filter((p) => secOf(p) === k && inBrand(p));
  const secCount = (k: Sec) => products.filter((p) => secOf(p) === k).length;
  const badge = (p: Product) => x(T.secs[secOf(p)].badge);
  const statClick = (k: string) => { setBrand('all'); setTimeout(() => goTo(k === 'all' ? 'products' : `sec-${k}`), 30); };
  const msg = lang === 'en'
    ? `Hello Moxyra Pharma,\nName: ${form.name}\nCompany: ${form.co}\nCity/Country: ${form.city}\nI am a: ${T.who[form.who].en}\nI need: ${T.need[form.need].en}\nNotes: ${form.notes}`
    : `مرحباً موكسيرا فارما،\nالاسم: ${form.name}\nالشركة: ${form.co}\nالمدينة والدولة: ${form.city}\nأنا: ${T.who[form.who].ar}\nأحتاج: ${T.need[form.need].ar}\nملاحظات: ${form.notes}`;
  const waHref = `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
  const goBrand = (b: Product['brand']) => { setBrand(b); setTimeout(() => goTo('products'), 30); };

  return (
    <div className="mx" ref={rootRef} dir={lang === 'ar' ? 'rtl' : 'ltr'} lang={lang}>
      <div className="mx-concept">{x(T.concept)}</div>
      <header className="mx-hero">
        <div className="mx-glow" />
        <nav className="mx-nav">
          <img className="mx-logo" src={logo} alt="Moxyra Pharma" />
          <div className="mx-links">
            {T.nav.map(([id, l]) => <a key={id} href={`#${id}`} onClick={(e) => { e.preventDefault(); document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' }); }}>{x(l)}</a>)}
          </div>
          <button type="button" className="mx-lang" onClick={() => setLang(lang === 'en' ? 'ar' : 'en')}>{lang === 'en' ? 'العربية' : 'English'}</button>
        </nav>
        <div className="mx-hero-grid">
          <div className="mx-hero-copy">
            <p className="mx-eyebrow">{x(T.eyebrow)}</p>
            <h1>{x(T.h1)}</h1>
            <p className="mx-lead">{x(T.lead)}</p>
            <div className="mx-cta">
              <button type="button" className="mx-btn mx-btn-light" onClick={() => document.getElementById('products')?.scrollIntoView({ behavior: 'smooth' })}>{x(T.cta1)}</button>
              <button type="button" className="mx-btn mx-btn-ghost" onClick={() => document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })}>{x(T.cta2)}</button>
            </div>
            <p className="mx-tag">{x(T.tag)}</p>
          </div>
          <div className="mx-hero-art" aria-hidden="false">
            {['a', 'b', 'c'].map((k, ki) => (
              <React.Fragment key={k}>
                {Array.from({ length: HERO_SETS }, (_, si) => { const p = products[(si * 3 + ki) % products.length]; return <img key={si} className={`mx-art-${k} mx-swap ${heroSet === si ? 'on' : ''}`} src={p.img} alt={heroSet === si ? x(p.alt) : ''} decoding="async" />; })}
              </React.Fragment>
            ))}
          </div>
        </div>
        <div className="mx-stats">
          {(['all', 'available', 'licensed', 'supp'] as const).map((k) => (
            <button type="button" key={k} className="mx-stat" onClick={() => statClick(k)}>
              <b>{k === 'all' ? products.length : secCount(k)}</b><span>{x(T.statL[k])}</span><i aria-hidden="true">{lang === 'en' ? '↓' : '↓'}</i>
            </button>
          ))}
        </div>
      </header>

      <section id="about" className="mx-sec mx-about">
        <div className="mx-two">
          <div>
            <h2 className="mx-h2">{x(T.aboutH)}</h2>
            <p className="mx-p">{x(T.aboutP)}</p>
          </div>
          <div className="mx-vm">
            {[T.vision, T.mission].map((v) => <div key={v[0].en} className="mx-vm-card"><h3>{x(v[0])}</h3><p>{x(v[1])}</p></div>)}
          </div>
        </div>
        <div className="mx-values">
          {T.values.map(([a, b], i) => (
            <button type="button" key={a.en} aria-expanded={openVal === i} className={`mx-tile mx-val ${openVal === i ? 'is-open' : ''}`} onClick={() => setOpenVal(openVal === i ? null : i)}>
              <span className="mx-num">0{i + 1}</span><h3>{x(a)}</h3><span className="mx-plus" aria-hidden="true" />
              <span className="mx-reveal"><p>{x(b)}</p></span>
            </button>
          ))}
        </div>
        <h3 className="mx-sub">{x(T.whatH)}</h3>
        <div className="mx-what">
          {T.what.map(([a, b], i) => (
            <button type="button" key={a.en} aria-expanded={openWhat === i} className={`mx-tile mx-wt ${openWhat === i ? 'is-open' : ''}`} onClick={() => setOpenWhat(openWhat === i ? null : i)}>
              <h4>{x(a)}</h4><span className="mx-plus" aria-hidden="true" />
              <span className="mx-reveal"><p>{x(b)}</p></span>
            </button>
          ))}
        </div>
      </section>

      <section id="brands" className="mx-brands">
        <h2 className="mx-h2 mx-center">{x(T.brandsH)}</h2>
        <div className="mx-brand-list">
          {T.brands.map((b) => (
            <article key={b.key} className={`mx-brand mx-${b.tone}`}>
              <img src={b.img} alt={b.key} />
              <div className="mx-brand-text">
                <h3>{b.key}</h3>
                <p className="mx-brand-a">{x(b.a)}</p>
                <p>{x(b.b)}</p>
                <button type="button" className="mx-link" onClick={() => goBrand(b.key)}>{x(T.explore)} {lang === 'en' ? '→' : '←'}</button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section id="products" className="mx-sec mx-prod">
        <div className="mx-prod-head">
          <div>
            <h2 className="mx-h2">{x(T.prodH)}</h2>
            <p className="mx-p">{x(T.prodSub)}</p>
          </div>
          <div className="mx-dl">
            <a href={`${SITE}/assets/company-profile/Moxyra-Pharma-Export-Company-Profile.pdf`} target="_blank" rel="noopener noreferrer">{x(T.dlExport)}</a>
            <a href={`${SITE}/assets/company-profile/Moxyra-Pharma-Egypt-Company-Profile.pdf`} target="_blank" rel="noopener noreferrer">{x(T.dlEgypt)}</a>
          </div>
        </div>
        <div className="mx-filters">
          {secKeys.map((k) => <button type="button" key={k} onClick={() => goTo(`sec-${k}`)}>{x(T.secs[k].t)} <em>{secCount(k)}</em></button>)}
        </div>
        <div className="mx-filters mx-filters-2">
          {([['all', T.fBrands.en], ['URYHIP', 'URYHIP'], ['MOXYGAIN', 'MOXYGAIN'], ['MOXYRA WELLNESS', 'MOXYRA WELLNESS']] as const).map(([k, l]) => <button type="button" key={k} className={brand === k ? 'on' : ''} onClick={() => setBrand(k as any)}>{k === 'all' ? x(T.fBrands) : l}</button>)}
        </div>
        {secKeys.map((k) => secItems(k).length > 0 && (
          <div key={k} id={`sec-${k}`} className={`mx-psec mx-psec-${k}`}>
            <div className="mx-psec-head">
              <h3>{x(T.secs[k].t)}</h3>
              <span className="mx-count">{secItems(k).length}</span>
              <p>{x(T.secs[k].s)}</p>
            </div>
            <div className="mx-grid">
              {secItems(k).map((p) => (
                <button type="button" key={p.id} className="mx-card" onClick={(e) => setOpen(p, e.currentTarget)}>
                  <div className="mx-card-img"><img src={p.img} alt={x(p.alt)} loading="lazy" /><span className="mx-open-hint" aria-hidden="true">+</span></div>
                  <div className="mx-card-body">
                    <span className="mx-chip">{p.brand} · {x(p.line)}</span>
                    <h3>{p.name}</h3>
                    <p className="mx-size">{x(p.size)}</p>
                    <span className={`mx-status ${p.status} s-${k}`}>{badge(p)}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </section>

      {open && (
        <div className="mx-modal" role="dialog" aria-modal="true" onClick={() => setOpenRaw(null)}>
          <div className="mx-modal-box" ref={boxRef} style={{ top: boxTop, visibility: ready ? 'visible' : 'hidden', ["--mh" as any]: `${maxH}px` }} onClick={(e) => e.stopPropagation()}>
            <button type="button" className="mx-x" aria-label={x(T.close)} onClick={() => setOpenRaw(null)}>×</button>
            <div className="mx-modal-scroll"><img src={open.img} alt={x(open.alt)} />
            <div className="mx-modal-text">
              <span className="mx-chip">{open.brand} · {x(open.line)}</span>
              <h3>{open.name}</h3>
              <p className="mx-size">{x(open.size)}</p>
              <p>{x(open.desc)}</p>
              <h4>{x(ingLabel)}</h4>
              <p className="mx-ing" dir="ltr">{open.ingredients}</p>
              <span className={`mx-status ${open.status} s-${secOf(open)}`}>{badge(open)}</span>
            </div></div>
          </div>
        </div>
      )}

      <section id="quality" className="mx-quality">
        <div className="mx-two">
          <div>
            <h2 className="mx-h2 mx-light">{x(T.qualH)}</h2>
            <p className="mx-p mx-light-p">{x(T.qualP)}</p>
            <h3 className="mx-sub mx-light">{x(T.certH)}</h3>
            <div className="mx-certs">
              {T.certs.map(([a, b], i) => <button type="button" key={a} aria-pressed={pickCert === i} className={`mx-cert ${pickCert === i ? 'is-on' : ''}`} onClick={() => setPickCert(pickCert === i ? null : i)}><b>{a}</b><span>{x(b)}</span><em>{x(T.certHeld)}</em></button>)}
            </div>
          </div>
          <div>
            <h3 className="mx-sub mx-light">{x(T.growH)}</h3>
            <ol className="mx-steps">
              {T.grow.map((g, i) => <li key={g.en}><button type="button" aria-pressed={pickGrow === i} className={`mx-step ${pickGrow === i ? 'is-on' : ''}`} onClick={() => setPickGrow(pickGrow === i ? null : i)}><span>{i + 1}</span><b>{x(g)}</b><i aria-hidden="true">✓</i></button></li>)}
            </ol>
          </div>
        </div>
      </section>

      <section id="partners" className="mx-sec">
        <h2 className="mx-h2 mx-center">{x(T.whyH)}</h2>
        <div className="mx-why">
          {T.why.map((w, i) => (
            <button type="button" key={w.en} aria-pressed={pickWhy === i} className={`mx-tile mx-wy ${pickWhy === i ? 'is-open' : ''}`} onClick={() => setPickWhy(pickWhy === i ? null : i)}>
              <span className="mx-num">0{i + 1}</span><span className="mx-wy-t">{x(w)}</span><span className="mx-tick" aria-hidden="true">✓</span>
            </button>
          ))}
        </div>
        <div className="mx-paths">
          <div className={`mx-path mx-path-egypt ${pickPath === 'egypt' ? 'is-on' : ''}`} onClick={togglePath('egypt')} onKeyDown={(e) => { if (e.target === e.currentTarget && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); setPickPath(pickPath === 'egypt' ? null : 'egypt'); } }} role="group" tabIndex={0} aria-label={x(T.localH)}>
            <h3>{x(T.localH)}</h3>
            <p>{x(T.localP)}</p>
            <ul>{T.local.map((l) => <li key={l.en}><button type="button" aria-pressed={pickLoc === l.en} className={`mx-pill ${pickLoc === l.en ? 'is-on' : ''}`} onClick={() => setPickLoc(pickLoc === l.en ? null : l.en)}>{x(l)}</button></li>)}</ul>
            <a className="mx-btn mx-btn-dark" href={`${SITE}/assets/company-profile/Moxyra-Pharma-Egypt-Company-Profile.pdf`} target="_blank" rel="noopener noreferrer">{x(T.dlEgypt)}</a>
          </div>
          <div className={`mx-path mx-path-export ${pickPath === 'export' ? 'is-on' : ''}`} onClick={togglePath('export')} onKeyDown={(e) => { if (e.target === e.currentTarget && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); setPickPath(pickPath === 'export' ? null : 'export'); } }} role="group" tabIndex={0} aria-label={x(T.intlH)}>
            <h3>{x(T.intlH)}</h3>
            <p>{x(T.intlP)}</p>
            <ul>{T.intl.map((l) => <li key={l.en}><button type="button" aria-pressed={pickLoc === l.en} className={`mx-pill ${pickLoc === l.en ? 'is-on' : ''}`} onClick={() => setPickLoc(pickLoc === l.en ? null : l.en)}>{x(l)}</button></li>)}</ul>
            <a className="mx-btn mx-btn-dark" href={`${SITE}/assets/company-profile/Moxyra-Pharma-Export-Company-Profile.pdf`} target="_blank" rel="noopener noreferrer">{x(T.dlExport)}</a>
          </div>
        </div>
      </section>

      <section id="contact" className="mx-contact">
        <div className="mx-two">
          <div>
            <h2 className="mx-h2 mx-light">{x(T.contactH)}</h2>
            <p className="mx-p mx-light-p">{x(T.contactP)}</p>
            <dl className="mx-dl2">
              <dt>{x(T.email)}</dt><dd dir="ltr">info@moxyrapharma.com</dd>
              <dt>{x(T.phone)}</dt><dd dir="ltr" className="mx-wa-row">+20 109 968 8827<a className="mx-wa" href={`https://wa.me/${WA}`} target="_blank" rel="noopener noreferrer" aria-label={lang === 'en' ? 'Chat on WhatsApp' : 'تواصل عبر واتساب'} title={lang === 'en' ? 'Chat on WhatsApp' : 'تواصل عبر واتساب'}><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2zm0 18.15c-1.48 0-2.93-.4-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.2 8.2 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.82 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.22-8.23 8.22zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.12-.16.25-.64.81-.78.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.42h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28z"/></svg></a></dd>
              <dt>{x(T.hq)}</dt><dd>{x(T.hqV)}</dd>
            </dl>
          </div>
          <div className="mx-form">
            <h3>{x(T.formH)}</h3>
            <p>{x(T.formP)}</p>
            <label>{x(T.fName)}<input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
            <label>{x(T.fCo)}<input value={form.co} onChange={(e) => setForm({ ...form, co: e.target.value })} /></label>
            <label>{x(T.fCity)}<input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} /></label>
            <label>{x(T.fWho)}<select value={form.who} onChange={(e) => setForm({ ...form, who: +e.target.value })}>{T.who.map((w, i) => <option key={w.en} value={i}>{x(w)}</option>)}</select></label>
            <label>{x(T.fNeed)}<select value={form.need} onChange={(e) => setForm({ ...form, need: +e.target.value })}>{T.need.map((w, i) => <option key={w.en} value={i}>{x(w)}</option>)}</select></label>
            <label>{x(T.fNotes)}<textarea rows={3} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} /></label>
            <a className="mx-btn mx-btn-wa" href={waHref} target="_blank" rel="noopener noreferrer">{x(T.send)}</a>
            <small>{x(T.note)}</small>
          </div>
        </div>
      </section>

      <footer className="mx-foot">
        <img src={logo} alt="Moxyra Pharma" />
        <p>{x(T.h1)}</p>
        <p>{x(T.foot)}</p>
      </footer>
    </div>
  );
}
