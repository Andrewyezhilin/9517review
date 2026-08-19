# GSOE9011 Individual Presentation — Speech Script

**Zhilin Ye | z5719978 | Group 95**
**Topic: Experimental Design & Feasibility for Context-Aware Non-Recurring Traffic Congestion Forecasting**

按 5 分钟设计（约 700 词）。每页附：幻灯片对应关系、英文逐字稿、中文提示。
如时限为 3 分钟：删除 Slide 7（风险页），Slide 4 与 Slide 5 各删最后一段。
如时限为 8 分钟：在 Slide 4 增加一个具体例子（见文末"扩展段落"）。

---

## Slide 1 — Title（约 20 秒）

> Good morning everyone. I'm Zhilin Ye from Group 95. Our project asks whether adding
> incident, weather and event data can make traffic forecasts more reliable during
> disruptions. My own role was the experimental design — in other words, making sure this
> question could be answered fairly, reproducibly, and within a twelve-month budget.

（提示：开场只给项目一句话，立刻转到自己的角色，不与组员的内容重复。）

---

## Slide 2 — The project in one minute（约 40 秒）

> Let me give you the project in one minute. We use the Greater Los Angeles freeway
> network, with three years of five-minute sensor data from 2022 to 2024, aligned with
> incident records, NOAA weather, and venue event calendars.
>
> Our research question is deliberately quantified: can a context-aware model reduce the
> 30-minute MAE gap between recurring and non-recurring congestion by at least twenty
> percent, while keeping routine-traffic error within a one percent non-inferiority margin?
>
> Notice what kind of claim this is — it's falsifiable. It can pass or fail. And a
> falsifiable claim is only as good as the experiment built around it. That experiment
> was my responsibility.

（提示："falsifiable" 一词要放慢强调，它是整场演讲的钩子。）

---

## Slide 3 — Four building blocks（约 30 秒）

> My work has four building blocks. First, defining the evaluation episodes — deciding
> transparently what counts as non-recurring congestion. Second, leakage controls, so the
> model can never cheat by seeing the future. Third, the metrics and the pre-registered
> decision rules that determine success or failure. And fourth, the ablation set,
> sensitivity analysis and risk planning. Let me walk through each one.

（提示：这页是地图，语速可稍快，评委会对照这四块给分。）

---

## Slide 4 — Episode definition（约 70 秒，重点一）

> Here is the core problem I had to solve. On a sensor, a detector fault, an ordinary
> evening peak, and a crash-induced queue all look exactly the same — low speed. If we
> can't separate them transparently, the whole research question collapses.
>
> So I designed a three-step rule, and you can see it on this chart. Step one: every
> threshold comes from training data only. Free-flow speed is the 85th percentile of
> overnight observations, and a congestion episode starts when speed stays below seventy
> percent of free-flow for fifteen minutes — both dips on this chart qualify.
>
> Step two: to be labelled non-recurring, an episode needs **two** independent signals.
> The speed must be at least twenty percent, or fifteen kilometres per hour, below the
> expected weekly profile — that's the gold arrow — **and** there must be an externally
> recorded disruption, such as an incident reported within five kilometres and ninety
> minutes. The evening peak on the right is just as slow, but it matches the expected
> profile and has no recorded disruption, so it stays recurring.
>
> Step three, and this is critical: these labels are used only to stratify the evaluation.
> They are never training targets, so the model cannot learn the labels instead of the
> traffic. This directly answered our tutor's feedback asking how non-recurring congestion
> would be labelled experimentally.

（提示：讲到金色箭头和右侧晚高峰时用激光笔指图；最后一句"回应导师反馈"是加分句。）

---

## Slide 5 — Leakage controls & fair comparison（约 60 秒，重点二）

> Traffic data is extremely easy to leak. If you split it randomly, two windows of the
> same crash can end up in both training and test — and the model looks brilliant for the
> wrong reason. So I enforced strictly chronological splits over the three-year period:
> roughly twenty-one months of training, seven of validation and seven of test, with a
> seven-day embargo at every boundary, and no congestion episode is allowed to cross a
> boundary. All preprocessing statistics — normalisation, free-flow speeds, median
> profiles — come from training data only. And at forecast time, the model may only see
> what an operator would actually have: no final incident durations, no future weather.
>
> The other half of fairness is the comparison itself, and I worked closely with Zhenyu
> here. The baseline and the context model share the same Graph WaveNet backbone, the
> same splits, and the same tuning budget. We even added a widened, parameter-matched
> traffic-only model — so if the context model wins, nobody can say it won just because
> it had more parameters.

---

## Slide 6 — Decision rules & statistics（约 60 秒，重点三）

