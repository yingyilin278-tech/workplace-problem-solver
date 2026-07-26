# workplace-problem-solver Skill 总览

## 1. Skill 定位

- 名称：`workplace-problem-solver`
- 目标：诊断并解决中文职场与求职问题，输出可直接使用的判断、建议、话术、后续动作和风险提示。
- 主要覆盖：
  - 在职问题：向上沟通、同事冲突、跨部门协作、加班边界、绩效晋升、离职、PIP、管理问题
  - 求职问题：求职定位、简历优化、JD 匹配、自我介绍、项目叙事、模拟面试、offer 比较、谈薪、复盘
  - 知识投喂：书籍、论文、视频、小红书正文/字幕蒸馏

## 2. 固定输出协议

任何正式回答，统一只用以下五段：

```md
## 判断

## 建议

## 话术

## 后续

## 风险
```

## 3. 路由框架

### 3.1 在职问题主分类 C1-C12

- `C1` 任务安排与向上沟通
- `C2` 领导关系、打压与 PUA
- `C3` 同事冲突与成果归属
- `C4` 跨部门协作与会议推进
- `C5` 工作量、加班与职业边界
- `C6` 汇报表达与职场存在感
- `C7` 绩效、薪酬与制度公平
- `C8` 晋升、成长与岗位匹配
  - 包含工作能力与岗位要求不匹配、岗位升级后的能力结构变化
- `C9` PIP、调岗降薪与裁员
- `C10` 职场人际与心理内耗
- `C11` 离职、裸辞与职业转向
- `C12` 管理者、带团队与下属协作

### 3.2 求职子域 J1-J7

- `J1` 方向定位与求职策略
- `J2` 经历盘点与素材库
- `J3` JD 解析与简历定制
- `J4` 自我介绍与项目叙事
- `J5` 面试准备与模拟追问
- `J6` offer 比较与谈薪决策
- `J7` 面试复盘与下一轮优化

## 4. Skill 怎么判定用户问题

### 4.1 先分两层

1. 先判断是 `在职问题` 还是 `求职问题`
2. 再判断具体属于哪个 `C 类` 或 `J 类`

### 4.2 判定信号

- 如果出现这些词，优先走求职子域：
  - `简历`
  - `JD`
  - `投递`
  - `面试`
  - `自我介绍`
  - `项目经历`
  - `offer`
  - `谈薪`
  - `校招`
  - `社招`
  - `转行找工作`

- 其他默认先按 C1-C12 分流

### 4.3 解决顺序

1. 分类
2. 收集最少必要信息
3. 判断风险和不可逆节点
4. 选择规则和资料
5. 用五段协议输出

## 5. 知识库层级

- `L0` 候选：仅线索
- `L1` 已核验：可进蒸馏队列
- `L2` 已蒸馏：已有规则、动作、话术、反例、边界
- `L3` 已测试：经过案例测试和人工复核

当前书库主体状态：**100 本书均已进入书库；当前主状态为 L2 已蒸馏，尚未全部升到 L3**

## 6. 全部书本名称

### A. 对话、谈判与边界

- `B01` *Difficult Conversations* — Douglas Stone、Bruce Patton、Sheila Heen
- `B02` *Getting to Yes* — Roger Fisher、William Ury、Bruce Patton
- `B03` *Thanks for the Feedback* — Douglas Stone、Sheila Heen
- `B04` *The Power of a Positive No* — William Ury
- `B08` *Crucial Conversations, 3rd Edition* — Joseph Grenny 等
- `B09` *Nonviolent Communication: A Language of Life* — Marshall Rosenberg
- `B10` *HBR Guide to Dealing with Conflict* — Amy Gallo
- `B11` *Getting Along* — Amy Gallo
- `B16` *HBR Guide to Negotiating* — Jeff Weiss
- `B25` *Failure to Communicate* — Holly Weeks
- `B26` *HBR's 10 Must Reads on Communication* — Harvard Business Review

### B. 向上管理、权力与复杂同事

- `B06` *Managing Up* — Melody Wilding
- `B07` *Ask a Manager* — Alison Green
- `B12` *Jerks at Work* — Tessa West
- `B14` *Radical Respect* — Kim Scott
- `B15` *HBR Guide to Office Politics* — Karen Dillon
- `B17` *Managing Up* — Harvard Business Review
- `B18` *The Art of Insubordination* — Todd B. Kashdan
- `B19` *Acting with Power* — Deborah Gruenfeld
- `B59` *The No Asshole Rule* — Robert Sutton
- `B60` *The Asshole Survival Guide* — Robert Sutton

### C. 汇报、书面表达与可见度

