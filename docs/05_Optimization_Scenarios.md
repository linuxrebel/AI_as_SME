SPDX-License-Identifier: CC-BY-SA-4.0

# Optimization Scenarios for Top SLM Models
## Phi-3 Mini, Mistral 7B, TinyLlama, Qwen 262K

**Research Scenarios**: July 28, 2026

---

## Model Selection & Optimization Contexts

### Top Tier Models Recap

| Category | Model | Key Strength | Params | Context |
|----------|-------|--------------|--------|---------|
| **Optimized** | Phi-3 Mini | Production-ready, tuned for quality | 3.8B | 128K |
| **Accuracy** | Mistral 7B | Best general performance | 7B | 32K |
| **Extreme Constraints** | TinyLlama | Minimal footprint | 1.1B | 2K |
| **Long Context** | Qwen 3.5 | Extended memory, multilingual | 3B | 262K |

---

## SCENARIO 1: PHI-3 MINI (Optimized)
### Enterprise Customer Support Copilot

**Context**: Financial services company with 500 customer support agents across 5 regions. 
- Current system: Cloud API calls at $15K/month
- Requirement: Real-time chat assistance, <200ms latency
- Constraint: Must stay current with product updates, policy changes
- Data: 50K support tickets/month, evolving FAQ database

### Optimization Goals
1. **Reduce latency** from 500ms to <200ms
2. **Cut API costs** by 80%
3. **Stay current** without full model retraining
4. **Maintain quality** across dynamic product catalog

### Recommended Setup: Hybrid Fine-tuning + RAG

```yaml
Architecture:
  Local Component:
    Model: Phi-3 Mini (4-bit quantized, 3GB)
    Hardware: 2x RTX 3060 per region
    Inference: 40-60 tokens/sec per GPU
    Latency: 150ms average
    
  Cloud Component:
    Storage: Vector DB (Pinecone/Weaviate)
    Updates: Daily refresh of product docs, policies
    Fallback: GPT-4 for edge cases
    
  Knowledge Layer:
    Static: Fine-tuned on 6-month historical support patterns
    Dynamic: RAG over latest product changes, policy updates
```

### Optimization Strategy: 80/20 Fine-tuning + RAG

**Fine-tuning (One-time, 80% of capability)**
```python
# Train on 5K representative conversations
# Focus: Company jargon, product names, common resolution patterns

training_data = {
    "customer_issue": "Card declined on international transaction",
    "agent_response": "This is often due to fraud detection. I'll verify your account...",
    "resolution": "Enabled international transfers in settings",
    "category": "fraud_prevention"
}

# LoRA fine-tuning (4 hours on single A100)
# Result: Model knows company context, resolution patterns, product features
```

**RAG Layer (Continuous, 20% currency)**
```python
# Daily scheduled updates
retriever = RAGRetriever(
    vector_db="pinecone",
    documents=[
        "latest_product_docs_2026_07_28.md",
        "policy_updates_this_week.md",
        "incident_alerts_yesterday.md",
        "new_feature_rollouts.md"
    ],
    update_schedule="daily"
)

# At inference time: Augment context with latest info
context = retriever.retrieve("customer asks about new fraud protection")
# Returns: Latest fraud protection feature docs + examples
```

### Why This Works

**Fine-tuning handles:**
- Company-specific terminology (product names, acronyms)
- Common resolution patterns (flowcharts, troubleshooting)
- Tone and voice standards (company style guidelines)
- Historical context from existing support approach
- One-time investment, amortized across all future queries

**RAG handles:**
- Weekly product launches and feature changes
- Policy updates from compliance team
- New incident alerts that agents need to reference
- External regulatory changes (PCI DSS, GDPR updates)
- Real-time information without model retraining

### Cost-Benefit Breakdown

```
Current State (Cloud API):
  - API cost: $15K/month
  - Latency: 500-800ms (unacceptable for chat)
  - Data exposure: Every query to external API
  Total: $180K/year + compliance risk

Proposed Hybrid:
  - Hardware: $6K one-time (2x RTX 3060)
  - Fine-tuning: $2K (one time, consultant labor)
  - Vector DB: $300/month (Pinecone serverless)
  - Ops: $1K/month (updates, monitoring)
  - Inference: $0 (local)
  Total: ~$18K/year + full data control
  
Savings: 90% reduction + 3-4x faster
```

### Maintenance Cadence

| Frequency | Task | Effort | Impact |
|-----------|------|--------|--------|
| **Monthly** | Review agent feedback | 4 hours | Catch drift |
| **Weekly** | Update RAG docs from product team | 2 hours | Stay current |
| **Quarterly** | Re-fine-tune if drift detected | 8 hours | Refresh company knowledge |
| **Annual** | Full model upgrade cycle | 1 day | Benefit from new model capabilities |

