# Catalogue 2 ("PRODUCT CATALOGUE", 223 pages) transcribed visually.
# page = original PDF page number = the printed "PAGE N" label (exceptions noted). Page 1 (cover) and
# page 223 (back cover / supplier contact page) are removed from the published catalogue.
# The trimmed PDF keeps original pages 2-222, so trimmed-PDF page = original page - 1.
# The catalogue prints no model numbers except two: F-191 (p.98) and P207 (p.95); those are published
# with the prefix "N". Every other product gets a reference code N-P<page>-<k> instead (see export).
# Arabic names are translations of the English catalogue text (rosary pages are printed in Arabic).
D2=[]
def P(page,cat,ar,en,specs,variants,box=None,note=''):
    D2.append(dict(page=page,cat=cat,ar=ar,en=en,specs=specs,variants=variants,box=box,note=note))
def C(s,model=''):  # 'black gray navy' -> variants without printed model
    out=[]
    for tok in s.split():
        k,_,lab=tok.partition('@'); out.append((model,k,lab.replace('_',' ')))
    return out
KIT='kits'; BAG='bags'; NB='notebooks'; ISL='islamic'; KEY='keychains'; CH='cardholders'; FR='fragrance'
EL='electronics'; DRK='drinkware'; PEN='pens'; ACC='accessories'; PRO='promo'; MP='mousepads'; BDG='badges'; CRT='certificates'

# ---- Employees welcome kits ----
P(4,BAG,'حقيبة لابتوب أنيقة (ظرف)','Elegant laptop bag (sleeve)','تصميم موحّد بعدة ألوان - مناسبة لهدايا الموظفين الجدد - قابلة للطباعة بالشعار',
  C('black@ص_17 gray@ص_7 navy@ص_13 green@ص_10 purple@ص_5'))
P(6,KIT,'طقم ترحيب الموظفين','Employees welcome kit','حقيبة لابتوب + نوت بوك، قلم معدني، حامل بطاقات مع ستاند جوال MagSafe، شريط تعليق، حامل بطاقة يويو معدني، حامل بطاقة تعريف',
  C('purple@ص_6 gray@ص_9 green@ص_11 navy@ص_16 black@ص_20'),note='صفحة 6 مكتوب عليها «Gray color» بينما الطقم المصوَّر بنفسجي؛ الأخضر بعنوان «Executive Office Gift Set in Dark Green»')
P(8,KIT,'طقم ترحيب المدراء','Managers welcome kit','نوت بوك، قلم، باور بانك، حامل بطاقات، ميدالية',
  C('gray@ص_8 green@ص_12 navy@ص_15 black@ص_19'))
P(24,KIT,'بوكس ترحيب بمقبض','Welcome kit box with handle','نوت بوك بشريط مطاطي، قلم، باور بانك، زمزمية حرارية، فلاش USB - بوكس بغطاء مائل ومقبض',
  C('white@ص_24 gray@ص_25 green@ص_26 navy@ص_27 black@ص_27'))
P(28,KIT,'طقم السفر (Flying set)','Flying set','علبة مغناطيسية قابلة للطي + كيس ورقي؛ قلم معدني، ميدالية، بروش معدني، حامل بطاقات مغناطيسي، نوت بوك',
  C('purple@ص_28 green@ص_29 white@ص_30 black@ص_32 navy@ص_33'),note='الصفحة 32 مطبوع عليها «PAGE 31»')
P(34,KIT,'طقم هدايا مكتبي فاخر','Luxury office gift set','علبة بدرج منزلق ولوحة قابلة للحفر؛ نوت بوك، قلم، باور بانك، ميدالية',
  C('black@ص_34 green@ص_35 navy@ص_36 white@ص_37'))
P(38,KIT,'طقم مكتبي تنفيذي (بوكس مغناطيسي)','Executive office set (welcome kit)','علبة مغناطيسية بيضاء؛ نوت بوك جلد، قلم معدني، مج حراري',
  C('red@ص_38 black@ص_39 purple@ص_40 gray@ص_41 navy@ص_42 white@ص_43 green@ص_44'))
