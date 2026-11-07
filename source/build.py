#!/usr/bin/env python3
"""Moxyra Pharma website generator (Python 3, no dependencies).

Run from the repository root:   python3 source/build.py
It writes only these 12 generated files into ../site (or $MOXYRA_OUT):
  ar/index.html en/index.html assets/main.css assets/main.js
  index.html home.html en.html 404.html robots.txt sitemap.xml _redirects _headers
Everything else inside site/ (images, favicon, cover.jpg, logo.jpg, maintenance/) is a plain file and is never touched.
Verify the result with:         python3 source/verify.py

Layout of this file (top to bottom): products (PR, GROUPS, status ST) -> bilingual copy (C) -> CSS -> JS ->
icons and helper functions -> page(i) template -> file writers. The CSS and JS are built from several appended
blocks on purpose: their order is the cascade, so they must not be reordered or merged without re-verifying output.
See source/CHANGELOG.md for what was cleaned up and why.
"""
import os, json, html
BASE = os.environ.get("SITE_URL", "https://moxyrapharma.com")  # change if the live domain differs
OUT = os.environ.get("MOXYRA_OUT") or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site"))
E, P = "info@moxyrapharma.com", "+20 109 968 8827"

# status: A available, L licensed/approved, P pipeline
ST = {"A": ("Commercially available", "مطروح تجارياً"), "L": ("Licensed / approved", "مرخّص / معتمد"),
      "P": ("Pipeline / upcoming", "قيد التطوير / قريباً")}
# id, brand, status, name, size(en,ar), category(en,ar), key ingredients (as supplied), description(en,ar)
PR = [
 ("body", "URYHIP", "A", "Uryhip Emollient Body Cream", ("200 g", "200 جم"), ("Skin care", "العناية بالبشرة"), "Urea 10% · Panthenol 5% · Rosehip oil 1%", ("Emollient moisturizing cream for very dry skin.", "كريم مرطّب ملطّف للبشرة شديدة الجفاف.")),
 ("face", "URYHIP", "A", "Uryhip Emollient Face Cream", ("120 g", "120 جم"), ("Skin care", "العناية بالبشرة"), "Urea 5% · Panthenol 5% · Rosehip oil 1%", ("Emollient face moisturizer for everyday dry skin.", "كريم مرطّب للوجه للاستخدام اليومي للبشرة الجافة.")),
 ("shower", "URYHIP", "A", "Uryhip Emollient Shower Gel", ("250 ml", "250 مل"), ("Skin care", "العناية بالبشرة"), "Urea 5% · Panthenol 2% · Rosehip oil 1%", ("Moisturizing shower gel for very dry skin. SLS-free, paraben-free.", "شاور جل مرطّب للبشرة شديدة الجفاف. خالٍ من SLS والبارابين.")),
 ("wash", "URYHIP", "A", "Uryhip Creamy Face Wash", ("200 ml", "200 مل"), ("Skin care", "العناية بالبشرة"), "Urea 2% · Panthenol 2.5% · Rosehip oil 1%", ("Moisturizing creamy face wash for very dry skin.", "غسول وجه كريمي مرطّب للبشرة شديدة الجفاف.")),
 ("antioily", "MOXYGAIN Scalp Care", "A", "Moxygain Anti Oily Dandruff Shampoo", ("200 ml", "200 مل"), ("Hair & scalp care", "العناية بالشعر وفروة الرأس"), "Selenium sulfide · Climbazole 0.5% · Piroctone olamine 1% · Salicylic acid · Bentonite 1% · Tea tree oil · Panthenol 2% · Fiberhance", ("Shampoo for oily scalp and oily dandruff. Paraben-free.", "شامبو لفروة الرأس الدهنية والقشرة الدهنية. خالٍ من البارابين.")),
 ("hydra", "MOXYGAIN Scalp Care", "A", "Moxygain Hydra Anti Dry Dandruff Shampoo", ("200 ml", "200 مل"), ("Hair & scalp care", "العناية بالشعر وفروة الرأس"), "Selenium sulfide · Climbazole 0.5% · Piroctone olamine 1% · Salicylic acid · Glycolic acid · Aloe vera · Panthenol 3% · Fiberhance", ("Hydrating shampoo for dry dandruff and dry scalp.", "شامبو مرطّب للقشرة الجافة وفروة الرأس الجافة.")),
 ("shampoo", "MOXYGAIN Intensa", "A", "Moxygain Intensa Repairing Shampoo", ("300 ml", "300 مل"), ("Hair care", "العناية بالشعر"), "Fiberhance 1% · Ceramide complex 0.3% · Hydrolyzed keratin & wheat protein · Zinc PCA 1% · Niacinamide 1%", ("Repairing shampoo for dry and damaged hair. Paraben-free, SLS-free.", "شامبو ترميمي للشعر الجاف والتالف. خالٍ من البارابين و SLS.")),
 ("conditioner", "MOXYGAIN Intensa", "A", "Moxygain Intensa Repairing Conditioner", ("300 ml", "300 مل"), ("Hair care", "العناية بالشعر"), "Squalene 1% · Hyalofill 0.5% · Fiberhance 1% · Ceramide complex 0.3% · Hydrolyzed keratin & wheat protein", ("Repairing conditioner for dry and damaged hair. Paraben-free, SLS-free.", "بلسم ترميمي للشعر الجاف والتالف. خالٍ من البارابين و SLS.")),
 ("leavein", "MOXYGAIN Intensa", "P", "Moxygain Intensa Repairing Leave-In Cream", ("300 g", "300 جم"), ("Hair care", "العناية بالشعر"), "Squalene · Hyalofill · Fiberhance · Ceramide complex · Hydrolyzed keratin & wheat protein · Macadamia oil · Jojoba oil", ("Leave-in cream for dry and damaged hair.", "كريم بدون شطف للشعر الجاف والتالف.")),
 ("mask", "MOXYGAIN Intensa", "P", "Moxygain Intensa Repairing Cream Mask", ("300 g", "300 جم"), ("Hair care", "العناية بالشعر"), "Squalene · Hyalofill · Fiberhance · Ceramide complex · Hydrolyzed keratin & wheat protein · Macadamia oil · Jojoba oil", ("Repairing cream mask for dry and damaged hair.", "ماسك كريمي ترميمي للشعر الجاف والتالف.")),
 ("bee", "MOXYRA Wellness", "L", "Moxyra Active Bee Multivitamin Kids Syrup", ("120 ml", "120 مل"), ("Dietary supplement", "مكمل غذائي"), "Royal jelly 75 mg · Vitamins C, E, A, D, folate, B-complex", ("Multivitamin syrup supplement for children.", "شراب مكمل غذائي متعدد الفيتامينات للأطفال.")),
 ("magnesium", "MOXYRA Wellness", "L", "Moxyra Magnesium Bisglycinate", ("30 tablets", "30 قرصاً"), ("Dietary supplement", "مكمل غذائي"), "Magnesium bisglycinate chelate 150 mg", ("Magnesium dietary supplement.", "مكمل غذائي من المغنيسيوم.")),
 ("respi", "MOXYRA Wellness", "L", "Moxyra Respi Health", ("20 tablets", "20 قرصاً"), ("Dietary supplement", "مكمل غذائي"), "Acetylcysteine · Bromelain · Ivy leaves extract", ("Respiratory wellness dietary supplement.", "مكمل غذائي لدعم الصحة التنفسية.")),
 ("gaselief", "MOXYRA Wellness", "L", "Moxyra Gaselief", ("30 capsules", "30 كبسولة"), ("Dietary supplement", "مكمل غذائي"), "Targeted gastrointestinal comfort formula", ("Dietary supplement that supports digestive health.", "مكمل غذائي يدعم صحة الجهاز الهضمي.")),
]