**Key Insight**: Fine-tuning captures stable, company-specific knowledge. RAG captures the 20% that changes frequently. This split minimizes retraining burden.

---

## SCENARIO 2: MISTRAL 7B (Accuracy-Focused)
### Legal Document Analysis Platform

**Context**: Legal firm analyzing M&A due diligence documents.
- Current problem: Associates spending 40 hours/week reviewing contracts for risk
- Requirement: 98%+ accuracy on risk identification, liability flagging
- Constraint: Cannot use cloud (attorney-client privilege)
- Data: Proprietary contract library (2000+ contracts), evolving case law

### Optimization Goals
1. **Achieve 98%+ accuracy** on known risk patterns
2. **Stay current** with evolving case law and precedents
3. **Explainability** - flag exactly which clause triggered warning
4. **Handle edge cases** that don't fit fine-tuned patterns

### Recommended Setup: Heavy Fine-tuning + Lightweight RAG

```yaml
Architecture:
  Local Component:
    Model: Mistral 7B (4-bit, 5GB)
    Hardware: Single RTX 4090 (on-premise law firm)
    Fine-tuning: 100+ hours on firm's contract library
    Goal: Deep knowledge of firm's specific risk framework
    
  Knowledge Layers:
    Tier 1 (Fine-tuned): Firm's known risk patterns, common clauses
    Tier 2 (RAG): Recent case law, regulatory updates, precedents
    Tier 3 (Fallback): Escalate to senior attorney for novel cases
```

### Optimization Strategy: 70/30 Fine-tuning + RAG

**Heavy Fine-tuning (70% capability)**

```python
# Start with 2000 contracts from firm's library
# Label 500 examples with:
#   - Risk category (liability, indemnity, limitation of liability, IP, etc.)
#   - Specific clause text
#   - Severity (critical, medium, low)
#   - Why it matters in M&A context

training_examples = [
    {
        "document": "...limitation of liability capped at annual fee...",
        "risk": "limitation_of_liability",
        "severity": "critical",
        "reasoning": "In $50M acquisition, caps revenue guarantees",
        "firm_precedent": "See Smith vs. Jones 2024 - similar clause led to $2M dispute"
    },
    # 500 more examples
]

# Full fine-tuning Mistral (48 hours on A100)
# Result: Model deeply understands:
#   - Firm's risk appetite and precedents
#   - Nuanced liability patterns specific to firm's deals
#   - Historical resolutions firm's negotiated
#   - Firm's specific triggering thresholds
```

**Lightweight RAG (30% capability)**

```python
# Curated legal knowledge base
rag_sources = [
    "recent_appellate_decisions_2026.md",     # Weekly updates
    "regulatory_guidance_sec_fca.md",          # Monthly updates
    "precedent_collection_firm.md",            # Historical firm wins/losses
    "model_language_library.md"                # Negotiated terms firm uses
]

# At analysis time:
def analyze_contract(contract_text):
    # 1. Fine-tuned model identifies known risk patterns
    known_risks = mistral_finetuned.analyze(contract_text)
    
    # 2. For novel patterns, query RAG for case law context
    for risk in known_risks:
        relevant_cases = rag.retrieve(
            f"Liability limitation in M&A context: {risk.clause}"
        )
        risk.precedents = relevant_cases
    
    # 3. Return with evidence and precedent support
    return known_risks
```

### Why This Works

**Fine-tuning (70%) solves:**
- Firm's specific risk classification system
- Nuanced interpretation of language firm has negotiated
- Historical patterns from firm's successful deals
- Firm's unique risk appetite (aggressive vs. conservative)
- Consistency with firm's documented approach

**RAG (30%) handles:**
- New case law that supersedes old precedents
- Regulatory changes (SEC guidance, FCA rules)
- Recent appellate decisions affecting risk interpretation
- Model language updates from industry groups
- Rare edge cases not in fine-tuning set

### Accuracy Scenario Analysis

```
Scenario: "Survival period limited to 18 months post-closing"

Fine-tuned Mistral output:
  - Risk: "Seller indemnity survival too short"
  - Severity: High (firm negotiated 3-year in last 5 M&A deals)
  - Why: Firm's historical data shows 18mo insufficient for tax disputes
  
RAG augmentation:
  - Retrieves: Recent case law (2026) about survival periods
  - Shows: Delaware court just ruled 18mo insufficient in similar case
  - Updates risk: CRITICAL (legal precedent now supports firm concern)
  
Result: Model catches nuance that simple keyword match would miss
```

### Maintenance Cadence