P(45,KIT,'طقم ترحيب صديق للبيئة','Eco-friendly welcome kit','نوت بوك فلين، قلم، حامل كروت شخصية، ميدالية',C('cork'))
P(46,KIT,'طقم مكتبي طبيعي 3 في 1','3-in-1 natural office gift set','زجاجة زجاج بغطاء بامبو، شمعة معطّرة، كوب زجاج مزدوج الجدار - مقاس البوكس 24.5×21.5 سم',C('natural'))
P(48,KIT,'طقم مكتبي أنيق (بوكس بمقبض)','Stylish office gift set','بوكس بمقبض قماش؛ نوت بوك + قلم معدني',
  C('gray@ص_48 black@ص_48 purple@ص_49 navy@ص_49 white@ص_50 green@ص_50'),note='صفحة 51 تعرض البوكس مغلقًا بالألوان الستة')
P(52,NB,'نوت بوك وقلم بذور صديق للبيئة','Eco-friendly notebook & seed pen','غلاف خشبي - شريط أخضر',C('natural'))
P(53,NB,'نوت بوك صديق للبيئة مع حامل جوال','Eco-friendly notebook with mobile holder','مصنوع من قش الأرز / كراتين الحليب المعاد تدويرها',C('kraft'))
P(54,NB,'طقم نوت بوك وقلم فلين / قماش صديق للبيئة','Eco-friendly cork & fabric notebook and pen set','',C('cork'))
P(55,BAG,'حقيبة لابتوب ومحطة عمل','Laptop case & workstation','33×28 سم - تتحول إلى ستاند للابتوب',C('black gray green navy beige'),note='الصفحتان 55-56')
P(57,CRT,'ملف شهادات جلد','Leather certificates folder','لحفظ وتقديم شهادات التخرج - مكان للشعار',C('black white navy green'),note='الصفحتان 57-58')
# ---- Prayer beads (misbaha) ----
RS='مسبحة 33 حبة - بلاكة قابلة للحفر بالاسم أو الشعار - علبة سوداء فاخرة'
P(60,ISL,'سبحة من العقيق الطبيعي','Natural agate prayer beads',RS,C('brown@عقيق'))
P(61,ISL,'سبحة من الحجر الطبيعي (رمادي مرقّط)','Natural stone prayer beads (snowflake)',RS,C('gray/black'))
P(62,ISL,'سبحة من الحجر الطبيعي (أبيض)','Natural stone prayer beads (white)',RS,C('white'))
P(63,ISL,'سبحة من الحجر الطبيعي (أسود) مع قلم','Natural stone prayer beads (black) with pen',RS+' - يمكن إضافة قلم',C('black'))
P(64,ISL,'سبحة من الحجر الطبيعي (وردي)','Natural stone prayer beads (pink)',RS,C('pink'))
P(65,ISL,'سبحة من الحجر الطبيعي (بني مرقّط)','Natural stone prayer beads (brown, speckled)',RS,C('brown/gray'))
P(66,ISL,'سبحة من الحجر الطبيعي (أخضر)','Natural stone prayer beads (green)',RS,C('green'))
P(67,ISL,'سبحة بلاستيك 33 حبة','Plastic prayer beads, 33 beads','مسبحة - بلاكة دائرية قابلة للحفر - كيس مخمل',
  C('greenmarble@ص_67 black@ص_68 olive@ص_69 darkolive@ص_70 purple@ص_71 blue@ص_72 teal@ص_73'))