# ---------------- bilingual copy: (en, ar) ----------------
C = {
 "title": ("Moxyra Pharma | Egyptian Healthcare & Beauty Company", "موكسيرا فارما | شركة مصرية للرعاية الصحية والتجميل"),
 "desc": ("Moxyra Pharma is an Egyptian healthcare and beauty company in Alexandria building proprietary brands in cosmeceuticals, hair care and nutritional wellness.",
          "موكسيرا فارما شركة مصرية للرعاية الصحية والتجميل مقرها الإسكندرية، تبني علامات تجارية خاصة في مستحضرات التجميل العلاجية والعناية بالشعر والعافية الغذائية."),
 "nav": [("about", "About", "عن الشركة"), ("what", "What we do", "مجالات عملنا"), ("brands", "Brands", "العلامات"), ("products", "Products", "المنتجات"), ("quality", "Quality", "الجودة"), ("partners", "Partnerships", "الشراكات"), ("contact", "Contact", "تواصل معنا")],
 "eyebrow": ("Egyptian Healthcare & Beauty Company · Alexandria · Est. 2024", "شركة مصرية للرعاية الصحية والتجميل · الإسكندرية · تأسست 2024"),
 "h1": ("Where Innovation Meets Healthcare.", "حيث يلتقي الابتكار بالرعاية الصحية."),
 "lead": ("Building distinctive healthcare and beauty brands through product development, qualified manufacturing partnerships, and sustainable business cooperation.",
          "نبني علامات صحية وتجميلية مميزة عبر تطوير المنتجات وشراكات التصنيع المؤهلة وتعاون تجاري مستدام."),
 "cta1": ("Explore our products", "استعرض منتجاتنا"), "cta2": ("Become a partner", "كن شريكاً"),
 "hero_note": ("Proudly Egyptian. Built for Healthcare. Designed for the Future.", "فخورون بمصريتنا. مبنيون للرعاية الصحية. مصمَّمون للمستقبل."),
 "about_h": ("Building today's healthcare solutions for tomorrow's healthcare vision.", "نبني حلول اليوم لرؤية صحية للغد."),
 "about_p": ("Moxyra Pharma is an Egyptian healthcare and beauty company established in 2024 and based in Alexandria. We develop proprietary brands in cosmeceuticals, skin care, hair care and nutritional wellness, turning real market needs into distinctive products. Our products are made through qualified external manufacturing partners. Expanding toward broader healthcare and pharmaceutical development is a long-term ambition, not a current manufacturing activity.",
             "موكسيرا فارما شركة مصرية للرعاية الصحية والتجميل تأسست عام 2024 ومقرها الإسكندرية. نطوّر علامات تجارية خاصة في مستحضرات التجميل العلاجية والعناية بالبشرة والشعر والعافية الغذائية، ونحوّل احتياجات السوق الفعلية إلى منتجات مميزة. تُصنَّع منتجاتنا عبر شركاء تصنيع خارجيين مؤهلين. أما التوسع نحو مجالات صحية ودوائية أوسع فهو طموح استراتيجي بعيد المدى وليس نشاط تصنيع قائماً."),
 "vis_h": ("Our vision", "رؤيتنا"), "mis_h": ("Our mission", "رسالتنا"),
 "vis": ("To build a trusted Egyptian healthcare and beauty company with a growing portfolio of distinctive brands, expanding across local and international markets while developing toward broader healthcare opportunities.",
         "بناء شركة مصرية موثوقة للرعاية الصحية والتجميل بمحفظة متنامية من العلامات المميزة، تتوسع في الأسواق المحلية والدولية وتتطور نحو فرص صحية أوسع."),
 "mis": ("To develop high-quality healthcare and beauty products that answer real consumer and market needs, build sustainable partnerships, and keep expanding our portfolio through innovation and responsible business development.",
         "تطوير منتجات صحية وتجميلية عالية الجودة تلبي احتياجات المستهلك والسوق، وبناء شراكات مستدامة، وتوسيع محفظتنا باستمرار عبر الابتكار والتطوير المسؤول للأعمال."),
 "values": [("Innovation", "الابتكار", "Consumer-led formulation design", "تصميم تركيبات منطلق من احتياج المستهلك"),
            ("Quality first", "الجودة أولاً", "Quality-focused manufacturing through qualified partners", "تصنيع يركّز على الجودة عبر شركاء مؤهلين"),
            ("Partnership", "الشراكة", "Long-term cooperation over one-off transactions", "تعاون طويل الأمد بدل الصفقات العابرة")],
 "what_h": ("What we do", "ما نقوم به"),
 "what": [("Cosmeceuticals & dermatological care", "مستحضرات التجميل العلاجية والعناية الجلدية", "Specialized skin care under proprietary brands.", "منتجات عناية متخصصة بالبشرة تحت علامات خاصة."),
          ("Hair & scalp care", "العناية بالشعر وفروة الرأس", "Solutions for different hair and scalp needs.", "حلول لاحتياجات الشعر وفروة الرأس المختلفة."),
          ("Nutritional wellness", "العافية الغذائية", "Dietary supplements, subject to each product's regulatory and commercial status.", "مكملات غذائية، وفق الوضع التنظيمي والتجاري لكل منتج."),
          ("Product development & proprietary brands", "تطوير المنتجات والعلامات الخاصة", "Distinctive products and consumer healthcare brands.", "منتجات مميزة وعلامات صحية استهلاكية خاصة بنا."),
          ("Pharmacy & distribution partnerships", "شراكات الصيدليات والتوزيع", "Relationships with pharmacies, chains, distributors and wholesalers.", "علاقات مع الصيدليات والسلاسل والموزعين وتجار الجملة."),
          ("Professional & commercial support", "الدعم المهني والتجاري", "Product awareness, education and professional communication.", "التوعية بالمنتجات والتثقيف والتواصل المهني."),
          ("Contract manufacturing & private label", "التصنيع للغير والعلامات الخاصة", "Explored through qualified partners, subject to technical and commercial arrangements.", "نستكشفها عبر شركاء مؤهلين، وفق الترتيبات الفنية والتجارية."),
          ("Future healthcare development", "التطوير الصحي المستقبلي", "A long-term ambition toward broader healthcare and pharmaceutical products.", "طموح بعيد المدى نحو منتجات صحية ودوائية أوسع.")],
 "brands_h": ("Our brands", "علاماتنا"),
 "brands": [("URYHIP", "Advanced emollient skin care", "عناية متقدمة بالبشرة بالمرطّبات الملطّفة", "uryhip", "body"),
            ("MOXYGAIN", "Hair repair, fiber care & specialized scalp care", "ترميم الشعر والعناية بالألياف وفروة الرأس", "moxygain", "shampoo"),
            ("MOXYRA WELLNESS", "Nutritional wellness & dietary supplements", "العافية الغذائية والمكملات الغذائية", "wellness", "magnesium")],
 "prod_h": ("Product portfolio", "محفظة المنتجات"),
 "prod_p": ("Every product carries its own status. Licensed products have not yet entered commercial manufacturing and are not currently available for delivery.",
            "لكل منتج وضعه الخاص. المنتجات المرخّصة لم تدخل بعد مرحلة التصنيع التجاري وغير متاحة حالياً للتسليم."),
 "all": ("All", "الكل"), "ing": ("Key ingredients (as labelled)", "أهم المكونات (كما في العبوة)"),
 "q_h": ("Product development & quality", "تطوير المنتجات والجودة"),
 "q_p": ("Moxyra focuses on product concepts, formulation development, brand development, portfolio expansion and manufacturing coordination. Our products are manufactured through qualified external contract manufacturing partners.",
         "تركّز موكسيرا على أفكار المنتجات وتطوير التركيبات وبناء العلامات وتوسيع المحفظة وتنسيق التصنيع. وتُصنَّع منتجاتنا عبر شركاء تصنيع خارجيين مؤهلين."),
 "q_c": ("Certifications held by our manufacturing partners", "شهادات يحملها شركاء التصنيع"),
 "q_n": ("These certifications belong to our manufacturing partners, not to Moxyra Pharma.", "هذه الشهادات تخص شركاء التصنيع لدينا وليست شهادات لشركة موكسيرا فارما."),
 "certs": [("GMP", "Good Manufacturing Practices", "ممارسات التصنيع الجيد"), ("ISO 9001", "Quality management systems", "أنظمة إدارة الجودة"), ("ISO 22716", "Cosmetics GMP", "ممارسات التصنيع الجيد لمستحضرات التجميل")],
 "why_h": ("Why partner with Moxyra", "لماذا الشراكة مع موكسيرا"),
 "why": [("Distinctive proprietary brands", "علامات خاصة مميزة"), ("Market-oriented product development", "تطوير منتجات موجَّه للسوق"), ("A growing, diversified portfolio", "محفظة متنامية ومتنوعة"),
         ("Qualified manufacturing partnerships", "شراكات تصنيع مؤهلة"), ("Flexible commercial cooperation", "تعاون تجاري مرن"), ("Understanding of local market needs", "فهم لاحتياجات السوق المحلي"),
         ("Product education and professional support", "تثقيف بالمنتجات ودعم مهني"), ("Long-term growth ambitions", "طموحات نمو بعيدة المدى")],
 "grow_h": ("How we grow", "كيف ننمو"),
 "grow": [("Identify market needs", "تحديد احتياجات السوق"), ("Develop relevant products", "تطوير منتجات مناسبة"), ("Build distinctive brands", "بناء علامات مميزة"), ("Educate and support partners", "تثقيف الشركاء ودعمهم"),
          ("Develop sustainable distribution", "بناء توزيع مستدام"), ("Monitor performance and opportunities", "متابعة الأداء والفرص"), ("Expand portfolio and partnerships", "توسيع المحفظة والشراكات")],
 "loc_h": ("Local market partnerships", "الشراكات في السوق المحلي"),
 "loc_p": ("We have established cooperation with several major pharmacy chains in Alexandria and with major pharmacies across several Egyptian governorates, and we are building broader distribution partnerships. We engage healthcare professionals through scientific communication and product education only.",
           "لدينا تعاون قائم مع عدة سلاسل صيدليات كبرى في الإسكندرية ومع صيدليات كبرى في عدد من المحافظات المصرية، ونعمل على بناء شراكات توزيع أوسع. ونتواصل مع المهنيين الصحيين عبر التواصل العلمي وتثقيف المنتجات فقط."),
 "loc_l": [("Pharmacy chains", "سلاسل الصيدليات"), ("Independent pharmacies", "الصيدليات المستقلة"), ("Pharmaceutical distributors", "موزعو الأدوية"), ("Distribution warehouses & wholesalers", "مخازن التوزيع وتجار الجملة"), ("Healthcare professionals", "المهنيون الصحيون")],
 "int_h": ("International business partnerships", "الشراكات الدولية"),
 "int_p": ("URYHIP is commercialized in Saudi Arabia through a local distribution partner. We welcome importers, distributors, brand owners and manufacturing partners. Commercial and product documentation is available on request.",
           "تُسوَّق علامة URYHIP في المملكة العربية السعودية عبر شريك توزيع محلي. نرحّب بالمستوردين والموزعين وأصحاب العلامات وشركاء التصنيع. تتوفر المستندات التجارية ومستندات المنتجات عند الطلب."),
 "int_l": [("Importers & wholesalers", "المستوردون وتجار الجملة"), ("International distributors", "الموزعون الدوليون"), ("Healthcare & beauty companies", "شركات الرعاية الصحية والتجميل"), ("Private-label clients", "عملاء العلامات الخاصة"), ("Contract manufacturing partners", "شركاء التصنيع للغير"), ("Strategic business partners", "شركاء أعمال استراتيجيون")],
 "con_h": ("Let's build together.", "لنبنِ معاً."),
 "con_p": ("Tell us who you are and what you are looking for.", "عرّفنا بنفسك وبما تبحث عنه."),
 "f": [("Name", "الاسم"), ("Company", "الشركة"), ("Email", "البريد الإلكتروني"), ("I am a…", "أنا…"), ("Message", "الرسالة")],
 "f_opts": [("Pharmacy / pharmacy chain", "صيدلية / سلسلة صيدليات"), ("Distributor / wholesaler", "موزع / تاجر جملة"), ("International importer", "مستورد دولي"), ("Private label / contract manufacturing", "علامة خاصة / تصنيع للغير"), ("Other", "أخرى")],
 "send": ("Open email draft", "افتح مسودة البريد"), "f_note": ("This opens your email app with the message ready to send to info@moxyrapharma.com.", "يفتح تطبيق البريد برسالة جاهزة للإرسال إلى info@moxyrapharma.com."),
 "email": ("Email", "البريد"), "phone": ("Phone / WhatsApp", "الهاتف / واتساب"), "loc": ("Headquarters", "المقر"), "city": ("Alexandria, Egypt", "الإسكندرية، مصر"),
 "foot": ("© 2026 Moxyra Pharma. All rights reserved.", "© 2026 موكسيرا فارما. جميع الحقوق محفوظة."),
 "skip": ("Skip to content", "انتقل إلى المحتوى"), "menu": ("Menu", "القائمة"), "alt_logo": ("Moxyra Pharma logo", "شعار موكسيرا فارما"),
 "bn": {"uryhip": ("Body, face and cleansing care", "عناية بالجسم والوجه والتنظيف"), "moxygain": ("Intensa repair line and scalp care line", "خط Intensa للترميم وخط العناية بفروة الرأس"), "wellness": ("Licensed supplements, not yet in manufacturing", "مكملات مرخّصة لم تدخل التصنيع بعد")},
}
X = lambda k, i: C[k][i]