| Frequency | Task | Effort | Critical? |
|-----------|------|--------|-----------|
| **Daily** | Monitor new appellate decisions | 30 min | Yes (legal liability) |
| **Weekly** | Update SEC/regulatory guidance | 1 hour | Yes |
| **Monthly** | Review missed risks (false negatives) | 4 hours | Yes |
| **Quarterly** | Re-fine-tune if drift detected (new clauses) | 16 hours | No (optional) |
| **Annual** | Incorporate new case law into fine-tuning | 1 week | No (next cycle) |

**Key Insight**: 98%+ accuracy requires deep specialization. Fine-tuning gets you 95% with known patterns. RAG adds the final 3% by staying current with evolving legal precedent.

---

## SCENARIO 3: TINYLLAMA 1.1B (Extreme Constraints)
### Smart Home Voice Assistant (Offline)

**Context**: Consumer IoT company building on-device voice assistant.
- Hardware: Raspberry Pi 5 (8GB RAM, CPU-only, low power)
- Requirement: Instant voice command response (<50ms latency)
- Constraint: Zero cloud connectivity (privacy requirement)
- Data: 10K possible voice commands, evolving smart home devices

### Optimization Goals
1. **Sub-50ms latency** for voice response
2. **Fit in 4GB RAM** (leave room for OS, transcription)
3. **Handle 10K+ voice commands** accurately despite tiny model
4. **Adapt as users add new smart home devices** without redeployment

### Recommended Setup: Aggressive Fine-tuning + In-Memory RAG

```yaml
Architecture:
  Hardware:
    CPU: Raspberry Pi 5 (2.4GHz, 8GB RAM)
    Model: TinyLlama 1.1B (4-bit quantized, 900MB)
    Transcription: Whisper.cpp (on-device, GPU optional)
    Memory available for inference: 6-7GB
    
  Software Stack:
    Inference: llama.cpp (optimized C++ runtime)
    Quantization: 4-bit + int8 weights
    Cache: In-memory KV cache (512 tokens max)
    
  Knowledge:
    Static: Fine-tuned on 500 most common voice commands
    Dynamic: In-memory hash table of device state (100KB max)
    Fallback: Simple rule engine for unmatched commands
```

### Optimization Strategy: 90/10 Fine-tuning + Minimal RAG

**Aggressive Fine-tuning (90% capability)**

```python
# Ultra-focused training: only what users actually say
# Collect 500-1000 examples of real voice commands

training_data = [
    {
        "audio_transcript": "turn on the living room lights",
        "parsed_intent": "device_control",
        "action": "lights_living_room_on",
        "device_id": "bulb_lr_001",
        "certainty": "high"
    },
    {
        "audio_transcript": "dim the bedroom lights to 30 percent",
        "parsed_intent": "device_control_with_param",
        "action": "lights_bedroom_dim",
        "device_id": "bulb_br_001",
        "level": 30,
        "certainty": "high"
    },
    # Only 500 most common command variations
]

# Fine-tuning strategy:
# 1. Start with TinyLlama (1.1B)
# 2. Remove unnecessary capabilities (document generation, long reasoning)
# 3. Optimize for: command parsing, device control, parameter extraction
# 4. Quantize aggressively: 4-bit (int4) weights
# 5. Training time: 4-8 hours on CPU (one-time)

# Result model:
# - Size: 900MB (4-bit)
# - Speed: 60-80 tokens/sec on Pi 5 CPU
# - Latency for "turn on lights": 40-50ms (within budget)
# - Accuracy on known commands: 95%+
```

**Minimal In-Memory RAG (10% capability)**

```python
# In-memory device registry (not machine learning, simple lookup)
device_registry = {
    "living_room": {
        "lights": {"id": "bulb_lr_001", "type": "rgb", "brand": "philips"},
        "tv": {"id": "tv_lr_001", "type": "sony_bravia"},
        "thermstat": {"id": "nest_001"}
    },
    "bedroom": {
        "lights": {"id": "bulb_br_001", "type": "white_only"},
        "fan": {"id": "fan_br_001"}
    }
}

# At inference time:
def process_voice_command(transcript):
    # 1. TinyLlama extracts intent and parameters
    parsed = tinyllama.parse(transcript)
    # Output: {"intent": "lights_control", "room": "bedroom", "action": "dim", "level": 30}
    
    # 2. Simple lookup: Is the requested device in registry?
    device = device_registry[parsed["room"]][parsed["device_type"]]
    
    # 3. If user mentions "new device added", update registry
    if "new" in transcript:
        # Schedule update on next sync with cloud
        queue_device_discovery()
    
    # 4. Execute command
    send_mqtt(device["id"], parsed["action"], parsed.get("level"))
    return "Dimming bedroom lights to 30%"
```

### Why This Works