# ---- Keychains ----
P(74,KEY,'ميدالية سيارة بحزام جلد','Car keychain with leather strap','سبيكة زنك - حزام جلد',C('black green navy'))
P(75,KEY,'ميدالية بحزام قماش منسوج','Keychain with woven fabric strap','',C('black blue green navy'))
P(76,KEY,'ميدالية بشريط ملوّن وحلقة لامعة','Keychain with coloured band & shiny ring','',C('black white green navy peach'))
# ---- Wallets & card holders ----
P(77,CH,'محفظة مغناطيسية وستاند MagSafe','Magnetic wallet & stand (MagSafe)','جلد - جيوب للبطاقات والصور',C('black gray blue'),note='الصفحتان 77-78')
P(79,CH,'حامل بطاقات مغناطيسي MagSafe مع ستاند','Magnetic MagSafe card holder with stand','6.5×9.5 سم',C('black gray white navy green purple'),note='الصفحتان 79-80')
P(81,CH,'محفظة بطاقات (Pop-up)','Cards wallet (pop-up card holder)','6×9.5 سم',C('black gray green blue'))
P(82,CH,'حامل كروت شخصية جلد ومعدن','Business card holder (leather & metal)','',C('black gray navy green'))
P(83,CH,'حامل كروت شخصية جلد بغطاء معدني','Business card holder (leather, metallic shell)','',C('black gray white navy'))
# ---- Fragrance ----
P(85,FR,'فواحة أعواد (ريد ديفيوزر)','Reed diffuser','100 مل - صلاحية 3 سنوات - زجاجة سوداء بغطاء ذهبي',C('black'))
P(86,FR,'معطر سيارة','Car air freshener','4.5×2.5 سم',C('purple blue green'))
P(87,FR,'مبخرة كهربائية معدن','Electric incense burner (metal)','كابل USB، حقيبة حفظ وملحقات - للاستخدام المنزلي',C('black green'),note='الصفحتان 87-88')
P(89,FR,'فواحة سيارة (مرطب)','Vehicle humidifier / diffuser','تعمل بقطرات الزيت العطري',C('black silver'))
# ---- Electronics ----
P(91,EL,'باور بانك مغناطيسي MagSafe لاسلكي 10000mAh','MagSafe magnetic wireless power bank 10000mAh','شحن سريع QC 22.5W و PD 20W - ستاند قابل للطي - بطارية ليثيوم بوليمر',C('navy black'))
P(92,EL,'باور بانك مغناطيسي بستاند قابل للطي','Foldable magnetic charging stand / power bank','شحن لاسلكي MagSafe - يستخدم كستاند أثناء الشحن',C('black white navy'))
P(93,EL,'باور بانك لاسلكي 10000mAh بشاشة رقمية','Wireless power bank 10000mAh with digital display','138×71×16 مم - مخرجين USB - Type-C - شاحن لاسلكي',C('navy white black'))
P(94,EL,'باور بانك MagSafe لاسلكي','MagSafe wireless power bank','متوافق مع جميع الهواتف الذكية والأجهزة اللوحية',C('black white gray green navy blue'))
P(95,EL,'شاحن لاسلكي وباور بانك فلين','Wireless charger & power bank (cork)','10000mAh / 37Wh - مدخل Type-C 5V 2A - مخرج USB 5V 2.1A - لاسلكي 5W',
  [('P207','cork','')],note='رقم الموديل مطبوع: Model No: P207 - لون واحد فقط')
P(96,EL,'باور بانك 8000mAh','Power bank 8000mAh (mobile power station)','37Wh - Type-C / Micro - مخرجين USB 5V/2A - بلاستيك مطفي مقاوم للبصمات',C('black gray white navy green'),note='الصفحتان 96-97')
P(98,EL,'ستاند شحن مغناطيسي قابل للطي 3 في 1','3-in-1 folding magnetic wireless charging stand','MagSafe 15W - دوران 360° - للجوال والساعة والسماعات',
  [('F-191','white',''),('F-191','black','')],note='رقم الموديل مطبوع: Product model: F-191 (الصفحتان 98-99)')
