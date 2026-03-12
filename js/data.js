// ==========================================
// data.js — All static data for Noah's Ark OS website
// ==========================================

const TILES = [
  { id:"T000", name:"TEV_EVALUATOR",   desc:"Kernel boot & tile health scan. First tile to execute — validates the entire registry before any scene can run.", tev:"1.0", status:"ok" },
  { id:"T100", name:"INIT",            desc:"Library imports & global pricing constants. Establishes the cost model for all downstream token accounting.", tev:"2.5", status:"ok" },
  { id:"T102", name:"QUOTA_SHIELD",    desc:"Catches 429 rate-limit errors. 65s cooldown with retry logic. Keeps scenes alive during API pressure.", tev:"2.0", status:"ok" },
  { id:"T103", name:"IDENTITY_VAULT",  desc:"Pulls character dossier + mood + briefing. Formats full persona string with hard scene-role constraint injection.", tev:"5.4", status:"evolving" },
  { id:"T104", name:"CONTEXT_SLIDER",  desc:"Pinned (2) + sliding (8) hybrid context window. Objective reminder anchored. Prevents context poisoning across 20+ turns.", tev:"3.5", status:"ok" },
  { id:"T105", name:"MAYA_META_OBSERVER", desc:"Maya watches every scene. Dialogue entropy scan, dossier updates, maya_kb.json writer. close_scene() reflection on archive.", tev:"5.2", status:"evolving" },
  { id:"T106", name:"CHARACTER_BRAIN", desc:"Final prompt assembly. [Thought]/[Urge]/[Speech] structured output. BL-Q02 self-reference constraint. BL-E10 phantom character guard.", tev:"5.5", status:"evolving" },
  { id:"T107", name:"STATE_ENGINE",    desc:"JSON CRUD, history persistence, scene reset. Manages noah_souls.json and global_history. reset_scene() + corrupt history filter.", tev:"4.5", status:"ok" },
  { id:"T108", name:"TOKEN_SENTINEL",  desc:"USD calculation & token ledger logging. int(x or 0) None-guard prevents TypeError on missing usage metadata.", tev:"3.0", status:"ok" },
  { id:"T109", name:"LOG_ARCHIVER",    desc:"Timestamped scene archive .txt files. Appends Maya's closing reflection as final entry before file close.", tev:"5.1", status:"ok" },
  { id:"T110", name:"ORACLE",          desc:"RAG-lite world intelligence from state + ledger. Answers creator questions about scenes, costs, and character history.", tev:"5.0", status:"evolving" },
  { id:"T111", name:"UI_SOVEREIGN",    desc:"Tabbed UI: Soul Forge + Cockpit + Console. Three-state mode toggle (Dialog/Story/Debug). Per-character briefing fields.", tev:"5.10", status:"evolving" },
  { id:"T112", name:"UI_ORACLE_TAB",   desc:"Renders Oracle queries and responses. Textarea console with contained scroll.", tev:"2.5", status:"ok" },
  { id:"T113", name:"UI_METRICS",      desc:"Live cost, tokens, character distribution. Real-time ledger view during scene runs.", tev:"4.0", status:"ok" },
  { id:"T114", name:"SIM_CONDUCTOR",   desc:"Urge-based competitive turn selection. Three-layer event classifier. Expression threshold separates internal pressure from willingness to speak.", tev:"5.5", status:"critical" },
  { id:"T115", name:"GEMINI_PROV",     desc:"google-genai Client wrapper. Safe text extraction. Provider-agnostic interface — remappable to any LLM backend.", tev:"3.0", status:"ok" },
  { id:"T116", name:"SMOKE_TESTER",    desc:"End-to-end BFT: registry, state, live API call. Single-button scene health validation before any production run.", tev:"2.0", status:"ok" },
  { id:"T117", name:"UI_CHASSIS",      desc:"Assembles master Tab widget from all UI tiles. The frame that holds Soul Forge, Cockpit, Console, Oracle, and Metrics together.", tev:"3.0", status:"ok" },
  { id:"T118", name:"ENV_LOADER",      desc:"Loads .env API keys. Replaces Colab userdata. Secure key injection at notebook boot.", tev:"1.5", status:"ok" },
];

