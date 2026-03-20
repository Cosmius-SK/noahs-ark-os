"""
Noah's Ark OS — Sprint 7 Patch Script
Chapter 2.8 — Scene Intelligence
Run: python3 patch_sprint7.py

What this does:
  1. Loads Noahs_Ark_v2_3_0_*_sprint6.ipynb (auto-detects)
  2. Patches T103 v5.4.2  — BL-Q05 thought variation
  3. Patches T106 v5.5.2  — extract + pass thought to T107
  4. Patches T107 v5.7.1  — update_last_utterances accepts thought_text
  5. Patches T114 v5.5.5  — scene_type modifiers from T120
  6. Patches T111 v5.12.0 — Wizard button + Scene Type + Injection field
  7. Inserts  T119         — SCENE_WIZARD (new cell after T118)
  8. Inserts  T120         — ORCHESTRATOR (new cell after T119)
  9. Updates  Assembly     — wires T119 + T120 into registry
  10. Saves   Noahs_Ark_v2_4_0_DDMMYYYY_sprint7.ipynb
"""

import json, glob, re, sys
from datetime import datetime

# ── Find source notebook ──────────────────────────────────────────────────────
candidates = glob.glob('Noahs_Ark_v2_3_0_*sprint6*.ipynb')
if not candidates:
    sys.exit('ERROR: No sprint6 notebook found in current directory.')
src_path = sorted(candidates)[-1]
print(f'Source: {src_path}')

nb = json.load(open(src_path, encoding='utf-8'))

def cell_src(nb, idx):
    return ''.join(nb['cells'][idx]['source'])

def set_cell(nb, idx, code):
    nb['cells'][idx]['source'] = [code]
    nb['cells'][idx]['outputs'] = []

def find_cell(nb, marker):
    """Return index of cell containing marker string."""
    for i, cell in enumerate(nb['cells']):
        if marker in ''.join(cell['source']):
            return i
    return None

def insert_cell_after(nb, idx, code):
    """Insert a new code cell after idx."""
    new_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [code]
    }
    nb['cells'].insert(idx + 1, new_cell)

# ── Locate cells ──────────────────────────────────────────────────────────────
IDX_T103 = find_cell(nb, '# T103 : IDENTITY_VAULT')
IDX_T106 = find_cell(nb, '# T106 : CHARACTER_BRAIN')
IDX_T107 = find_cell(nb, '# T107 : STATE_ENGINE')
IDX_T111 = find_cell(nb, '# T111 : COMMAND_CENTER')
IDX_T114 = find_cell(nb, '# T114 : SIM_CONDUCTOR')
IDX_T118 = find_cell(nb, '# T118 : ENV_LOADER')

print(f'T103={IDX_T103} T106={IDX_T106} T107={IDX_T107} '
      f'T111={IDX_T111} T114={IDX_T114} T118={IDX_T118}')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 1 — T103 v5.4.2  (BL-Q05: thought variation)
# Add last_thoughts to anti-rep block
# ════════════════════════════════════════════════════════════════════════════════
OLD_T103_HEADER = '# VERSION: 5.4.1 | STATUS: Evolved'
NEW_T103_HEADER = '''# VERSION: 5.4.2 | STATUS: Evolved
# Version Remarks: v5.4.2 — BL-Q05 Sprint 7.
#   Anti-repetition block now covers [Thought] as well as [Speech].
#   last_thoughts list added alongside last_utterances.
#   Prevents verbatim thought repetition on consecutive unselected turns.
#
#   v5.4.1 — BL-T03 Sprint 5. Name injection.'''

OLD_T103_ANTIREP = '''        # ------------------------------------------
        # SECTION 4: ANTI-REPETITION BLOCK (BL-E02)
        # ------------------------------------------
        last_utterances = data.get('last_utterances', [])
        if last_utterances:
            repeat_block = "\\n        DO NOT REPEAT OR CLOSELY ECHO any of these recent utterances:\\n"
            for i, utt in enumerate(last_utterances, 1):
                short = utt[:120] + "..." if len(utt) > 120 else utt
                repeat_block += f"        {i}. {short}\\n"
        else:
            repeat_block = ""'''