C.update({
 "desc": ("Moxyra Pharma is an Egyptian healthcare and beauty company building proprietary brands in skin care, hair care and nutritional wellness.",
          "موكسيرا فارما شركة مصرية للرعاية الصحية والتجميل، تطوّر علامات تجارية خاصة في العناية بالبشرة والشعر والمكملات الغذائية."),
 "eyebrow": ("Egyptian Healthcare & Beauty Company", "شركة مصرية للرعاية الصحية والتجميل"),
 "h1": ("Where Innovation Meets Healthcare.", "حيث يلتقي الابتكار بالرعاية الصحية"),
 "lead": ("Building distinctive healthcare and beauty brands through product development, qualified manufacturing partnerships, and sustainable business cooperation.",
          "نبني علامات صحية وتجميلية مميزة من خلال تطوير المنتجات، والعمل مع شركاء تصنيع مؤهلين، وبناء شراكات تجارية مستدامة."),
 "hero_note": ("Quality-focused. Partnership-driven. Future-ready.", "الجودة نهجنا، والشراكة طريقنا، والمستقبل وجهتنا."),
 "about_h": ("Building today's healthcare solutions for tomorrow's healthcare vision.", "نبني حلول اليوم لرؤية صحية أفضل للغد."),
 "about_p": ("Moxyra Pharma is an Egyptian healthcare and beauty company. We develop proprietary brands in cosmeceuticals, skin care, hair care and nutritional wellness, turning real market needs into distinctive products. Our products are made through qualified manufacturing partners. Expanding toward broader healthcare and pharmaceutical development is a medium to long-term ambition, not a current manufacturing activity.",
             "موكسيرا فارما شركة مصرية للرعاية الصحية والتجميل. نطوّر علامات تجارية خاصة في مستحضرات التجميل العلاجية والعناية بالبشرة والشعر والمكملات الغذائية، ونحوّل احتياجات السوق الحقيقية إلى منتجات مميزة. تُصنَّع منتجاتنا لدى شركاء تصنيع مؤهلين. أما التوسع نحو مجالات صحية ودوائية أوسع فهو هدف على المدى المتوسط إلى البعيد، وليس نشاط تصنيع قائماً اليوم."),
 "vis": ("To build a trusted Egyptian healthcare and beauty company with a growing portfolio of distinctive brands, expanding across local and international markets while developing toward broader healthcare opportunities.",
         "أن نكون شركة مصرية موثوقة في الرعاية الصحية والتجميل، بمحفظة متنامية من العلامات المميزة، نتوسع في الأسواق المحلية والدولية ونتطور نحو فرص صحية أوسع."),
 "mis": ("To develop high-quality healthcare and beauty products that answer real consumer and market needs, build sustainable partnerships, and keep expanding our portfolio through innovation and responsible business development.",
         "تطوير منتجات صحية وتجميلية عالية الجودة تلبّي احتياجات المستهلك والسوق، وبناء شراكات مستدامة، وتوسيع محفظتنا بالابتكار والتطوير المسؤول لأعمالنا."),
 "values": [("Innovation", "الابتكار", "Consumer-led formulation design", "تصميم تركيبات ينطلق من احتياجات المستهلك"),
            ("Quality first", "الجودة أولاً", "Quality-focused manufacturing through qualified partners", "تصنيع يهتم بالجودة لدى شركاء مؤهلين"),
            ("Partnership", "الشراكة", "Long-term cooperation over one-off transactions", "تعاون طويل الأمد بدلاً من الصفقات العابرة")],
 "what_h": ("What we do", "مجالات عملنا"),
 "what": [("Cosmeceuticals & dermatological care", "مستحضرات التجميل العلاجية والعناية بالبشرة", "Specialized skin care under proprietary brands.", "منتجات متخصصة للعناية بالبشرة تحت علاماتنا الخاصة."),
          ("Hair & scalp care", "العناية بالشعر وفروة الرأس", "Solutions for different hair and scalp needs.", "حلول تناسب احتياجات الشعر وفروة الرأس المختلفة."),
          ("Nutritional wellness", "العافية الغذائية", "Dietary supplements, subject to each product's regulatory and commercial status.", "مكملات غذائية، وفق الوضع التنظيمي والتجاري لكل منتج."),
          ("Product development & proprietary brands", "تطوير المنتجات والعلامات الخاصة", "Distinctive products and consumer healthcare brands.", "منتجات مميزة وعلامات خاصة في الرعاية الصحية والتجميل."),
          ("Pharmacy & distribution partnerships", "شراكات الصيدليات والتوزيع", "Relationships with pharmacies, chains, distributors and wholesalers.", "علاقات مع الصيدليات والسلاسل والموزعين وتجار الجملة."),
          ("Professional & commercial support", "الدعم المهني والتجاري", "Product awareness, education and professional communication.", "التعريف بالمنتجات والتثقيف والتواصل المهني."),
          ("Contract manufacturing & private label", "التصنيع للغير والعلامات الخاصة", "Explored through qualified partners, subject to technical and commercial arrangements.", "نستكشفها مع شركاء تصنيع مؤهلين، وفق الاتفاقيات الفنية والتجارية."),
          ("Future healthcare development", "التطوير الصحي المستقبلي", "A long-term ambition toward broader healthcare and pharmaceutical products.", "هدف بعيد المدى للتوسع نحو منتجات صحية ودوائية أوسع.")],
 "brands": [("URYHIP", "Advanced emollient skin care", "عناية متقدمة بالبشرة بكريمات ومرطّبات ملطّفة", "uryhip", "body"),
            ("MOXYGAIN", "Hair care & specialized scalp care", "العناية بالشعر وفروة الرأس", "moxygain", "shampoo"),
            ("MOXYRA WELLNESS", "Nutritional wellness & dietary supplements", "العافية الغذائية والمكملات الغذائية", "wellness", "magnesium")],
 "bn": {"uryhip": ("Body, face and cleansing care", "عناية بالجسم والوجه والتنظيف"), "moxygain": ("Intensa repair line and scalp care line", "خط Intensa للترميم وخط العناية بفروة الرأس"), "wellness": ("Licensed supplements", "مكملات غذائية مرخّصة")},
 "prod_h": ("Product portfolio", "منتجاتنا"),
 "prod_p": ("Every product carries its own status.", "لكل منتج حالته الظاهرة عليه."),
 "ing": ("Key ingredients (as labelled)", "أهم المكونات (كما على العبوة)"),
 "q_h": ("Product development & quality", "تطوير المنتجات والجودة"),
 "q_p": ("Moxyra focuses on product concepts, formulation development, brand development, portfolio expansion and manufacturing coordination. Our products are manufactured through qualified external manufacturing partners.",
         "نركّز على أفكار المنتجات وتطوير التركيبات وبناء العلامات وتوسيع المحفظة وتنسيق التصنيع. وتُصنَّع منتجاتنا لدى شركاء تصنيع خارجيين مؤهلين."),
 "q_c": ("Certifications held by our manufacturing partners", "شهادات يحملها شركاء التصنيع"),
 "certs": [("GMP", "Good Manufacturing Practices", "ممارسات التصنيع الجيد"), ("ISO 9001", "Quality management systems", "نظام إدارة الجودة"), ("ISO 22716", "Cosmetics GMP", "ممارسات التصنيع الجيد لمستحضرات التجميل")],
 "why_h": ("Why partner with Moxyra", "لماذا الشراكة مع موكسيرا"),
 "why": [("Distinctive proprietary brands", "علامات خاصة مميزة"), ("Market-oriented product development", "تطوير منتجات يلبّي احتياجات السوق"), ("A growing, diversified portfolio", "محفظة متنامية ومتنوعة"),
         ("Qualified manufacturing partnerships", "شراكات تصنيع مؤهلة"), ("Flexible commercial cooperation", "تعاون تجاري مرن"), ("Understanding of local market needs", "فهم لاحتياجات السوق المحلي"),
         ("Product education and professional support", "تثقيف بالمنتجات ودعم مهني"), ("Long-term growth ambitions", "طموح للنمو على المدى الطويل")],
 "grow_h": ("How we grow", "كيف ننمو"),
 "grow": [("Identify market needs", "تحديد احتياجات السوق"), ("Develop relevant products", "تطوير منتجات مناسبة"), ("Build distinctive brands", "بناء علامات مميزة"), ("Educate and support partners", "تثقيف الشركاء ودعمهم"),
          ("Develop sustainable distribution", "بناء توزيع مستدام"), ("Monitor performance and opportunities", "متابعة الأداء والفرص"), ("Expand portfolio and partnerships", "توسيع المحفظة والشراكات")],
 "loc_h": ("Local market partnerships", "الشراكات في السوق المحلي"),
 "loc_p": ("We have established cooperation with several major pharmacy chains across several Egyptian governorates, and we are building broader distribution partnerships. We engage healthcare professionals through scientific communication and product education.",
           "لدينا تعاون قائم مع عدة سلاسل صيدليات كبرى في عدد من المحافظات المصرية، ونعمل على بناء شراكات توزيع أوسع. ونتواصل مع المهنيين الصحيين من خلال التواصل العلمي وتثقيف المنتجات."),
 "loc_l": [("Pharmacy chains", "سلاسل الصيدليات"), ("Independent pharmacies", "الصيدليات المستقلة"), ("Pharmaceutical distributors", "موزعو الأدوية"), ("Distribution warehouses & wholesalers", "مخازن التوزيع وتجار الجملة"), ("Healthcare professionals", "المهنيون الصحيون")],
 "int_h": ("International business partnerships", "الشراكات الدولية"),
 "int_p": ("URYHIP is commercialized in Saudi Arabia through a local distribution partner. We welcome importers, distributors, brand owners and manufacturing partners. Commercial and product documentation is available on request.",
           "تُسوَّق علامة URYHIP في المملكة العربية السعودية عبر شريك توزيع محلي. نرحّب بالمستوردين والموزعين وأصحاب العلامات التجارية وشركاء التصنيع. تتوفر المعلومات التجارية ومعلومات المنتجات عند الطلب."),
 "int_l": [("Importers & wholesalers", "المستوردون وتجار الجملة"), ("International distributors", "الموزعون الدوليون"), ("Healthcare & beauty companies", "شركات الرعاية الصحية والتجميل"), ("Private-label clients", "عملاء العلامات الخاصة"), ("Contract manufacturing partners", "شركاء التصنيع للغير"), ("Strategic business partners", "شركاء أعمال استراتيجيون")],
 "con_h": ("Let's build together.", "لنبنِ معاً."),
 "send": ("Send message", "إرسال الرسالة"),
 "f_ok": ("Thank you. Your message has been sent.", "شكراً لك، تم إرسال رسالتك."),
 "f_err": ("Could not send right now. Please email us at info@moxyrapharma.com", "تعذّر الإرسال حالياً. يرجى مراسلتنا على info@moxyrapharma.com"),
})
ST.pop("P")
PR = [(p[0], p[1], "L" if p[0] in ("leavein", "mask") else p[2]) + p[3:] for p in PR]
LANG = {0: ("en", "ltr", "English", "en_US"), 1: ("ar", "rtl", "العربية", "ar_EG")}

