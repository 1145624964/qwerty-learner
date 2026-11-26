from __future__ import annotations

import json
import pathlib
import re
from typing import Any

REPO_ROOT = pathlib.Path(r"C:\Users\hp\Documents\qwerty-learner")
DICT_PATH = REPO_ROOT / "public" / "dicts" / "shanguo_kaoyan_2023_book_order.json"
ARTICLES_JSON_OUT = REPO_ROOT / "src" / "resources" / "shanguo_kaoyan_2023_articles.json"
DESKTOP_ARTICLE_DIR = pathlib.Path(r"C:\Users\hp\Desktop\23考研英语词汇闪过_每日英语文章")

WORD_COUNT_RE = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")


def count_english_words(paragraphs: list[list[str]]) -> int:
    total = 0
    for en_p, _ in paragraphs:
        plain = en_p.replace("**", "")
        total += len(WORD_COUNT_RE.findall(plain))
    return total


ARTICLES_SPEC: list[dict[str, Any]] = [
    # ==================== DAY 1 (2026-11-19, ky23-high-wl01-day-1, rows 0..42) ====================
    {
        "id": "ky23-high-wl01-day-1-art-1",
        "chapterId": "ky23-high-wl01-day-1",
        "group": "高频词",
        "groupDay": 1,
        "wordList": "Word List 1",
        "articleNumber": 1,
        "scheduledDate": "2026-11-19",
        "title": "The Certificate on the Clinic Wall",
        "zhTitle": "诊所墙上的合格证书",
        "paragraphs": [
            [
                "An imagined district clinic hangs a framed **certificate** beside its reception desk after buying an **artificial** scheduling tool to manage daily **operation**. The software promises to **facilitate** appointments across **various** departments and raise weekly patient **output** without adding extra clerks. Visitors see a reassuring display of modernization. Yet an official document only confirms that a product passed an initial check, not that its **technical** **design** suits the people who must use it every morning when the doors open.",
                "一家设想的街区诊所在购入一套管理日常运作的人工排班工具后，把装裱好的合格证书挂在接待台旁。该软件承诺无需增加办事员即可促进各科室预约并提高每周接诊产出。来访者看到一副令人安心的现代化景象。然而，正式证书只确认产品通过了初步核验，并不证明其技术设计适合每天清晨开门时必须使用它的人。",
            ],
            [
                "A **significant** problem appears as soon as a reception **technician** meets cases that do not fit the standard menu. The programme treats every consultation as a fixed fifteen-minute **variable**, ignoring the **significance** of subtle differences between a routine repeat prescription and a frail patient's first visit. When experienced staff use their own **technique** to hold a quiet slot open for an anxious caller, the screen records an **operational** delay. A **mechanical** rule intended to save time thus turns flexible care into an apparent fault on the weekly chart.",
                "接待技术员一旦遇到不合标准菜单分类的病例，重大问题便显现出来。程序把每次问诊都当作固定的十五分钟变量，忽视了常规续方与体弱患者初诊之间细微差别的重要性。当有经验的工作人员运用自己的技巧为焦急的来电者留出一个安静时段时，屏幕却将其记录为操作延误。一条旨在节省时间的机械规则，就这样在周报图表上把灵活照护变成了表面上的失误。",
            ],
            [
                "Managers often **attribute** early complaints to stubborn staff habits rather than to the booking **mechanism** itself. In their optimistic **outlook**, a worker with the right **qualification** should adapt quickly, while hesitation is just a private **affair** to be corrected through training. That judgement overlooks a practical **factor**: front-line workers **witness** what happens when an automated queue leaves no **outlet** for urgent questions. If nobody at the desk can adjust the schedule without special permission, minor delays **contribute** to a worse **outcome** in the crowded waiting room.",
                "管理者常把早期抱怨归因于员工固执的习惯，而非那套预约机制本身。在他们乐观的看法里，具备相应资格的员工理应迅速适应，而犹豫不过是可以通过培训纠正的个人私事。这种判断忽略了一个实际因素：一线人员亲眼目击，当自动队列不为紧急提问留出渠道时会发生什么。如果前台谁也不能在未经特别许可的情况下调整排班，细小延误就会促成拥挤候诊室里更糟的结果。",
            ],
            [
                "Supporters of strict automation reply that personal discretion used to create quiet unfairness. Without a common standard, a friendly clerk might **offer** an early appointment to a familiar neighbour while strangers waited in line. That objection deserves weight. Informal arrangements can indeed hide favouritism, and a shared record helps a clinic **review** how its doctors' time is spent across the week. However, removing every human choice does not make a public service neutral; it merely shifts authority to whoever wrote the software categories months earlier.",
                "支持严格自动化的人回应说，个人裁量过去常造成隐蔽的不公。没有共同标准，热心的办事员可能把靠前的预约提供给熟识的邻居，却让陌生人排队等待。这一异议值得重视。非正式安排确实可能掩盖偏袒，共用的记录也有助于诊所审视一周内医生的时间如何分配。然而，取消一切人为选择并不会使公共服务变得中立，它只是把权力转移给了数月前编写软件分类的人。",
            ],
            [
                "Even clinics with **similar** patient numbers may need very different booking rules. A centre serving elderly residents cannot **simplify** intake in the same way as a campus health office for young adults. When administrators **sacrifice** local judgement just to keep the central dashboard tidy, staff either invent secret paper workarounds or stop reporting problems altogether. The certificate on the wall remains valid, while the daily record grows less honest about how care is actually delivered.",
                "即便患者人数相似的诊所，也可能需要截然不同的预约规则。服务老年居民的中心，不能像面向年轻人的校园保健室那样用同一种方式简化接诊流程。当管理人员只为保持中心看板整洁而牺牲本地判断时，员工要么私下发明纸质变通办法，要么干脆不再上报问题。墙上的证书依然有效，日常记录却越来越无法诚实反映照护究竟是如何提供的。",
            ],
            [
                "A better reform would treat the software as a working draft rather than a final verdict. The clinic could keep its shared booking record while giving receptionists a visible way to mark exceptions and explain why a slot was changed. Regular meetings between nurses, clerks, and system designers would then test whether the categories still match real visits. Technology serves a medical institution best when its rules remain open to the people who bear the daily cost of its mistakes.",
                "更好的改革应把软件当作工作初稿而非最终定论。诊所可以保留共用的预约记录，同时给接待员提供公开方式，标注例外情况并说明调整时段的理由。护士、办事员与系统设计者之间的定期会面，随后便能检验那些分类是否仍契合真实就诊情况。当技术规则对那些每天承担其失误代价的人保持开放时，技术才能最好地服务于医疗机构。",
            ],
        ],
        "glossary": [
            {"dayOrder": 1, "word": "various", "surface": "various", "para": "P1", "meaning": "a. 各种各样的；across various departments在各个科室。"},
            {"dayOrder": 2, "word": "variable", "surface": "variable", "para": "P2", "meaning": "n. 变量；a fixed fifteen-minute variable被固定的十五分钟变量，本文作名词。"},
            {"dayOrder": 3, "word": "design", "surface": "design", "para": "P1", "meaning": "n. 设计；technical design技术设计。"},
            {"dayOrder": 4, "word": "significant", "surface": "significant", "para": "P2", "meaning": "a. 重大的、明显的；a significant problem重大问题。"},
            {"dayOrder": 5, "word": "significance", "surface": "significance", "para": "P2", "meaning": "n. 重要性、意义；the significance of subtle differences细微差别的重要性。"},
            {"dayOrder": 6, "word": "operation", "surface": "operation", "para": "P1", "meaning": "n. 运作、日常运行；daily operation诊所日常运转，此处不是外科手术。"},
            {"dayOrder": 7, "word": "operational", "surface": "operational", "para": "P2", "meaning": "a. 操作上的、运行中的；an operational delay运行延误。"},
            {"dayOrder": 8, "word": "technique", "surface": "technique", "para": "P2", "meaning": "n. 技巧、工作方法；use their own technique运用自己的处理技巧。"},
            {"dayOrder": 9, "word": "technical", "surface": "technical", "para": "P1", "meaning": "a. 技术的；technical design技术设计。"},
            {"dayOrder": 10, "word": "technician", "surface": "technician", "para": "P2", "meaning": "n. 技术人员、专职操作员；a reception technician接待处技术人员。"},
            {"dayOrder": 11, "word": "attribute", "surface": "attribute", "para": "P3", "meaning": "v. 把……归因于；attribute complaints to staff habits把抱怨归因于员工习惯，注意不同于名词“属性”。"},
            {"dayOrder": 12, "word": "contribute", "surface": "contribute", "para": "P3", "meaning": "v. 促成、导致；contribute to a worse outcome促成更糟的结果，此处不是捐献。"},
            {"dayOrder": 13, "word": "output", "surface": "output", "para": "P1", "meaning": "n. 产出、接诊量；weekly patient output每周接诊产出。"},
            {"dayOrder": 14, "word": "outlook", "surface": "outlook", "para": "P3", "meaning": "n. 观点、看法；in their optimistic outlook在他们乐观的看法中。"},
            {"dayOrder": 15, "word": "outcome", "surface": "outcome", "para": "P3", "meaning": "n. 结果；a worse outcome更糟的结果。"},
            {"dayOrder": 16, "word": "outlet", "surface": "outlet", "para": "P3", "meaning": "n. 发泄或表达途径、出口；no outlet for urgent questions没有紧急提问的渠道，不是专卖店。"},
            {"dayOrder": 17, "word": "mechanical", "surface": "mechanical", "para": "P2", "meaning": "a. 机械刻板的；a mechanical rule刻板的规则，非机械装置义。"},
            {"dayOrder": 18, "word": "mechanism", "surface": "mechanism", "para": "P3", "meaning": "n. 机制、办法；the booking mechanism预约机制本身。"},
            {"dayOrder": 19, "word": "facilitate", "surface": "facilitate", "para": "P1", "meaning": "v. 促进、使便利；facilitate appointments使预约便利。"},
            {"dayOrder": 20, "word": "certificate", "surface": "certificate", "para": "P1", "meaning": "n. 证书、合格证明；a framed certificate装裱好的合格证书。"},
            {"dayOrder": 21, "word": "qualification", "surface": "qualification", "para": "P3", "meaning": "n. 资格、技能条件；the right qualification合适的资格条件。"},
            {"dayOrder": 22, "word": "sacrifice", "surface": "sacrifice", "para": "P5", "meaning": "v. 牺牲；sacrifice local judgement牺牲本地判断。"},
            {"dayOrder": 23, "word": "artificial", "surface": "artificial", "para": "P1", "meaning": "a. 人工的、人造的；an artificial scheduling tool人工开发的排班工具。"},
            {"dayOrder": 24, "word": "factor", "surface": "factor", "para": "P3", "meaning": "n. 因素；a practical factor一个实际因素。"},
            {"dayOrder": 25, "word": "affair", "surface": "affair", "para": "P3", "meaning": "n. 事情、事务；a private affair个人私事。"},
        ],
        "crossovers": [
            {"word": "witness", "para": "P3", "meaning": "v. 目击、亲眼见到；witness what happens亲眼看见发生的情况。"},
            {"word": "review", "para": "P4", "meaning": "v. 审查、审视；review how its doctors' time is spent审视医生时间如何分配。"},
            {"word": "offer", "para": "P4", "meaning": "v. 提供；offer an early appointment提供靠前的预约。"},
            {"word": "simplify", "para": "P5", "meaning": "v. 简化；simplify intake简化接诊流程。"},
            {"word": "similar", "para": "P5", "meaning": "a. 相似的；similar patient numbers相似的患者数量。"},
        ],
        "questions": [
            {
                "ordinal": 1,
                "stem": "The framed certificate in Paragraph 1 is mentioned to show that",
                "options": [
                    "A. official approval does not guarantee suitability for daily work.",
                    "B. patients care more about wall displays than about waiting times.",
                    "C. the clinic failed to test the software before purchasing it.",
                    "D. technical design should be left entirely to reception staff.",
                ],
                "answer": "A",
                "explanation": "A正确，P1末句指出证书只说明产品通过初步核验，不证明其技术设计适合每天使用它的人。B无中生有；C与“passed an initial check”矛盾；D把需要贴合使用者夸大为完全交给接待员设计。",
            },
            {
                "ordinal": 2,
                "stem": "Why does the software record an operational delay in Paragraph 2?",
                "options": [
                    "A. Technicians lack the qualification to operate the new menu.",
                    "B. It treats flexible time reserved for complex visits as a deviation.",
                    "C. Routine prescriptions take longer than fifteen minutes to process.",
                    "D. Patients frequently arrive late for their morning appointments.",
                ],
                "answer": "B",
                "explanation": "B正确，P2指出程序把每次问诊固定为15分钟，员工留出机动时段照顾特殊患者时，屏幕便记为延误。A偷换P3管理者的偏见；C、D在文中无依据。",
            },
            {
                "ordinal": 3,
                "stem": "In Paragraph 3, 'contribute to' most nearly means",
                "options": [
                    "A. donate money for.",
                    "B. compensate for.",
                    "C. help bring about.",
                    "D. publicly report on.",
                ],
                "answer": "C",
                "explanation": "C正确，细小延误累积后会“促成、导致（help bring about）”候诊室里更糟的结果。A是常见义“捐款”干扰；B“补偿”、D“公开报道”均与语境相反。",
            },
            {
                "ordinal": 4,
                "stem": "What point from supporters of automation does the author concede in Paragraph 4?",
                "options": [
                    "A. Software categories are always freer from bias than human clerks.",
                    "B. Unchecked personal discretion could favour familiar patients unfairly.",
                    "C. Shared booking records are unnecessary in small neighbourhood clinics.",
                    "D. Strangers prefer automated menus to speaking with receptionists.",
                ],
                "answer": "B",
                "explanation": "B正确，P4承认支持者的顾虑值得重视：缺乏共同标准时，办事员可能偏袒熟人，非正式安排可能掩盖偏袒。A与P4末句“只是把权力转移给编写分类的人”相反；C、D违背文意。",
            },
            {
                "ordinal": 5,
                "stem": "The author would most likely endorse a scheduling system that",
                "options": [
                    "A. hides all local exceptions so that the dashboard stays tidy.",
                    "B. replaces shared records with informal arrangements among clerks.",
                    "C. applies identical intake rules to elderly centres and student offices.",
                    "D. allows staff to record reasoned exceptions and revise categories.",
                ],
                "answer": "D",
                "explanation": "D正确，P6建议保留共用记录，同时允许接待员公开标注例外并说明理由，定期检验分类是否契合实际。A是P5批评的做法；B否定了P4肯定的共用记录；C与P5相反。",
            },
        ],
        "sentences": [
            {
                "sentence": "Yet an official document only confirms that a product passed an initial check, not that its technical design suits the people who must use it every morning when the doors open.",
                "analysis": "confirms后接两个由that引导的并列宾语从句，以only... not that...构成取舍对照：肯定“通过初步核验”，否定“因此就适合每天开门时必须使用它的人”；who定语从句限定people。",
            },
            {
                "sentence": "However, removing every human choice does not make a public service neutral; it merely shifts authority to whoever wrote the software categories months earlier.",
                "analysis": "分号前以动名词短语removing every human choice作主语，否定“消除人为选择即中立”；分号后merely限定实际后果，whoever引导宾语从句作to的宾语，指出权力转移到了规则编写者手中。",
            },
        ],
    },
    {
        "id": "ky23-high-wl01-day-1-art-2",
        "chapterId": "ky23-high-wl01-day-1",
        "group": "高频词",
        "groupDay": 1,
        "wordList": "Word List 1",
        "articleNumber": 2,
        "scheduledDate": "2026-11-19",
        "title": "When One City Borrows Another's Bus Rule",
        "zhTitle": "当一座城市照搬另一座城市的公交规则",
        "paragraphs": [
            [
                "When a city council wants to reform its bus network, officials naturally **compare** their routes with those of a successful neighbour. Cross-city **comparison** seems a sensible way to **simplify** planning: if an express lane worked across the river, leaders assume they can **transfer** the same **provision** into local bylaws without starting from zero. Yet borrowing a rule is much easier than borrowing the conditions that made it work. A policy that looks tidy on paper can fail when its new setting is treated as an afterthought rather than part of the design.",
                "当市政议会想要改革公交网络时，官员自然会将本地线路与成功的邻近城市相比较。跨城比较看似是简化规划的明智办法：如果快速公交道在河对岸奏效，领导者便以为无需从零开始，就能把同一条款直接移入本地法规。然而，照搬一条规则远比照搬使它奏效的条件容易。当新环境被当作事后才考虑的末节而非设计的一部分时，纸面上整洁的政策就会碰壁。",
            ],
            [
                "To draw a reliable **inference** from another town's success, planners must **review** what happened outside the main avenue. Suppose a model report praises a fare rule for narrowing the **divide** between outer housing estates and the commercial centre. Used as a single **reference**, that report may omit the late-night factory buses and flexible ticket inspection that supported riders on the ground. If a second council copies only the fare table, early shift workers may still **suffer** long waits at unlit stops when winter rain delays the connecting line.",
                "要从另一座城镇的成功中得出可靠推论，规划者必须审视主干道之外发生了什么。假设一份示范报告称赞某项票价规则缩小了远郊住宅区与商业中心之间的鸿沟。若只把这份报告当作唯一参考，它可能略去了在实地支撑乘客出行的夜间厂车与弹性验票安排。如果第二个议会只复制票价表，当冬雨延误接驳线路时，早班工人可能仍要在没有路灯的站台忍受漫长等待。",
            ],
            [
                "The mistake becomes more likely when officials **confer** chiefly with outside advisers who favour uniform national charts. Rankings **offer** a clean picture for a committee meeting, yet they carry a built-in **preference** for numbers that are easy to collect in a hurry. The practical **wisdom** of drivers and regular passengers rarely fits into those neat columns. Treating street experience as **separate** from formal evaluation leaves decision-makers blind to the small frictions that decide whether a timetable holds together on a rainy weekday.",
                "当官员主要与偏爱统一全国图表的外部顾问商议时，这种错误就更容易发生。排名能为委员会会议提供清爽的画面，却天生偏爱匆忙间易于收集的数字。司机与常客的实践智慧很少能塞进那些整洁的表格栏里。把街头经验与正式评估割裂开来，会让决策者看不见决定时刻表在雨天工作日能否维持运转的细小阻力。",
            ],
            [
                "Even districts with **similar** population totals can react differently to the same legal **provision**. In one town, major employers adjust shift hours to match the bus schedule; in another, rigid factory gates turn a ten-minute delay into lost wages for workers. First-hand **witness** accounts from drivers and riders show that a route's value depends on the surrounding habits of work, shopping, and school. Importing the rule without adjusting those everyday supports only reproduces the outward appearance of reform while leaving daily travel just as difficult.",
                "即便人口总数相似的地区，对同一法律条款的反应也可能不同。在一座城镇，主要雇主会调整班次时间以配合公交时刻表；在另一座城镇，死板的工厂大门会让十分钟的延误变成工人的工资损失。司机与乘客的一手目击证词表明，一条线路的价值取决于周边工作、购物与上学的日常习惯。只引进规则而不调整这些日常配套支撑，不过是复制了改革的外表，却让日常出行依然同样艰难。",
            ],
            [
                "Defenders of standard templates argue that stressing local difference gives slow councils an easy excuse to delay action. If every town insists its streets are unique, overdue reform may never begin. That warning is fair, because administrative inertia often hides behind local pride. Still, learning from neighbours does not mean copying their bylaws word for word. It means asking which principle solved the problem and what local adjustments are needed to support it in a different town.",
                "标准模板的捍卫者辩称，强调地方差异会给行动迟缓的议会提供拖延的现成借口。如果每个城镇都坚称自己的街道独一无二，早该进行的改革或许永远无法启动。这一警告不无道理，因为行政惰性常躲在地方自豪感背后。即便如此，向邻城学习并不意味着逐字照抄其法规，而是要追问究竟是哪条原则解决了问题，以及在另一座城镇需要哪些本地调整来支撑它。",
            ],
            [
                "A sounder method would pair outside examples with a short local trial before officials **divide** the annual transport budget. Councils could test a borrowed timetable on two busy corridors, invite drivers and passengers to point out bottlenecks, and revise the stops accordingly. Comparative evidence works best when it sharpens local questions rather than replaces the need to ask them in public.",
                "更稳妥的做法是在官员分配年度交通预算之前，将外部范例与简短的本地试运行结合起来。议会可以在两条繁忙的走廊线路上测试借来的时刻表，邀请司机和乘客指出瓶颈，并据此调整站点。当比较证据被用来厘清本地问题，而非取代公开提问的必要时，才最能发挥效用。",
            ],
        ],
        "glossary": [
            {"dayOrder": 26, "word": "witness", "surface": "witness", "para": "P4", "meaning": "n. 目击者、亲历者；first-hand witness accounts一手亲历证词，此处作名词定语。"},
            {"dayOrder": 27, "word": "review", "surface": "review", "para": "P2", "meaning": "v. 审视、复核；review what happened审视实际发生的情况。"},
            {"dayOrder": 28, "word": "divide", "surface": "divide", "para": "P2, P6", "meaning": "n./v. 分歧鸿沟/分配；P2 narrowing the divide作名词指缩小差距，P6 divide the budget作动词指分配预算。"},
            {"dayOrder": 29, "word": "provision", "surface": "provision", "para": "P1, P4", "meaning": "n. 条款、规定；transfer the same provision移入相同条款，本文不是物质供应。"},
            {"dayOrder": 30, "word": "wisdom", "surface": "wisdom", "para": "P3", "meaning": "n. 智慧、经验之谈；practical wisdom实践智慧。"},
            {"dayOrder": 31, "word": "confer", "surface": "confer", "para": "P3", "meaning": "v. 商议、协商；confer chiefly with outside advisers主要与外部顾问商议，注意不是confer a degree授予学位义。"},
            {"dayOrder": 32, "word": "inference", "surface": "inference", "para": "P2", "meaning": "n. 推论；draw a reliable inference得出可靠推论。"},
            {"dayOrder": 33, "word": "reference", "surface": "reference", "para": "P2", "meaning": "n. 参考依据；used as a single reference作为唯一参考。"},
            {"dayOrder": 34, "word": "preference", "surface": "preference", "para": "P3", "meaning": "n. 偏爱、偏向；a built-in preference for对……的内在偏向。"},
            {"dayOrder": 35, "word": "offer", "surface": "offer", "para": "P3", "meaning": "v. 提供、呈现；offer a clean picture呈现清爽的画面。"},
            {"dayOrder": 36, "word": "transfer", "surface": "transfer", "para": "P1", "meaning": "v. 转移、移植；transfer the same provision into把同一条款移入。"},
            {"dayOrder": 37, "word": "suffer", "surface": "suffer", "para": "P2", "meaning": "v. 遭受、忍受；suffer long waits忍受漫长等待。"},
            {"dayOrder": 38, "word": "compare", "surface": "compare", "para": "P1", "meaning": "v. 比较；compare their routes with把线路与……比较。"},
            {"dayOrder": 39, "word": "comparison", "surface": "comparison", "para": "P1", "meaning": "n. 比较；cross-city comparison跨城比较。"},
            {"dayOrder": 40, "word": "separate", "surface": "separate", "para": "P3", "meaning": "a. 分开的、割裂的；treat A as separate from B把A与B当作割裂的两件事。"},
            {"dayOrder": 41, "word": "simplify", "surface": "simplify", "para": "P1", "meaning": "v. 简化；simplify planning简化规划。"},
            {"dayOrder": 42, "word": "similar", "surface": "similar", "para": "P4", "meaning": "a. 相似的；similar population totals相似的人口总数。"},
        ],
        "crossovers": [],
        "questions": [
            {
                "ordinal": 1,
                "stem": "Why does borrowing a transport rule from another city often fail?",
                "options": [
                    "A. Local bylaws forbid copying express lanes from neighbouring towns.",
                    "B. Officials copy the rule without the local conditions that supported it.",
                    "C. Express lanes are only effective in cities separated by a river.",
                    "D. Planners spend too much time comparing different fare tables.",
                ],
                "answer": "B",
                "explanation": "B正确，P1指出照搬规则容易，照搬使其奏效的条件却难，忽视新环境条件会导致纸面政策碰壁。A、C、D均是对P1例子的曲解。",
            },
            {
                "ordinal": 2,
                "stem": "The example of the fare rule in Paragraph 2 suggests that a model report can",
                "options": [
                    "A. prove that outer estates need fewer buses than the city centre.",
                    "B. eliminate the need for late-night factory transport.",
                    "C. leave out supporting arrangements that made the fare rule workable.",
                    "D. show why shift workers prefer fixed ticket inspection.",
                ],
                "answer": "C",
                "explanation": "C正确，P2指出示范报告可能略去夜间厂车和弹性验票等配套支持，导致只抄票价表的城市仍让工人久等。A、B、D与原文相反。",
            },
            {
                "ordinal": 3,
                "stem": "In Paragraph 4, 'provision' most nearly means",
                "options": [
                    "A. food supply.",
                    "B. legal clause.",
                    "C. emergency fund.",
                    "D. passenger count.",
                ],
                "answer": "B",
                "explanation": "B正确，P1与P4中的provision均指法规或政策中的“条款、规定（legal clause）”。A是常见字面义干扰；C、D不合语境。",
            },
            {
                "ordinal": 4,
                "stem": "How does the author respond to defenders of standard templates in Paragraph 5?",
                "options": [
                    "A. By agreeing that local pride is sometimes used to excuse inaction.",
                    "B. By arguing that every town's streets are too unique for reform.",
                    "C. By recommending that councils copy neighbour bylaws word for word.",
                    "D. By claiming that outside examples are useless for transport planning.",
                ],
                "answer": "A",
                "explanation": "A正确，P5明确承认“That warning is fair, because administrative inertia often hides behind local pride”，然后再区分“提炼原则并做本地调整”与“拖延不作为”。B、C、D均与P5论点相反。",
            },
            {
                "ordinal": 5,
                "stem": "What does the author recommend before officials divide the transport budget?",
                "options": [
                    "A. Hiring outside advisers to rank all routes by passenger numbers.",
                    "B. Waiting until local employers adopt uniform factory hours.",
                    "C. Running a small local trial and adjusting the borrowed timetable with feedback.",
                    "D. Replacing express lanes with late-night buses across the whole city.",
                ],
                "answer": "C",
                "explanation": "C正确，P6主张在分配预算前，先在两条线路上试运行借来的时刻表，听取司机与乘客反馈并调整站点。A是P3批评的做法；B、D在文中无依据。",
            },
        ],
        "sentences": [
            {
                "sentence": "Treating street experience as separate from formal evaluation leaves decision-makers blind to the small frictions that decide whether a timetable holds together on a rainy weekday.",
                "analysis": "Treating...动名词短语作主语；leaves decision-makers blind to...为主干（“使决策者看不见……”）；that定语从句修饰frictions，其中whether引导宾语从句说明摩擦阻力的实际影响。",
            },
            {
                "sentence": "Still, learning from neighbours does not mean copying their bylaws word for word.",
                "analysis": "Still表示让步后的转折；主语learning from neighbours与宾语copying their bylaws word for word均为动名词短语，通过does not mean厘清“借鉴经验”与“逐字照抄”的界限。",
            },
        ],
    },
    # ==================== DAY 2 (2026-11-20, ky23-high-wl01-day-2, rows 42..84) ====================
    {
        "id": "ky23-high-wl01-day-2-art-1",
        "chapterId": "ky23-high-wl01-day-2",
        "group": "高频词",
        "groupDay": 2,
        "wordList": "Word List 1",
        "articleNumber": 1,
        "scheduledDate": "2026-11-20",
        "title": "The Extra Form Before the Research Grant",
        "zhTitle": "科研经费申请前的那张额外表格",
        "paragraphs": [
            [
                "To **eliminate** accounting errors, an imagined university adds a **preliminary** review before any research **proposal** can leave a department. In principle, clear rules **supervise** public money and protect the institution's good name. Yet administrative caution rarely recognizes its own **limit**. New checklists appear each semester until preparation becomes a **superfluous** routine, taking quiet hours that a **graduate** assistant or senior **scholar** would otherwise spend in the archive or laboratory testing ideas.",
                "为了消除账目错误，一所设想的大学在任何科研申请书离开院系之前，增加了一道初步审查。原则上，清晰的规则能监督公共资金并维护机构声誉。然而，行政上的谨慎很少知道自身的界限。每个学期都有新核查表出现，直到准备工作变成多余的例行公事，占用了研究生助教或资深学者本可用于在档案馆或实验室检验想法的安静时间。",
            ],
            [
                "The pressure grows when university leaders equate a **superior** public **profile** with strict internal control. Eager to **promote** the campus in national tables, boards **provide** polished summary charts while leaving **limited** funds for everyday equipment repair and technical help. That **policy** choice marks a quiet change in **political** weight inside the university: deans who once shielded departments from outside **politics** now judge projects chiefly by how neatly they fit the reporting calendar.",
                "当大学领导把优越的公众形象等同于严格的内部控制时，压力便进一步增大。为了急于在全国榜单上推介学校，理事会提供光鲜的汇总图表，却只给日常设备维修和技术协助留出有限资金。这种政策选择标志着校内政治分量的悄然变化：曾为院系挡住外部政治纷争的院长，如今主要看项目是否整齐契合汇报日历来评判它们。",
            ],
            [
                "Rather than preventing waste, an **aggressive** inspection system can **prolong** simple purchases for weeks and **provoke** quiet resentment across the faculty. A biologist waiting six weeks to order standard glass tubes may miss an entire spring breeding season while the forms sit on an administrator's desk. Meanwhile, outside software firms **profit** handsomely by selling compliance packages advertised as a necessary **upgrade** for modern campuses. The **profound** irony is that rules built to protect integrity can reward tidy paperwork more than careful science.",
                "激进的检查制度非但不能防止浪费，反而会把简单的采购拖延数周，并在院系间激起暗中的不满。一位等待六周才获准订购标准玻璃试管的生物学家，在表格搁在行政人员办公桌上期间，可能会错过整个春季繁殖期。与此同时，外部软件公司通过销售被宣传为现代校园必要升级的合规软件包而获利颇丰。深刻的讽刺在于，为保护诚信而建立的规则，奖励整洁文书的程度反而超过严谨的科学。",
            ],
            [
                "Members of **congress** who call for tighter oversight seldom see this **gradual** drain on working energy from their distant offices in the capital. From a committee room, every extra signature looks like a **progressive** step toward public accountability. Up close, however, a standard form can only **measure** whether a rule was followed on paper, not whether a scientific question was worth asking or an experiment was sound. To a noticeable **degree**, heavy reporting can even hide weak methods behind a high wall of completed boxes.",
                "在首都远处办公室里呼吁加强监管的国会议员，很少看到这种对工作精力的逐渐消耗。在委员会会议室里，每一个额外签名都像是迈向公共问责的进步之举。然而近距离看，一张标准表格只能衡量纸面上是否遵守了规则，却无法衡量一个科学问题是否值得探究或实验是否可靠。在相当程度上，繁重的汇报甚至会把薄弱的研究方法藏在一堵填满方框的高墙后。",
            ],
            [
                "Defenders of central review reply that public grants carry real obligations to taxpayers, and that informal trust has left **serious** gaps in the past. That point is fair: unexamined freedom can indeed shelter carelessness or private interest in any large institution. Yet recognizing the need for supervision does not justify every procedural delay. A sensible system would separate high-value contracts from routine supply orders, placing detailed checks where the risk of misuse is real rather than imaginary.",
                "集中审查的捍卫者回应说，公共拨款对纳税人负有切实义务，而非正式的信任在过去曾留下严重漏洞。这一点很公允：在任何大型机构里，不受审视的自由确实可能庇护粗心或私利。然而，承认需要监督并不能证明每一次程序拖延都合理。明智的制度会把高额合同与日常耗材订单分开，将详细核查放在真正存在而非凭空想象的滥用风险之处。",
            ],
            [
                "Oversight works best when it treats researchers as partners in stewardship rather than as suspects by default. A university could replace repeated prior approvals for small items with random audits after a project ends and clear rules for public disclosure. When rules respect the practical pace of inquiry, compliance stops being an exhausting contest over forms. Trustworthy research ultimately depends on open criticism among peers, not on counting how many stamps a folder collected before the work began.",
                "当监管把研究者当作共同管理的伙伴而非默认嫌疑人时，效果最好。大学可以用项目结束后的随机抽查和清晰的公开披露规则，取代对小额物品的反复事前审批。当规则尊重探究的实际节奏时，合规就不再是一场围绕表格的累人较量。可靠的研究归根结底依赖同行间的公开批评，而不是看工作开始前文件夹集齐了多少枚印章。",
            ],
        ],
        "glossary": [
            {"dayOrder": 1, "word": "eliminate", "surface": "eliminate", "para": "P1", "meaning": "v. 消除、排除；eliminate accounting errors消除账目错误。"},
            {"dayOrder": 2, "word": "preliminary", "surface": "preliminary", "para": "P1", "meaning": "a. 初步的、预备的；a preliminary review初步审查。"},
            {"dayOrder": 3, "word": "limit", "surface": "limit", "para": "P1", "meaning": "n. 限度、界限；recognize its own limit认识自身的限度。"},
            {"dayOrder": 4, "word": "limited", "surface": "limited", "para": "P2", "meaning": "a. 有限的；limited funds有限的资金。"},
            {"dayOrder": 5, "word": "superfluous", "surface": "superfluous", "para": "P1", "meaning": "a. 多余的、不必要的；a superfluous routine多余的例行程序。"},
            {"dayOrder": 6, "word": "superior", "surface": "superior", "para": "P2", "meaning": "a. 优越的、出众的；a superior public profile优越的公众形象。"},
            {"dayOrder": 7, "word": "supervise", "surface": "supervise", "para": "P1", "meaning": "v. 监督、管理；supervise public money监督公共资金。"},
            {"dayOrder": 8, "word": "policy", "surface": "policy", "para": "P2", "meaning": "n. 政策、方针；that policy choice那种政策选择。"},
            {"dayOrder": 9, "word": "politics", "surface": "politics", "para": "P2", "meaning": "n. 政治纷争、权术；outside politics外部政治干预。"},
            {"dayOrder": 10, "word": "political", "surface": "political", "para": "P2", "meaning": "a. 政治的、权力关系的；political weight政治分量。"},
            {"dayOrder": 11, "word": "promote", "surface": "promote", "para": "P2", "meaning": "v. 宣传推介、提升；promote the campus推介学校。"},
            {"dayOrder": 12, "word": "provide", "surface": "provide", "para": "P2", "meaning": "v. 提供；provide polished summary charts提供光鲜的汇总图表。"},
            {"dayOrder": 13, "word": "prolong", "surface": "prolong", "para": "P3", "meaning": "v. 延长、拖延；prolong simple purchases拖延简单采购。"},
            {"dayOrder": 14, "word": "profound", "surface": "profound", "para": "P3", "meaning": "a. 深刻的；the profound irony深刻的讽刺。"},
            {"dayOrder": 15, "word": "profile", "surface": "profile", "para": "P2", "meaning": "n. 公众形象、概况；a public profile公众形象，不是人物侧脸。"},
            {"dayOrder": 16, "word": "proposal", "surface": "proposal", "para": "P1", "meaning": "n. 申请书、提案；a research proposal科研课题申请书。"},
            {"dayOrder": 17, "word": "provoke", "surface": "provoke", "para": "P3", "meaning": "v. 激起、引发；provoke quiet resentment激起暗中的不满。"},
            {"dayOrder": 18, "word": "profit", "surface": "profit", "para": "P3", "meaning": "v. 获利、得利；profit handsomely by selling通过销售获利，此处作动词。"},
            {"dayOrder": 19, "word": "upgrade", "surface": "upgrade", "para": "P3", "meaning": "n. 升级版本；a necessary upgrade必要的升级，此处作名词。"},
            {"dayOrder": 20, "word": "graduate", "surface": "graduate", "para": "P1", "meaning": "n. 研究生、毕业生；a graduate assistant研究生助教。"},
            {"dayOrder": 21, "word": "gradual", "surface": "gradual", "para": "P4", "meaning": "a. 逐渐的；this gradual drain这种逐渐的消耗。"},
            {"dayOrder": 22, "word": "degree", "surface": "degree", "para": "P4", "meaning": "n. 程度；to a noticeable degree在相当明显程度上，非学位义。"},
            {"dayOrder": 23, "word": "congress", "surface": "congress", "para": "P4", "meaning": "n. 国会、代表大会；members of congress国会议员。"},
            {"dayOrder": 24, "word": "aggressive", "surface": "aggressive", "para": "P3", "meaning": "a. 激进的、强势推进的；an aggressive inspection system激进的检查制度。"},
            {"dayOrder": 25, "word": "progressive", "surface": "progressive", "para": "P4", "meaning": "a. 进步的、向前的；a progressive step进步之举。"},
        ],
        "crossovers": [
            {"word": "scholar", "para": "P1", "meaning": "n. 学者；senior scholar资深学者。"},
            {"word": "measure", "para": "P4", "meaning": "v. 衡量；measure whether a rule was followed衡量是否遵守了规则。"},
            {"word": "serious", "para": "P5", "meaning": "a. 严重的；serious gaps严重漏洞。"},
        ],
        "questions": [
            {
                "ordinal": 1,
                "stem": "What is the author's main concern about the preliminary review in Paragraph 1?",
                "options": [
                    "A. It fails to detect accounting errors in large departments.",
                    "B. It expands into needless paperwork that takes time from research.",
                    "C. It prevents graduate assistants from joining laboratory projects.",
                    "D. It allows scholars to bypass public funding rules.",
                ],
                "answer": "B",
                "explanation": "B正确，P1指出核查表每个学期增加，最终变成多余的例行公事（superfluous routine），占用了研究者在档案馆或实验室的时间。A、C、D在P1均无依据。",
            },
            {
                "ordinal": 2,
                "stem": "Paragraph 2 suggests that university deans have increasingly",
                "options": [
                    "A. protected departments from national ranking tables.",
                    "B. prioritized laboratory repair over summary charts.",
                    "C. evaluated projects by their fit with administrative reporting.",
                    "D. refused to cooperate with the governing board.",
                ],
                "answer": "C",
                "explanation": "C正确，P2末句指出曾经为院系阻挡外部政治的院长，如今主要根据项目是否整齐契合汇报日历来评判它们。A、B、D与原文相反。",
            },
            {
                "ordinal": 3,
                "stem": "The biologist's glass-tube order is mentioned in Paragraph 3 to illustrate",
                "options": [
                    "A. how procedural delay can disrupt time-sensitive scientific work.",
                    "B. why commercial compliance software is cheaper than laboratory glass.",
                    "C. how researchers profit from upgrading their equipment each season.",
                    "D. why breeding experiments require stricter financial supervision.",
                ],
                "answer": "A",
                "explanation": "A正确，P3以等待六周订购标准试管导致错过整个春季繁殖期为例，说明激进检查拖延简单采购、干扰科研时效。B、C、D曲解例证目的。",
            },
            {
                "ordinal": 4,
                "stem": "According to Paragraph 4, standardized forms are limited because they",
                "options": [
                    "A. are rarely read by members of congress.",
                    "B. verify paper compliance rather than the value or quality of research.",
                    "C. encourage scholars to ask overly ambitious questions.",
                    "D. cannot record when an official signature was obtained.",
                ],
                "answer": "B",
                "explanation": "B正确，P4指出表格只能衡量纸面上是否守规，无法衡量科学问题是否值得探究，甚至会把薄弱方法掩盖在填好的方框后。A、C、D不合文意。",
            },
            {
                "ordinal": 5,
                "stem": "Which reform would best match the author's proposal?",
                "options": [
                    "A. Removing all financial supervision from public research grants.",
                    "B. Requiring committee approval for every laboratory tube purchase.",
                    "C. Using post-project random audits for small items while checking high-risk contracts closely.",
                    "D. Judging research integrity by the number of stamps collected before work begins.",
                ],
                "answer": "C",
                "explanation": "C正确，结合P5“把高额合同与日常耗材分开”和P6“用项目后随机抽查取代小额物品的反复事前审批”可得C。A违背P5让步；B、D正是作者反对的做法。",
            },
        ],
        "sentences": [
            {
                "sentence": "New checklists appear each semester until preparation becomes a superfluous routine, taking quiet hours that a graduate assistant or senior scholar would otherwise spend in the archive or laboratory testing ideas.",
                "analysis": "until引导结果状语从句；现在分词短语taking quiet hours...作伴随结果状语；that引导定语从句修饰hours，其中would otherwise spend表示“原本可以用在……”，突出多余表格对科研时间的挤占。",
            },
            {
                "sentence": "The profound irony is that rules built to protect integrity can reward tidy paperwork more than careful science.",
                "analysis": "that引导表语从句；过去分词短语built to protect integrity后置修饰rules；reward A more than B比较了规则的实际激励方向，点明初衷与结果的倒置。",
            },
        ],
    },
    {
        "id": "ky23-high-wl01-day-2-art-2",
        "chapterId": "ky23-high-wl01-day-2",
        "group": "高频词",
        "groupDay": 2,
        "wordList": "Word List 1",
        "articleNumber": 2,
        "scheduledDate": "2026-11-20",
        "title": "One Soil Test for Every Hill",
        "zhTitle": "套用每一座山丘的同一套土壤检测",
        "paragraphs": [
            [
                "Modern **agriculture** faces steady **pressure** to produce more food while keeping fertilizer out of streams and village wells. In response, an imagined ministry introduces a single **procedure** for green grants: every farm must send **regular** soil samples to a central lab each spring. The rule looks like an **obvious** improvement over guesswork. Yet a **paradox** appears when one national **measure** is applied to fields with very different water and rock beneath them.",
                "现代农业面临着既要多产粮食、又要防止化肥流入溪流和村井的持续压力。为此，一个设想的部委推出了统一的绿色补贴程序：每个农场必须每年春天定期向中心实验室寄送土壤样本。这条规则看似是对凭感觉估算的明显改进。然而，当单一的全国衡量标准被套用到地下水分与岩石截然不同的田地时，悖论便出现了。",
            ],
            [
                "In hill districts with **peculiar** drainage, heavy rain washes minerals down a slope in a few days. A farmer who follows a fixed calendar may record high nitrogen **exposure** in April and a sharp shortage in June without changing habits at all. When an **ambitious** county office cuts support after one bad reading, smallholders become **anxious** about passing the test rather than building healthy soil over time. Fear of official **failure** nudges them toward quick chemical treatments that steady the numbers right before the inspector arrives.",
                "在排水情况特殊的丘陵地区，大雨几天之内就会把矿物质冲下山坡。遵循固定日历的农户即便完全不改变耕作习惯，也可能在四月测出高氮暴露，而在六月出现急剧的氮短缺。当雄心勃勃的县办公室仅凭一次不佳读数就削减扶持时，小农户便开始焦虑如何通过检测，而非长期培育健康土壤。对官方考核失败的恐惧，促使他们转向能在检查员到来前稳住数字的速效化学处理。",
            ],
            [
                "Researchers who study **parallel** programmes in neighbouring valleys note that **serious** soil recovery cannot be summed up in a single **paragraph** on an annual certificate. Building organic matter in tired fields is a **gradual** task whose reward often lags behind the initial expense by two or three harvests. If a visiting **scholar** judges a valley only by one season's chart, **cautious** growers who plant slow cover crops look worse than neighbours who time a quick synthetic dose right before test week.",
                "研究邻近山谷并行项目的学者指出，真正的土壤恢复无法概括成年度证书上的短短一段话。在疲敝田地里积累有机质是一项渐进的工作，其回报往往比初期投入滞后两三个收成季。如果来访学者仅凭一个季节的图表评判山谷，种植慢效覆盖作物的谨慎农户，看起来就会比赶在检测周前施用速效合成化肥的邻居更差。",
            ],
            [
                "This distortion shows how a measurement tool can reshape the everyday practice it was meant to observe. Once a laboratory threshold becomes the sole gatekeeper for farm income, growers naturally work for the assay rather than for resilient land over the decade. The difficulty is not that chemical testing is false, but that an isolated reading strips away the weather, crop rotation, and slope needed to interpret what the number actually means.",
                "这种扭曲表明，测量工具会重塑它本应观察的日常实践。一旦实验室阈值成为决定农场收入的唯一守门人，耕作者自然会围着化验转，而不是在十年间培育有韧性的土地。问题不在于化学检测有假，而在于孤立的读数剥离了天气、轮作与坡度背景，使人无法解读那个数字究竟意味着什么。",
            ],
            [
                "Supporters of a uniform standard reply that flexible local rules can invite quiet favouritism in rural offices. Without clear national numbers, grants might flow to well-connected estates regardless of how they treat the land or nearby water. That warning carries real weight, because vague rules have weakened rural programmes before. Even so, administrative fairness does not require pretending that steep hill clay and flat river soil behave alike after a heavy spring storm.",
                "支持统一标准的人回应说，灵活的地方规则可能在基层办公室招致隐蔽的偏袒。没有清晰的全国数值，补贴可能流向人脉深厚的庄园，而不管它们如何对待土地或附近水源。这一警告确实很有分量，因为含糊的规则过去曾削弱过农村项目。即便如此，行政上的公平并不要求我们假装陡坡黏土与平地河泥在一场春雨暴发后表现相同。",
            ],
            [
                "A better scheme would combine lab tests with multi-year trend records and field visits by local advisers who know the terrain well. Instead of penalizing a single odd sample, the agency could use it to start a practical check of drainage and crop cover on the farm. When data serves as a guide for repair rather than an automatic fine, farmers can care for the land without fearing that a wet week will cost them their annual grant.",
                "更好的方案会把实验室检测与多年趋势记录及熟悉地形的当地顾问实地走访结合起来。机构不必惩罚单次异常样本，而是可以用它启动对农场排水和作物覆盖情况的实地核查。当数据充当修复指南而非自动罚单时，农户就能悉心照料土地，而不必担心一周阴雨会让自己丢掉年度补贴。",
            ],
        ],
        "glossary": [
            {"dayOrder": 26, "word": "failure", "surface": "failure", "para": "P2", "meaning": "n. 失败、考核未通过；official failure官方考核不及格。"},
            {"dayOrder": 27, "word": "pressure", "surface": "pressure", "para": "P1", "meaning": "n. 压力；steady pressure持续的压力。"},
            {"dayOrder": 28, "word": "measure", "surface": "measure", "para": "P1", "meaning": "n. 衡量标准、尺度；one national measure单一全国衡量标准，此处非“措施”。"},
            {"dayOrder": 29, "word": "procedure", "surface": "procedure", "para": "P1", "meaning": "n. 程序、手续；a single procedure统一的程序。"},
            {"dayOrder": 30, "word": "exposure", "surface": "exposure", "para": "P2", "meaning": "n. 暴露量、接触；high nitrogen exposure高氮暴露读数。"},
            {"dayOrder": 31, "word": "agriculture", "surface": "agriculture", "para": "P1", "meaning": "n. 农业；modern agriculture现代农业。"},
            {"dayOrder": 32, "word": "parallel", "surface": "parallel", "para": "P3", "meaning": "a. 并行的、类似的；parallel programmes并行开展的项目。"},
            {"dayOrder": 33, "word": "paradox", "surface": "paradox", "para": "P1", "meaning": "n. 悖论、事与愿违的情况；a paradox appears出现悖论。"},
            {"dayOrder": 34, "word": "paragraph", "surface": "paragraph", "para": "P3", "meaning": "n. 段落；a single paragraph短短一段话。"},
            {"dayOrder": 35, "word": "obvious", "surface": "obvious", "para": "P1", "meaning": "a. 明显的；an obvious improvement明显的改进。"},
            {"dayOrder": 36, "word": "serious", "surface": "serious", "para": "P3", "meaning": "a. 真正的、严肃认真的；serious soil recovery真正的土壤恢复。"},
            {"dayOrder": 37, "word": "cautious", "surface": "cautious", "para": "P3", "meaning": "a. 谨慎的；cautious growers谨慎的耕作者。"},
            {"dayOrder": 38, "word": "ambitious", "surface": "ambitious", "para": "P2", "meaning": "a. 急于求成的、雄心勃勃的；an ambitious county office急于出政绩的县办公室。"},
            {"dayOrder": 39, "word": "anxious", "surface": "anxious", "para": "P2", "meaning": "a. 焦虑的；anxious about passing the test对通过检测感到焦虑。"},
            {"dayOrder": 40, "word": "scholar", "surface": "scholar", "para": "P3", "meaning": "n. 学者；a visiting scholar来访学者。"},
            {"dayOrder": 41, "word": "regular", "surface": "regular", "para": "P1", "meaning": "a. 定期的；send regular soil samples定期寄送土壤样本。"},
            {"dayOrder": 42, "word": "peculiar", "surface": "peculiar", "para": "P2", "meaning": "a. 特有的、特殊的；peculiar drainage特殊的排水地形，不是贬义“古怪”。"},
        ],
        "crossovers": [
            {"word": "gradual", "para": "P3", "meaning": "a. 渐进的；a gradual task一项渐进的工作。"},
        ],
        "questions": [
            {
                "ordinal": 1,
                "stem": "The paradox in Paragraphs 1 and 2 is that a uniform soil test can",
                "options": [
                    "A. encourage short-term chemical fixes instead of long-term soil care.",
                    "B. make hill farmers abandon fertilizer altogether.",
                    "C. work better on steep slopes than on flat valleys.",
                    "D. prevent central labs from measuring nitrogen levels in spring.",
                ],
                "answer": "A",
                "explanation": "A正确，P1—P2指出统一检测忽视地形排水差异，反而促使小农户为稳住纸面读数而采用速效化学处理（quick chemical treatments），违背了绿色补贴初衷。B、C、D均与文意相反。",
            },
            {
                "ordinal": 2,
                "stem": "In Paragraph 2, 'peculiar' most nearly means",
                "options": [
                    "A. artificial.",
                    "B. distinctive.",
                    "C. negligible.",
                    "D. suspicious.",
                ],
                "answer": "B",
                "explanation": "B正确，peculiar drainage指丘陵地区“特殊、独特（distinctive）”的排水条件，不是贬义的“可疑（suspicious）”或“人为（artificial）”。",
            },
            {
                "ordinal": 3,
                "stem": "Why do cautious growers planting cover crops look worse on one season's chart?",
                "options": [
                    "A. Cover crops wash minerals down the slope faster than rain does.",
                    "B. Organic recovery takes longer to show on a chart than a timed chemical dose.",
                    "C. Neighbouring valleys forbid the use of organic matter in spring.",
                    "D. Visiting scholars refuse to test fields planted with cover crops.",
                ],
                "answer": "B",
                "explanation": "B正确，P3指出积累有机质是渐进工作，回报滞后于投入，因而在单季图表上不如赶在检测周施用合成化肥的邻居好看。A、C、D无中生有。",
            },
            {
                "ordinal": 4,
                "stem": "What concern raised by supporters of uniform standards does the author accept?",
                "options": [
                    "A. Steep clay and flat river soil react identically to spring storms.",
                    "B. Vague local rules could allow grants to favour well-connected farms.",
                    "C. Multi-year trend records are too costly for county offices to keep.",
                    "D. Chemical testing has no scientific value for modern agriculture.",
                ],
                "answer": "B",
                "explanation": "B正确，P5承认统一标准支持者的警告很有分量：缺乏清晰标准时，含糊规则可能让补贴流向人脉深厚的庄园。A与P5末句相反；C无依据；D与P4“not that chemical testing is false”矛盾。",
            },
            {
                "ordinal": 5,
                "stem": "How should an unusual soil reading be used according to Paragraph 6?",
                "options": [
                    "A. As an automatic reason to cancel a farm's green grant.",
                    "B. As proof that the central laboratory made an error.",
                    "C. As a prompt for a field check and practical advice on drainage.",
                    "D. As a confidential record kept hidden from local advisers.",
                ],
                "answer": "C",
                "explanation": "C正确，P6建议不必惩罚单次异常样本，而应将其用于启动对排水与作物覆盖情况的实地核查（start a practical check）。",
            },
        ],
        "sentences": [
            {
                "sentence": "If a visiting scholar judges a valley only by one season's chart, cautious growers who plant slow cover crops look worse than neighbours who time a quick synthetic dose right before test week.",
                "analysis": "If引导条件从句；主句中两个who定语从句分别修饰cautious growers与neighbours，对比“种慢效覆盖作物”与“卡在检测周前施速效合成化肥（time作动词，意为专门择时）”在短期图表上的反差。",
            },
            {
                "sentence": "The difficulty is not that chemical testing is false, but that an isolated reading strips away the weather, crop rotation, and slope needed to interpret what the number actually means.",
                "analysis": "not that... but that...连接两个并列表语从句，否定“检测本身造假”，指出真正问题在于“孤立读数剥离了天气、轮作和坡度等解读背景”；过去分词短语needed to interpret...后置修饰并列名词。",
            },
        ],
    },
    # ==================== DAY 3 (2026-11-21, ky23-high-wl02-day-3, rows 84..127) ====================
    {
        "id": "ky23-high-wl02-day-3-art-1",
        "chapterId": "ky23-high-wl02-day-3",
        "group": "高频词",
        "groupDay": 3,
        "wordList": "Word List 2",
        "articleNumber": 1,
        "scheduledDate": "2026-11-21",
        "title": "The Cool Plaza That Nobody Uses",
        "zhTitle": "无人问津的降温广场",
        "paragraphs": [
            [
                "As summers grow hotter, **urban** authorities have tested **diverse** ways to cool crowded streets. An **influential** planning **philosophy** holds that a computer model can guide shade and pavement choices everywhere. When a university **professor** introduces a **universal** heat map, city hall often greets the **initial** **version** as an objective answer to a hard political question. Yet the **influence** of a clean diagram can hide how people actually move through a block during the hottest hours of the day.",
                "随着夏季越来越热，城市主管部门测试了多种为拥挤街道降温的办法。一种有影响力的规划理念认为，计算机模型可以指导所有地方的遮阴与铺装选择。当大学教授推出通用热力图时，市政厅常把最初版本当作棘手政治问题的客观答案来欢迎。然而，干净图表的影响力可能掩盖人们在一天中最热时段在街区里的真实活动方式。",
            ],
            [
                "A **major** gap appears when designers **ignore** daily routines on the ground. On screen, a pale stone square lowers midday heat for the **majority** of passers-by in the district. Set **apart** from bus stops and evening food stalls, however, that square stays empty while narrow lanes nearby remain stifling. A **professional** **philosopher** would remind the team that a map is a summary, not the street itself: what a sensor records at noon differs from the heat felt by an older **resident** carrying groceries home at six.",
                "当设计者忽视实地日常惯例时，重大缺口就出现了。在屏幕上，浅色石材广场降低了街区内大多数正午过路人所处的温度。然而，由于同公交站与夜间小吃摊隔开，这座广场空空荡荡，附近窄巷却依旧闷热。专业哲学家会提醒团队，地图只是概括而非街道本身：传感器在正午记录的数值，不同于傍晚六点提着杂货回家的老年居民感受到的暑热。",
            ],
            [
                "Using satellite scores alone to **assess** a local **initiative** can also **upset** workable street habits that residents built over years. In an older **settlement**, shopkeepers stretch cloth awnings across the lane each afternoon to protect fruit and customers from the sun. Because the overhead model does not count movable cloth, inspectors may order the awnings taken down to **reverse** a supposed clutter problem. Without honest **conversation** between city engineers and stallholders, a project meant to cool the quarter removes its best shade.",
                "仅凭卫星评分来评估地方倡议，还会打乱居民多年来建立的可行街头习惯。在一处老聚居区，店主每天下午在巷道上方拉开布篷，为水果和顾客遮挡烈日。由于高空模型不统计活动布篷，检查员可能下令将其拆除，以扭转所谓的杂乱问题。如果城市工程师与摊主之间缺乏坦诚交谈，旨在为街区降温的项目反而会拆掉当地最好的阴凉。",
            ],
            [
                "Work in **cognitive** science helps explain why bright maps win arguments so easily in committee rooms. Neat colour bands quiet public doubt and give an agency **president** a simple success story for the evening news broadcast. Each pilot **episode** of stone paving is shown in reports as proof that the master plan works as promised. Yet visual certainty can breed overconfidence, tempting officials to treat unmapped habits as noise rather than useful evidence about how a street lives.",
                "认知科学的研究有助于解释为何鲜亮的地图如此容易在会议室里赢得争论。整齐的色带能平息公众疑虑，并为机构负责人提供登上晚间新闻广播的简单成功故事。石材铺装的每个试点片段都在报告中被展示为总体规划如期奏效的证据。然而，视觉上的确定感会滋生过度自信，诱使官员把未绘入地图的习惯当作杂音，而非反映一条街道如何运转的有用证据。",
            ],
            [
                "Supporters of citywide modelling reply that climate planning cannot rely on street anecdotes alone. Without a common baseline, wealthy districts often lobby for extra trees and fountains while industrial quarters are forgotten. That point is sound: broad maps are needed to expose unequal shade across a large metropolis. Still, using a city map to distribute funds differs from using it to redesign a narrow lane without asking the people who walk there every day.",
                "支持全市建模的人回应说，气候规划不能只靠街头轶事。没有共同基线，富裕街区常会游说争取更多树木与喷泉，而工业区则被遗忘。这一点站得住脚：需要宏观地图来揭露大都市内遮阴分布的不公。但用城市地图分配资金，与不问每天走过那里的人就用它改造窄巷，是两回事。",
            ],
            [
                "Better adaptation would pair overhead maps with patient observation on foot across the summer months. Before removing shop awnings or moving bus shelters, planners should visit the street at different hours and ask where heat lingers after dark. When technical models are revised through local experience, cooling projects become both fairer on paper and more likely to be used by the neighbourhood in daily life.",
                "更好的适应方案会把高空地图与整个夏季耐心的徒步观察结合起来。在拆除商铺布篷或挪动公交候车亭之前，规划者应在不同时段走访街道，询问入夜后暑热停留在哪里。当技术模型通过本地经验得到修正时，降温项目才能既在账面上更公平，又更可能在日常生活中被街区居民实际使用。",
            ],
        ],
        "glossary": [
            {"dayOrder": 1, "word": "influence", "surface": "influence", "para": "P1", "meaning": "n. 影响；the influence of a clean diagram干净图表的影响。"},
            {"dayOrder": 2, "word": "influential", "surface": "influential", "para": "P1", "meaning": "a. 有影响力的；an influential planning philosophy有影响力的规划理念。"},
            {"dayOrder": 3, "word": "professor", "surface": "professor", "para": "P1", "meaning": "n. 教授；a university professor大学教授。"},
            {"dayOrder": 4, "word": "professional", "surface": "professional", "para": "P2", "meaning": "a. 专业的；a professional philosopher专业哲学家。"},
            {"dayOrder": 5, "word": "diverse", "surface": "diverse", "para": "P1", "meaning": "a. 多种多样的；diverse ways多种办法。"},
            {"dayOrder": 6, "word": "reverse", "surface": "reverse", "para": "P3", "meaning": "v. 扭转、消除；reverse a supposed clutter problem扭转所谓的杂乱问题。"},
            {"dayOrder": 7, "word": "version", "surface": "version", "para": "P1", "meaning": "n. 版本；the initial version最初版本。"},
            {"dayOrder": 8, "word": "universal", "surface": "universal", "para": "P1", "meaning": "a. 通用的、普遍适用的；a universal heat map通用热力图。"},
            {"dayOrder": 9, "word": "conversation", "surface": "conversation", "para": "P3", "meaning": "n. 交谈、沟通；honest conversation坦诚交谈。"},
            {"dayOrder": 10, "word": "philosophy", "surface": "philosophy", "para": "P1", "meaning": "n. 指导理念、哲学；planning philosophy规划理念。"},
            {"dayOrder": 11, "word": "philosopher", "surface": "philosopher", "para": "P2", "meaning": "n. 哲学家；a philosopher哲学家。"},
            {"dayOrder": 12, "word": "initial", "surface": "initial", "para": "P1", "meaning": "a. 最初的；the initial version最初版本。"},
            {"dayOrder": 13, "word": "initiative", "surface": "initiative", "para": "P3", "meaning": "n. 新方案、倡议；a local initiative地方降温倡议。"},
            {"dayOrder": 14, "word": "urban", "surface": "urban", "para": "P1", "meaning": "a. 城市的；urban authorities城市主管部门。"},
            {"dayOrder": 15, "word": "major", "surface": "major", "para": "P2", "meaning": "a. 重大的、主要的；a major gap重大缺口。"},
            {"dayOrder": 16, "word": "majority", "surface": "majority", "para": "P2", "meaning": "n. 大多数；the majority of passers-by大多数过路人。"},
            {"dayOrder": 17, "word": "apart", "surface": "apart", "para": "P2", "meaning": "ad. 分开、相隔；set apart from与……隔开。"},
            {"dayOrder": 18, "word": "cognitive", "surface": "cognitive", "para": "P4", "meaning": "a. 认知的；cognitive science认知科学。"},
            {"dayOrder": 19, "word": "ignore", "surface": "ignore", "para": "P2", "meaning": "v. 忽视；ignore daily routines忽视日常惯例。"},
            {"dayOrder": 20, "word": "upset", "surface": "upset", "para": "P3", "meaning": "v. 打乱、搅乱；upset workable street habits打乱原本可行的街头习惯，不是情绪难过。"},
            {"dayOrder": 21, "word": "settlement", "surface": "settlement", "para": "P3", "meaning": "n. 聚居区、住区；an older settlement老聚居区，此处非协议解决。"},
            {"dayOrder": 22, "word": "resident", "surface": "resident", "para": "P2", "meaning": "n. 居民；an older resident老年居民。"},
            {"dayOrder": 23, "word": "president", "surface": "president", "para": "P4", "meaning": "n. 机构负责人、总裁、院长；an agency president机构负责人。"},
            {"dayOrder": 24, "word": "assess", "surface": "assess", "para": "P3", "meaning": "v. 评估；assess a local initiative评估地方新方案。"},
            {"dayOrder": 25, "word": "episode", "surface": "episode", "para": "P4", "meaning": "n. 片段、一期工程；each pilot episode每个试点片段。"},
        ],
        "crossovers": [],
        "questions": [
            {
                "ordinal": 1,
                "stem": "Why does the pale stone square in Paragraph 2 remain empty?",
                "options": [
                    "A. Its surface becomes hotter than nearby lanes at noon.",
                    "B. It is separated from the places where residents actually wait and shop.",
                    "C. Older residents are forbidden to enter it with groceries.",
                    "D. Sensors failed to record its midday temperature.",
                ],
                "answer": "B",
                "explanation": "B正确，P2指出该广场与公交站和夜间小吃摊隔开（set apart from bus stops and evening food stalls），忽视了日常动线，因而空无一人。A、C、D均与P2矛盾。",
            },
            {
                "ordinal": 2,
                "stem": "The cloth awnings in Paragraph 3 are discussed to show that",
                "options": [
                    "A. movable shade is a major cause of street clutter.",
                    "B. stallholders refuse to speak with municipal engineers.",
                    "C. judging a street only by an overhead model can destroy effective local shade.",
                    "D. older settlements cannot benefit from cooling initiatives.",
                ],
                "answer": "C",
                "explanation": "C正确，P3指出高空模型不统计活动布篷，检查员下令拆除反而毁掉了当地最好的阴凉。A把“supposed clutter problem”当成事实；B、D无依据。",
            },
            {
                "ordinal": 3,
                "stem": "According to Paragraph 4, bright heat maps appeal to officials partly because they",
                "options": [
                    "A. automatically include unmapped street habits.",
                    "B. reduce doubt and provide a clear story for public reports.",
                    "C. prevent cognitive scientists from questioning the master plan.",
                    "D. cost less than talking with shopkeepers.",
                ],
                "answer": "B",
                "explanation": "B正确，P4指出整齐色带能平息疑虑，并为机构负责人提供登上晚间新闻的简单成功故事。A与P4末句相反；C、D无中生有。",
            },
            {
                "ordinal": 4,
                "stem": "What role for citywide heat maps does the author endorse in Paragraph 5?",
                "options": [
                    "A. Designing narrow lanes without consulting walkers.",
                    "B. Replacing street observation in industrial quarters.",
                    "C. Revealing unequal shade distribution across the city to guide funding.",
                    "D. Helping wealthy districts lobby for additional trees.",
                ],
                "answer": "C",
                "explanation": "C正确，P5肯定宏观地图对于揭露全市遮阴分布不公、指导资金分配的必要性，但反对不问居民就用它直接规定小巷设计（排除A、B）；D是缺乏基线时的弊端。",
            },
            {
                "ordinal": 5,
                "stem": "Which action best matches the author's conclusion?",
                "options": [
                    "A. Walking the street at different hours and revising models with resident feedback.",
                    "B. Removing all cloth awnings before testing pavement temperatures.",
                    "C. Relying solely on noon satellite scores to judge cooling projects.",
                    "D. Abandoning computer models in favour of neighbourhood anecdotes.",
                ],
                "answer": "A",
                "explanation": "A正确，P6建议把高空地图与不同时段的徒步走访和居民反馈结合起来修正模型。B、C与全文相反；D忽略了P5对宏观地图的肯定。",
            },
        ],
        "sentences": [
            {
                "sentence": "A professional philosopher would remind the team that a map is a summary, not the street itself: what a sensor records at noon differs from the heat felt by an older resident carrying groceries home at six.",
                "analysis": "冒号前that从句提出“地图是概括而非街道本身”；冒号后what从句作主语，与differs from后的the heat对照，过去分词短语felt by...及现在分词短语carrying...层层修饰，具象化“传感器读数”与“人体实际感受”的差异。",
            },
            {
                "sentence": "Still, using a city map to distribute funds differs from using it to redesign a narrow lane without asking the people who walk there every day.",
                "analysis": "两个动名词短语using a city map to...与using it to...通过differs from对比，区分了“宏观分配资金”与“不问行人就微观改造窄巷”的合理边界。",
            },
        ],
    },
    {
        "id": "ky23-high-wl02-day-3-art-2",
        "chapterId": "ky23-high-wl02-day-3",
        "group": "高频词",
        "groupDay": 3,
        "wordList": "Word List 2",
        "articleNumber": 2,
        "scheduledDate": "2026-11-21",
        "title": "What the Scanner Leaves Behind",
        "zhTitle": "扫描仪留下的隐患",
        "paragraphs": [
            [
                "Public archives increasingly scan old newspapers and parish books so that readers can **collect** historical material from home without travelling. Yet a digital **collection** is only as safe as the legal and technical **structure** beneath it. When a library decides to **import** high-speed cameras or **export** catalogue files to an outside server, managers may miss the full **import** of giving up direct custody. Treating preservation as a quick software purchase rather than lasting civic **infrastructure** puts shared memory at risk over the long run.",
                "公共档案馆越来越多地扫描旧报纸和教区簿册，以便读者无需奔波即可在家收集历史资料。然而，数字馆藏的安全性取决于其底层的法律与技术结构。当图书馆决定进口高速相机或将目录文件导出到外部服务器时，管理者可能忽视了放弃直接保管权的全部严重含意。把文献保存当作快速软件采购而非持久的公共基础设施，长期来看会让共同记忆面临风险。",
            ],
            [
                "A regional museum learned this lesson after hiring a private firm to manage the **transport** and scanning of fragile glass plates from the nineteenth century. Only a small **proportion** of the annual budget went to open file maintenance, while most funded a bright search page for online visitors. A local **reporter** later found that hundreds of folders could no longer be opened because the custom viewer lacked clear **instruction** notes after the firm closed its doors. What looked like a permanent vault depended on one company's survival.",
                "一家地区博物馆在聘请私人公司管理十九世纪脆弱玻璃底片的运输与扫描后，吸取了这一教训。年度预算中只有很小比例用于开放文件维护，大部分都投给了面向线上访客的华丽搜索页面。一名当地记者后来发现，在该公司关门倒闭后，由于定制阅读器缺乏清晰的使用说明，数百个文件夹已无法打开。看似永久保险库的系统，竟取决于一家公司的存续。",
            ],
            [
                "Choosing what to scan first also shapes **intellectual** life across a university and beyond. Because money is tight, archivists must **select** certain boxes while others wait on dark shelves for years. If their **selection** consistently favours big city papers over village or **religious** newsletters, historians inherit a narrow picture of the past. Even a careful **colleague** can misjudge a period by treating an online index as the whole social record rather than a partial sample.",
                "决定先扫描什么同样塑造着大学内外的学术生活。由于经费紧张，档案员必须挑选部分档案盒，而让其他档案在昏暗架子上等待多年。如果他们的遴选一贯偏爱大城市报纸，却冷落乡村或宗教简报，历史学家继承的就会是一幅狭窄的过去图景。即便是严谨的同行，若把线上索引当作全部社会记录而非局部样本，也会误判一个时代。",
            ],
            [
                "Nor are commercial server rooms free from physical **destruction**. Coastal floods, fires, and software faults can erase digital copies faster than dry air wears down rag paper in a basement. A scanner is a valuable **instrument** for widening public access, but it does not replace cool storage rooms and acid-free boxes. A **reliable** archive keeps both readable originals and open-format files in more than one place so that a single accident cannot wipe out both at once.",
                "商业机房也并非免于物理损毁。沿海洪水、火灾和软件故障抹去数字副本的速度，比地下室干燥空气磨损棉纸更快。扫描仪是扩大公众获取范围的宝贵工具，但它不能取代阴凉库房与无酸档案盒。可靠的档案馆会在不止一处地点同时保存可读原件与开放格式文件，以免单次事故将两者一并抹去。",
            ],
            [
                "Some commentators still argue that storing paper is wasteful once clear images are online for everyone to read. Selling old storage halls, they say, frees scarce urban space for bright student reading rooms and exhibition desks. That view confuses present screen convenience with survival across decades. A page printed two hundred years ago can still be read by eye, whereas a file locked in an obsolete format turns blank as soon as its matching machine disappears.",
                "一些评论者仍然辩称，一旦清晰图像上线供所有人阅读，保存纸张就是浪费。他们说，卖掉旧库房能为明亮的学生阅览室和展台腾出稀缺的城市空间。这种看法把眼前的屏幕便利与跨越数十年的存续混为一谈了。两百年前印出的书页至今仍能用肉眼阅读，而锁在过时格式里的文件，一旦配套机器消失就会变成一片空白。",
            ],
            [
                "Good stewardship therefore resists the easy promise of effortless permanence. Public grant agencies should ask archives to publish their selection rules, use open file formats, and budget for regular copying onto new drives every few years. When digital tools support physical care instead of replacing it, readers gain speed at their desks without losing the historical record itself.",
                "因此，良好的保管会抵制“不费力即可永久保存”的轻率许诺。公共资助机构应要求档案馆公布遴选规则、使用开放文件格式，并为每隔几年定期转录到新硬盘预留预算。当数字工具支撑而非取代实物保护时，读者才能在书桌前获得便捷，同时不丢失历史记录本身。",
            ],
        ],
        "glossary": [
            {"dayOrder": 26, "word": "import", "surface": "import", "para": "P1", "meaning": "v./n. 进口/重要含意；import cameras为动词“进口”，the full import为名词“全部严重含意、利害关系”。"},
            {"dayOrder": 27, "word": "export", "surface": "export", "para": "P1", "meaning": "v. 导出、输出；export catalogue files导出目录文件。"},
            {"dayOrder": 28, "word": "transport", "surface": "transport", "para": "P2", "meaning": "n. 运输；the transport and scanning运输与扫描。"},
            {"dayOrder": 29, "word": "reporter", "surface": "reporter", "para": "P2", "meaning": "n. 记者；a local reporter当地记者。"},
            {"dayOrder": 30, "word": "proportion", "surface": "proportion", "para": "P2", "meaning": "n. 比例、份额；a small proportion of the annual budget年度预算的一小部分。"},
            {"dayOrder": 31, "word": "collect", "surface": "collect", "para": "P1", "meaning": "v. 收集；collect historical material收集历史资料。"},
            {"dayOrder": 32, "word": "collection", "surface": "collection", "para": "P1", "meaning": "n. 馆藏、收藏品；a digital collection数字馆藏。"},
            {"dayOrder": 33, "word": "select", "surface": "select", "para": "P3", "meaning": "v. 挑选、遴选；select certain boxes挑选部分档案盒。"},
            {"dayOrder": 34, "word": "selection", "surface": "selection", "para": "P3, P6", "meaning": "n. 遴选、选择；their selection他们的遴选。"},
            {"dayOrder": 35, "word": "intellectual", "surface": "intellectual", "para": "P3", "meaning": "a. 学术的、智识的；intellectual life学术生活。"},
            {"dayOrder": 36, "word": "instrument", "surface": "instrument", "para": "P4", "meaning": "n. 工具、手段；a valuable instrument宝贵的工具。"},
            {"dayOrder": 37, "word": "instruction", "surface": "instruction", "para": "P2", "meaning": "n. 用法说明、操作指南；instruction notes使用说明。"},
            {"dayOrder": 38, "word": "destruction", "surface": "destruction", "para": "P4", "meaning": "n. 毁坏、毁灭；physical destruction物理损毁。"},
            {"dayOrder": 39, "word": "structure", "surface": "structure", "para": "P1", "meaning": "n. 结构；legal and technical structure法律与技术结构。"},
            {"dayOrder": 40, "word": "infrastructure", "surface": "infrastructure", "para": "P1", "meaning": "n. 基础设施；civic infrastructure公共基础设施。"},
            {"dayOrder": 41, "word": "reliable", "surface": "reliable", "para": "P4", "meaning": "a. 可靠的；a reliable archive可靠的档案馆。"},
            {"dayOrder": 42, "word": "colleague", "surface": "colleague", "para": "P3", "meaning": "n. 同行、同事；a careful colleague严谨的同行。"},
            {"dayOrder": 43, "word": "religious", "surface": "religious", "para": "P3", "meaning": "a. 宗教的；religious newsletters宗教简报。"},
        ],
        "crossovers": [],
        "questions": [
            {
                "ordinal": 1,
                "stem": "In Paragraph 1, 'the full import' most nearly means",
                "options": [
                    "A. the foreign tax on cameras.",
                    "B. the serious consequence and meaning.",
                    "C. the speed of file transfer.",
                    "D. the total number of scanned pages.",
                ],
                "answer": "B",
                "explanation": "B正确，P1同一句中前一个import是动词“进口（相机）”，后一个the full import of giving up direct custody是名词生义“放弃直接保管权的全部严重含意与后果”。",
            },
            {
                "ordinal": 2,
                "stem": "What went wrong in the regional museum case in Paragraph 2?",
                "options": [
                    "A. Glass plates were broken during road transport.",
                    "B. The local reporter deleted hundreds of digital folders.",
                    "C. Reliance on a closed firm's custom software left files unreadable.",
                    "D. The museum spent too much money on open file maintenance.",
                ],
                "answer": "C",
                "explanation": "C正确，P2指出博物馆把钱花在门面上，只留极少预算给开放文件维护，结果外包公司倒闭后定制阅读器缺乏说明，导致数百个文件夹打不开。A、B、D与原文不符。",
            },
            {
                "ordinal": 3,
                "stem": "Paragraph 3 warns that selective scanning can lead historians to",
                "options": [
                    "A. mistake an incomplete online index for the whole historical record.",
                    "B. pay more attention to village newsletters than to city papers.",
                    "C. refuse to share catalogue files with careful colleagues.",
                    "D. stop reading nineteenth-century newspapers altogether.",
                ],
                "answer": "A",
                "explanation": "A正确，P3末句指出，若把有取舍偏向的线上索引当作全部记录而非局部样本，即便是严谨的同行也会误判一个时代。B与原文偏向大城市报纸相反；C、D无依据。",
            },
            {
                "ordinal": 4,
                "stem": "Why does the author disagree with selling paper storage halls in Paragraph 5?",
                "options": [
                    "A. Public reading rooms are no longer needed by online readers.",
                    "B. Two-hundred-year-old paper cannot be photographed clearly.",
                    "C. Digital files can become unreadable when their formats and machines grow obsolete.",
                    "D. Cool storage rooms are cheaper to run than small server racks.",
                ],
                "answer": "C",
                "explanation": "C正确，P5指出两百年前的纸页仍能肉眼阅读，而锁在过时格式里的文件一旦配套机器消失就会变成空白，不能把当前便利当成跨年代存续。A、B、D不合文意。",
            },
            {
                "ordinal": 5,
                "stem": "Which practice would the author most likely support?",
                "options": [
                    "A. Outsourcing all archival custody to a single software vendor.",
                    "B. Keeping physical originals while migrating open-format files onto new drives.",
                    "C. Hiding selection rules so that readers trust the online index.",
                    "D. Disposing of paper books as soon as they are scanned.",
                ],
                "answer": "B",
                "explanation": "B正确，结合P4“同时保存可读原件与开放格式文件”和P6“公布遴选规则、使用开放格式、为定期转录新硬盘留预算”可得B。",
            },
        ],
        "sentences": [
            {
                "sentence": "When a library decides to import high-speed cameras or export catalogue files to an outside server, managers may miss the full import of giving up direct custody.",
                "analysis": "When从句中import与export作动词并列（“进口相机或导出目录文件”）；主句中the full import作miss的宾语，取名词“重要性、深远含意”之义，在一句之内直观对比同形词的两种考法。",
            },
            {
                "sentence": "A page printed two hundred years ago can still be read by eye, whereas a file locked in an obsolete format turns blank as soon as its matching machine disappears.",
                "analysis": "whereas连接纸质原件与数字文件的对比；printed...与locked...均为过去分词短语后置修饰各自名词；as soon as引导时间条件，点明数字文件对硬件与格式链条的依赖。",
            },
        ],
    },
]