- `B20` *The Pyramid Principle, 3rd Edition* — Barbara Minto
- `B21` *Storytelling with Data* — Cole Nussbaumer Knaflic
- `B22` *HBR Guide to Persuasive Presentations* — Nancy Duarte
- `B23` *HBR Guide to Better Business Writing* — Bryan A. Garner
- `B24` *Good Charts* — Scott Berinato

### D. 绩效、反馈、薪酬与晋升

- `B13` *Radical Candor* — Kim Scott
- `B27` *HBR's 10 Must Reads on Performance Management*
- `B28` *HBR Guide to Delivering Effective Feedback*
- `B29` *How to Be Good at Performance Appraisals* — Dick Grote
- `B30` *Giving Effective Feedback* — Harvard Business Review
- `B31` *Performance Reviews* — Harvard Business Review
- `B32` *The Alliance* — Reid Hoffman、Ben Casnocha、Chris Yeh
- `B33` *Forget a Mentor, Find a Sponsor* — Sylvia Ann Hewlett
- `B63` *Nine Lies About Work* — Marcus Buckingham、Ashley Goodall
- `B68` *Drive* — Daniel H. Pink
- `B69` *Work Rules!* — Laszlo Bock

### E. 工作量、倦怠与心理内耗

- `B34` *Boundaries, Priorities, and Finding Work-Life Balance* — HBR
- `B35` *The Truth About Burnout* — Christina Maslach、Michael P. Leiter
- `B36` *Breaking Point* — Irvin Schonfeld、Renzo Bianchi
- `B37` *Chatter* — Ethan Kross
- `B38` *Emotional Agility* — Susan David
- `B39` *A Liberated Mind* — Steven C. Hayes
- `B40` *The Good Enough Job* — Simone Stolzoff
- `B41` *The Work Happiness Method* — Stella Grizont
- `B64` *No Hard Feelings* — Liz Fosslien、Mollie West Duffy
- `B65` *Essentialism* — Greg McKeown
- `B66` *Slow Productivity* — Cal Newport
- `B67` *Four Thousand Weeks* — Oliver Burkeman

### F. 职业成长、转岗与离职

- `B42` *The First 90 Days* — Michael Watkins
- `B43` *Master Your Next Move* — Michael Watkins
- `B44` *HBR Guide to Your Professional Growth*
- `B45` *HBR Guide to Getting the Mentoring You Need*
- `B46` *HBR Guide to Changing Your Career*
- `B47` *HBR Guide to Managing Up and Across*
- `B48` *Designing Your Life* — Bill Burnett、Dave Evans
- `B49` *Tiny Experiments* — Anne-Laure Le Cunff

### G. 管理者与团队

- `B05` *The Fearless Organization* — Amy Edmondson
- `B50` *High Output Management* — Andrew Grove
- `B51` *The Making of a Manager* — Julie Zhuo
- `B52` *The Coaching Habit* — Michael Bungay Stanier
- `B53` *HBR Guide to Leading Teams* — Mary L. Shapiro
- `B54` *HBR Guide to Motivating People*
- `B55` *Primal Leadership* — Daniel Goleman、Richard Boyatzis、Annie McKee
- `B56` *Resonant Leadership* — Richard Boyatzis、Annie McKee
- `B57` *Teaming* — Amy Edmondson
- `B58` *The 4 Stages of Psychological Safety* — Timothy R. Clark
- `B61` *The Five Dysfunctions of a Team* — Patrick Lencioni
- `B62` *Multipliers* — Liz Wiseman

### H. 中国大陆劳动关系与高风险事项

- `B70` 《HR全程法律指导：企业用工法律风险防控实操手册》
- `B71` 《员工关系：合规管理实务》
- `B72` 《企业劳动关系管理》
- `B73` 《中华人民共和国劳动合同法：案例注释版（第六版）》
- `B74` 《劳动和劳动合同法规全编（2024年版）》
- `B75` 《高效HR：企业劳动用工合规实务指南》

### I. 跨文化、决策、招聘与组织策略（补充书库）