CSS = """
:root{--purple:#5A3B83;--blue:#0056B3;--teal:#00A896;--dark:#1A252F;--ink:#26303a;--mute:#5d6873;--line:#e4dfee;--bg:#fbfaf8;--tint:#f3eff9;--r:6px}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--bg);color:var(--ink);font:400 1.0625rem/1.7 'Inter','IBM Plex Sans Arabic',system-ui,sans-serif}
[lang=ar] body{font-family:'IBM Plex Sans Arabic','Segoe UI',Tahoma,sans-serif;line-height:1.95}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;color:var(--dark);line-height:1.12;margin:0 0 .5em;font-weight:600}
[lang=ar] h1,[lang=ar] h2,[lang=ar] h3{font-family:'IBM Plex Sans Arabic',sans-serif;font-weight:600;line-height:1.4}
h1{font-size:clamp(2.6rem,6vw,4.6rem)}h2{font-size:clamp(1.9rem,3.6vw,2.8rem)}h3{font-size:1.3rem}
[lang=ar] h1{font-size:clamp(2.2rem,5vw,3.8rem)}
img{max-width:100%;height:auto;display:block}a{color:var(--blue)}
.w{width:min(1160px,100% - 2.5rem);margin-inline:auto}
.skip{position:absolute;inset-inline-start:-999px}.skip:focus{inset-inline-start:1rem;top:1rem;background:#fff;padding:.5rem 1rem;z-index:99}
:focus-visible{outline:3px solid var(--teal);outline-offset:3px}
header{position:sticky;top:0;z-index:20;background:rgba(251,250,248,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:1.2rem;min-height:68px}
.brand{display:flex;align-items:center;gap:.7rem;text-decoration:none;color:var(--purple);font:600 1.25rem 'Cormorant Garamond',serif;letter-spacing:.12em;margin-inline-end:auto}
.brand img{height:44px;width:auto;border-radius:4px}
nav ul{display:flex;gap:1.2rem;list-style:none;margin:0;padding:0}
nav a{color:var(--ink);text-decoration:none;font-size:.95rem;font-weight:500;padding:.4rem 0;border-bottom:2px solid transparent}nav a:hover{border-color:var(--teal)}
.lang{border:1px solid var(--purple);color:var(--purple);border-radius:var(--r);padding:.3rem .8rem;text-decoration:none;font-weight:600;font-size:.9rem}
.lang:hover{background:var(--purple);color:#fff}
#mb{display:none;background:none;border:1px solid var(--line);border-radius:var(--r);padding:.4rem .8rem;font:inherit}
.hero{background:linear-gradient(135deg,#1c1030 0%,#3b2563 60%,#5A3B83 100%);color:#fff;padding:4.5rem 0 4rem;overflow:hidden}
.hero .w{display:grid;grid-template-columns:1.15fr .85fr;gap:3rem;align-items:center}
.hero h1{color:#fff}.eyebrow{color:#cdb8ee;font-size:.95rem;margin:0 0 1.2rem}
.hero p.lead{font-size:1.2rem;color:#e7defa;max-width:34em}.hn{color:#bfa9e6;font-size:.95rem;margin-top:2rem}
.btns{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:1.8rem}
.btn{display:inline-block;padding:.8rem 1.5rem;border-radius:var(--r);text-decoration:none;font-weight:600;border:2px solid var(--teal);background:var(--teal);color:#0c1f1c}
.btn.o{background:transparent;color:#fff;border-color:#cdb8ee}.btn:hover{filter:brightness(1.1)}
.stack{position:relative;display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;align-items:end}
.stack img{border-radius:var(--r);aspect-ratio:4/5;object-fit:cover;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.stack img:nth-child(2){transform:translateY(-1.6rem)}
section{padding:4.5rem 0}section.t{background:var(--tint)}
.sh{max-width:46rem;margin-bottom:2.2rem}.sh p{color:var(--mute)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2.5rem}
.vm{display:grid;gap:1rem;margin-top:1.5rem}.vm div{border-inline-start:4px solid var(--purple);padding:.2rem 1.2rem;background:#fff}
.vm h3{margin:.3rem 0}.vm p{margin:0 0 .5rem}
.vals{display:flex;flex-wrap:wrap;gap:1rem;margin-top:1.5rem}.vals div{flex:1 1 180px;border-top:3px solid var(--teal);padding-top:.6rem}.vals b{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1.2rem}
.c{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1.4rem}.c h3{font-size:1.15rem}.c p{margin:0;color:var(--mute);font-size:.98rem}
.bg3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem}
.bc{background:#fff;border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.bc img{aspect-ratio:4/3;object-fit:cover;width:100%}.bc div{padding:1.2rem 1.4rem}.bc h3{letter-spacing:.08em}
.bc.uryhip{border-top:5px solid #9b1c2a}.bc.moxygain{border-top:5px solid var(--purple)}.bc.wellness{border-top:5px solid var(--teal)}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1.5rem}
.chip{border:1px solid var(--purple);background:#fff;color:var(--purple);border-radius:99px;padding:.35rem 1rem;font:inherit;font-size:.92rem;cursor:pointer}
.chip[aria-pressed=true]{background:var(--purple);color:#fff}
.pc{background:#fff;border:1px solid var(--line);border-radius:var(--r);display:flex;flex-direction:column}
.pc img{aspect-ratio:4/5;object-fit:cover;width:100%;border-radius:var(--r) var(--r) 0 0}
.pb{padding:1rem 1.2rem 1.2rem;display:flex;flex-direction:column;gap:.4rem;flex:1}
.pb .br{font-size:.85rem;color:var(--mute)}.pb h3{font-size:1.1rem;margin:0}.pb .m{font-size:.9rem;color:var(--mute)}.pb p{margin:0;font-size:.96rem}
.bd{align-self:flex-start;font-size:.82rem;font-weight:600;border-radius:99px;padding:.15rem .7rem}
.bd.A{background:#dff5ee;color:#0b6b4f}.bd.L{background:#e4ecfb;color:#0a3f8a}.bd.P{background:#fdf0d6;color:#8a5a00}
details{font-size:.9rem;margin-top:auto;padding-top:.4rem}summary{cursor:pointer;color:var(--purple);font-weight:600}details p{margin:.4rem 0 0}
.cl{list-style:none;margin:1rem 0 0;padding:0;display:flex;flex-wrap:wrap;gap:.5rem}.cl li{background:#fff;border:1px solid var(--line);border-radius:99px;padding:.25rem .9rem;font-size:.93rem}
.certs{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1.2rem 0}.certs div{background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:1rem}.certs b{color:var(--blue);font-size:1.2rem;display:block}
.note{font-size:.95rem;color:var(--mute)}
ol.steps{list-style:none;counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1rem;padding:0;margin:0}
ol.steps li{counter-increment:s;border-top:3px solid var(--purple);padding-top:.5rem;font-weight:500}ol.steps li:before{content:counter(s);display:block;color:var(--purple);font:600 1.6rem 'Cormorant Garamond',serif}
.ct{background:var(--dark);color:#dfe6ec}.ct h2{color:#fff}.ct a{color:#8fe0d5}
.ct form{display:grid;gap:.9rem}.ct label{display:grid;gap:.25rem;font-size:.92rem}
.ct input,.ct select,.ct textarea{font:inherit;padding:.65rem;border-radius:var(--r);border:1px solid #4a5865;background:#fff;color:var(--ink)}
.ct button{justify-self:start;cursor:pointer}.ct dl{margin:0}.ct dt{font-size:.85rem;color:#9fb0bd;margin-top:1rem}.ct dd{margin:0;font-size:1.15rem}
footer{background:#10171d;color:#9fb0bd;padding:1.5rem 0;font-size:.9rem}
@media(max-width:900px){.hero .w,.two,.bg3{grid-template-columns:1fr}.stack{max-width:420px}.certs{grid-template-columns:1fr}
#mb{display:block}nav{position:absolute;inset-inline:0;top:100%;background:var(--bg);border-bottom:1px solid var(--line);display:none}nav.o{display:block}
nav ul{flex-direction:column;gap:0;padding:.5rem 1.25rem}nav a{display:block;padding:.7rem 0}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
"""