P(100,EL,'شاحن متعدد 3 في 1 قابل للطي','Multi charger 3-in-1 (foldable)','للجوال والساعة والسماعات - قاعدة مثلثة قابلة للطي',C('black gray white navy'),note='الصفحتان 100-101')
P(102,EL,'ستاند شحن لاسلكي 3 في 1 متعدد الوظائف','Multi-functional 3-in-1 foldable wireless charging stand','وضع ستاند أو وضع مسطح - قابل للطي',C('black white'),note='الصفحتان 102-103')
P(104,EL,'شاحن سيارة مغناطيسي لاسلكي','Magnetic wireless car charger','15W شحن سريع - 9.4×6.4 سم',C('black white'))
P(105,EL,'ستاند شاحن لاسلكي فلين','Cork wireless charger stand','قابل للطي - 5W - 8.5×14.4 سم - كابل Micro USB 30 سم',C('cork'))
P(106,EL,'ماوس باد بشاحن لاسلكي','Mouse pad with wireless charger','فلين - مدخل DC9V/2A - شحن لاسلكي 15W',C('cork'))
P(107,EL,'حامل أقلام بشاحن لاسلكي (قش القمح)','Wheat straw wireless charger & pen holder','15W - قاعدة بامبو - معاد تدويره من قش الأرز/القمح',C('natural'))
P(108,EL,'منظم مكتب بشاحن لاسلكي','Wireless charging pencil case / organizer','15W - مخارج USB و Type-C - حامل أقلام',C('black white navy'))
P(109,EL,'حامل أقلام ذكي بشاحن لاسلكي','Smart pen case with wireless charger','',C('white black'))
P(110,EL,'محوّل سفر عالمي','Universal travel adapter','أكثر من 150 دولة - مقابس UK / US / EU / AUS',C('black white'))
P(111,EL,'طقم كابلات بيانات','Data cable set','علبة دائرية 8 سم - Type-C/Lightning/Micro/USB - تتحول إلى ستاند جوال',C('black gray white navy'),note='الصفحتان 111-112')
P(113,EL,'فلاش ميموري Type-C + USB دوّار','Flash memory Type-C + USB 3.0 (360° rotation)','منفذين: USB-A و Type-C',C('silver'))
P(114,EL,'فلاش USB بشعار مضيء','Illuminated logo USB flash drive','USB-C أو USB-A - الشعار يضيء عند التوصيل',C('black'))
P(115,EL,'فلاشات USB معدنية','Metal USB flash drives','معدن مقاوم للخدش - أشكال متنوعة - تعليق بالميدالية',C('silver@أشكال_متنوعة'))
P(116,EL,'فلاش USB صديق للبيئة 16GB','Eco flash drive 16GB (wheat straw)','USB 2.0 - قش القمح والبولي بروبيلين',C('natural'))
# ---- Bottles & mugs ----
P(118,DRK,'مج قهوة حراري 260 مل','Vacuum coffee mug 260 ml','13×8 سم - غطاء مانع للتسريب',C('black beige navy green'),note='الصفحتان 118-119')
P(120,DRK,'مج قهوة حراري صغير بقاعدة فلين 180 مل','RCS recycled-steel cork vacuum coffee mug 180 ml','ستيل معاد تدويره (RCS) - قاعدة فلين',C('navy white silver black'))
P(121,DRK,'كوب قهوة 350 مل','Coffee mug 350 ml','ستيل مقاوم للصدأ - غطاء محكم مع فتحة للشرب أو للمصاصة',C('black gray white navy pink'))
P(122,DRK,'زمزمية 500 مل بستاند جوال MagSafe','Water bottle 500 ml with MagSafe phone stand','حرارة / برودة 12 ساعة - SS304 داخلي / SS201 خارجي',C('black gray white navy'),note='الصفحتان 122-123')
P(124,DRK,'زمزمية ماء معزولة','Insulated water bottle','جدار مزدوج - غطاء مانع للتسريب',C('black gray white navy green purple'))
P(125,DRK,'زمزمية ذكية بشاشة حرارة','Smart thermos (LED temperature display)','شاشة لمس LED - مصفاة شاي ستيل 304',C('black gray white green pink purple navy maroon'),note='الصفحتان 125-126')
P(127,DRK,'زمزمية ذكية 200 مل','Smart thermos 200 ml','حرارة 12 ساعة / برودة 24 ساعة - مصفاة',C('black gray white green pink navy purple'))
P(128,DRK,'زمزمية بامبو 500 مل','Bamboo thermos 500 ml','7×24 سم - غلاف بامبو - غطاء سيليكون - ستيل غذائي - شاشة حرارة',C('natural'))
P(129,DRK,'زمزمية سيليكون قابلة للطي','Collapsible water bottle','سيليكون غذائي - خالية من BPA - 13 سم مطوية / 24 سم مفتوحة',C('black gray navy green teal pink'))
P(130,DRK,'زمزمية ماء بفلتر فواكه','Infuser water bottle','بلاستيك شفاف بفلتر داخلي للفواكه',C('black white red blue'))
P(131,DRK,'مج سيراميك بقاعدة فلين وغطاء','Cork base ceramic mug','بورسلين - غطاء مانع للرذاذ - قاعدة فلين - مقبض كبير',C('black gray white green navy purple'))
P(132,DRK,'طقم كوسترات فلين دائرية مع حامل','Round cork coaster set with stand','فلين طبيعي - عازل للحرارة - غير قابل للانزلاق',C('cork'))
P(133,DRK,'طقم كوسترات فلين مربعة مع حامل','Square cork coaster set with holder','4 قطع - 10×10 سم في الرسم (المواصفات تذكر 12×12 سم بسماكة 3)',C('cork'))
P(134,PRO,'أصيص زرع فلين','Cork flower pot','فلين طبيعي - يُقدَّم فارغًا للزراعة - علبة كرافت',C('cork'))
P(135,DRK,'علبة طعام صديقة للبيئة','Eco-friendly lunch box','غطاء بلمسة خشبية - أدوات طعام (ملعقة، شوكة، سكين) - رباط مطاطي',C('cream'),note='لون واحد فقط')
# ---- Notebooks ----
P(137,NB,'نوت بوك ذكي MagSafe','Smart notebook MagSafe','باور بانك 10000mAh / 38Wh - شحن لاسلكي MagSafe 10W - فلاش 32GB - شعار مضيء - كابلات مدمجة',C('black gray blue'),note='الصفحات 137-139')
P(140,NB,'نوت بوك بشاحن لاسلكي وباور بانك وفلاش','Wireless charger notebook with power bank & USB flash','باور بانك 10000mAh / 38Wh - فلاش 16GB - شعار مضيء - أوراق قابلة للتبديل',C('black gray green blue'),note='الصفحات 140-143')
P(144,NB,'منظم نوت بوك A5','Notebook organizer A5','جيوب للبطاقات - نافذة شفافة لبطاقة التعريف - إغلاق مغناطيسي',C('black gray white green purple navy'),note='الصفحتان 144-145')
P(146,NB,'منظم نوت بوك A6','Notebook organizer A6','إغلاق مغناطيسي - حواف دائرية',C('black gray white navy sage'),note='مطبوع على الصفحة «PAGE 52» (الصفحة 146 في الملف)')
P(147,NB,'نوت بوك جيب A5 بخطوط بارزة','Pocket A5 notebook (textured cover)','14.5×21 سم - غلاف علوي بخطوط عمودية',C('black gray white purple green blue'),note='الصفحتان 147-148')
P(149,NB,'نوت بوك مع حامل قلم','Notebook with pen holder','A5 (14×21 سم) - غلاف صلب - رباط مطاطي وشريط فاصل',C('black gray white purple green yellow blue cork'),note='الصفحتان 149-150')
P(151,NB,'نوت بوك Curve','Curve notebook','غلاف ملمس جلد بزوايا دائرية - فاصل أحمر',C('black gray white purple red green navy brown pink sky'),note='الصفحتان 151-152')
P(153,NB,'نوت بوك صديق للبيئة بمسطرة','Eco-friendly notebook with ruler','قش الأرز المعاد تدويره - مسطرة كرتون 0-20 سم',C('kraft'))
P(154,NB,'نوت بوك صديق للبيئة بقاعدة فلين','Eco-friendly easel notebook (cork base)','قاعدة مائلة - حامل قلم - قش الأرز',C('white'))
P(155,NB,'منظم ستيكي نوت (فوليو)','Sticky note folio organizer','غلاف صلب - ستيكي نوت وفواصل نيون - مفكرة',C('gray blue green cork'))
P(156,NB,'طقم ستيكي نوت بعلبة جلد وتقويم','Sticky note set with leather box & calendar','فواصل ملونة لاصقة - تقويم 2024',C('white'))
P(157,NB,'بوكس ستيكي نوت قابل للطي','Foldable sticky notes memo box','10×11.5×8.8 سم - 5 ألوان فواصل - 200 ورقة - مشابك وقلم',C('green beige navy'))
P(158,NB,'ستيكي نوت مع نوت وقلم','Sticky notes with post notes & pen','جيبين داخليين - حامل قلم - شريطين فاصلين',C('white cork blue purple'))
P(159,NB,'دفتر ستيكي نوت','Sticky notebook','10.5×15.5×2.3 سم - قلم كرتون معاد تدويره - 70 ورقة - 25 ستيكي 7.5×7.5 - 125 ستيكي صغير',C('gray blue green cork'))
# ---- Pens ----
P(161,PEN,'قلم معدني مع علبة كرتون','Metal pen with cardboard box','',C('gunmetal'),note='لون واحد فقط')
P(162,PEN,'قلم ستيل','Steel pen','',C('black gray'))
P(163,PEN,'قلم معدني مطاطي (حلقة لامعة)','Rubber metal pen (shiny ring)','',C('black white navy green'))
P(164,PEN,'قلم معدني','Metal pen','نصف معدن ونصف قماش',C('black gray white navy green purple'))
P(165,PEN,'قلم معدني مطاطي','Rubber metal pen','',C('black gray white navy blue'))
P(166,PEN,'قلم مستدام 2 في 1','Sustainable pen (2-in-1)','قلم حبر جاف + قلم بدون حبر برأس معدني',C('black gray white navy blue'))
P(167,PEN,'قلم ألمنيوم بفلين وقلم لمس','Aluminium pen with cork & stylus','',C('black gray white navy'))
P(168,PEN,'قلم ألمنيوم بقلم لمس','Aluminium pen with stylus','ملمس مطاطي',C('black gray white navy purple green sky blue red'))
P(169,PEN,'قلم ألمنيوم','Aluminium pen','',C('black gray white navy green blue magenta'))
P(170,PEN,'قلم بحامل جوال','Mobile pen holder (pen with phone stand)','',C('black white blue'))
P(171,PEN,'قلم بلاستيك','Plastic pen','',C('black gray white navy green sky blue red purple pink'))
P(172,PEN,'قلم بلاستيك 1.0 مم','Plastic pen (1.0 mm)','',C('black white blue sky'))
P(173,PEN,'قلم فلين صديق للبيئة','Eco-friendly cork pen','',C('cork'))
P(174,PEN,'قلم رصاص بالبذور (للزراعة)','Plant pen (seed pencil)','ورق جرائد معاد تدويره - بذرة في الطرف',C('natural'),note='لون واحد فقط')
P(175,PEN,'قلم رصاص','Lead pencil','18 سم',C('black white'))
P(176,PEN,'علبة أقلام دائرية','Round pen box','',C('black silver white'))
P(177,PEN,'علبة أقلام','Pen box','مستطيلة بفاصل معدني فضي',C('black navy'))
# ---- Bags ----
P(179,BAG,'شنطة كانفاس VIP','VIP canvas bag','36×28×12.5 سم - جيب أمامي وجيب شبك - لوحة معدنية قابلة للحفر - سحاب علوي',C('gray charcoal bluegray'))
P(180,BAG,'شنطة توت','Tote bag','قماش منسوج - مقاسات 21.5×29 / 29×34.5 / 36×40 سم',
  C('black white gray beige red blue purple lightgreen green navy'),note='الصفحات 180-184')
