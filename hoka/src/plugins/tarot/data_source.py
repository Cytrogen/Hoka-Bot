import os
from nonebot.adapters.cqhttp import MessageSegment


img_path = 'file:///' + os.path.split(os.path.realpath(__file__))[0] + '\\resources\\'
death1 = img_path + 'death1.png'
death2 = img_path + 'death2.png'
justice1 = img_path + 'justice1.png'
justice2 = img_path + 'justice2.png'
strength1 = img_path + 'strength1.png'
strength2 = img_path + 'strength2.png'
temperance1 = img_path + 'temperance1.png'
temperance2 = img_path + 'temperance2.png'
chariot1 = img_path + 'thechariot1.png'
chariot2 = img_path + 'thechariot2.png'
devil1 = img_path + 'thedevil1.png'
devil2 = img_path + 'thedevil2.png'
emperor1 = img_path + 'theemperor1.png'
emperor2 = img_path + 'theemperor2.png'
empress1 = img_path + 'theempress1.png'
empress2 = img_path + 'theempress2.png'
fool1 = img_path + 'thefool1.png'
fool2 = img_path + 'thefool2.png'
hanged1 = img_path + 'thehangedman1.png'
hanged2 = img_path + 'thehangedman2.png'
hermit1 = img_path + 'thehermit.png'
hermit2 = img_path + 'thehermit2.png'
hierop1 = img_path + 'thehierophant1.png'
hierop2 = img_path + 'thehierophant2.png'
highpri1 = img_path + 'thehighpriestess1.png'
highpri2 = img_path + 'thehighpriestess2.png'
judgement1 = img_path + 'thejudgement1.png'
judgement2 = img_path + 'thejudgement2.png'
lovers1 = img_path + 'thelovers1.png'
lovers2 = img_path + 'thelovers2.png'
magician1 = img_path + 'themagician1.png'
magician2 = img_path + 'themagician2.png'
moon1 = img_path + 'themoon1.png'
moon2 = img_path + 'themoon2.png'
star1 = img_path + 'thestar1.png'
star2 = img_path + 'thestar2.png'
sun1 = img_path + 'thesun1.png'
sun2 = img_path + 'thesun2.png'
tower1 = img_path + 'thetower1.png'
tower2 = img_path + 'thetower2.png'
wof1 = img_path + 'thewheeloffortune1.png'
wof2 = img_path + 'thewheeloffortune2.png'
world1 = img_path + 'theworld1.png'
world2 = img_path + 'theworld2.png'