IC = ["M12 2.7C12 2.7 5 9.9 5 14.7a7 7 0 0 0 14 0C19 9.9 12 2.7 12 2.7z",
 "M3 7c3-3 6 3 9 0s6 3 9 0M3 13c3-3 6 3 9 0s6 3 9 0M3 19c3-3 6 3 9 0s6 3 9 0",
 "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z",
 "M9 2h6M10 2v6.5L4.5 19a2 2 0 0 0 1.7 3h11.6a2 2 0 0 0 1.7-3L14 8.5V2",
 "M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9h18M9 20v-6h6v6",
 "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8",
 "M2 21V9l6 4V9l6 4V5h6v16zM2 21h20",
 "M3 17l6-6 4 4 8-8M15 7h6v6"]
ico = lambda n: f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{IC[n]}"/></svg>'
EYE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8S1 12 1 12z"/><circle cx="12" cy="12" r="3"/></svg>'
TGT = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
CSS += """
.brand img{height:58px;width:auto;border-radius:0}
.slider{max-width:380px;justify-self:center;width:100%}
.sf{position:relative;aspect-ratio:4/5;border-radius:var(--r);overflow:hidden;box-shadow:0 18px 40px rgba(0,0,0,.35);background:#2b1a4a}
.sl{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .8s}.sl.on{opacity:1}
.sc{display:flex;align-items:center;gap:.6rem;margin-top:.8rem;color:#e7defa;font-size:.9rem}.cap{flex:1;text-align:center}
.sc button{background:rgba(255,255,255,.15);border:1px solid #cdb8ee;color:#fff;border-radius:50%;width:2.4rem;height:2.4rem;font-size:1.3rem;cursor:pointer}
.vm{margin:0}.vm>div{border:0;border-radius:12px;padding:1.6rem;color:#fff}
.vm .v{background:linear-gradient(135deg,#3b2563,#5A3B83)}.vm .m{background:linear-gradient(135deg,#0a4f8f,#00857a)}
.vm h3{color:#fff;display:flex;align-items:center;gap:.7rem}.vm p{color:#f0eafb}
.vm svg{width:34px;height:34px;stroke:#fff;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.ic{transition:transform .25s,box-shadow .25s,border-color .25s}
.ic:hover,.ic:focus-visible{transform:translateY(-6px);box-shadow:0 14px 28px rgba(90,59,131,.18);border-color:var(--purple)}
.ico{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:var(--tint);margin-bottom:.9rem;transition:background .25s}
.ico svg{width:26px;height:26px;stroke:var(--purple);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round;transition:stroke .25s}
.ic:hover .ico,.ic:focus-visible .ico{background:var(--purple)}.ic:hover .ico svg,.ic:focus-visible .ico svg{stroke:#fff}
.fs{min-height:1.4em}
"""

def esc(s): return html.escape(s, quote=True)