NEW_T103_ANTIREP = '''        # ------------------------------------------
        # SECTION 4: ANTI-REPETITION BLOCK (BL-E02 + BL-Q05)
        # ------------------------------------------
        last_utterances = data.get('last_utterances', [])
        last_thoughts   = data.get('last_thoughts', [])
        repeat_block = ""
        if last_utterances:
            repeat_block += "\\n        DO NOT REPEAT OR CLOSELY ECHO any of these recent [Speech] utterances:\\n"
            for i, utt in enumerate(last_utterances, 1):
                short = utt[:120] + "..." if len(utt) > 120 else utt
                repeat_block += f"        {i}. {short}\\n"
        if last_thoughts:
            repeat_block += "\\n        DO NOT REPEAT OR CLOSELY ECHO any of these recent [Thought] blocks:\\n"
            for i, th in enumerate(last_thoughts, 1):
                short = th[:120] + "..." if len(th) > 120 else th
                repeat_block += f"        {i}. {short}\\n"'''

src = cell_src(nb, IDX_T103)
src = src.replace(OLD_T103_HEADER, NEW_T103_HEADER)
src = src.replace(OLD_T103_ANTIREP, NEW_T103_ANTIREP)
set_cell(nb, IDX_T103, src)
print('✅ T103 patched')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 2 — T106 v5.5.2  (BL-Q05: extract thought + pass to T107)
# ════════════════════════════════════════════════════════════════════════════════
OLD_T106_HEADER = '# VERSION: 5.5.1 | STATUS: Evolved'
NEW_T106_HEADER = '''# VERSION: 5.5.2 | STATUS: Evolved
# Version Remarks: v5.5.2 — BL-Q05 Sprint 7.
#   _extract_thought() added. Thought text extracted after each turn
#   and passed to T107.update_last_utterances() so T103 anti-rep
#   block can suppress verbatim thought repetition.
#
#   v5.5.1 — Sprint 6. BL-E07 passive_mode + ROOM PRESENCE RULE.'''

OLD_T106_EXTRACT = '''    def _extract_speech(self, text: str) -> str:'''

NEW_T106_EXTRACT = '''    def _extract_thought(self, text: str) -> str:
        if not text:
            return ""
        match = re.search(r'\\[Thought\\]:\\s*(.+?)(?=\\n\\[|$)', text, re.DOTALL)
        return match.group(1).strip()[:200] if match else ""

    def _extract_speech(self, text: str) -> str:'''

OLD_T106_PERSIST = '''        speech_text = self._extract_speech(txt)
        if speech_text and speech_text != "--" and 'state' in self.r:
            self.r['state'].update_last_utterances(actor_name, speech_text)

        return txt, urge_value, token_map, scene_end'''

NEW_T106_PERSIST = '''        speech_text = self._extract_speech(txt)
        thought_text = self._extract_thought(txt)
        if 'state' in self.r:
            if speech_text and speech_text != "--":
                self.r['state'].update_last_utterances(actor_name, speech_text)
            if thought_text:
                self.r['state'].update_last_thoughts(actor_name, thought_text)

        return txt, urge_value, token_map, scene_end'''

src = cell_src(nb, IDX_T106)
src = src.replace(OLD_T106_HEADER, NEW_T106_HEADER)
src = src.replace(OLD_T106_EXTRACT, NEW_T106_EXTRACT)
src = src.replace(OLD_T106_PERSIST, NEW_T106_PERSIST)
set_cell(nb, IDX_T106, src)
print('✅ T106 patched')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 3 — T107 v5.7.1  (BL-Q05: add update_last_thoughts + clear)
# ════════════════════════════════════════════════════════════════════════════════
OLD_T107_HEADER = '# VERSION: 5.7.0 | STATUS: Evolved'
NEW_T107_HEADER = '''# VERSION: 5.7.1 | STATUS: Evolved
# Version Remarks: v5.7.1 — BL-Q05 Sprint 7.
#   update_last_thoughts() mirrors update_last_utterances() for [Thought].
#   last_thoughts list capped at MAX_UTTERANCES (3) per character.
#   reset_scene() clears last_thoughts alongside last_utterances.
#
#   v5.7.0 — BL-I07 Sprint 4. reload_history() + SCENE_BOUNDARY.'''