**Fine-tuning (90%) solves:**
- Command intent recognition (what user wants to do)
- Parameter extraction (which room, which device, what value)
- Handles natural language variations ("dim to 30%" vs "set to 30 percent")
- Lightning-fast inference on tiny model
- Works completely offline, no network latency

**Minimal RAG (10%) handles:**
- Device registry (which devices exist in home)
- New device discovery (user adds smart light)
- Device state (currently on/off, brightness level)
- Static lookup, not ML—keeps memory footprint minimal

### Performance on Raspberry Pi

```
Latency breakdown for "turn on bedroom lights":
  - Audio capture: 100ms (user speech duration)
  - Transcription (Whisper.cpp): 50-100ms
  - TinyLlama inference: 40-50ms ← optimization target
  - Device lookup + MQTT send: 10ms
  Total: 200-260ms (acceptable for voice UI)

Memory usage at inference:
  - TinyLlama 4-bit: 900MB
  - KV cache: 50MB
  - Device registry: 100KB
  - Inference overhead: 200MB
  Total: ~1.2GB (out of 8GB available = 15%)
```

### Adaptation Without Redeployment

```python
# User adds new Philips smart bulb to living room

# Option 1: Simple (no retraining)
# 1. Device discovered via mDNS or manual setup
# 2. Added to device_registry in memory
# 3. User says "turn on the new light"
# 4. TinyLlama still uses generic "lights" command
# 5. User might need to say "living room lights"
# Works: 80% of the time

# Option 2: Optimal (lightweight RAG update)
# 1. Schedule weekly cloud sync (when WiFi available)
# 2. Download latest device_registry from cloud
# 3. Restart voice assistant with updated registry
# 4. No model retraining needed
# Works: 99% of the time
# Cost: Slight delay (hours) before new device is "known"

# Option 3: Advanced (fine-tune new variant)
# 1. Collect 10 new voice commands with new device
# 2. Fine-tune new model variant on Pi (4 hours, background task)
# 3. Deploy new variant next morning
# 4. Model learns new device names, roles
# Works: 100% of the time
# Cost: One night of CPU time, but one-time per device discovery
```

### Maintenance Cadence

| Frequency | Task | Effort | Offline? |
|-----------|------|--------|----------|
| **Daily** | Monitor voice commands for failures | 5 min | Yes |
| **Weekly** | Sync device registry from cloud | 5 min | Queued |
| **Monthly** | Collect new command variations, plan fine-tune | 30 min | Yes |
| **Quarterly** | Run fine-tuning on new commands observed | 8 hours | Background |
| **Annually** | Full re-fine-tune with year's command data | 8 hours | Major update |

**Key Insight**: TinyLlama can't handle 10K commands through fine-tuning alone (model too small). Solution: Fine-tune on most common 500 commands (covers 90% of real-world usage), use simple lookup registry for device names. Hybrid approach achieves 95%+ accuracy without model bloat.

---

## SCENARIO 4: QWEN 3.5 3B (Long Context)
### Research Paper Analysis Engine

**Context**: Academic research institute processing 100+ papers/week.
- Current bottleneck: Manual extraction of methodology, findings, related work
- Requirement: Analyze full 20-40 page PDFs in single inference
- Constraint: On-premise, no data shared with external services
- Data: Dynamic corpus of papers (evolving literature, trending topics)

### Optimization Goals
1. **Process 40-page PDFs** in single context window (262K tokens = ~80K words)
2. **Extract methodology, findings, literature gaps** in one pass
3. **Stay current** with new research trends and methodologies
4. **Handle domain-specific terminology** across ML, biology, chemistry

### Recommended Setup: Moderate Fine-tuning + Large RAG

```yaml
Architecture:
  Local Component:
    Model: Qwen 3.5 3B (4-bit, 2.5GB)
    Hardware: Single GPU (RTX 4060, 8GB) or powerful CPU
    Context: 262K tokens (full 30-40 page paper + instructions)
    Inference: 30-40 tokens/sec on GPU
    
  Fine-tuning:
    Scope: Research methodology taxonomies, domain terminology
    Data: 200 annotated papers from institute's past work
    Goal: Learn institute's analysis framework
    
  RAG Layer:
    Scope: Recent papers, trending methodologies, related work
    Update: Weekly scan of arXiv, conference proceedings
    Goal: Stay current with literature landscape
```

### Optimization Strategy: 50/50 Fine-tuning + Substantial RAG

**Moderate Fine-tuning (50% capability)**

