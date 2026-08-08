# 第一集《地牢》分镜数据(v2:逐句配音 + 多关键帧动作 + 动态氛围特效)
# 角色音色统一在 VOICES 中定义,保证全片一致

VOICES = {
    # speaker: (edge-tts voice, rate, pitch)
    "narr": ("zh-CN-YunjianNeural", "-8%", "+0Hz"),      # 旁白:沉稳男声
    "guard": ("zh-CN-YunjianNeural", "+12%", "-12Hz"),   # 守卫:粗声急促
    "man": ("zh-CN-YunyangNeural", "-12%", "-14Hz"),     # 黑斗篷男人:低沉平静
    "zhuofeng": ("zh-CN-YunxiNeural", "-4%", "+2Hz"),    # 卓峰:少年音
}

# 每个分镜:
#   keyframes  : 1~2 张关键帧;2 张时在 kf_switch(第几句台词开始时,-1 表示按 kf_frac)交叉溶解,形成动作
#   cam        : Ken Burns 运镜类型
#   fx         : flicker(火光闪烁) / fog(飘雾) / snow(飘雪) / shake(镜头震动,从关键帧切换点开始)
#   lines      : [(speaker, 配音文本, 字幕文本)] —— 原文逐句对应
SHOTS = [
    {
        "id": "s01",
        "keyframes": ["s01_dungeon_wide.png"],
        "cam": "zoom_in",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "在阴冷的地牢里,少年卓峰,被锁在铁链中。",
             "在阴冷的地牢里,\n少年卓峰,被锁在铁链中。"),
            ("narr", "昏暗的火光,照出他满身伤痕。",
             "昏暗的火光,\n照出他满身伤痕。"),
        ],
    },
    {
        "id": "s02",
        "keyframes": ["s02_guard_mock.png", "s02b_guard_laugh.png"],
        "kf_switch": 1,
        "cam": "zoom_in_slow",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "守卫们嘲笑他是,废物。",
             "守卫们嘲笑他是——废物。"),
            ("guard", "废物!你被关在这里三年了,早就不可能再翻身了!哈哈哈哈!",
             "「守卫」废物!关了三年,\n你早就不可能再翻身了!"),
        ],
    },
    {
        "id": "s03",
        "keyframes": ["s03_face_closeup.png"],
        "cam": "zoom_in_slow",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "少年沉默,只在心里默数着时间。",
             "少年沉默,\n只在心里默数着时间。"),
            ("zhuofeng", "我知道,今晚,会有变化。",
             "(卓峰)我知道——\n今晚,会有变化。"),
        ],
    },
    {
        "id": "s04",
        "keyframes": ["s04_corridor_arrival.png", "s04b_man_closer.png"],
        "kf_switch": 1,
        "cam": "zoom_in_slow",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "深夜,脚步声靠近。",
             "深夜,脚步声靠近。"),
            ("narr", "来者不是守卫,而是一个披着黑斗篷的男人。",
             "来者不是守卫,而是一个\n披着黑斗篷的男人。"),
        ],
    },
    {
        "id": "s05",
        "keyframes": ["s05_man_at_bars.png"],
        "cam": "zoom_in_slow",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "他的声音低沉而平静,像是早已看穿一切。",
             "他的声音低沉而平静,\n像是早已看穿一切。"),
            ("man", "你想离开这里吗?",
             "「男人」你想离开这里吗?"),
        ],
    },
    {
        "id": "s06",
        "keyframes": ["s06a_eyes_before.png", "s06_eyes_fire.png"],
        "kf_switch": -1,
        "kf_frac": 0.32,
        "cam": "zoom_in_fast",
        "fx": ["flicker", "shake"],
        "lines": [
            ("narr", "少年抬头。那一瞬间,眼底的倔强,像火一样亮。",
             "少年抬头——那一瞬间,\n眼底的倔强,像火一样亮。"),
        ],
    },
    {
        "id": "s07",
        "keyframes": ["s07_unlock_chains.png", "s07b_chains_fall.png"],
        "kf_switch": 1,
        "cam": "zoom_out",
        "fx": ["flicker", "fog"],
        "lines": [
            ("narr", "男人解开他的锁链,却没有解释原因,只说,",
             "男人解开他的锁链,\n却没有解释原因,只说——"),
            ("man", "你欠我一个答案。你想成为猎物,还是成为猎人?",
             "「男人」你欠我一个答案——\n你想成为猎物,还是成为猎人?"),
        ],
    },
    {
        "id": "s08",
        "keyframes": ["s08_door_open.png", "s08b_step_out.png"],
        "kf_switch": 1,
        "cam": "zoom_in",
        "fx": ["snow"],
        "lines": [
            ("narr", "铁门打开,寒风灌入。少年第一次,踏出地牢。",
             "铁门打开,寒风灌入。\n少年第一次,踏出地牢。"),
            ("narr", "身后,是他被囚禁的三年;面前,是未知的黑夜。",
             "身后,是被囚禁的三年;\n面前,是未知的黑夜。"),
        ],
    },
    {
        "id": "s09",
        "keyframes": ["s09_man_walks_away.png", "s09b_man_ahead.png"],
        "kf_switch": 1,
        "cam": "zoom_out_slow",
        "fx": ["snow"],
        "lines": [
            ("narr", "男人转身离去,只留下一句话。",
             "男人转身离去,\n只留下一句话——"),
            ("man", "跟上我,你的命运,会改写。",
             "「男人」跟上我,\n你的命运,会改写。"),
        ],
    },
    {
        "id": "s10",
        "keyframes": ["s10_into_the_night.png", "s10b_walk_far.png"],
        "kf_switch": 1,
        "cam": "zoom_out_slow",
        "fx": ["snow"],
        "lines": [
            ("narr", "少年咬紧牙,迈步追上。",
             "少年咬紧牙,迈步追上。"),
            ("narr", "他不知道自己将面对什么。他只知道,这,是他唯一的机会。",
             "他不知道自己将面对什么。他只知道\n——这,是他唯一的机会。"),
        ],
    },
]

TITLE = "《猎人》"
SUBTITLE = "第一集 · 地牢"
END_CARD = "第一集 完"