OLD_T107_CLEAR = '''    def clear_last_utterances(self):'''

NEW_T107_CLEAR = '''    def update_last_thoughts(self, actor_name: str, thought_text: str):
        """BL-Q05: Track recent Thought blocks for anti-repetition."""
        if actor_name not in self.state['participants']:
            return
        soul = self.state['participants'][actor_name]
        thoughts = soul.get('last_thoughts', [])
        thoughts.append(thought_text)
        if len(thoughts) > self.MAX_UTTERANCES:
            thoughts = thoughts[-self.MAX_UTTERANCES:]
        soul['last_thoughts'] = thoughts
        self.state['participants'][actor_name] = soul

    def clear_last_utterances(self):'''

OLD_T107_RESET = '''    def reset_scene(self):'''
# Find the reset_scene body to also clear last_thoughts
src = cell_src(nb, IDX_T107)
# Insert update_last_thoughts method
src = src.replace(OLD_T107_HEADER, NEW_T107_HEADER)
src = src.replace(OLD_T107_CLEAR, NEW_T107_CLEAR)
# Also patch reset_scene to clear last_thoughts
src = src.replace(
    "soul['last_utterances'] = []",
    "soul['last_utterances'] = []\n                soul['last_thoughts'] = []"
)
set_cell(nb, IDX_T107, src)
print('✅ T107 patched')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 4 — T114 v5.5.5  (T120 scene type modifier hook)
# ════════════════════════════════════════════════════════════════════════════════
OLD_T114_HEADER = '# VERSION: 5.5.4 | STATUS: Evolved'
NEW_T114_HEADER = '''# VERSION: 5.5.5 | STATUS: Evolved
# Version Remarks: v5.5.5 — BL-N02 Sprint 7.
#   reset_urge_state() reads scene_type from T111 and applies T120
#   ORCHESTRATOR modifiers at scene start.
#   Interview: interviewer margin=0 (holds back), candidate margin=+2.0.
#   Debate: standard margins, CONTRADICTION sensitivity x2.
#   Social: standard BL-C02 margins (unchanged).
#
#   v5.5.4 — Sprint 6. BL-E07 passive_mode + pre-entry fix.'''

OLD_T114_RESET = '''    def reset_urge_state(self, active_souls):
        """BL-C02: Initialise urge = threshold + 1.5 per character.
        Equal starting margin of 1.5 for all tones. Called on Start."""
        self.threshold_state = {}
        for soul in active_souls:
            try:
                data = self.r['state'].get_actor_data(soul)
                tone = data.get('tone', 'Neutral')
                self.threshold_state[soul] = self.TONE_THRESHOLD.get(
                    tone, self.DEFAULT_THRESHOLD)
            except Exception:
                self.threshold_state[soul] = self.DEFAULT_THRESHOLD
        self.urge_state = {
            s: self.threshold_state.get(s, self.DEFAULT_THRESHOLD) + 1.5
            for s in active_souls
        }'''