def page(i):
    code, d, lname, loc = LANG[i]; o = 1 - i; oc = LANG[o][0]
    url = f"{BASE}/{code}/"; alt = f"{BASE}/{oc}/"
    nav = "".join(f'<li><a href="#{k}">{esc(a if i == 0 else b)}</a></li>' for k, a, b in C["nav"])
    img = lambda n, s="480", extra="": f'<img src="/assets/img/{n}-{s}.webp" srcset="/assets/img/{n}-480.webp 480w,/assets/img/{n}-900.webp 900w" sizes="(max-width:900px) 90vw,320px" {extra}>'
    def card(p):
        pid, br, st, nm, sz, cat, ing, ds = p
        return (f'<article class="pc" data-s="{st}"><img src="/assets/img/{pid}-480.webp" srcset="/assets/img/{pid}-480.webp 480w,/assets/img/{pid}-900.webp 900w" sizes="(max-width:600px) 90vw,280px" width="480" height="600" loading="lazy" alt="{esc(nm)} {esc(sz[i])}">'
                f'<div class="pb"><span class="bd {st}">{esc(ST[st][i])}</span><span class="br">{esc(br)} · {esc(cat[i])}</span><h3 dir="ltr">{esc(nm)}</h3><span class="m">{esc(sz[i])}</span><p>{esc(ds[i])}</p>'
                f'<details><summary>{esc(X("ing", i))}</summary><p dir="ltr">{esc(ing)}</p></details></div></article>')
    chips = f'<button class="chip" data-f="all" aria-pressed="true">{esc(X("all", i))}</button>' + "".join(f'<button class="chip" data-f="{k}" aria-pressed="false">{esc(v[i])}</button>' for k, v in ST.items())
    byid = {p[0]: p for p in PR}
    def card2(p):
        pid, br, st, nm, sz, cat, ing, ds = p
        return (f'<article class="pc ic" data-s="{st}"><button class="zi" type="button" data-full="/assets/img/{pid}-900.webp" data-alt="{esc(nm)}" aria-label="{esc(X("zoom", i))}: {esc(nm)}">'
                f'<img src="/assets/img/{pid}-480.webp" srcset="/assets/img/{pid}-480.webp 480w,/assets/img/{pid}-900.webp 900w" sizes="(max-width:600px) 90vw,280px" width="480" height="600" loading="lazy" alt="{esc(nm)} {esc(sz[i])}"><span class="zm" aria-hidden="true">+</span></button>'
                f'<div class="pb"><span class="br">{esc(br)} · {esc(cat[i])}</span><h3 dir="ltr">{esc(nm)}</h3><span class="m">{esc(sz[i])}</span><p>{esc(ds[i])}</p>'
                f'<details><summary>{esc(X("ing", i))}</summary><p dir="ltr">{esc(ing)}</p></details></div></article>')
    def groups():
        out = ""
        for st, subs in GROUPS:
            out += f'<div class="pg" data-s="{st}"><h3 class="gh"><span class="bd {st}">{esc(ST[st][i])}</span></h3>'
            for title, ids in subs:
                out += f'<h4 class="sh4">{esc(title[i])}</h4><div class="grid">{"".join(card2(byid[k]) for k in ids)}</div>'
            out += '</div>'
        return out
    li = lambda L: "".join(f"<li>{esc(a if i == 0 else b)}</li>" for a, b in L)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Moxyra Pharma", "url": BASE + "/", "logo": BASE + "/assets/img/logo.png", 
                     "email": E, "telephone": P, "address": {"@type": "PostalAddress", "addressLocality": "Alexandria", "addressCountry": "EG"}}, ensure_ascii=False)
    fl = C["f"]; opts = "".join(f"<option>{esc(a if i == 0 else b)}</option>" for a, b in C["f_opts"])
    ab = X("about_p", i)
    return f"""<!DOCTYPE html>
<html lang="{code}" dir="{d}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(X("title", i))}</title><meta name="description" content="{esc(X("desc", i))}">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{BASE}/en/"><link rel="alternate" hreflang="ar" href="{BASE}/ar/"><link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(X("title", i))}"><meta property="og:description" content="{esc(X("desc", i))}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/img/body-900.webp"><meta property="og:locale" content="{loc}"><meta property="og:locale:alternate" content="{LANG[o][3]}">
<meta name="theme-color" content="#5A3B83"><link rel="icon" href="/favicon.png?v={VER}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=IBM+Plex+Sans+Arabic:wght@400;500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/main.css?v={VER}"><script type="application/ld+json">{ld}</script></head>
<body><a class="skip" href="#main">{esc(X("skip", i))}</a>
<header><div class="w bar"><a class="brand" href="/{code}/"><img src="/assets/img/logo.png?v={VER}" width="170" height="115" alt=""><span dir="ltr">MOXYRA PHARMA</span></a>
<nav id="nav" aria-label="Main"><ul>{nav}<li class="nc"><a class="btn p" href="#contact">{esc(X("cta2", i))}</a></li></ul></nav><a class="btn sm p hc" href="#contact">{esc(X("cta2", i))}</a><a class="lang" href="/{oc}/" hreflang="{oc}" lang="{oc}">{LANG[o][2]}</a>
<button id="mb" aria-controls="nav" aria-expanded="false">{esc(X("menu", i))}</button></div></header>
<main id="main">
<div class="hero"><div class="w"><div><p class="eyebrow">{esc(X("eyebrow", i))}</p><h1>{esc(X("h1", i))}</h1><p class="lead">{esc(X("lead", i))}</p>
<div class="btns"><a class="btn" href="#products">{esc(X("cta1", i))}</a><a class="btn o" href="#contact">{esc(X("cta2", i))}</a></div><p class="hn">{esc(X("hero_note", i))}</p></div>
{slider(i)}</div></div>
{facts(i)}<section id="about"><div class="w two"><div><h2>{esc(X("about_h", i))}</h2><p>{esc(ab)}</p>
<div class="vals">{"".join(f"<div><b>{esc(v[i])}</b>{esc(v[2 + i])}</div>" for v in C["values"])}</div></div>
{vm(i)}</div></section>
<section id="what" class="t"><div class="w"><div class="sh"><h2>{esc(X("what_h", i))}</h2></div><div class="grid">{"".join(f'<div class="c ic" tabindex="0"><span class="ico">{ico(n)}</span><h3>{esc(w[i])}</h3><p>{esc(w[2 + i])}</p></div>' for n, w in enumerate(C["what"]))}</div></div></section>
<section id="brands"><div class="w"><div class="sh"><h2>{esc(X("brands_h", i))}</h2></div><div class="bg3">{"".join(f'<div class="bc ic {b[3]}" tabindex="0">{img(b[4], extra=chr(108)+"oading=lazy width=480 height=360 alt=" + chr(34) + chr(34))}<div><h3 dir="ltr">{b[0]}</h3><p>{esc(b[1 + i])}</p><p class="note">{esc(C["bn"][b[3]][i])}</p><a class="tl" href="#products">{esc(X("explore", i))} {"←" if i else "→"}</a></div></div>' for b in C["brands"])}</div></div></section>
<section id="products" class="t"><div class="w"><div class="sh"><h2>{esc(X("prod_h", i))}</h2><p>{esc(X("prod_p", i))}</p></div><div class="chips" role="group">{chips}</div>
{groups()}</div></section>
<section id="quality"><div class="w"><div class="sh"><h2>{esc(X("q_h", i))}</h2><p>{esc(X("q_p", i))}</p></div><h3>{esc(X("q_c", i))}</h3>
<div class="grid g3">{"".join(f'<div class="c ic" tabindex="0"><span class="ico">{svg(CI[n])}</span><h3>{c[0]}</h3><p>{esc(c[1 + i])}</p></div>' for n, c in enumerate(C["certs"]))}</div>
<h2 class="mt">{esc(X("grow_h", i))}</h2><div class="grid">{"".join(f'<div class="c ic" tabindex="0"><span class="num">{n + 1}</span><span class="ico">{svg(GI[n])}</span><h3>{esc(g[i])}</h3></div>' for n, g in enumerate(C["grow"]))}</div></div></section>
<section class="t"><div class="w"><div class="sh"><h2>{esc(X("why_h", i))}</h2></div><div class="grid">{"".join(f'<div class="c"><h3>{esc(w[i])}</h3></div>' for w in C["why"])}</div></div></section>
<section id="partners"><div class="w two"><div><h2>{esc(X("loc_h", i))}</h2><p>{esc(X("loc_p", i))}</p><ul class="cl">{li(C["loc_l"])}</ul></div>
<div><h2>{esc(X("int_h", i))}</h2><p>{esc(X("int_p", i))}</p><ul class="cl">{li(C["int_l"])}</ul><p style="margin-top:1.5rem"><a class="btn d" href="#contact">{esc(X("discuss", i))}</a></p></div></div></section>
<section id="contact" class="ct"><div class="w"><div class="sh"><h2>{esc(X("con_h", i))}</h2><p>{esc(X("con_p", i))}</p></div>
<div class="grid g3 cc"><a class="c ic" href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to={E}" target="_blank" rel="noopener"><span class="ico">{svg(MAILP)}</span><h3>{esc(X("email", i))}</h3><p>{E}</p></a>
<a class="c ic" href="https://wa.me/201099688827" target="_blank" rel="noopener"><span class="ico">{svg(CHATP)}</span><h3>{esc(X("phone", i))}</h3><p dir="ltr">{P}</p></a>
<div class="c ic" tabindex="0"><span class="ico">{svg(PINP)}</span><h3>{esc(X("loc", i))}</h3><p>{esc(X("city", i))}</p></div></div></div></section>
</main>{footer_html(i)}<dialog id="lb" aria-label="{esc(X('zoom', i))}"><button class="x" type="button" aria-label="{esc(X('close', i))}">×</button><img alt=""></dialog><script src="/assets/main.js?v={VER}" defer></script></body></html>"""

def w(path, s):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(s)


# ---- v3 changes ----
import hashlib
w_ = list(C["what"]); w_[2] = ("Nutrition & Wellness", "التغذية والصحة العامة", w_[2][2], w_[2][3]); C["what"] = w_
C["about_p"] = (C["about_p"][0].replace("nutritional wellness", "nutrition & wellness"), C["about_p"][1])
C["desc"] = (C["desc"][0].replace("nutritional wellness", "nutrition & wellness"), C["desc"][1])
b_ = list(C["brands"]); b_[2] = ("MOXYRA WELLNESS", "Wellness & dietary supplements", "الصحة العامة والمكملات الغذائية", "wellness", "magnesium"); C["brands"] = b_
w2 = list(C["why"]); w2[5] = ("Understanding of local and international market needs", "فهم لاحتياجات الأسواق المحلية والدولية"); C["why"] = w2
l_ = list(C["loc_l"]); l_[4] = ("Healthcare professionals", "متخصصو الرعاية الصحية"); C["loc_l"] = l_
C.update({
 "q_p": ("Moxyra focuses on product concepts, formulation development, brand development, portfolio expansion and manufacturing coordination. Our products are manufactured through qualified manufacturing partners.",
         "نركّز على أفكار المنتجات وتطوير التركيبات وبناء العلامات وتوسيع المحفظة وتنسيق التصنيع. وتُصنَّع منتجاتنا لدى شركاء تصنيع مؤهلين."),
 "loc_p": ("We have established cooperation with many pharmacies and major pharmacy chains across a number of Egyptian governorates, and we are building broader distribution partnerships. We engage healthcare professionals through scientific communication and product education.",
           "لدينا تعاون قائم مع العديد من الصيدليات وسلاسل صيدليات كبرى في عدد من المحافظات المصرية، ونعمل على بناء شراكات توزيع أوسع. ونتواصل مع متخصصي الرعاية الصحية من خلال التواصل العلمي والتثقيف بالمنتجات."),
 "con_p": ("Tell us who you are and what you are looking for.", "عرّفنا بنفسك وبم تبحث عنه."),
 "zoom": ("Enlarge image", "تكبير الصورة"), "close": ("Close", "إغلاق"),
})
D = {"shower": ("Moisturizing shower gel for sensitive, dry, and very dry skin. SLS-free, paraben-free.", "شاور جل مرطّب للبشرة الحساسة والجافة والجافة جداً. خالٍ من SLS والبارابين."),
     "wash": ("Moisturizing creamy face wash for very dry skin. SLS-free and paraben-free.", "غسول وجه كريمي مرطّب للبشرة شديدة الجفاف. خالٍ من SLS والبارابين."),
     "magnesium": ("Magnesium bisglycinate dietary supplement.", "مكمل غذائي من المغنيسيوم بيسجلايسينات"),
     "respi": ("Dietary supplement that supports respiratory health.", "مكمل غذائي لدعم صحة الجهاز التنفسي")}