```python
# Fine-tune on institute's analysis framework
# 200 papers previously analyzed by researchers

training_examples = [
    {
        "paper_abstract": "We propose novel approach using transformers...",
        "paper_body": "[Full 10K-word paper text]",
        "analysis": {
            "methodology": "Transformer-based architecture with attention mechanisms",
            "key_findings": [
                "25% improvement over baseline",
                "Scales to 1M+ tokens"
            ],
            "related_work": "Extends Vaswani et al. 2017, comparable to Mistral 7B",
            "gaps": "Limited to English text, requires 100GB training data",
            "significance": "High - enables long-context reasoning",
            "institutional_relevance": "Directly applicable to our multimodal research",
            "future_directions": [
                "Extend to multilingual",
                "Reduce memory requirements"
            ]
        }
    },
    # 200 papers × institute's analysis format
]

# Fine-tuning:
# Input: Full paper (30K tokens)
# Output: Structured analysis (500 tokens)
# Training: 8 hours on A100 GPU
# Result: Model learns institute's analysis framework
#   - What constitutes methodology in your field
#   - How to identify gaps relevant to your research
#   - What makes work significant for your institution
```

**Substantial RAG (50% capability)**

```python
# Large knowledge base of recent research
rag_sources = {
    "recent_papers": {
        "source": "arXiv daily download",
        "schedule": "daily",
        "categories": ["cs.LG", "cs.AI", "stat.ML"],
        "retention": "Last 3 months (1000s papers)",
        "indexing": "Semantic embedding with nomic-embed-text"
    },
    "conference_proceedings": {
        "source": "ICLR, NeurIPS, ICML proceedings 2024-2026",
        "categories": ["papers"],
        "retention": "Full proceedings",
        "indexing": "Semantic + keyword hybrid"
    },
    "related_work_collection": {
        "source": "Manually curated by research group",
        "categories": ["foundational", "recent_advances", "competing_approaches"],
        "retention": "All",
        "indexing": "Semantic + citation graph"
    },
    "methodological_library": {
        "source": "Common techniques, benchmarks, datasets",
        "categories": ["techniques", "datasets", "benchmarks"],
        "retention": "All",
        "indexing": "Semantic + keyword"
    }
}

# At inference time:
def analyze_paper_comprehensive(paper_text):
    # 1. Run fine-tuned Qwen on full paper (using 262K context)
    institute_analysis = qwen_finetuned.analyze(paper_text)
    
    # 2. Retrieve related work from RAG
    related_papers = rag.retrieve(
        query=institute_analysis["methodology"],
        k=5,  # Top 5 related papers
        filter_date_range="Last 12 months"
    )
    
    # 3. Check if methodology aligns with trends
    trending_methods = rag.retrieve_trending(
        category="methodology",
        timeframe="Last 3 months"
    )
    
    # 4. Find related datasets/benchmarks
    relevant_benchmarks = rag.retrieve(
        query=institute_analysis["methodology"],
        k=3,
        type_filter="benchmark"
    )
    
    # 5. Compile comprehensive analysis
    comprehensive_analysis = {
        "institute_analysis": institute_analysis,
        "related_papers": related_papers,
        "novelty_assessment": assess_novelty(
            institute_analysis,
            related_papers
        ),
        "trending_alignment": align_with_trends(
            institute_analysis,
            trending_methods
        ),
        "recommended_benchmarks": relevant_benchmarks,
        "suggested_experiments": generate_suggestions(
            institute_analysis,
            related_papers
        )
    }
    
    return comprehensive_analysis
```

### Why This Works

**Fine-tuning (50%) solves:**
- Institution-specific analysis framework (what matters to your research group)
- Domain-specific terminology interpretation (neuroscience vs. NLP terminology differs)
- Institutional goals and priorities (what research aligns with your mission)
- Historical patterns from past analyses (consistency in analysis style)
- Quality standards your group expects (depth, rigor, specificity)