NEW_T114_RESET = '''    def reset_urge_state(self, active_souls):
        """BL-C02 + BL-N02: Initialise urge with scene type modifiers from T120."""
        self.threshold_state = {}
        for soul in active_souls:
            try:
                data = self.r['state'].get_actor_data(soul)
                tone = data.get('tone', 'Neutral')
                self.threshold_state[soul] = self.TONE_THRESHOLD.get(
                    tone, self.DEFAULT_THRESHOLD)
            except Exception:
                self.threshold_state[soul] = self.DEFAULT_THRESHOLD

        # BL-N02: apply T120 scene type modifiers if available ---------------
        scene_type = 'Social'
        role_map   = {}
        if 'ui_cmd' in self.r:
            ui = self.r['ui_cmd']
            scene_type = getattr(ui, 'scene_type_value', 'Social')
            role_map   = {
                name: cfg['role'].value.lower()
                for name, cfg in ui.active_config.items()
                if cfg.get('role')
            }

        orchestrator = self.r.get('orchestrator')
        if orchestrator:
            self.urge_state = orchestrator.apply_scene_type(
                active_souls, self.threshold_state, scene_type, role_map)
        else:
            # Fallback: standard BL-C02 equal margins
            self.urge_state = {
                s: self.threshold_state.get(s, self.DEFAULT_THRESHOLD) + 1.5
                for s in active_souls
            }'''

src = cell_src(nb, IDX_T114)
src = src.replace(OLD_T114_HEADER, NEW_T114_HEADER)
src = src.replace(OLD_T114_RESET,  NEW_T114_RESET)
set_cell(nb, IDX_T114, src)
print('✅ T114 patched')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 5 — T111 v5.12.0  (Wizard + Scene Type + Injection)
# Three targeted additions to existing T111
# ════════════════════════════════════════════════════════════════════════════════
OLD_T111_HEADER = '# VERSION: 5.11.0 | STATUS: Evolved'
NEW_T111_HEADER = '''# VERSION: 5.12.0 | STATUS: Evolved
# Version Remarks: v5.12.0 — BL-N01 + BL-N02 Sprint 7.
#   BL-N01: 🧙 Scene Wizard button + input panel. Calls T119.draft_scene(),
#     pre-fills env, scene context, and role fields. Fields remain editable.
#   BL-N02: Scene Type dropdown (Interview/Debate/Social/Custom).
#     Live Injection field + 💉 Inject button — writes [SCENE_EVENT] to
#     history during running scene. Picked up by characters next turn.
#
#   v5.11.0 — Sprint 6. BL-U09 + BL-U10 UI elevation.'''

# Add scene_type_value attr and new widgets after kill_btn definition
OLD_T111_KILLBTN = '''        self.bft_btn       = widgets.Button(description="🧪 BFT",       button_style='info',
                                           tooltip="Run Smoke Tester — BFT integrity check")  # BL-I05'''

NEW_T111_KILLBTN = '''        self.bft_btn       = widgets.Button(description="🧪 BFT",       button_style='info',
                                           tooltip="Run Smoke Tester — BFT integrity check")  # BL-I05

        # ── Scene Type + Wizard + Injection (BL-N01, BL-N02) ─────────────────
        self.scene_type_value = 'Social'   # read by T114 reset_urge_state
        self.scene_type_dd = widgets.Dropdown(
            options=['Social', 'Interview', 'Debate', 'Custom'],
            value='Social', description='Scene Type:',
            layout={'width': '200px'}, style={'description_width': '90px'})
        self.scene_type_dd.observe(self._on_scene_type_change, names='value')

        self.wizard_input = widgets.Textarea(
            placeholder="Describe your scene in plain language...",
            layout={'width': '99%', 'min_height': '60px', 'max_height': '100px',
                    'overflow_y': 'auto', 'display': 'none'})
        self.wizard_btn   = widgets.Button(description="🧙 Scene Wizard",
                                           button_style='info', layout={'width': '140px'})
        self.wizard_gen   = widgets.Button(description="✨ Generate",
                                           button_style='success', layout={'width': '100px',
                                           'display': 'none'})
        self.wizard_status = widgets.Label(value='')

        self.injection_box = widgets.Text(
            placeholder="Type a scene event to inject mid-scene...",
            layout={'flex': '1 1 auto', 'min_width': '0'})
        self.inject_btn = widgets.Button(description="💉 Inject",
                                         button_style='warning', layout={'width': '80px'})'''

# Add scene type change handler and wizard/inject methods before get_render_box
OLD_T111_RENDERBOX = '''    def get_render_box(self):
        return self.sub_tabs'''

