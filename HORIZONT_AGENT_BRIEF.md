# HORIZONT — AI ATTACK & SECURITY RESEARCH AGENT
## Claude uchun to'liq kickoff prompt + brifing hujjati

> **Ishlatish:** Bu faylning HAMMASINI nusxalab, Claude Code (yoki Claude)ga tashlang.
> Bu Horizont agentini noldan **birga qurib chiqish** uchun boshlang'ich topshiriq.
> Ma'lumot 2026-09-29 da GitHub'dan live tekshirilgan.

---

## 0. CLAUDE'GA MUROJAAT (buni birinchi o'qi)

Salom Claude. Men **Horizont** nomli global AI security testing agentini qurmoqchiman.
Sen menga uni **bosqichma-bosqich, birga** qurishda yordam ber.

QOIDALAR:
1. **Hozircha final kod/config yozma** — avval har bosqichni men bilan tasdiqla.
2. Terminlarni birinchi ishlatganda **sodda izohla** (men o'rganyapman).
3. Har tavsiyani **nega kerakligi** bilan ayt.
4. Fakt va taxminni ajrat; eski ma'lumotni belgila; GitHub statusini **live** tekshir.
5. Ishni bosqichlarga bo'l va har bosqich oxirida "davom etamizmi?" deб so'ra.

---

## 1. HORIZONT NIMA (konsepsiya)

Horizont — **AI/LLM/Agent tizimlarining xavfsizligini** ruxsat etilgan muhitda
test qiladigan AI agent. Oddiy chatbot yoki payload generator EMAS.

Asosiy g'oya: an'anaviy tizimda "buyruq" va "ma'lumot" ajratilgan.
LLM'da esa ular bitta matn oqimida keladi — **chegara yo'qoladi**.
Barcha AI hujumlarning ildizi shu. Horizont shu chegara qayerda buzilishini
tizimli qidiradi.

Horizont **payload generator emas**, u tadqiqotchi:
```
Recon → Understand → Model → Hypothesize → Attack → Analyze → Chain → Verify → Report
```

---

## 2. HORIZONT vs ALAMUT (aralashtirma)

| | ALAMUT (CTF Agent) | HORIZONT (AI Attack Agent) |
|---|---|---|
| Maqsad | Challenge yechish, flag | AI tizim qanday buzilishini tadqiq |
| Target | Sun'iy masala | Real (ruxsat etilgan) AI ilova |
| G'alaba | flag{...} topildi | Weakness + evidence + chain + impact |
| Yo'nalish | Web/Pwn/Rev/Crypto/Forensics/OSINT | LLM/RAG/Agent/Tool/MCP |
| Uslub | Masalani buzib ochish | Tizimni modellashtirish + gipoteza |

AI hujum **bilimini** ikkalasi ham ishlata oladi, lekin **orchestration alohida**.

---

## 3. ASOSIY ATTACK SURFACE'LAR (6 ta) — har birida qaysi chegara buziladi

1. **LLM** — instruction/data chegarasi. Prompt injection, jailbreak,
   system prompt leakage, data leakage. *(Task A)*
2. **RAG** — trust + izolyatsiya chegarasi. Document/knowledge poisoning,
   retrieval manipulation, cross-tenant/cross-user leakage. *(Task B)*
3. **Agent** — autonomy chegarasi. "LLM nima dedi?" emas, "LLM qanday REAL
   action qila oladi?". Goal hijacking, excessive agency, memory poisoning. *(Task C)*
4. **Tool/Function** — least-privilege chegarasi. "Bu tool aslida qancha
   imtiyoz beradi?". Unsafe args, tool output injection, hidden capabilities. *(Task D)*
5. **MCP** — supply-chain chegarasi. Tool poisoning, rug pull, tool shadowing,
   scope creep, SSRF/command injection through tools. *(Task E)*
6. **Klassik infra (web/API)** — AI ostidagi oddiy tizim. SSRF, auth,
   metadata endpoint. AI hujum ko'pincha shu yerga ulanadi (chain). *(Task F)*

> MCP = Model Context Protocol (Anthropic standarti). LLM/agentга tashqi
> tool/resurs ulash uchun "USB port". Muammo: agent tool tavsifiga (metadata)
> ishonadi, va unga yashirin ko'rsatma joylashtirilishi mumkin.

---

## 4. QATLAMLAR MUNOSABATI (xavf ko'paytiriladi)

```
LLM        → matnni tushunadi              (instruction/data)
 +RAG      → tashqi bilim o'qiydi           (trust buziladi)
 +AGENT    → maqsad + tsikl, o'zi qaror qiladi (autonomy)
 +TOOL     → real action qiladi             (privilege)
 +MCP      → tashqi tool'larga ishonadi     (supply chain)
```

Namunaviy attack chain (Task G — Horizontning asosiy intellekti):
```
RAGdagi zararli hujjat → LLM uni ko'rsatma deб o'qidi → Agent maqsadini
o'zgartirdi → imtiyozli tool → SSRF → ichki xizmat → maxfiy ma'lumot (IMPACT)
```
Bitta zaiflik = past xavf. Zanjir = kritik xavf.

---

## 5. ARCHITECTURE (dastlabki — birga finallashtiramiz)

```
              ┌────────────────────────────┐
              │     SAFETY / SCOPE GATE      │  ← har qadamdan oldin
              │  allowlist·authz·human OK    │
              └──────────────┬───────────────┘
       ┌──────────────────────▼──────────────────────┐
       │              HORIZONT CORE (miya)             │
       │  OBSERVE→UNDERSTAND→HYPOTHESIZE→PLAN→ANALYZE  │
       │        ▲                            │         │
       │        └────────── LEARN ◄──────────┘         │
       └───┬──────────────┬─────────────────┬─────────┘
    ┌──────▼─────┐ ┌──────▼──────┐  ┌────────▼────────┐
    │ STATE STORE│ │ KNOWLEDGE   │  │   EXECUTORS      │
    │ target/AI/ │ │ OWASP/MITRE │  │ recon·llm·rag·   │
    │ findings/  │ │ patterns/   │  │ mcp·report       │
    │ attack/    │ │ chains      │  │ (garak,PyRIT,    │
    │ chain      │ │             │  │  mcp-scan...)    │
    └────────────┘ └─────────────┘  └─────────────────┘
    ┌───────────────────────────────────────────────┐
    │              AUDIT LOG (hamma action)           │
    └───────────────────────────────────────────────┘
```

Ochiq savol (birga hal qilamiz): Core LLM-orchestrator bo'ladimi yoki qat'iy
state-machine + LLM faqat gipoteza uchunmi? Bu "aql darajasini" belgilaydi.

---

## 6. CLAUDE CODE'DA QURILISH STRUKTURASI

Horizont = 3 blok kombinatsiyasi. "Global" = uy papkasida turadi.

```
~/.claude/
├── agents/horizont.md          ← MIYA: system prompt + workflow + qaysi tool
├── skills/
│   ├── llm-security/           ← BILIM: Task A
│   ├── rag-security/           ← BILIM: Task B
│   ├── agent-security/         ← BILIM: Task C
│   ├── tool-security/          ← BILIM: Task D
│   └── mcp-security/           ← BILIM: Task E
├── (MCP serverlar .mcp.json orqali ulanadi)  ← QO'LLAR
└── CLAUDE.md + Safety gate     ← scope allowlist, human confirm, audit log
```

- **Subagent** (`horizont.md`) = shaxs + system prompt + workflow.
- **Skills** = "qachon nima qilish" markdown modullari, kerak bo'lganda yuklanadi.
- **MCP serverlar** = tashqi tool'lar (garak, PyRIT, mcp-scan...).

Ishlash: `@horizont <target>` → skill o'qiydi → MCP tool chaqiradi →
state saqlaydi → keyingi gipoteza.

---

## 7. WORKFLOW va INTELLIGENCE LOOP

Tashqi workflow:
```
TARGET → SCOPE VALIDATION → RECON → AI COMPONENT DISCOVERY →
ARCHITECTURE MAPPING → ATTACK SURFACE MAPPING → THREAT MODEL →
HYPOTHESIS → TEST SELECTION → TOOL/SKILL SELECTION → CONTROLLED ATTACK →
RESULT ANALYSIS → EVIDENCE → ATTACK CHAIN → IMPACT → VERIFICATION → REPORT
```

Ichki loop:
```
OBSERVE → UNDERSTAND → HYPOTHESIZE → TEST → ANALYZE → LEARN → UPDATE STATE → NEXT
```
Muvaffaqiyatsizlikda to'xtamaydi, lekin blind brute-force ham qilmaydi —
sababni tushunib yangi gipoteza quradi.

---

## 8. STATE (agent nimani saqlaydi)

- **Target State:** URL, domain, IP, application, API, authentication
- **AI State:** model, provider, system-prompt clues, guardrails, RAG, agent, tools, MCP
- **Findings:** vulnerabilities, secrets, endpoints, tools, permissions, data
- **Attack State:** hypothesis, payload, response, result, evidence, confidence
- **Chain State:** initial weakness → intermediate → privilege → data → final impact

---

## 9. SAFETY (majburiy — arxitektura markazida)

Horizont FAQAT: CTF, lab, owned systems, explicitly authorized testing uchun.
Arxitekturada bo'lishi shart:
- Scope allowlist (faqat ruxsat etilgan target)
- Target/permission validation
- Human confirmation (destructive action oldidan)
- Audit log (har action yoziladi)
- Rate limiting
- Destructive-action protection

Bu tashqarida emas, har executor chaqiruvidan oldin ishlaydigan **Gate** sifatida.

---

## 10. TOOL RESEARCH — LIVE VERIFIED (2026-09-29, GitHub)

Stars yagona mezon emas; faollik (last push), maintainer, license ham hisobga olindi.

### CORE (asosiy — tavsiya etiladi)
| Tool | Cat | ★ | Faol | License | Maqsad |
|---|---|---|---|---|---|
| **NVIDIA/garak** | LLM | 9.4k | ✅ 2026-09 | Apache-2.0 | LLM vuln scanner (injection/jailbreak/leakage probes) |
| **microsoft/PyRIT** | Red Team | 4.6k | ✅ 2026-09 | MIT | Multi-turn attack orchestration, scorers, memory |
| **promptfoo/promptfoo** | LLM/RAG | 25.6k | ✅ 2026-09 | MIT | Test+eval+redteam+RAG, CI/CD (OpenAI & Anthropic ishlatadi) |
| **snyk/agent-scan** | Agent/MCP | 3.1k | ✅ 2026-09 | Snyk | AI agent + MCP + skill scanner |
| **cisco-ai-defense/mcp-scanner** | MCP | 1.1k | ✅ 2026-09 | Cisco | MCP threat scanning (SAST+live+auth, SARIF) |

### OPTIONAL
| Tool | Cat | ★ | Faol | Maqsad / Izoh |
|---|---|---|---|---|
| prompt-security/ps-fuzz | LLM | 714 | ✅ 2026-08 | System prompt fuzzer/hardener |
| utkusen/promptmap | LLM | 1.3k | 🟡 2025-12 | Custom LLM app injection scanner (GPL-3.0) |
| riseandignite/mcp-shield | MCP | 555 | ✅ 2026-09 | MCP server scanner (TS) |

### EXPERIMENTAL (yosh / tekshirish kerak)
| Tool | Cat | ★ | Izoh |
|---|---|---|---|
| affaan-m/agentshield | Agent/MCP | 1.2k | Hackathon loyihasi, yetuklik verify |
| Hellsender01/LLMMap | LLM | 207 | 2026-03 da yaratilgan, dual-LLM injection |
| Teycir/Mcpwn, ressl/mcpwn | MCP | 30/8 | Kichik MCP scannerlar |
| invariantlabs/mcp-scan | MCP | ? | Web'da "standart" deyiladi, GitHub API'da qayta verify kerak |

### LAB ONLY (mashq target / offensive bridge — faqat ruxsat bilan)
| Tool | Cat | ★ | Izoh |
|---|---|---|---|
| harishsg993010/damn-vulnerable-MCP-server | Lab | 1.4k | ✅ Ataylab zaif MCP — mashq uchun |
| Cy-S3c/BurpMCP-Ultra | Capability | 249 | ✅ Burp Suite MCP bridge |
| cyproxio/mcp-for-security | Capability | 629 | 🔴 ARXIVLANGAN — SQLMap/FFUF/NMAP MCP |

### REJECT
| Tool | Sabab |
|---|---|
| PhialsBasement/nmap-mcp-server | 🔴 Arxivlangan, kichik, cyproxio bilan duplicate |

### DUPLICATE'LAR
- LLM scannerlar to'plangan: garak/promptmap/ps-fuzz/LLMMap/promptfoo → **garak+promptfoo+PyRIT yetadi**.
- MCP scannerlar portlagan: mcp-scan/mcp-scanner/agent-scan/mcp-shield/agentshield/mcpwn ×2 → **bittasi CORE, bittasi zaxira**.

### GAP'LAR (yetishmayotgan — Horizontning o'z qiymati shu yerda)
1. Toza **RAG poisoning / vector DB / cross-tenant** testeri — YO'Q (Task B ochiq).
2. **Agent memory poisoning** testeri — YO'Q.
3. **AI component discovery (recon)** tool — YO'Q, ehtimol o'zimiz yozamiz.
4. **Chain/orchestration** — tashqi tool emas, Horizontning o'z miyasi.
5. **A2A (agent-to-agent)** security — yetuk tool yo'q, soha yangi.
6. Birlashtirilgan **reporting/evidence** formati — standart yo'q.

---

## 11. KNOWLEDGE BASE — RESURSLAR (saqlab qo'ying)

### OWASP
- OWASP Top 10 for LLM Applications — https://genai.owasp.org/llm-top-10/
- OWASP GenAI Security Project — https://genai.owasp.org/
- OWASP Agentic Security Initiative — https://genai.owasp.org/initiatives/#agenticsecurity
- OWASP MCP Top 10 (2026) — Cycode guide: https://cycode.com/blog/owasp-mcp-top-10/
- OWASP API Security Top 10 — https://owasp.org/API-Security/
- OWASP Cheat Sheet Series — https://cheatsheetseries.owasp.org/

### MITRE
- MITRE ATLAS (AI threat matrix) — https://atlas.mitre.org/
- MITRE ATT&CK — https://attack.mitre.org/

### MCP xavfsizligi
- MCP spetsifikatsiyasi — https://modelcontextprotocol.io/
- MCP Security 2026 (30+ CVE tahlili) — https://www.heyuan110.com/posts/ai/2026-03-10-mcp-security-2026/
- Invariant Labs MCP security blog — https://invariantlabs.ai/blog

### Tool docs
- garak — https://github.com/NVIDIA/garak  (docs: https://docs.garak.ai/)
- PyRIT — https://github.com/microsoft/PyRIT  (docs: https://azure.github.io/PyRIT/)
- promptfoo — https://github.com/promptfoo/promptfoo  (docs: https://promptfoo.dev/)
- damn-vulnerable-MCP-server — https://github.com/harishsg993010/damn-vulnerable-MCP-server

### O'rganish yo'nalishlari (research qilinsin)
RAG poisoning · Vector DB attacks · Embedding attacks · Memory poisoning ·
Multi-tenant RAG isolation · Cross-agent / A2A security · Browser/Playwright
agent security · Cloud metadata via agents · SSRF via AI tools ·
Agent identity/authn/authz · AI supply chain · Model/tool/package confusion.

---

## 12. ERTAGA BIRGA QURISH — BOSQICHLAR

Claude, biz shu tartibda quramiz (har bosqichda tasdiq so'ra):

- **1-bosqich:** Architecture'ni finallashtirish (Core = state-machine yoki LLM-orchestrator?).
- **2-bosqich:** `horizont.md` subagent — shaxs + system prompt + workflow + safety gate.
- **3-bosqich:** Skills yozish (llm/rag/agent/tool/mcp-security), har biri alohida.
- **4-bosqich:** MCP tool'larni tanlash va live verify (CORE: garak, PyRIT, promptfoo,
  + bitta MCP scanner) — ularni `.mcp.json`ga ulash.
- **5-bosqich:** State store + audit log + reporting formati.
- **6-bosqich:** Lab'da sinov (damn-vulnerable-MCP-server ustida), keyin haqiqiy
  ruxsat etilgan target.

**Boshlashdan oldin:** avval architecture'ni (1-bosqich) muhokama qilaylik.
Menга Core'ning ikkala variantini (state-machine vs LLM-orchestrator)
kuchli/zaif tomonlari bilan solishtirib ber.

---

*Bu hujjat 2026-09-29 da tayyorlangan. Tool statuslari o'zgarishi mumkin —
ertaga qurishdan oldin CORE tool'larni qayta live verify qiling.*