const CHAPTERS = [
  {
    num: "Chapter 1",
    status: "complete",
    title: "Conceptualisation & Proof of Concept",
    desc: "The first spark. A hardcoded world: a solar storm strikes the lunar habitat and one crew member must remain outside. Characters were fixed Gemini instances inhabiting a single, scripted scene. The question was simple: can AI agents <em>live</em> in a world? The answer was yes.",
    tags: [
      { label:"Hardcoded World", style:"teal" },
      { label:"Fixed Characters", style:"teal" },
      { label:"Single Scene", style:"teal" },
      { label:"Agentic AI Concept", style:"" },
      { label:"Proof of Life ✓", style:"" },
    ],
    sprints: [],
    date: "Dec 2025"
  },
  {
    num: "Chapter 2",
    status: "complete",
    title: "Dynamic Scene Ingestion",
    desc: "The world opened up. UI-based scene ingestion replaced hardcoded environments. Peripheral characters began spawning dynamically from scene definitions. Success — but a snowball effect on token consumption revealed the next frontier: context management.",
    tags: [
      { label:"Dynamic Scene Input", style:"teal" },
      { label:"Peripheral Characters", style:"teal" },
      { label:"UI Controls", style:"" },
      { label:"Context Snowball Identified", style:"" },
    ],
    sprints: [],
    date: "Jan 2026"
  },
  {
    num: "Chapter 2.1",
    status: "complete",
    title: "Tile Architecture & Modular Engine",
    desc: "The great restructuring. A monolith became a living architecture of 20+ tiles — each with defined Input, Process, and Output contracts. Tile Master tracks evolution. When a tile grows too complex it divides. When its purpose is void it deprecates. First real multi-turn scene produced with full Oracle, Metrics, and persistence.",
    tags: [
      { label:"20+ Tiles", style:"gold" },
      { label:"Oracle", style:"gold" },
      { label:"Persistence Layer", style:"gold" },
      { label:"Token Ledger", style:"gold" },
      { label:"Maya Observer", style:"gold" },
      { label:"First Full Scene Run ✓", style:"" },
    ],
    sprints: [
      { id:"Sprint 1 (2.1)", items:["google-genai SDK migration", "T115 GEMINI_PROV rewrite", "Textarea console", "T107 reset_scene()", "Error routing to console"] }
    ],
    date: "Feb–Mar 2026"
  },
  {
    num: "Chapter 2.2",
    status: "complete",
    title: "Scene Intelligence & Creator Experience",
    desc: "The engine learns to close. Organic scene endings via character cognition. Pace control for the creator. Context poisoning prevention. Character identity stability. The simulation becomes something worth watching at human speed.",
    tags: [
      { label:"Organic Scene End", style:"gold" },
      { label:"Pace Control", style:"gold" },
      { label:"Identity Stability", style:"gold" },
      { label:"Context Architecture", style:"" },
      { label:"Creator UX Revamp", style:"" },
    ],
    sprints: [
      { id:"Sprint 1 (2.2)", items:["[[SCENE_END]] signal + T114 detection", "Digital/Human/Cinematic pace control", "Cockpit semantic rework (New Scene / Start / Pause-Resume / Reset)", "Oracle scroll containment", "Token sentinel None-guard", "Anti-repetition last_utterances block", "Pinned+sliding context hybrid"] }
    ],
    date: "08 Mar 2026"
  },
  {
    num: "Chapter 2.3",
    status: "complete",
    title: "Multi-Character Scene Reliability",
    desc: "The engine proves it can manage five characters simultaneously for 20+ turns — each in their correct role, without context loss, repetition, or identity confusion. Urge-based competitive turn selection replaces round-robin. Maya's voice sharpens with a closing reflection on every archived scene.",
    tags: [
      { label:"5-Character Scenes", style:"gold" },
      { label:"Urge-Based Turn Selection", style:"gold" },
      { label:"Event Classifier", style:"gold" },
      { label:"Maya Closing Reflection", style:"gold" },
      { label:"Story/Debug Toggle", style:"teal" },
      { label:"Sprint 2 Complete ✓", style:"" },
    ],
    sprints: [
      {
        id:"Sprint 2 (2.3)", items:[
          "BL-E05: Scene role boundary — per-character hard constraint injection",
          "BL-M01: Maya close_scene() reflection appended to every archive",
          "BL-E09: Urge-based competitive speaker selection (margin = Urge − Threshold)",
          "Three-layer event classifier: name → pronoun → domain keyword",
          "Expression threshold — separates internal urge from willingness to speak",
          "Tiebreak randomisation — fixed silent Valentina across 34 turns",
          "Story/Debug console toggle — live during scene",
        ]
      }
    ],
    date: "09–11 Mar 2026"
  },
  {
    num: "Chapter 2.4",
    status: "complete",
    title: "Scene Quality & Character Integrity",
    desc: "Characters stop referring to themselves in the third person. Phantom characters stop speaking before they're called. Private briefings give each character secret knowledge no one else can see. Maya starts writing to a persistent knowledge base across scenes.",
    tags: [
      { label:"BL-Q02 Self-Reference Fix", style:"gold" },
      { label:"BL-E10 Phantom Character Fix", style:"gold" },
      { label:"Private Briefings", style:"gold" },
      { label:"Maya Knowledge Base", style:"teal" },
      { label:"HTML Card Console", style:"teal" },
      { label:"Sprint 3 Complete ✓", style:"" },
    ],
    sprints: [
      {
        id:"Sprint 3 (2.4)", items:[
          "BL-Q02: Third-person self-reference constraint injected in T106",
          "BL-E10: Phantom character constraint — characters cannot narrate absent characters speaking",
          "BL-E08: Private briefing field per character — secret knowledge block in T103",
          "T105: maya_kb.json writer in close_scene()",
          "T111: Three-state console mode toggle (Dialog / Story / Debug)",
          "HTML card console replacing plain Textarea",
        ]
      }
    ],
    date: "12 Mar 2026"
  },
  {
    num: "Chapter 2.5",
    status: "active",
    title: "Token Intelligence & Scene Control",
    desc: "Sprint 4 in progress. The engine gains awareness of its own cost trajectory mid-scene. Soft token budgets, mid-scene summarisation, and smarter context compression. The goal: longer, richer scenes without runaway cost.",
    tags: [
      { label:"Token Budget Control", style:"gold" },
      { label:"Mid-Scene Summarisation", style:"gold" },
      { label:"Context Compression", style:"" },
      { label:"Sprint 4 Active ⚡", style:"" },
    ],
    sprints: [],
    date: "Active"
  },
  {
    num: "Chapter 3+",
    status: "planned",
    title: "Maya Model & Multi-World Curriculum",
    desc: "Maya graduates from observer to student. Structured training data — tagged with ethical dilemmas, emotion spectra, and conflict arcs — feeds the Maya Model. Multiple creator worlds run in parallel. The synthetic data engine reaches its true purpose.",
    tags: [
      { label:"Maya Model Training", style:"" },
      { label:"Ethical Curriculum", style:"" },
      { label:"Emotion Tagging", style:"" },
      { label:"Multi-World Simulation", style:"" },
      { label:"Creator Platform", style:"" },
      { label:"100+ Characters", style:"" },
    ],
    sprints: [],
    date: "Planned"
  },
];