NEW_T111_RENDERBOX = '''    def _on_scene_type_change(self, change):
        self.scene_type_value = change['new']

    def _toggle_wizard(self, _):
        visible = self.wizard_input.layout.display == 'none'
        self.wizard_input.layout.display = '' if visible else 'none'
        self.wizard_gen.layout.display   = '' if visible else 'none'

    def _run_wizard(self, _):
        desc = self.wizard_input.value.strip()
        if not desc:
            self.wizard_status.value = '⚠️ Enter a scene description first.'
            return
        if 'wizard' not in self.r:
            self.wizard_status.value = '⚠️ T119 SceneWizard not in registry.'
            return
        self.wizard_status.value = '✨ Generating...'
        try:
            active = [n for n, cfg in self.active_config.items()
                      if cfg['status'].value != 'No']
            result = self.r['wizard'].draft_scene(desc, active)
            if result:
                self.env_box.value = result.get('environment', '')
                self.obj_box.value = result.get('scene_context', '')
                roles = result.get('roles', {})
                for name, cfg in self.active_config.items():
                    if name in roles and cfg.get('role'):
                        cfg['role'].value = roles[name]
                self.wizard_status.value = '✅ Fields populated — review and edit before starting.'
            else:
                self.wizard_status.value = '⚠️ Wizard returned empty result.'
        except Exception as e:
            self.wizard_status.value = f'⚠️ Wizard error: {e}'

    def _inject_event(self, _):
        text = self.injection_box.value.strip()
        if not text:
            return
        event_str = f"[SCENE_EVENT]: {text}"
        try:
            self.r['state'].state['global_history'].append(event_str)
            self._log(f"💉 Injected: {event_str}")
            self.injection_box.value = ''
        except Exception as e:
            self._log(f"⚠️ Injection error: {e}")

    def get_render_box(self):
        return self.sub_tabs'''

# Add Wizard + Scene Type + Injection rows to cockpit layout
OLD_T111_COCKPIT_BTNS = '''            widgets.HBox([
                self.new_scene_btn, self.start_btn, self.pause_btn,
                self.reset_ark_btn, self.kill_btn, self.bft_btn,
                self.pace_dropdown,
            ], layout={'margin': '4px 0', 'flex_wrap': 'wrap'}),
            self.console,'''

NEW_T111_COCKPIT_BTNS = '''            widgets.HBox([
                self.new_scene_btn, self.start_btn, self.pause_btn,
                self.reset_ark_btn, self.kill_btn, self.bft_btn,
                self.pace_dropdown, self.scene_type_dd,
            ], layout={'margin': '4px 0', 'flex_wrap': 'wrap'}),
            widgets.HBox([
                self.wizard_btn, self.wizard_gen, self.wizard_status,
            ], layout={'margin': '2px 0'}),
            self.wizard_input,
            widgets.VBox([
                widgets.HTML('<div style="font-weight:600;color:#333;font-size:12px;'
                             'padding:3px 0;border-bottom:1px solid #e0e0e0;margin-bottom:3px;">'
                             '💉 Live Scene Injection</div>'),
                widgets.HBox([self.injection_box, self.inject_btn],
                             layout={'width': '99%'}),
            ], layout={'margin': '4px 0'}),
            self.console,'''

# Wire wizard_btn and inject_btn in _ui_cockpit
OLD_T111_COCKPIT_WIRE = '''        self.bft_btn.on_click(self._run_bft)  # BL-I05'''
NEW_T111_COCKPIT_WIRE = '''        self.bft_btn.on_click(self._run_bft)    # BL-I05
        self.wizard_btn.on_click(self._toggle_wizard)
        self.wizard_gen.on_click(self._run_wizard)
        self.inject_btn.on_click(self._inject_event)'''

