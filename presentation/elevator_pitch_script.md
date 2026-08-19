# Elevator Pitch (Video Pitch) — Script & Recording Guide

**Zhilin Ye | z5719978 | Group 95 | GSOE9011**
**基于整份研究提案的电梯演讲（视频提交版）**

内容覆盖整个项目（不是个人贡献）。两个版本：2 分钟主版约 300 词，90 秒精简版约 220 词。
要求提醒：必须**本人配音**（禁止 TTS）、**不可用 AI 生成视频**、**出镜有加分**。

---

## 2 分钟主版（约 300 词，正常语速 150 词/分钟）

### Slide 1 — 开场钩子（约 15 秒）

> Hi, I'm Zhilin Ye from Group 95. Let me ask you something: what good is a traffic
> forecast that works perfectly every ordinary day — but fails the moment a crash happens?
> That's exactly the problem our research tackles.

（提示：第一句直视镜头，语气像抛问题给观众；"fails" 加重。）

### Slide 2 — 问题（约 30 秒）

> Modern deep-learning models learn from millions of sensor readings, but those readings
> mostly capture routine weekday patterns. So when a collision, a rain cell, or a stadium
> crowd suddenly changes the road, the model keeps saying "everything looks normal" —
> you can see that grey line on the chart. The red area is the blind spot: the biggest
> forecasting errors happen exactly when travellers, freight and emergency services need
> early warning the most.

（提示：讲到 "grey line" 和 "red area" 时用鼠标或手势指图。）

### Slide 3 — 我们的方案（约 35 秒）

> Our idea is simple to state: give the model the context it cannot see. We take a strong
> graph neural network — Graph WaveNet — and feed it three extra sources: live incident
> reports, weather observations, and event schedules, which are known hours in advance.
> A gated-attention layer learns when each source matters. And crucially, the model only
> ever sees information available at forecast time — no future data, ever.
>
> We turned this into one falsifiable question: can context cut the 30-minute error gap
> between normal and disrupted traffic by at least twenty percent, without hurting
> everyday forecasts by more than one percent?

（提示："falsifiable" 放慢；两个数字 "twenty percent" "one percent" 清晰咬字。）

### Slide 4 — 凭什么可信（约 25 秒）

> And you can trust the answer, because the experiment is built to be fair. Three years
> of real Los Angeles freeway data. A matched baseline with the same backbone, the same
> leak-free chronological splits, the same tuning budget. Source-by-source ablations,
> plus a shuffled-context negative control — a built-in lie detector that exposes fake
> gains. And success is defined in advance, with pre-registered decision rules.

### Slide 5 — 价值收尾（约 15 秒）

> Whatever the outcome, transport agencies get an auditable answer to one practical
> question: is context data worth investing in? Reliable forecasts, when it matters most.
> Thank you.

（提示：最后一句放慢，微笑收尾，停顿一秒再停止录制。）

---

## 90 秒精简版（约 220 词）

> Hi, I'm Zhilin Ye from Group 95. What good is a traffic forecast that works every
> ordinary day — but fails the moment a crash happens?
>
> Deep-learning traffic models learn routine weekday patterns from millions of sensor
> readings. So when a collision, a rain cell or a stadium crowd suddenly changes the
> road, the model keeps predicting "normal". That red area on the chart is the blind
> spot — the biggest errors, exactly when early warning matters most.
>
> Our answer: give the model the context it cannot see. We take a strong graph neural
> network and add live incident reports, weather, and event schedules, fused by gated
> attention — using only information available at forecast time.
>
> We test one falsifiable claim on three years of Los Angeles freeway data: context must
> cut the 30-minute error gap between normal and disrupted traffic by at least twenty
> percent, without hurting everyday forecasts by more than one percent. A matched
> baseline, leak-free splits, ablations and a shuffled-context negative control keep the
> comparison honest — and success is defined before we ever touch the test set.
>
> Whatever the outcome, transport agencies get an auditable answer: is context data worth
> investing in? Reliable forecasts, when it matters most. Thank you.

---

## 录制指南（对照作业要求）

**满足硬性要求**

1. **本人配音**：直接对着幻灯片朗读上面的稿子并录音，不要使用任何配音软件。先朗读
   两三遍熟悉节奏，录的时候语气自然一点，不要念稿感太重。
2. **视觉材料**：本 PPT（`group95_elevator_pitch.pptx`）即满足 "visual aids, graphics
   and pictures" 要求。建议你自己过一遍每页内容并做少量修改（改一两处措辞、调整顺序），
   确保你能对每一页的内容负责，并按课程 AI 使用政策做相应披露。
3. **出镜加分**：录制时让摄像头画面叠加在幻灯片角落即可拿到加分。

**推荐录制方式（三选一）**

- **PowerPoint 自带录制**：幻灯片放映 → 录制幻灯片演示（Record），右下角会自动叠加
  摄像头画面，录完导出为 MP4。最简单，推荐。
- **Zoom**：开个人会议 → 共享 PPT 全屏 → 开摄像头（画面自动出现在角落）→ 本地录制。
- **OBS Studio**：想要更好画质时用，场景里加"显示器采集 + 视频采集设备"。

**录制细节**

- 找安静房间，手机或耳机麦克风离嘴 20–30 厘米；先录 10 秒试听底噪。
- 摄像头位置：画面右下角，不要遮住图表（Slide 2 的图表主要在左上方，Slide 3 的
  架构图在中部，右下角是安全区）。
- 看镜头的时机：开场第一句和最后收尾句看镜头，中间可以看稿/看幻灯片。
- 一页一录也可以：PowerPoint 的录制是按页保存的，某一页说错了只需重录那一页。
- 时长控制：先用手机计时朗读一遍全稿；超时优先删 Slide 4 的例子性从句，不要加快语速。

**上传**

- 导出 MP4（1080p）→ 上传 YouTube 选 **Unlisted（不公开列出）** → 复制链接提交到
  portal。不想用 YouTube 就传 OneDrive（UNSW 账号自带）并开启"任何拥有链接的人可查看"。
- 提交前用无痕窗口打开链接确认无需登录即可播放。