PR = [p[:7] + (D.get(p[0], p[7]),) for p in PR]
GROUPS = [("A", [(("Skin care", "العناية بالبشرة"), ["body", "face", "wash", "shower"]), (("Hair care", "العناية بالشعر"), ["antioily", "hydra", "shampoo", "conditioner"])]),
          ("L", [(("Cosmeceuticals", "مستحضرات التجميل العلاجية"), ["leavein", "mask"]), (("Wellness & Dietary Supplements", "الصحة العامة والمكملات الغذائية"), ["bee", "magnesium", "respi", "gaselief"])])]
svg = lambda d: f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{d}"/></svg>'
CI = ["M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10zM9 12l2 2 4-4",
      "M12 15a7 7 0 1 0 0-14 7 7 0 0 0 0 14zM8.2 13.9L7 23l5-3 5 3-1.2-9.1",
      "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8zM14 2v6h6M9 15l2 2 4-4"]
GI = ["M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.3-4.3",
      "M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.2 1 2V17h6v-.3c0-.8.4-1.5 1-2A7 7 0 0 0 12 2z",
      "M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8zM7 7h.01",
      IC[5],
      "M1 3h15v13H1zM16 8h4l3 3v5h-7zM5.5 21a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM18.5 21a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5z",
      "M12 20V10M18 20V4M6 20v-4",
      IC[7]]
def slider(i):
    pv, nx = ("‹", "›") if i == 0 else ("›", "‹")
    ids = ",".join(p[0] for p in PR); names = "|".join(p[3] for p in PR)
    fig = "".join(f'<figure><img src="/assets/img/{p[0]}-480.webp" width="480" height="600" alt="{esc(p[3])}"></figure>' for p in PR[:3])
    return (f'<div class="slider" role="region" aria-roledescription="carousel" aria-label="{("Our products", "منتجاتنا")[i]}" data-ids="{ids}" data-names="{esc(names)}"><div class="row3">{fig}</div>'
            f'<div class="sc"><button class="pv" type="button" aria-label="{("Previous", "السابق")[i]}">{pv}</button><button class="nx" type="button" aria-label="{("Next", "التالي")[i]}">{nx}</button></div></div>')
CSS += """
.c{position:relative}.num{position:absolute;top:.8rem;inset-inline-end:1rem;font:600 1.5rem 'Cormorant Garamond',serif;color:#cdbfe6}
.g3{grid-template-columns:repeat(3,1fr)}.mt{margin-top:3rem}
.pg{margin-bottom:2.5rem}.gh{margin:0 0 .5rem}.gh .bd{font-size:1rem;padding:.25rem 1rem}
.sh4{font:600 1.15rem Inter,'IBM Plex Sans Arabic',sans-serif;margin:1.4rem 0 .8rem;color:var(--purple)}
.slider{max-width:340px}.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:.7rem}
.row3 figure{margin:0;aspect-ratio:4/5;border-radius:var(--r);overflow:hidden;box-shadow:0 14px 30px rgba(0,0,0,.35);background:#2b1a4a;transition:opacity .3s}
.row3 figure:nth-child(2){transform:translateY(-.8rem)}.row3 img{width:100%;height:100%;object-fit:cover}.row3 figure.f{opacity:0}
.sc{justify-content:center;margin-top:1.2rem}
.zi{display:block;width:100%;padding:0;border:0;background:none;cursor:zoom-in;position:relative;overflow:hidden;border-radius:var(--r) var(--r) 0 0}
.zi img{transition:transform .4s}.pc:hover .zi img{transform:scale(1.05)}
.zm{position:absolute;bottom:.6rem;inset-inline-end:.6rem;background:rgba(90,59,131,.9);color:#fff;border-radius:50%;width:2rem;height:2rem;display:grid;place-items:center;font-size:1.3rem}
.bc.ic{cursor:default}
dialog{border:0;padding:0;background:#fff;border-radius:12px;width:min(92vw,560px);overflow:visible}
dialog::backdrop{background:rgba(10,5,20,.78)}dialog img{display:block;width:100%;max-height:88vh;object-fit:contain;border-radius:12px}
.x{position:absolute;top:-.8rem;inset-inline-end:-.8rem;width:2.4rem;height:2.4rem;border-radius:50%;border:0;background:var(--teal);color:#0c1f1c;font-size:1.5rem;cursor:pointer;z-index:2}
@media(max-width:600px){.g3{grid-template-columns:1fr}.brand{font-size:1rem;letter-spacing:.06em;line-height:1.1;gap:.4rem}.brand img{height:44px}
.bar{gap:.5rem}.lang,#mb{padding:.3rem .6rem;font-size:.85rem}section{padding:3rem 0}.hero{padding:2.5rem 0 3rem}.slider{max-width:300px}}
"""
JS = r"""(function(){var b=document.getElementById('mb'),n=document.getElementById('nav');
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
function play(){stop();if(!matchMedia('(prefers-reduced-motion:reduce)').matches)t=setInterval(function(){go(1)},3000)}
s.querySelector('.pv').onclick=function(){go(-1)};s.querySelector('.nx').onclick=function(){go(1)};
s.addEventListener('mouseenter',stop);s.addEventListener('mouseleave',play);s.addEventListener('focusin',stop);s.addEventListener('focusout',play);play()}
var lb=document.getElementById('lb');if(lb){document.querySelectorAll('.zi').forEach(function(z){z.addEventListener('click',function(){var im=lb.querySelector('img');im.src=z.dataset.full;im.alt=z.dataset.alt;lb.showModal()})});
lb.addEventListener('click',function(e){if(e.target===lb||e.target.className=='x')lb.close()})}
var f=document.getElementById('cf');if(f)f.addEventListener('submit',function(e){e.preventDefault();var s=f.querySelector('.fs'),b=f.querySelector('button'),d=new FormData(f);
if(d.get('_honey'))return;b.disabled=true;
fetch('https://formsubmit.co/ajax/info@moxyrapharma.com',{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({name:d.get('n'),company:d.get('c'),email:d.get('e'),type:d.get('t'),message:d.get('m'),_subject:'Moxyra website enquiry',_replyto:d.get('e')})})
.then(function(r){return r.json()}).then(function(j){if(j.success===true||j.success==='true'){s.textContent=f.dataset.ok;f.reset()}else throw 0}).catch(function(){s.textContent=f.dataset.err}).finally(function(){b.disabled=false})})})();
"""

def vm(i):
    return (f'<div class="vm2"><div class="c ic vc v" tabindex="0"><span class="ico big">{EYE}</span><h3>{esc(X("vis_h", i))}</h3><p>{esc(X("vis", i))}</p></div>'
            f'<div class="c ic vc m" tabindex="0"><span class="ico big">{TGT}</span><h3>{esc(X("mis_h", i))}</h3><p>{esc(X("mis", i))}</p></div></div>')
CSS += """
.slider{max-width:510px}
@media(min-width:901px){.hero .w{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.slider{max-width:100%}}
.vm2{display:grid;gap:1.2rem}
.vc{padding:1.8rem;border-top:5px solid var(--purple)}.vc.m{border-top-color:#00857a}
.vc .ico.big{width:64px;height:64px;margin-bottom:1.1rem}.vc .ico.big svg{width:32px;height:32px}
.vc h3{font-size:1.45rem}.vc p{color:var(--ink);font-size:1.03rem}
.vc.m .ico svg{stroke:#00857a}
.vc.m:hover,.vc.m:focus-visible{border-color:#00857a}
.vc.m:hover .ico,.vc.m:focus-visible .ico{background:#00857a}
.vc.m:hover .ico svg,.vc.m:focus-visible .ico svg{stroke:#fff}
"""

CSS += """
.vc.v{background:linear-gradient(135deg,#3b2563,#5A3B83)}.vc.m{background:linear-gradient(135deg,#0a4f8f,#00857a)}
.vc,.vc:hover,.vc:focus-visible,.vc.m:hover,.vc.m:focus-visible{border-color:#cdb8ee}.vc.m,.vc.m:hover,.vc.m:focus-visible{border-color:#8fe0d5}
.vc h3{color:#fff}.vc p{color:#f0eafb}
.vc .ico,.vc.m .ico{background:rgba(255,255,255,.18)}
.vc .ico svg,.vc.m .ico svg{stroke:#fff}
.vc:hover .ico,.vc:focus-visible .ico{background:#fff}.vc.m:hover .ico,.vc.m:focus-visible .ico{background:#fff}
.vc:hover .ico svg,.vc:focus-visible .ico svg{stroke:#5A3B83}.vc.m:hover .ico svg,.vc.m:focus-visible .ico svg{stroke:#00857a}
.vc:hover,.vc:focus-visible{box-shadow:0 16px 32px rgba(40,20,80,.3)}
"""