src = cell_src(nb, IDX_T111)
src = src.replace(OLD_T111_HEADER,       NEW_T111_HEADER)
src = src.replace(OLD_T111_KILLBTN,      NEW_T111_KILLBTN)
src = src.replace(OLD_T111_RENDERBOX,    NEW_T111_RENDERBOX)
src = src.replace(OLD_T111_COCKPIT_BTNS, NEW_T111_COCKPIT_BTNS)
src = src.replace(OLD_T111_COCKPIT_WIRE, NEW_T111_COCKPIT_WIRE)
set_cell(nb, IDX_T111, src)
print('✅ T111 patched')

# ════════════════════════════════════════════════════════════════════════════════
# INSERT T119 — SCENE_WIZARD (new cell after T118)
# ════════════════════════════════════════════════════════════════════════════════
T119_CODE = '''\
# ==========================================
# T119 : SCENE_WIZARD
# ==========================================
# VERSION: 1.0.0 | STATUS: New
# ROLE: Generative Scene Setup — Plain Language → Structured Scene
# Version Remarks: v1.0.0 — BL-N01 Sprint 7.
#   Creator describes scene in plain language.
#   T119 makes a single LLM call and returns a structured dict:
#   {environment, scene_context, roles: {name: role_string}}.
#   T111 Wizard button calls draft_scene() and pre-fills cockpit fields.
#   Creator reviews and edits before pressing Start.
# ------------------------------------------

import json as _json
import re as _re

class SceneWizard:
    def __init__(self, model_handle, shield_handle):
        self.model  = model_handle
        self.shield = shield_handle

    def draft_scene(self, description: str, active_souls: list) -> dict:
        """
        Input:   Plain-language scene description + list of active soul names
        Process: Single LLM call → parse JSON response
        Output:  {environment, scene_context, roles: {name: role_string}}
                 or None on failure
        """
        souls_str = ", ".join(active_souls) if active_souls else "unknown"

        prompt = f"""You are a scene architect for an immersive simulation engine.
A creator has described a scene. Draft a structured scene setup.

CREATOR DESCRIPTION:
{description}

ACTIVE CHARACTERS: {souls_str}

Return ONLY a valid JSON object with these exact keys:
{{
  "environment": "2-4 sentences. Physical space, time, atmosphere, sensory details.",
  "scene_context": "2-3 sentences. The shared situation all characters know. What is happening and why.",
  "roles": {{
    "{active_souls[0] if active_souls else 'Character'}": "their specific role/objective in this scene (1 sentence)"
  }}
}}

Rules:
- Include one role entry per character listed in ACTIVE CHARACTERS.
- environment and scene_context are shared — no character-specific secrets here.
- Roles should define what each character is doing or trying to achieve.
- Keep language concrete and specific, not generic.
- Return ONLY the JSON. No preamble, no explanation, no markdown fences."""

        raw, usage = self.shield.protect(self.model.generate_content, prompt)
        if not raw:
            return None

        # Strip markdown fences if model added them -------------------------
        cleaned = _re.sub(r\'```json|```\', \'\', raw).strip()
        try:
            result = _json.loads(cleaned)
            # Validate required keys ----------------------------------------
            required = {\'environment\', \'scene_context\', \'roles\'}
            if not required.issubset(result.keys()):
                print(f"⚠️ T119: Missing keys in response: {result.keys()}")
                return None
            # Ensure all active souls have a role ---------------------------
            for soul in active_souls:
                if soul not in result[\'roles\']:
                    result[\'roles\'][soul] = "Active participant"
            return result
        except (_json.JSONDecodeError, Exception) as e:
            print(f"⚠️ T119: JSON parse failed: {e}")
            print(f"   Raw response: {raw[:200]}")
            return None

# ------------------------------------------
# IPO CHECK:
# Input:   description (str), active_souls (list), model, shield
# Process: Single LLM call → JSON parse → validate → fill missing roles
# Output:  {environment, scene_context, roles} dict or None on failure
# ------------------------------------------
'''