**RAG (50%) solves:**
- Related work that supersedes old literature
- Trending methodologies (what's hot in the field right now)
- Recent benchmarks and datasets
- Competing approaches published last month
- New tools and libraries relevant to work

### Example Analysis

```
Input: A new 35-page paper on "Efficient Attention Mechanisms for Long-Context LLMs"

Fine-tuned Qwen analysis:
  Methodology: "Sliding window attention + local attention layers"
  Findings: "Reduces memory 40%, speed 30% with minimal quality loss"
  Relevance to institute: "High - institute working on efficient inference"
  Gaps: "Only tested on English, requires further work on multilingual"

RAG augmentation:
  Related work: 
    - "Window Attention in Longformer" (Beltagy 2020)
    - "Local Attention for Long-Context LLMs" (recent arXiv)
    - "Memory-Efficient Transformers Survey" (2025)
  
  Trends: 
    - Efficient attention is trending (50+ papers in last 3 months)
    - Sliding window more popular than sparse attention (15:5 ratio)
    - Multilingual long-context still open problem
  
  Relevant benchmarks:
    - LongBench (English long-context tasks)
    - LongEval (multilingual long-context)
    - Custom benchmark institute created for multilingual

Final output: Paper is solid contribution to trending area, but competitor group 
already published similar work 2 weeks ago (found via RAG). Suggests institute 
focus on multilingual variants (gap identified).
```

### Handling Knowledge Decay

```
Knowledge has different half-lives:

Stable knowledge (fine-tuned):
  - Analytical frameworks (3-5 year half-life)
  - Institutional values and priorities (stable)
  - Domain-specific terminology (slow to change)
  → Re-fine-tune: Annual cycle

Moderately stable (RAG):
  - Related work and trends (6-month half-life)
  - Benchmark popularity (6-month half-life)
  - Common datasets in use (annual cycle)
  → RAG update: Monthly

Volatile knowledge (RAG):
  - Breaking new techniques (1-week half-life)
  - New papers posted (daily half-life)
  - Trending topics (real-time)
  → RAG update: Daily
```

### Maintenance Cadence

| Frequency | Task | Effort | Impact |
|-----------|------|--------|--------|
| **Daily** | Download new papers from arXiv | 1 hour | Catch breaking research |
| **Weekly** | Semantic indexing of new papers | 2 hours | Enable RAG retrieval |
| **Monthly** | Analyze trending topics, update trend tracking | 4 hours | Keep analysis current |
| **Quarterly** | Curate related work, update benchmarks | 8 hours | Maintain RAG quality |
| **Annually** | Re-fine-tune on year's papers + analysis | 16 hours | Refresh model knowledge |

**Key Insight**: 262K context allows processing entire papers in one shot. Fine-tuning captures institution-specific analysis framework (stable). RAG captures rapidly-changing literature landscape (volatile). This split optimizes both recency and consistency.

---

## FINE-TUNING VS RAG: The Fundamental Argument
### Staying Current in Dynamic Environments

### The Dilemma

Both approaches claim to keep models current:

**Fine-tuning advocates say:**
> "Train the model on your latest data. Then it knows everything."

**RAG advocates say:**
> "Retrieve latest information at query time. No retraining overhead."

**Reality:**
> Neither works alone. Both are needed, but in different proportions.

---

## Deep Dive: When Each Works

### Fine-tuning Strengths

**Best for: Stable, frequently-accessed knowledge**

1. **Structural Understanding**
   - Company jargon and terminology
   - Domain-specific concepts (medical diagnosis codes, legal liability categories)
   - Analytical frameworks (how your institution analyzes problems)
   - Business logic and decision trees

   Example: A hospital fine-tunes model on 5000 discharge summaries. Model learns:
   - ICD-10 coding patterns specific to your hospital
   - Which lab results matter for your patient population
   - How your physicians reason about diagnoses
   - This knowledge persists across all future queries

2. **Performance Optimization**
   - Faster inference (model learns what matters, ignores distractions)
   - Reduced hallucinations (model grounded in your patterns)
   - Better generalization to similar problems
   - One-time training cost, amortized across thousands of queries

   Example: A fraud detection model fine-tuned on 10K transactions learns patterns specific to your customer base. Result: Better accuracy on YOUR fraud patterns vs. general models.

3. **Consistent Voice & Style**
   - Company writing standards
   - Terminology consistency
   - Tone and personality
   - Document structure preferences

4. **Offline Capability**
   - Works without internet connection
   - No external dependencies or API calls
   - No latency waiting for retrieval

### RAG Strengths

**Best for: Volatile, rarely-repeated knowledge**

1. **Factual Recency**
   - Latest product catalog (new items, discontinued items)
   - Current prices (change daily)
   - Real-time policies (updated regulations)
   - Breaking news (yesterday's events)

   Example: A customer support chatbot needs latest product info. Products change daily. Fine-tuning model 365 times/year is wasteful. RAG: Retrieve latest product DB at query time.

2. **Knowledge Scale**
   - Too much knowledge to fit in model
   - External databases (customer records, inventory systems)
   - Real-world state (account balance, order status)
   - Personalization (this customer's specific data)

   Example: A legal firm analyzing contracts needs access to:
   - 10,000+ precedent cases (too large for fine-tuning)
   - Latest regulatory guidance (too frequently updated)
   - Case-specific related work (different per query)
   RAG: Retrieve relevant subset per query without bloating model

3. **Explainability & Citation**
   - Show where information came from
   - Provide evidence (case law precedents, source documents)
   - Enable human verification
   - Comply with regulations (audit trail)

   Example: A medical AI recommending treatment must cite which papers support recommendation. Fine-tuning embeds knowledge opaquely. RAG explicitly shows sources.

4. **Personalization at Query Time**
   - Different users see different context
   - Avoid cross-customer data leakage
   - Handle one-off customer situations
   - Tailor context to specific query intent

   Example: A bank's fraud detection system. Customer A has high-risk transactions (travel); Customer B's same transaction pattern is normal (frequent business travel). RAG: Retrieve Customer B's transaction history to personalize risk assessment.

---

## Hybrid Framework: Optimal Model Selection

### Core Principle

> **Fine-tune for stable, structural knowledge.**  
> **Use RAG for volatile, factual knowledge.**

### Decision Matrix

```
Question: Should I fine-tune or use RAG?

1. How often does this knowledge change?
   
   Changes daily/weekly/event-driven?
   └─ Use RAG (faster update, no retraining)
   
   Stable for months/years?
   └─ Fine-tune (amortize cost, improve performance)

2. How critical is accuracy on this knowledge?
   
   Nice-to-have facts (trending topics, competitor news)?
   └─ RAG only (no retraining overhead)
   
   Mission-critical understanding (company operations, legal liability)?
   └─ Fine-tune (guarantee knowledge is embedded)

3. Is this knowledge about your organization or the external world?
   
   About you (company jargon, internal processes, past decisions)?
   └─ Fine-tune (stable, internal)
   
   About external world (current events, market conditions, regulations)?
   └─ RAG (changes independently, you don't control updates)

4. How much knowledge is there?
   
   Small amount (100 documents or concepts)?
   └─ Fine-tune (fits in model)
   
   Huge amount (10,000+ documents, databases)?
   └─ RAG (can't fit in model without bloat)

5. How personalized does it need to be?
   
   Same answer for all users?
   └─ Fine-tune (build into model)
   
   Different answer per user/query?
   └─ RAG (retrieve user-specific context at query time)
```

### The 70/30 Rule (Adapted to Your Domain)

**For Customer Support** (Phi-3 Mini example):
- 70% fine-tuning: Company products, FAQs, common resolutions
- 30% RAG: Current product specs, active promotions, policy updates
- Reasoning: Support patterns stable; product catalog changes monthly

**For Legal** (Mistral 7B example):
- 70% fine-tuning: Firm's risk framework, precedents firm has negotiated
- 30% RAG: New case law (changes weekly), regulatory updates
- Reasoning: Firm's framework stable; law changes continuously

**For Voice Assistant** (TinyLlama example):
- 90% fine-tuning: Common voice commands, device control logic
- 10% RAG: Device registry (changes when user adds devices)
- Reasoning: Commands stable; device inventory changes rarely

**For Research** (Qwen example):
- 50% fine-tuning: Analysis framework, institutional terminology
- 50% RAG: Recent papers, trending methods, related work
- Reasoning: Framework stable; literature changes daily

---

## Knowledge Decay Analysis

### How knowledge ages

```
At time T=0 (when you train/retrieve):
  - Knowledge is 100% accurate

At time T=1 month:
  - Fine-tuned knowledge: 99% accurate (very stable)
  - RAG knowledge: 95% accurate (older papers, trends shift)

At time T=1 quarter:
  - Fine-tuned knowledge: 97% accurate (some knowledge ages)
  - RAG knowledge: 80% accurate (much newer work published)

At time T=1 year:
  - Fine-tuned knowledge: 85% accurate (needs refresh)
  - RAG knowledge: 50% accurate (if not updated, useless)
```

### Knowledge half-life by domain

| Domain | Stable Knowledge | Volatile Knowledge |
|--------|-----------------|-------------------|
| **Customer Support** | Company processes (1-2 yr) | Product catalog (monthly) |
| **Legal** | Risk frameworks (5 yr) | Case law (weekly) |
| **Voice Assistant** | Command patterns (1 yr) | Device inventory (realtime) |
| **Research** | Analysis frameworks (3-5 yr) | Literature (daily) |
| **Medicine** | Diagnostic logic (2-3 yr) | Drug approvals (realtime) |
| **Finance** | Risk models (6-12 mo) | Market prices (realtime) |

**Key Insight**: Knowledge has different shelf lives. Fine-tune what decays slowly. Update via RAG what decays fast.

---

## Cost-Benefit Analysis: Fine-tuning vs RAG

### Scenario: Customer Support (1M queries/month)

**Option A: RAG Only**
```
Costs:
  - Vector DB: $500/month (Pinecone)
  - Embedding model hosting: $200/month
  - Daily data refresh: $100/month ops labor
  - Base model inference: $5K/month (cloud API)
  Total: ~$5,800/month ($69,600/year)

Benefits:
  - Always up-to-date product info
  - No retraining overhead
  
Risks:
  - Every query hits external system (latency, availability)
  - 30% hallucination rate on company-specific FAQ
  - High inference cost (uses expensive cloud LLM)
```

**Option B: Fine-tuning Only**
```
Costs:
  - Fine-tuning (one-time): $2K
  - Hardware (amortized): $1K/month
  - Local inference: $500/month ops
  Total: ~$1,500/month ($18,000/year)

Benefits:
  - Sub-200ms latency (all local)
  - Guaranteed knowledge of company processes
  - Low inference cost
  
Risks:
  - Product catalog stale after 1 month
  - Need retraining every month ($2K each)
  - Total: ~$26,000/year (fine-tuning + inference)
  - New products take time to reach model
```

**Option C: Hybrid (70/30 Fine-tuning + RAG)**
```
Costs:
  - Fine-tuning (monthly): $500/month
  - Hardware: $1K/month
  - Vector DB (lightweight): $100/month
  - Local inference: $500/month ops
  Total: ~$2,100/month ($25,200/year)

Benefits:
  - Fast local inference (company-specific knowledge)
  - Current product info (RAG updated daily)
  - High accuracy (70% from model, 30% from retrieval)
  - Balanced approach
  
Performance:
  - Latency: 150-200ms (mostly local)
  - Hallucination: 5% (model grounded)
  - Availability: 99%+ (no external service dependency)
```

**Winner: Hybrid saves 64% vs RAG-only, 27% vs monthly fine-tuning only, and delivers better UX.**

---

## The Real Answer: It Depends On...

### Decision Framework

```python
def choose_approach(scenario):
    score = 0
    
    # Scoring for fine-tuning (+1 point each)
    if scenario.knowledge_changes_less_than("6 months"):
        score += 1
    if scenario.knowledge_amount_is_less_than("1000 documents"):
        score += 1
    if scenario.importance_is("mission_critical"):
        score += 1
    if scenario.model_needs_offline_capability():
        score += 1
    if scenario.has_consistent_user_base():
        score += 1
    
    # Scoring for RAG (+1 point each)
    if scenario.knowledge_changes_more_than("weekly"):
        score -= 1
    if scenario.knowledge_amount_is_more_than("10000 documents"):
        score -= 1
    if scenario.needs_personalization_per_query():
        score -= 1
    if scenario.needs_explainability_with_sources():
        score -= 1
    if scenario.needs_to_scale_to_massive_kb():
        score -= 1
    
    # Decision
    if score > 2:
        return "Fine-tune"
    elif score < -2:
        return "RAG only"
    else:
        return "Hybrid (recommended)"
```

### The 4 Quadrants

```
                    Fast Change (RAG needed)
                            ↑
                            │
      Hybrid approach ←─────┼─────→ RAG only
      (recommended)         │
                            │
    Low Volume ←────────────┼────────→ High Volume
                            │ (can't fine-tune)
      Fine-tuning ←─────────┼─────→ Hybrid
      only              │
                            │
                            ↓
                    Slow Change (Fine-tune works)
```

---

## Practical Maintenance Schedule

### For Fine-tuning Component

```
Weekly:
  - Monitor inference quality (accuracy, hallucinations)
  - Collect feedback (false negatives, missing edge cases)
  - Plan next fine-tuning cycle if needed

Monthly:
  - Run fine-tuning on accumulated feedback (4-8 hours)
  - Evaluate accuracy improvements
  - Roll out new version if acceptable

Quarterly:
  - Comprehensive accuracy audit
  - Benchmark against new model versions
  - Plan major model upgrade if needed

Annually:
  - Full cycle review: Is fine-tuning still the best approach?
  - Consider fine-tuning a different base model
  - Plan 2-3 year roadmap
```

### For RAG Component

```
Daily:
  - Automated data refresh from source systems
  - Monitor retrieval quality (relevant documents returned)
  - Check embedding model performance

Weekly:
  - Manual review of complex queries that used RAG
  - Update knowledge base curation
  - Fix incorrect retrievals

Monthly:
  - Analyze retrieval patterns (what gets retrieved?)
  - Identify knowledge gaps
  - Plan new data sources if needed

Quarterly:
  - Upgrade vector DB if needed
  - Benchmark retrieval quality
  - Optimize indexing strategy

Annually:
  - Full knowledge base audit
  - Consider alternative retrieval methods (BM25 vs semantic)
  - Plan architectural changes
```

---

## Conclusion: The Unifying Principle

**Fine-tuning = embed stable, structural knowledge into the model**  
**RAG = retrieve volatile, factual knowledge at query time**

The models we analyzed above all follow this principle:

- **Phi-3 Mini** (support): Fine-tune on company FAQ (stable), RAG on current products (volatile)
- **Mistral 7B** (legal): Fine-tune on risk framework (stable), RAG on case law (volatile)
- **TinyLlama** (voice): Fine-tune on commands (stable), device registry as lookup (static)
- **Qwen 262K** (research): Fine-tune on analysis framework (stable), RAG on papers (volatile)

**The winning teams use both, optimized to the nature of their knowledge domain.**