from kaoyan_articles_spec_days_04_06 import ARTICLES_SPEC_DAYS_04_06  # noqa: E402
from kaoyan_articles_spec_days_07_08 import ARTICLES_SPEC_DAYS_07_08  # noqa: E402
from kaoyan_articles_spec_days_09_10 import ARTICLES_SPEC_DAYS_09_10  # noqa: E402
from kaoyan_articles_spec_days_11_12 import ARTICLES_SPEC_DAYS_11_12  # noqa: E402
from kaoyan_articles_spec_days_13_14 import ARTICLES_SPEC_DAYS_13_14  # noqa: E402
from kaoyan_articles_spec_days_15_16 import ARTICLES_SPEC_DAYS_15_16  # noqa: E402
from kaoyan_articles_spec_days_17_18 import ARTICLES_SPEC_DAYS_17_18  # noqa: E402
from kaoyan_articles_spec_days_19_20 import ARTICLES_SPEC_DAYS_19_20  # noqa: E402
from kaoyan_articles_spec_medium_01_02 import ARTICLES_SPEC_MEDIUM_01_02  # noqa: E402
from kaoyan_articles_spec_medium_03_04 import ARTICLES_SPEC_MEDIUM_03_04  # noqa: E402
from kaoyan_articles_spec_medium_05_06 import ARTICLES_SPEC_MEDIUM_05_06  # noqa: E402
from kaoyan_articles_spec_medium_07_08 import ARTICLES_SPEC_MEDIUM_07_08  # noqa: E402
from kaoyan_articles_spec_low_01_02 import ARTICLES_SPEC_LOW_01_02  # noqa: E402
from kaoyan_articles_spec_low_03_04 import ARTICLES_SPEC_LOW_03_04  # noqa: E402
from kaoyan_articles_spec_low_05_06 import ARTICLES_SPEC_LOW_05_06  # noqa: E402
from kaoyan_articles_spec_low_07_08 import ARTICLES_SPEC_LOW_07_08  # noqa: E402
from kaoyan_articles_spec_low_09_10 import ARTICLES_SPEC_LOW_09_10  # noqa: E402
from kaoyan_articles_spec_low_11_12 import ARTICLES_SPEC_LOW_11_12  # noqa: E402
from kaoyan_articles_spec_low_13_14 import ARTICLES_SPEC_LOW_13_14  # noqa: E402
from kaoyan_articles_spec_low_15_16 import ARTICLES_SPEC_LOW_15_16  # noqa: E402
from kaoyan_articles_spec_rare_01_02 import ARTICLES_SPEC_RARE_01_02  # noqa: E402
from kaoyan_articles_spec_rare_03_04 import ARTICLES_SPEC_RARE_03_04  # noqa: E402
from kaoyan_articles_spec_rare_05_06 import ARTICLES_SPEC_RARE_05_06  # noqa: E402
from kaoyan_articles_spec_rare_07_08 import ARTICLES_SPEC_RARE_07_08  # noqa: E402
from kaoyan_articles_spec_rare_09_10 import ARTICLES_SPEC_RARE_09_10  # noqa: E402
from kaoyan_articles_spec_rare_11_12 import ARTICLES_SPEC_RARE_11_12  # noqa: E402
from kaoyan_articles_spec_rare_13_14 import ARTICLES_SPEC_RARE_13_14  # noqa: E402
from kaoyan_articles_spec_rare_15_16 import ARTICLES_SPEC_RARE_15_16  # noqa: E402
from kaoyan_articles_spec_rare_17_18 import ARTICLES_SPEC_RARE_17_18  # noqa: E402
from kaoyan_articles_spec_rare_19_20 import ARTICLES_SPEC_RARE_19_20  # noqa: E402
from kaoyan_articles_spec_rare_21_22 import ARTICLES_SPEC_RARE_21_22  # noqa: E402
from kaoyan_articles_spec_rare_23_24 import ARTICLES_SPEC_RARE_23_24  # noqa: E402

ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_04_06)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_07_08)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_09_10)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_11_12)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_13_14)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_15_16)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_17_18)
ARTICLES_SPEC.extend(ARTICLES_SPEC_DAYS_19_20)
ARTICLES_SPEC.extend(ARTICLES_SPEC_MEDIUM_01_02)
ARTICLES_SPEC.extend(ARTICLES_SPEC_MEDIUM_03_04)
ARTICLES_SPEC.extend(ARTICLES_SPEC_MEDIUM_05_06)
ARTICLES_SPEC.extend(ARTICLES_SPEC_MEDIUM_07_08)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_01_02)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_03_04)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_05_06)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_07_08)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_09_10)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_11_12)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_13_14)
ARTICLES_SPEC.extend(ARTICLES_SPEC_LOW_15_16)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_01_02)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_03_04)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_05_06)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_07_08)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_09_10)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_11_12)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_13_14)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_15_16)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_17_18)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_19_20)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_21_22)
ARTICLES_SPEC.extend(ARTICLES_SPEC_RARE_23_24)