# ════════════════════════════════════════════════════════════════════════════════
# INSERT T120 — ORCHESTRATOR (new cell after T119)
# ════════════════════════════════════════════════════════════════════════════════
T120_CODE = '''\
# ==========================================
# T120 : ORCHESTRATOR
# ==========================================
# VERSION: 1.0.0 | STATUS: New
# ROLE: Scene Type Governance & Live Narrative Control
# Version Remarks: v1.0.0 — BL-N02 Sprint 7.
#   Two responsibilities:
#   (1) Scene type pre-sets: Interview, Debate, Social, Custom.
#       Each type returns a urge modifier profile applied by T114
#       at scene start via apply_scene_type().
#   (2) Live injection: handled by T111 directly (no LLM call needed).
#       T120 provides the config layer only.
#
#   Scene type profiles:
#   Interview — interviewer starts at threshold (margin 0, holds back).
#               candidate starts at threshold + 2.0 (eager to speak).
#               Role detection: "interviewer"/"director" vs "candidate".
#   Debate    — all participants threshold + 1.5 (equal, BL-C02 standard).
#               CONTRADICTION_KW sensitivity flag set for T114.
#   Social    — all threshold + 1.5 (current default, unchanged).
#   Custom    — all threshold + 1.5 (same as Social, creator controls via briefing).
# ------------------------------------------

class Orchestrator:

    # Scene type urge profiles -----------------------------------------------
    SCENE_CONFIGS = {
        'Interview': {
            'default_margin': 1.5,
            'interviewer_margin': 0.0,   # holds back — low margin at start
            'candidate_margin':   2.0,   # eager — high margin at start
            'interviewer_keywords': ['interviewer', 'director', 'assessor',
                                      'evaluator', 'panel', 'coordinator'],
            'candidate_keywords':   ['candidate', 'applicant', 'interviewee'],
        },
        'Debate': {
            'default_margin': 1.5,
            'debate_mode': True,         # T114 can read this flag if desired
        },
        'Social': {
            'default_margin': 1.5,
        },
        'Custom': {
            'default_margin': 1.5,
        },
    }

    def apply_scene_type(self, active_souls, threshold_state,
                         scene_type='Social', role_map=None):
        """
        Input:   active_souls list, threshold_state dict, scene_type str,
                 role_map {name: role_string_lower}
        Process: Assign per-character urge based on scene type + role
        Output:  urge_state dict {name: float}
        Returns standard BL-C02 margins if scene_type not recognised.
        """
        cfg = self.SCENE_CONFIGS.get(scene_type, self.SCENE_CONFIGS['Social'])
        role_map = role_map or {}
        urge_state = {}

        for soul in active_souls:
            threshold = threshold_state.get(soul, 6.0)
            role_str  = role_map.get(soul, '').lower()

            if scene_type == 'Interview':
                is_interviewer = any(
                    kw in role_str for kw in cfg['interviewer_keywords'])
                is_candidate   = any(
                    kw in role_str for kw in cfg['candidate_keywords'])

                if is_interviewer:
                    margin = cfg['interviewer_margin']
                elif is_candidate:
                    margin = cfg['candidate_margin']
                else:
                    margin = cfg['default_margin']  # fallback for unassigned
            else:
                margin = cfg.get('default_margin', 1.5)

            urge_state[soul] = threshold + margin

        return urge_state

    def get_scene_config(self, scene_type: str) -> dict:
        """Return the raw config dict for a scene type."""
        return self.SCENE_CONFIGS.get(scene_type, self.SCENE_CONFIGS['Social'])

# ------------------------------------------
# IPO CHECK:
# Input:   active_souls, threshold_state, scene_type, role_map
# Process: Per-character urge assignment based on scene type + role detection
# Output:  urge_state dict {name: float} (→ T114 reset_urge_state)
# ------------------------------------------
'''

# Insert T119 after T118, then T120 after T119
IDX_T118_now = find_cell(nb, '# T118 : ENV_LOADER')
insert_cell_after(nb, IDX_T118_now, T119_CODE)
IDX_T119_now = IDX_T118_now + 1
insert_cell_after(nb, IDX_T119_now, T120_CODE)
print('✅ T119 inserted')
print('✅ T120 inserted')