MAILP = "M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zM22 6l-10 7L2 6"
CHATP = "M21 11.5a8.4 8.4 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.4 8.4 0 0 1-3.8-.9L3 21l1.9-5.7a8.4 8.4 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.4 8.4 0 0 1 3.8-.9h.5a8.5 8.5 0 0 1 8 8z"
PINP = "M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0zM12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"
C["con_p"] = ("Reach us by email or WhatsApp and tell us who you are and what you are looking for.", "تواصل معنا عبر البريد أو واتساب، وعرّفنا بنفسك وبم تبحث عنه.")
import re as _re
JS, n_ = _re.subn(r"var f=document\.getElementById\('cf'\);.*?\.finally\(function\(\)\{b\.disabled=false\}\)\}\)", "", JS, flags=_re.S); assert n_ == 1
CSS += """
.cc{margin-top:1.5rem}.ct .sh p{color:#b9c6d1}
.ct a.c{color:var(--ink);text-decoration:none;display:block}.ct .c h3{color:var(--dark)}.ct .c p{color:var(--mute);overflow-wrap:anywhere}
"""

C.update({
 "lead": ("Building distinctive healthcare and beauty brands through innovation, product development, and quality-focused partnerships.",
          "نطوّر علامات تجارية متميزة في مجالات الرعاية الصحية والجمال، من خلال الابتكار وتطوير المنتجات وشراكات التصنيع القائمة على الجودة."),
 "cta1": ("Explore Our Portfolio", "استكشف منتجاتنا"), "cta2": ("Become a Partner", "كن شريكًا لنا"),
 "explore": ("Explore products", "استكشف المنتجات"),
 "discuss": ("Discuss Distribution Opportunities", "ناقش فرص التوزيع معنا"),
 "f_tag": ("Where Innovation Meets Healthcare", "حيث يلتقي الابتكار بالرعاية الصحية"),
 "f_links": ("Quick links", "روابط سريعة"), "f_contact": ("Contact", "تواصل معنا"),
 "facts": [("Products in our portfolio", "منتجًا في محفظتنا"), ("Commercially available", "منتجات مطروحة تجاريًا"), ("Licensed / approved", "منتجات مرخّصة / معتمدة"), ("Brand groups", "مجموعات علامات")],
})
def facts(i):
    n = len(PR); na = sum(p[2] == "A" for p in PR); nl = sum(p[2] == "L" for p in PR); nb = len(C["brands"])
    return '<div class="facts"><div class="w">' + "".join(f'<div><b>{v}</b><span>{esc(C["facts"][k][i])}</span></div>' for k, v in enumerate((n, na, nl, nb))) + '</div></div>'
def footer_html(i):
    nv = "".join(f'<li><a href="#{k}">{esc(a if i == 0 else b)}</a></li>' for k, a, b in C["nav"])
    return (f'<footer class="ft"><div class="w fg"><div><img src="/assets/img/logo-white.png?v={VER}" width="170" height="115" alt="Moxyra Pharma" loading="lazy"><p class="ftl">{esc(X("f_tag", i))}</p></div>'
            f'<div><h4>{esc(X("f_links", i))}</h4><ul>{nv}</ul></div>'
            f'<div><h4>{esc(X("f_contact", i))}</h4><ul><li><a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to={E}" target="_blank" rel="noopener">{E}</a></li>'
            f'<li><a href="https://wa.me/201099688827" target="_blank" rel="noopener" dir="ltr">{P}</a></li><li>{esc(X("city", i))}</li></ul></div></div>'
            f'<div class="w fb">{esc(X("foot", i))}</div></footer>')
CSS += """
:root{--purple-d:#2b1a4a;--lav:#cdb8ee;--sh-1:0 1px 2px rgba(26,37,47,.06),0 10px 28px rgba(26,37,47,.07);--t:.25s ease}
.bar{min-height:64px}nav a[aria-current]{border-color:var(--purple);color:var(--purple)}
.btn{min-height:48px;display:inline-flex;align-items:center;justify-content:center;transition:filter var(--t),transform var(--t),background var(--t)}.btn:hover{transform:translateY(-1px)}
.btn.sm{min-height:40px;padding:.4rem 1.1rem;font-size:.92rem}.btn.p{background:var(--purple);border-color:var(--purple);color:#fff}
.btn.d{background:transparent;color:var(--purple);border-color:var(--purple)}.btn.d:hover{background:var(--purple);color:#fff}.nc{display:none}
.hero{position:relative;background:radial-gradient(ellipse at 85% 10%,#5A3B83 0%,transparent 55%),linear-gradient(135deg,#1c1030 0%,#34205a 100%)}
.hero::before{content:"";position:absolute;inset-block:-12%;inset-inline-end:-6%;width:52%;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%23a8b8f5'/%3E%3Cstop offset='1' stop-color='%235A3B83'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M70 20h80l190 360h-80z' fill='url(%23g)'/%3E%3Cpath d='M330 20h-80L60 380h80z' fill='url(%23g)' opacity='.7'/%3E%3C/svg%3E") no-repeat center/contain;opacity:.16;pointer-events:none}
.hero .w{position:relative}
.facts{background:#fff;border-bottom:1px solid var(--line)}.facts .w{display:grid;grid-template-columns:repeat(4,1fr)}
.facts>.w>div{padding:1.4rem 1rem;border-inline-end:1px solid var(--line);text-align:center}.facts>.w>div:last-child{border:0}
.facts b{display:block;font:600 2.2rem/1 'Cormorant Garamond',serif;color:var(--purple)}[lang=ar] .facts b{font-family:'IBM Plex Sans Arabic',sans-serif}
.facts span{font-size:.88rem;color:var(--mute)}
.tl{display:inline-block;margin-top:.6rem;font-weight:600;color:var(--purple);text-decoration:none}.tl:hover{text-decoration:underline}
.bc{box-shadow:var(--sh-1)}.bc img{transition:transform .5s}.bc:hover img{transform:scale(1.04)}
.ft{background:linear-gradient(135deg,#1c1030,#2b1a4a);color:#cfc3e6;padding:3.5rem 0 1.5rem}
.fg{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:2.5rem}.ft h4{color:#fff;margin:0 0 .8rem;font-size:1rem}
.ft ul{list-style:none;margin:0;padding:0}.ft li{margin:.35rem 0}.ft a{color:#cfc3e6;text-decoration:none}.ft a:hover{color:#8fe0d5}.ftl{max-width:22rem;margin-top:1rem}
.fb{border-top:1px solid rgba(255,255,255,.12);margin-top:2rem;padding-top:1.2rem;font-size:.9rem}
@media(max-width:900px){.hc{display:none}.nc{display:block;padding:.6rem 0 .8rem}.nc .btn{width:100%}
.facts .w{grid-template-columns:repeat(2,1fr)}.facts>.w>div:nth-child(2){border-inline-end:0}.facts>.w>div:nth-child(-n+2){border-bottom:1px solid var(--line)}
.fg{grid-template-columns:1fr}.hero::before{width:90%;opacity:.1}}
"""
JS += r"""(function(){var ls=[].slice.call(document.querySelectorAll('#nav a[href^="#"]')),m={};ls.forEach(function(a){m[a.getAttribute('href').slice(1)]=a});
if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ls.forEach(function(a){a.removeAttribute('aria-current')});var a=m[e.target.id];if(a)a.setAttribute('aria-current','true')}})},{rootMargin:'-45% 0px -50% 0px'});
Object.keys(m).forEach(function(k){var s=document.getElementById(k);if(s)o.observe(s)})})();
"""
VER = hashlib.md5((CSS + JS).encode()).hexdigest()[:8]

for i in (0, 1): w(f"{LANG[i][0]}/index.html", page(i))
w("assets/main.css", CSS); w("assets/main.js", JS)
red = lambda t: f'<!DOCTYPE html><meta charset="utf-8"><title>Moxyra Pharma</title><link rel="canonical" href="{BASE}{t}"><meta http-equiv="refresh" content="0;url={t}"><a href="{t}">Moxyra Pharma</a>'
w("home.html", red("/ar/")); w("en.html", red("/en/"))
w("index.html", f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Moxyra Pharma | موكسيرا فارما</title>
<link rel="canonical" href="{BASE}/"><link rel="alternate" hreflang="en" href="{BASE}/en/"><link rel="alternate" hreflang="ar" href="{BASE}/ar/"><link rel="alternate" hreflang="x-default" href="{BASE}/">
<style>body{{font:1.2rem system-ui;display:grid;place-items:center;min-height:100vh;margin:0;background:#2b1a4a;color:#fff;text-align:center}}a{{color:#8fe0d5;margin:0 1rem;font-size:1.4rem}}</style>
<script>var l=(navigator.language||'').slice(0,2);location.replace(l=='ar'?'/ar/':'/en/')</script></head>
<body><div><h1>MOXYRA PHARMA</h1><p><a href="/en/">English</a><a href="/ar/">العربية</a></p></div></body></html>''')
w("404.html", '<!DOCTYPE html><meta charset="utf-8"><title>404 | Moxyra Pharma</title><meta name="viewport" content="width=device-width,initial-scale=1"><body style="font:1.2rem system-ui;text-align:center;padding:4rem"><h1>404</h1><p><a href="/en/">English home</a> · <a href="/ar/">الصفحة الرئيسية</a></p></body>')
w("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(
    f'<url><loc>{BASE}/{c}/</loc><xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/"/><xhtml:link rel="alternate" hreflang="ar" href="{BASE}/ar/"/></url>\n' for c in ("en", "ar")) + "</urlset>\n")
w("_redirects", "/home.html /ar/ 301\n/en.html /en/ 301\n")
w("_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
print("built", OUT)