P(185,BAG,'شنطة توت صديقة للبيئة بقاعدة فلين','Eco-friendly tote bag (cork base)','40×36 سم',C('beige/cork'))
P(186,BAG,'حقيبة ظهر برباط صديقة للبيئة بقاعدة فلين','Eco-friendly drawstring backpack (cork base)','40×36 سم - قطن',C('beige/cork'))
P(187,BAG,'حقيبة ظهر برباط صديقة للبيئة','Eco-friendly drawstring backpack','40×36 سم',C('beige'))
P(188,BAG,'حقيبة ظهر سبليميشن','Sublimation drawstring bag','33.5×39.5 سم - أبيض للطباعة',C('white'))
P(189,BAG,'شنطة سبليميشن','Sublimation bag','A3: 24.5×41.5 سم - A4: 24.5×30.5 سم',C('white@A3 white@A4'))
P(190,BAG,'كيس قماش صغير برباط','Small drawstring pouch (eco)','14.5×21 سم',C('beige'))
# ---- Accessories ----
P(191,ACC,'حامل جوال بامبو','Bamboo mobile holder','',C('natural'))
P(192,ACC,'ستاند جوال قابل للطي','Folding phone stand','بلاستيك صلب - قابل لتعديل الزاوية والارتفاع',C('black white'))
P(193,ACC,'بوب سوكيت بامبو للجوال','Bamboo phone grip (pop socket)','لاصق قوي - ستاند ومقبض',C('natural white'))
# ---- Promo ----
P(194,PRO,'كرة ضغط باللافندر','Lavender stress ball','محشوة بزهور اللافندر',C('navy black gray navy/gray'))
P(195,PRO,'كرة ضغط','Stress ball','فوم ناعم - مكان للشعار',C('black white purple red orange green pink navy'))
P(196,PRO,'مكعب ضغط','Stress cube','',C('navy green white black'))
P(197,PRO,'كرة ضغط قلب','Heart stress ball','7×7 سم - فوم مرن',C('red'),note='لون واحد فقط')
P(198,PRO,'مكعب روبيك 3×3 بالصور','3×3×3 photo cube','يُطبع بالصور أو الشعار',C('white'))
P(199,PRO,'منظم مكتب تقويم (Calendar cube)','Calendar cube desk organizer','21×7×7 سم - 3 وحدات قابلة للطي',C('white'))
P(200,PRO,'بازل للتلوين','Blank jigsaw puzzle','20×20 سم - مُجمّع مسبقًا',C('white'))
P(201,PRO,'بازل خشبي','Wooden puzzle','12×12 سم',C('natural'))
# ---- Mouse pads ----
P(203,MP,'ماوس باد فلين','Cork mouse pad','22×18 سم',C('cork'))
P(204,MP,'ماوس باد','Mouse pad','22×18 سم - سماكة 4 مم - قابل للطباعة',C('white'))
P(205,MP,'ماوس باد دائري','Circular mouse pad','قطر 22 سم - سماكة 4 مم',C('white'))
P(206,MP,'ماوس باد بمسند جل للمعصم','Ergonomic gel wrist mouse pad','قاعدة غير قابلة للانزلاق',C('black navy gray green pink'))
# ---- Badges ----
P(208,BDG,'حامل بطاقة مضيء','Illuminated (photoelectric) card holder','70×118 مم - بطارية ليثيوم 15-25 ساعة - شحن Type-C - لانيارد',C('white'))
P(209,BDG,'حامل بطاقة تعريف جلد','Leather ID card holder','7×12 سم - نافذة شفافة لبطاقتين',C('black white gray purple blue green'))
P(210,BDG,'حامل بطاقة تعريف','ID card holder (soft)','',C('black gray white blue'))
P(211,BDG,'حامل بطاقة تعريف شفاف','Transparent ID card holder','فتحة علوية للانيارد أو المشبك',C('clear'))
P(212,BDG,'لانيارد دائري','Circular lanyard','لانيارد للشركات والمدارس والفعاليات',C('multi@ألوان_متعددة'))
P(213,BDG,'لانيارد قطن بطباعة حرارية','Cotton lanyard (thermal printing)','مشبك بلاستيك',C('multi@ألوان_متعددة'))
P(214,BDG,'لانيارد بمشبكين','Double-clip lanyard','',C('black navy white'))
P(215,BDG,'لانيارد قطن بمشبك قابل للفصل','Cotton lanyard (detachable clip)','عرض 1.5 سم - طول 50 سم',C('black blue gray white'))
P(216,BDG,'لانيارد مع حامل بطاقة يويو','Lanyard with badge holder (yo-yo)','',C('black white blue green navy purple'))
P(217,BDG,'حامل بطاقة يويو ستيل','Steel badge holder (yo-yo)','بكرة قابلة للسحب - شريط بلاستيك شفاف',C('silver'),note='لون واحد فقط')
P(218,BDG,'حامل بطاقة يويو','Yo-yo ID holder','سطح للطباعة أو ستيكر ريزن',C('black white gray blue'))
P(219,BDG,'يويو بطاقة مربع','Opaque square card hanger (yo-yo)','',C('black purple blue white'))
P(220,BDG,'بروش معدني','Metal brooch','قابل للحفر بالاسم أو الشعار',C('silver'))
# ---- Others ----
P(221,ACC,'مظلة شمس للسيارة','Car sunshade','قابلة للطي - تعكس أشعة الشمس',C('silver'))
P(222,ISL,'سجادة صلاة مع حقيبة','Prayer rug with bag','صديقة للبيئة - 67.5×104 سم - حقيبة 29×20 سم',C('cream'))