def card(num):
    if num == 0:
        return(MessageSegment.image(fool1) + '【愚人】正位：\n与众不同、幸运、不拘一格、追求新奇的梦想、眼界狭小、勇于冒险、向往自由、有艺术家气质、直攻要害、情感起伏不定、自由恋爱')
    elif num == 1:
        return(MessageSegment.image(fool2) + '【愚人】逆位：\n自负、固执、不安定、墨守成规、缺乏责任心、生活在梦幻中、不现实、不会应变、停滞不前、行为古怪、方向错误、感情不稳定')
    elif num == 2:
        return(MessageSegment.image(magician1) + '【魔术师】正位：\n成功、果断、好的开端、计划完美、发展空间大、智力非凡、思维活跃、想象力丰富、拥有默契的伴侣、出现新恋人')
    elif num == 3:
        return(MessageSegment.image(magician2) + '【魔术师】逆位：\n失败、态度消极、做事匆忙、优柔寡断、才能平庸、缺乏技术、没有判断力、没有创造力、爱情没有进展、注意伴侣的行为')
    elif num == 4:
        return(MessageSegment.image(highpri1) + '【女祭司】正位：\n知性、优秀的判断力和洞察力、独立自主、有知己、善于交流、意志坚强、擅长精神方面的研究、柏拉图式的恋爱、冷淡的恋情')
    elif num == 5:
        return(MessageSegment.image(highpri2) + '【女祭司】逆位：\n无知、冲动、缺乏理解力、神经质、有洁癖、对人冷淡、自我封闭、与女性朋友争执、单相思、健康不佳、晚婚或独身主义、不孕')
    elif num == 6:
        return(MessageSegment.image(empress1) + '【女皇】正位：\n繁荣、感情丰富、信仰坚定、心胸开阔、生活优雅、财运佳、公众人物、有魅力的女性、充实的爱、有结果的恋情、怀孕')
    elif num == 7:
        return(MessageSegment.image(empress2) + '【女皇】逆位：\n平庸、任性、迷惑、内心动摇、不思进取、自负、傲慢、疲倦、浪费、虚荣心强、计划搁置、不良的男女关系、不孕、流产')
    elif num == 8:
        return(MessageSegment.image(emperor1) + '【皇帝】正位：\n坚强的意志、成绩突出、果断、专制、有领袖风范、值得信赖、物质条件优越、伴侣与你年龄悬殊、嫁妆丰厚')
    elif num == 9:
        return(MessageSegment.image(emperor2) + '【皇帝】逆位：\n意志薄弱、幼稚、武断、固执、傲慢、疲劳过度、经济基础薄弱、爱情很勉强、痛苦而没结果的恋情')
    elif num == 10:
        return(MessageSegment.image(hierop1) + '【教皇】正位：\n温柔、博爱、受人信赖、受重视、工作出色、贡献突出、眼界狭窄、从善如流而得到好处、有贵人相助、适宜接触宗教、与年长的异性有缘、姻缘佳')
    elif num == 11:
        return(MessageSegment.image(hierop2) + '【教皇】逆位：\n冷漠、善于表达、太罗嗦、孤立无援、成功无望、眼界开阔、思路敏捷、改变以往感情上的不足、不被认同的恋情、对伴侣关心过度、姻缘淡')
    elif num == 12:
        return(MessageSegment.image(lovers1) + '【恋人】正位：\n敏感、前途光明、有志同道合的朋友、与人合作、对未来的抉择、决定未来命运的时机、浪漫的爱情、有爱情出现的预感')
    elif num == 13:
        return(MessageSegment.image(lovers2) + '【恋人】逆位：\n幼稚、退休、孤独、有阻力、眼花缭乱、血气方刚、对结果失望、充满戒心、逃避爱情、恋情短暂、分手、多情')
    elif num == 14:
        return(MessageSegment.image(chariot1) + '【战车】正位：\n活泼、有野心、握有指挥权、出发、前进必胜、速战速决、战果辉煌、开拓精神、击败对手、恋爱的胜利者、热烈的爱情')
    elif num == 15:
        return(MessageSegment.image(chariot2) + '【战车】逆位：\n怯懦、有强敌、受挫折、丧失斗志、急性子导致失败、缺少资金、不感兴趣、被拒绝、使对方失去信任、对爱情采取逃避态度')
    elif num == 16:
        return(MessageSegment.image(strength1) + '【力量】正位：\n不屈不挠、全力以赴、克服难关、坚强的信念、旺盛的斗志、刻苦的努力、超凡的勇气、神秘的力量、轰轰烈烈的能够经受考验的牢固爱情')
    elif num == 17:
        return(MessageSegment.image(strength2) + '【力量】逆位：\n疑心过度、犹豫不决、缺乏实力、没有耐心、危险的赌注、失去自信、失去别人的信任、故弄玄虚、自大、蛮干、禁不住诱惑、爱情无法持久')
    elif num == 18:
        return(MessageSegment.image(hermit1) + '【隐士】正位：\n高度智慧、思虑周密、冷静寡言、追求高层次的事物、正中要害、渐入佳境、出局、追求柏拉图式恋情、单相思')
    elif num == 19:
        return(MessageSegment.image(hermit2) + '【隐士】逆位：\n工作狂、铁面无私、偏见、有怨言、不够通融、孤独、固执、戒备心强、迷失方向、举止轻浮、怀疑和逃避爱情')
    elif num == 20:
        return(MessageSegment.image(wof1) + '【命运之轮】正位：\n幸运、好时机到来、非富即贵、善于随机应变、有望升职、命中注定的相逢、一见钟情、婚姻幸福')
    elif num == 21:
        return(MessageSegment.image(wof2) + '【命运之轮】逆位：\n劣势、时机不好、生活困苦、毫无头绪、情况恶化、工作易出错、停止前进、失恋、恋情短暂')
    elif num == 22:
        return(MessageSegment.image(justice1) + '【正义】正位：\n公正、中立、诚实、心胸坦荡、表里如一、身兼二职、追求合理化、协调者、与法律有关、光明正大的交往、感情和睦')
    elif num == 23:
        return(MessageSegment.image(justice2) + '【正义】逆位：\n失衡、偏见、纷扰、诉讼、独断专行、问心有愧、无法两全、表里不一、男女性格不合、情感波折、无视社会道德的恋情')
    elif num == 24:
        return(MessageSegment.image(hanged1) + '【倒吊人】正位：\n接受考验、行动受限、牺牲、不畏艰辛、不受利诱、有失必有得、吸取经验教训、浴火重生、广泛学习、奉献的爱')
    elif num == 25:
        return(MessageSegment.image(hanged2) + '【倒吊人】逆位：\n无谓的牺牲、骨折、厄运、不够努力、处于劣势、任性、利己主义者、缺乏耐心、受惩罚、逃避爱情、没有结果的恋情')
    elif num == 26:
        return(MessageSegment.image(death1) + '【死神】正位：\n失败、接近毁灭、生病、失业、维持停滞状态、持续的损害、交易停止、枯燥的生活、别离、重新开始、双方有很深的鸿沟、恋情终止')
    elif num == 27:
        return(MessageSegment.image(death2) + '【死神】逆位：\n抱有一线希望、起死回生、回心转意、摆脱低迷状态、挽回名誉、身体康复、突然改变计划、逃避现实、斩断情丝、与旧情人相逢')
    elif num == 28:
        return(MessageSegment.image(temperance1) + '【节制】正位：\n单纯、调整、平顺、互惠互利、好感转为爱意、纯爱、深爱')
    elif num == 29:
        return(MessageSegment.image(temperance2) + '【节制】逆位：\n消耗、下降、疲劳、损失、不安、不融洽、爱情的配合度不佳')
    elif num == 30:
        return(MessageSegment.image(devil1) + '【恶魔】正位：\n被束缚、堕落、生病、恶意、屈服、欲望的俘虏、不可抗拒的诱惑、颓废的生活、举债度日、不可告人的秘密、私密恋情')
    elif num == 31:
        return(MessageSegment.image(devil2) + '【恶魔】逆位：\n逃离拘束、解除困扰、治愈病痛、告别过去、暂停、别离、拒绝诱惑、舍弃私欲、别离时刻、爱恨交加的恋情')
    elif num == 32:
        return(MessageSegment.image(tower1) + '【塔】正位：\n破产、逆境、被开除、急病、致命的打击、巨大的变动、受牵连、信念崩溃、玩火自焚、纷扰不断、突然分离，破灭的爱')
    elif num == 33:
        return(MessageSegment.image(tower2) + '【塔】逆位：\n困境、内讧、紧迫的状态、状况不佳、趋于稳定、骄傲自大将付出代价、背水一战、分离的预感、爱情危机')
    elif num == 34:
        return(MessageSegment.image(star1) + '【星星】正位：\n前途光明、充满希望、想象力、创造力、幻想、满足愿望、水准提高、理想的对象、美好的恋情')
    elif num == 35:
        return(MessageSegment.image(star2) + '【星星】逆位：\n挫折、失望、好高骛远、异想天开、仓皇失措、事与愿违、工作不顺心、情况悲观、秘密恋情、缺少爱的生活')
    elif num == 36:
        return(MessageSegment.image(moon1) + '【月亮】正位：\n不安、迷惑、动摇、谎言、欺骗、鬼迷心窍、动荡的爱、三角关系')
    elif num == 37:
        return(MessageSegment.image(moon2) + '【月亮】逆位：\n逃脱骗局、解除误会、状况好转、预知危险、等待、正视爱情的裂缝')
    elif num == 38:
        return(MessageSegment.image(sun1) + '【太阳】正位：\n活跃、丰富的生命力、充满生机、精力充沛、工作顺利、贵人相助、幸福的婚姻、健康的交际')
    elif num == 39:
        return(MessageSegment.image(sun2) + '【太阳】逆位：\n消沉、体力不佳、缺乏连续性、意气消沉、生活不安、人际关系不好、感情波动、离婚')
    elif num == 40:
        return(MessageSegment.image(judgement1) + '【审判】正位：\n复活的喜悦、康复、坦白、好消息、好运气、初露锋芒、复苏的爱、重逢、爱的奇迹')
    elif num == 41:
        return(MessageSegment.image(judgement2) + '【审判】逆位：\n一蹶不振、幻灭、隐瞒、坏消息、无法决定、缺少目标、没有进展、消除、恋恋不舍')
    elif num == 42:
        return(MessageSegment.image(world1) + '【世界】正位：\n完成、成功、完美无缺、连续不断、精神亢奋、拥有毕生奋斗的目标、完成使命、幸运降临、快乐的结束、模范情侣')
    elif num == 43:
        return(MessageSegment.image(world2) + '【世界】逆位：\n未完成、失败、准备不足、盲目接受、一时不顺利、半途而废、精神颓废、饱和状态、合谋、态度不够融洽、感情受挫')
    else:
        pass