const VERSIONS = [
  { v:"v2.0.0",     date:"12 Mar 2026", ch:"2.4", title:"Scene Quality & Character Integrity",         sub:"BL-Q02 self-reference fix, BL-E10 phantom character fix, BL-E08 private briefings per character, Maya Knowledge Base, HTML card console. T103 v5.4, T106 v5.5, T111 v5.10.1." },
  { v:"v1.9.4",     date:"11 Mar 2026", ch:"2.3", title:"Sprint 2 Final — Tiebreak & Threshold",       sub:"Tiebreak randomisation window. Contradiction keyword tightening. Threshold floor fix. Story/Debug toggle. T114 v5.5.1, T111 v5.9.2." },
  { v:"v1.9.3",     date:"10 Mar 2026", ch:"2.3", title:"Expression Threshold + Event Classifier",     sub:"Three-layer event classifier (name → pronoun → domain). Expression threshold separates internal urge from willingness to speak. 7 event types with targeted deltas. T114 v5.5, T111 v5.9.1." },
  { v:"v1.9.2",     date:"10 Mar 2026", ch:"2.3", title:"Cockpit Layout Redesign",                     sub:"Vertical stack layout, full-width sections, 3-line scrollable textboxes, flex role field. T111 v5.9." },
  { v:"v1.9.1",     date:"10 Mar 2026", ch:"2.3", title:"Urge-Based Competitive Speaker Selection",    sub:"Round-robin replaced with margin-based selection (Urge − Threshold). Tone-derived initial thresholds. Anxious characters build pressure faster. T114 v5.4." },
  { v:"v1.9.0",     date:"09 Mar 2026", ch:"2.3", title:"Sprint 2 Base — Role Boundary + Maya Reflection", sub:"BL-E05 per-scene role as hard constraint injected into T103 persona. BL-M01 Maya close_scene() method + archive reflection. T103 v5.3, T105 v5.1, T109 v5.1, T111 v5.8." },
  { v:"v1.8.0",     date:"08 Mar 2026", ch:"2.2", title:"Sprint 1 Complete",                           sub:"Scene end detection, pace control, cockpit semantic rework, oracle scroll, token sentinel None-guard, anti-repetition block, context poisoning prevention. 8 DoD items passed." },
  { v:"v1.7.1",     date:"05 Mar 2026", ch:"2.1", title:"Errors Visible Edition",                      sub:"T102/T115 errors routed to Textarea console. T107 reset_scene() + corrupt history filter. New Scene + Test API buttons in Cockpit." },
  { v:"v1.7.0",     date:"05 Mar 2026", ch:"2.1", title:"Structured Output Edition",                   sub:"T115 safe text extraction (_safe_extract_text). T106 [Thought]/[Urge]/[Speech] structured prompt + urge regex. T111 Textarea console with scroll." },
  { v:"v1.6.1",     date:"05 Mar 2026", ch:"2.1", title:"Persistent World Edition",                    sub:"global_history.json persistence. T102 rate-limit sleep+retry. T108 zero-token filter. T111 thread-safe output. Hard Kill archives scene." },
  { v:"v1.5.0",     date:"04 Mar 2026", ch:"2.1", title:"google-genai SDK Migration",                  sub:"Full migration from deprecated google.generativeai to google-genai. T115 GEMINI_PROV rewritten. T000 BIOS updated. Client object injected from boot." },
  { v:"v1.0–v1.4",  date:"Feb–Mar 2026",ch:"2.1", title:"Tile Architecture Foundation",               sub:"20+ tile modular restructure. T000 BIOS, T111 Command Center, T110 Oracle, T113 Metrics, T114 SIM_CONDUCTOR established. Colab → VSCode migration." },
  { v:"Chapter 2.0",date:"Jan 2026",    ch:"2.0", title:"Dynamic Scene Ingestion",                     sub:"UI-based scene config. Dynamic peripheral character spawning. Token snowball effect identified as next constraint." },
  { v:"Chapter 1.0",date:"Dec 2025",    ch:"1.0", title:"Proof of Concept — The First World",          sub:"Hardcoded lunar habitat. Solar storm scenario. Fixed Gemini character instances. Agentic AI living in a scene — first proof of life." },
];