# ════════════════════════════════════════════════════════════════════════════════
# PATCH 6 — Assembly cell (last cell — find it after insertions)
# ════════════════════════════════════════════════════════════════════════════════
IDX_ASSEMBLY = find_cell(nb, 'MASTER ASSEMBLY')

OLD_ASSEMBLY_HEADER = '''# ── T116 SmokeTester — BL-I05 ─────────────────────────────────────────────────
tester = SmokeTester(registry)
registry['tester'] = tester'''

NEW_ASSEMBLY_HEADER = '''# ── T116 SmokeTester — BL-I05 ─────────────────────────────────────────────────
tester = SmokeTester(registry)
registry['tester'] = tester

# ── T119 Scene Wizard — BL-N01 ────────────────────────────────────────────────
wizard = SceneWizard(gateway, shield)
registry['wizard'] = wizard

# ── T120 Orchestrator — BL-N02 ────────────────────────────────────────────────
orchestrator = Orchestrator()
registry['orchestrator'] = orchestrator'''

OLD_ASSEMBLY_TITLE = "# NOAH'S ARK v2.3.0: MASTER ASSEMBLY — Sprint 6"
NEW_ASSEMBLY_TITLE = "# NOAH'S ARK v2.4.0: MASTER ASSEMBLY — Sprint 7"

src = cell_src(nb, IDX_ASSEMBLY)
src = src.replace(OLD_ASSEMBLY_TITLE,  NEW_ASSEMBLY_TITLE)
src = src.replace(OLD_ASSEMBLY_HEADER, NEW_ASSEMBLY_HEADER)
set_cell(nb, IDX_ASSEMBLY, src)
print('✅ Assembly updated')

# ── Update title cell ─────────────────────────────────────────────────────────
OLD_TITLE = "# Noah's Ark OS — v2.3.0 Sprint 6"
NEW_TITLE = "# Noah's Ark OS — v2.4.0 Sprint 7"
src0 = cell_src(nb, 0)
src0 = src0.replace(OLD_TITLE, NEW_TITLE)
src0 = src0.replace('Chapter 2.7 — Output Quality & Interface Elevation',
                    'Chapter 2.8 — Scene Intelligence')
src0 = src0.replace('Tiles Changed: T103 v5.4.1, T105 v5.4.0, T106 v5.5.1,',
                    'Tiles Changed: T103 v5.4.2, T106 v5.5.2, T107 v5.7.1,')
src0 = src0.replace('#                T107 v5.7.0, T108 v5.3.0, T109 v5.2.0,',
                    '#                T111 v5.12.0, T114 v5.5.5,')
src0 = src0.replace('#                T111 v5.11.0, T114 v5.5.4',
                    '# New Tiles: T119 SCENE_WIZARD v1.0.0, T120 ORCHESTRATOR v1.0.0')
src0 = src0.replace('# Sprint 6 Items: BL-Q04, BL-Q01, BL-E07, BL-U09, BL-U10',
                    '# Sprint 7 Items: BL-N01 T119, BL-N02 T120, BL-Q05')
set_cell(nb, 0, src0)

# ── Save ──────────────────────────────────────────────────────────────────────
today = datetime.now().strftime('%d%m%Y')
out_path = f'Noahs_Ark_v2_4_0_{today}_sprint7.ipynb'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'\n✅ Sprint 7 notebook saved: {out_path}')
print(f'   Total cells: {len(nb["cells"])} (was 22, added T119+T120)')

# Quick verification
nb2 = json.load(open(out_path, encoding='utf-8'))
versions = {}
for cell in nb2['cells']:
    src = ''.join(cell['source'])
    m_tile = None
    for line in src.split('\n')[:4]:
        if '# T' in line and ':' in line and '====' not in line:
            m_tile = line.strip()
        if 'VERSION:' in line:
            versions[m_tile or '?'] = line.strip()
            break

print('\nVersion map:')
for tile, ver in versions.items():
    print(f'  {tile[:35]:<35} {ver}')
