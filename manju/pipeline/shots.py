# 第一集《地牢》分镜数据:画面、台词、角色、运镜
# 角色音色统一在 VOICES 中定义,保证全片一致

VOICES = {
    # speaker: (edge-tts voice, rate, pitch)
    "narr": ("zh-CN-YunjianNeural", "-8%", "+0Hz"),      # 旁白:沉稳男声
    "guard": ("zh-CN-YunjianNeural", "+12%", "-12Hz"),   # 守卫:粗声急促
    "man": ("zh-CN-YunyangNeural", "-12%", "-14Hz"),     # 黑斗篷男人:低沉平静
    "zhuofeng": ("zh-CN-YunxiNeural", "-4%", "+2Hz"),    # 卓峰:少年音
}

# (shot_id, image, speaker, 台词, 字幕(手动换行), 运镜)
SHOTS = [
    ("s01", "s01_dungeon_wide.png", "narr",
     "阴冷的地牢深处,少年卓峰,已经被铁链锁了整整三年。",
     "阴冷的地牢深处,少年卓峰,\n已经被铁链锁了整整三年。",
     "zoom_in"),
    ("s02", "s02_guard_mock.png", "guard",
     "废物!关了三年,你这辈子都别想翻身!",
     "「守卫」废物!关了三年,\n你这辈子都别想翻身!",
     "zoom_out"),
    ("s03", "s03_face_closeup.png", "zhuofeng",
     "笑吧。我在心里数着时间。今晚,会有变化。",
     "(卓峰)笑吧。我在心里数着时间\n——今晚,会有变化。",
     "zoom_in_slow"),
    ("s04", "s04_corridor_arrival.png", "narr",
     "深夜,脚步声靠近。来的,不是守卫。",
     "深夜,脚步声靠近。\n来的,不是守卫。",
     "zoom_out"),
    ("s05", "s05_man_at_bars.png", "man",
     "你想离开这里吗?",
     "「男人」你想离开这里吗?",
     "zoom_in_slow"),
    ("s06", "s06_eyes_fire.png", "narr",
     "那一瞬间,他眼底的倔强,亮得像火。",
     "那一瞬间,他眼底的倔强,\n亮得像火。",
     "zoom_in_fast"),
    ("s07", "s07_unlock_chains.png", "man",
     "你欠我一个答案。你想成为猎物,还是成为猎人?",
     "「男人」你欠我一个答案——\n你想成为猎物,还是成为猎人?",
     "zoom_out"),
    ("s08", "s08_door_open.png", "narr",
     "身后,是被囚禁的三年。面前,是未知的黑夜。",
     "身后,是被囚禁的三年。\n面前,是未知的黑夜。",
     "zoom_in"),
    ("s09", "s09_man_walks_away.png", "man",
     "跟上我。你的命运,会被改写。",
     "「男人」跟上我。\n你的命运,会被改写。",
     "zoom_out"),
    ("s10", "s10_into_the_night.png", "narr",
     "他不知道前方是什么。他只知道,这,是他唯一的机会。",
     "他不知道前方是什么。他只知道\n——这,是他唯一的机会。",
     "zoom_out_slow"),
]

TITLE = "《猎人》"
SUBTITLE = "第一集 · 地牢"
END_CARD = "第一集 完"