- `B76` *The Culture Map* — Erin Meyer
- `B77` *Range* — David Epstein
- `B78` *An Everyone Culture* — Robert Kegan、Lisa Laskow Lahey
- `B79` *The Manager's Path* — Camille Fournier
- `B80` *First-Time Manager Companion*
- `B81` *Radical Inclusion* — David Moinina Sengeh
- `B82` *Industry Psychological Safety Companion*
- `B83` *The Body Keeps the Score* — Bessel van der Kolk
- `B84` *Permission to Feel* — Marc Brackett
- `B85` *Dare to Lead* — Brené Brown
- `B86` *Leaders Eat Last* — Simon Sinek
- `B87` *The Culture Code* — Daniel Coyle
- `B88` *An Elegant Puzzle* — Will Larson
- `B89` *The Power of Others* — Michael Bond
- `B90` *Together* — Vivek Murthy
- `B91` *Give and Take* — Adam Grant
- `B92` *Originals* — Adam Grant
- `B93` *Option B* — Sheryl Sandberg、Adam Grant
- `B94` *Thinking, Fast and Slow* — Daniel Kahneman
- `B95` *Noise* — Daniel Kahneman、Olivier Sibony、Cass Sunstein
- `B96` *Thinking in Bets* — Annie Duke
- `B97` *The Innovator's Dilemma* — Clayton Christensen
- `B98` *Measure What Matters* — John Doerr
- `B99` *The Effective Hiring Manager* — Marc Golab 等
- `B100` *Designing Your Work Life* — Bill Burnett、Dave Evans

## 7. 已蒸馏了谁

### 7.1 书籍

- 书库已扩展到 `B01-B100`
- 当前主状态：**L2 结构化蒸馏**
- 当前已有结构化书籍卡：`book-bXX.md`
- 法律边界书卡：
  - `B73`
  - `B74`
- 当前不应说“100 本都已经 L3 验收完成”

### 7.2 论文

- `P01` Employee Voice and Silence — Morrison
- `P02` Consequences of Abusive Supervision — Tepper
- `P03` The Job Demands–Resources Model of Burnout — Demerouti 等
- `P04` On the Dimensionality of Organizational Justice — Colquitt
- `P05` Task versus Relationship Conflict — De Dreu、Weingart
- `P06` Psychological Safety and Learning Behavior in Work Teams — Edmondson
- `P07` Building a Practically Useful Theory of Goal Setting — Locke、Latham
- `P08` The Development and Validation of the Workplace Ostracism Scale — Ferris 等

### 7.3 视频 / 官方 transcript

- `V01` Adam Grant / WorkLife
- `V02` Betsy Kauffman
- `V03` Adar Cohen
- `V04` Sarah Crawford-Bohl
- `V05` Kim Scott

状态：**V01-V05 已做 transcript 蒸馏**

### 7.4 小红书博主与内容

#### 账号定位级

- JustOneAPI 原始账号：`665`
- 相关账号：`643`
- 按昵称合并后账号档案：`596`
- 这层属于 `creator-knowledge/`
- 只能证明账号公开定位，**不能证明博主具体说过某条方法**

#### 内容级正文/字幕蒸馏

当前已落进内容级知识层 `xhs-content-knowledge/` 的真实/样例内容包括：

- `大除草家阿乌`  
  - 内容：`领导临时塞活，别秒回“好的”`
- `书书`
  - 内容：`我的工作沟通语料库19（被临时加活篇）`
- `职场内容样例`
  - 内容：`领导临时加活时，不要先说做不到，先让对方选优先级`

说明：

- `大除草家阿乌`、`书书` 是当前已经进内容级卡片的对象
- `596` 个账号档案是账号级蒸馏，不等于 596 个人都做了正文级内容蒸馏

## 8. 求职类外部 skill 已吸收对象

当前接进架构层的问题模型来自：

- `liyupi/yupi-skill`
- `dominciyue/resume_skill`
- `chen3tu/interview-master-skill`
- `spontaneousai/job-hunt-copilot`
- `coinluu/resume-jd-optimizer-cn`
- `Bughouse1024/interviewer-skill`

这些仓库现在不是直接替代本 skill，而是被吸收成求职子域 `J1-J7` 的问题框架。

## 9. 当前状态判断

### 已经成立的

- Skill 主文件可用
- 在职问题 `C1-C12` 可路由
- 求职问题 `J1-J7` 已接进架构
- 已有 121 个自动化案例：100 个在职问题 + 21 个求职问题
- C1-C12 与 J1-J7 的路由、必问信息、规则覆盖和五段输出协议验证通过
- 书库 100 本已纳入统一索引
- V01-V05 已蒸馏
- 小红书账号级蒸馏已完成 596 份档案
- 小红书内容级蒸馏链路已打通

### 还不能夸大的

- 不能说 100 本都已全文阅读完
- 不能说 100 本都已 L3
- 不能说 596 个博主都完成正文级蒸馏
- 不能说 JustOneAPI 当前环境下还能实时重爬，因为当前未读到 `JUSTONEAPI_TOKEN`

## 10. 你现在看这个 skill，最该核的框架点

1. 五段输出是不是你要的固定交付
2. C1-C12 是否覆盖你常见在职问题
3. J1-J7 是否覆盖你现在想加的求职问题
4. 100 本书的分组和覆盖主题是否合理
5. “账号级蒸馏”和“内容级蒸馏”是否分得够清楚