> So how do we decide success? I pre-registered a decision rule with three conditions,
> all required. One: the reliability gap — the MAE difference between non-recurring and
> recurring episodes — must shrink by at least twenty percent. Two: the improvement must
> be statistically real — a ninety-five percent bootstrap interval that excludes zero,
> resampling whole episodes rather than individual windows, because adjacent five-minute
> windows are heavily correlated. Three: routine traffic must not get worse by more than
> one percent.
>
> On metrics: we use MAE because it's directly interpretable in kilometres per hour, and
> we replaced MAPE with WAPE, because percentage errors explode in stop-and-go traffic
> near zero speed.
>
> And my favourite part is the negative control. We re-run the model with the context
> data shuffled within time-of-day. If shuffled context still "helps", our pipeline is
> lying to us. It's a built-in lie detector.

（提示："lie detector" 是全场记忆点，讲完停顿一秒。）

---

## Slide 7 — Feasibility & risk（约 40 秒）

> I also owned the risk analysis. The biggest risk isn't building the model — it's not
> having enough well-aligned disruption episodes to say anything meaningful. So the plan
> starts with a month-one data audit, with hard thresholds: at least two hundred test
> episodes overall, and thirty per source. If we fall short, the pre-declared contingency
> is to relax the completeness gate to eighty-five percent and extend to the next-largest
> connected component. Every risk on this table has a trigger and a fallback decided in
> advance. And importantly: even if the twenty percent target fails, the project still
> succeeds — because the threshold is a decision rule, not a promised result.

---

## Slide 8 — Reflection & closing（约 30 秒）

> Looking back, my contribution wasn't one section of the document — it was the
> connective tissue. I aligned data-quality assumptions with Xin, comparison fairness
> with Zhenyu, and turned the group's model idea into something testable and reproducible.
> The real product of this project is not a model — it's an auditable answer to when and
> where context data actually helps. My job was to make that answer worth believing.
> Thank you.

---

## 追问应答卡（每条背 2–3 句）

**Q1: Why exactly 20% and 1%?**
> Twenty percent is an ex-ante minimum practical effect — clearly larger than typical
> marginal benchmark gains, and large enough to justify the data-engineering cost of
> maintaining incident, weather and event feeds. One percent caps the operational loss on
> routine traffic. Both are varied in sensitivity analysis — margins of zero, one and two
> percent — so neither number is load-bearing on its own.

**Q2: Why episode-block bootstrap instead of a t-test on all windows?**
> Because thousands of overlapping five-minute windows are not independent — treating
> them as independent would massively understate uncertainty. Resampling whole episodes,
> stratified by disruption type, preserves within-episode dependence. We also run a
> Diebold–Mariano test with a dependence-robust variance as a secondary diagnostic, and
> Holm adjustment across the three source-specific ablations.

**Q3: If attention weights highlight weather, doesn't that show weather caused the improvement?**
> No — attention measures model salience, not causality. That's why attribution comes
> from the ablation set instead: traffic-only, plus each source individually, plus all
> sources together. The architecture never gets credit that the ablations can't confirm.

**Q4: What if your episode definition is wrong?**
> That's what the sensitivity envelope is for: anomaly thresholds of ten, twenty and
> thirty percent; incident radii of two, five and ten kilometres; time windows of thirty,
> ninety and one hundred eighty minutes; event catchments of five, ten and fifteen
> kilometres. We only claim robustness if the direction of the result survives all
> reasonable definitions. Ambiguous episodes are excluded from the primary analysis but
> reported in sensitivity.

**Q5: What was your biggest personal difficulty?（中文场合）**
> 最难的是平衡严谨和可行——一万次 bootstrap、五个随机种子、九组消融（E0–E8），
> 算力预算很容易爆。我的解决办法是把约束做进设计里：预设 300–800 个传感器上限、
> 混合精度训练、固定调参次数和早停规则，而不是靠事后补救。

---

## 扩展段落（8 分钟版，插入 Slide 4 之后）

> Let me make this concrete. Imagine a Friday evening at a major LA stadium. From the
> sensor history alone, the first thirty minutes of post-game congestion look identical
> to a slightly heavy ordinary peak — the sensors simply haven't seen the crowd yet. But
> the event calendar knew the game's end time three hours in advance. Our episode rules
> capture exactly this: the venue is within ten kilometres, the timestamp falls in the
> window from three hours before scheduled start to two hours after scheduled end, and
> the speed drop exceeds the anomaly threshold. That's a non-recurring episode the
> context model gets a fair chance to predict — and the baseline, by construction, cannot.

---

## 时间分配速查（5 分钟版）

| 页 | 内容 | 时长 |
|---|---|---|
| 1 | 开场 | 20 s |
| 2 | 项目一分钟 | 40 s |
| 3 | 贡献总览 | 30 s |
| 4 | Episode 定义 | 70 s |
| 5 | 防泄漏与公平 | 60 s |
| 6 | 判定准则 | 60 s |
| 7 | 风险 | 40 s |
| 8 | 反思收尾 | 30 s |
| 合计 | | ~5 min |
