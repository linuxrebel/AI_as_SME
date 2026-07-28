SPDX-License-Identifier: CC-BY-SA-4.0

# Architectural Assumptions in Cost Analysis
## Breaking Down the Hidden Assumptions Behind the Numbers

**Analysis Date**: July 28, 2026

---

## Overview: The Cost Analysis Numbers Are NOT Universal

The cost analysis in the Customer Support scenario presents specific numbers, but each number rests on **architectural assumptions** that may or may not apply to your situation. This document makes all hidden assumptions explicit.

---

## OPTION A: RAG Only ($5,800/month)

### Assumption Set 1: Cloud LLM Inference Model

**Stated**: "Base model inference: $5K/month (cloud API)"

**What this assumes**:
- Using cloud LLM API (OpenAI GPT-4, Claude, Mistral API)
- Pricing: ~$0.005 per 1K input tokens + $0.015 per 1K output tokens
- Average query: 500 tokens input (customer question + context) + 200 tokens output
- Cost per query: ~$0.004
- 1M queries/month = $4,000/month inference cost

**This assumption breaks if**:
- You negotiate volume discounts (AWS, Azure enterprise deals: -30% to -50%)
- You use cheaper LLM API (Mistral API: $0.0014/1K tokens vs OpenAI's $0.005)
- You use open-source model inference (free if you host, but need hardware)
- You use model pruning/quantization to reduce token consumption

**Real-world impact**: 
- Startup with low volume: $5K/month estimate is HIGH (you're paying for burst pricing)
- Enterprise with 10M queries/month: $5K/month is LOW (negotiations, better rates)

---

### Assumption Set 2: Vector Database Pricing

**Stated**: "Vector DB: $500/month (Pinecone)"

**What this assumes**:
- Using Pinecone managed vector database
- Pricing tier: Standard (not free, not enterprise)
- Queries: 1M semantic searches/month
- Storage: ~100K product documents (typical e-commerce)
- Vector dimension: 1536 (OpenAI embedding size)
- Pinecone Standard pricing: ~$50/month base + $0.25 per million vectors stored beyond 1M

**This assumption breaks if**:
- You use self-hosted Weaviate or Milvus: $0/month (but needs ops team)
- You use Supabase pgvector: $25-100/month (depends on DB size)
- You use basic full-text search (Elasticsearch): $100-200/month (but lower quality)
- You're a startup (Pinecone free tier: first 1M vectors free)

**Real-world impact**:
- Startup: $0-50/month (free tier)
- Scale-up (100K vectors): $100-300/month
- Enterprise (1M+ vectors): $500-2000/month

---

### Assumption Set 3: Embedding Model Hosting

**Stated**: "Embedding model hosting: $200/month"

**What this assumes**:
- Using cloud-hosted embedding service (e.g., Replicate, Modal)
- Not using OpenAI embeddings (would add another $0.0001/token = ~$100-200/month)
- Self-hosted embedding model on small GPU (t3.medium AWS: $60/month compute + $50/month ops)
- Embedding model: text-embedding-ada-002 or similar
- Queries: 1M embeddings/month (every retrieval needs to embed query)
- Cost: ~$200/month for managed inference

**This assumption breaks if**:
- You use OpenAI embeddings API: +$100/month (instead of hosting)
- You cache query embeddings: -50% (common queries cached, no recompute)
- You batch embeddings at ingest time only (not at query time): ~$50/month
- You use cheaper embedding model (nomic-embed-text open-source): $0 (self-hosted)

**Real-world impact**:
- Using OpenAI embeddings instead of hosted: +$100/month (+20% total cost)
- Self-hosting embedding model on CPU: -$150/month (-3%)
- Aggressive caching: -$100/month (-2%)

---

### Assumption Set 4: Ops Labor for RAG Refresh

**Stated**: "Daily data refresh: $100/month ops labor"

**What this assumes**:
- Automated daily sync of product catalog to vector DB (Pinecone sync connector)
- ~1 hour/week of ops work to maintain sync pipeline
- Ops labor cost: $100/hour (junior ops engineer)
- ~1 hour/week × 4 weeks = $400/month ÷ 4 = $100/month stated
- Reality: This is UNDER-STATED for most companies

**This assumption breaks if**:
- Catalog changes are complex (require data validation, transformation): +$200-500/month
- You have multiple data sources to sync (product DB, pricing DB, inventory): +$100-200/month
- You use manual data entry (customer service team updates docs): +$500-2000/month
- You need SLA for sync (99.9% uptime guarantee): +$100-300/month
- You use enterprise data pipeline (Fivetran, Stitch): +$500-1000/month

**Real-world impact**:
- Simple automated sync: $100/month (assumption correct)
- Complex sync with validation: $300-500/month (+200-400% over assumption)
- Manual updates by humans: $1000-2000/month (+1000-2000% over assumption)

**Critical insight**: This is the most under-stated cost in most RAG deployments.

---

### Option A Total Cost Sensitivity Analysis

```
Base estimate: $5,800/month ($69,600/year)

Cost Variations by Scenario:

Lean RAG Setup (startup, aggressive optimization):
  - Use Mistral API ($0.0014/1K tokens instead of $0.005): -$3,000/month
  - Use self-hosted Weaviate: -$500/month
  - Self-host embeddings: -$200/month
  - Aggressive caching: -$100/month
  - Total: ~$2,000/month ($24,000/year) ← 65% savings
  
Heavy RAG Setup (enterprise, full managed services):
  - Use OpenAI GPT-4 API: +$1,000/month
  - Use Pinecone enterprise: +$500/month
  - Use OpenAI embeddings: +$100/month
  - Complex data sync pipeline: +$400/month
  - Dedicated RAG ops engineer: +$2,000/month
  - Total: ~$9,800/month ($117,600/year) ← 69% more expensive

Mid-market (typical):
  - Slightly cheaper API (Mistral): -$1,000/month
  - Standard vector DB (Pinecone): $500/month
  - Hosted embeddings: $200/month
  - Moderate ops labor: $200/month
  - Total: ~$4,700/month ($56,400/year) ← 19% savings
```

**Key finding**: RAG cost can vary 3.7x depending on architecture choices.

---

## OPTION B: Fine-tuning Only ($1,500/month = $18,000/year)

### Assumption Set 1: Hardware Amortization

**Stated**: "Hardware (amortized): $1K/month"

**What this assumes**:
- Purchase: 1x RTX 4090 ($1,500 upfront cost)
- Amortization: Over 3 years = $500/month
- OR: Monthly cloud GPU rental (p3.2xlarge AWS = $3.06/hour = ~$2,200/month)
- Taking conservative middle ground: $1K/month

**This assumption breaks if**:
- You already have GPUs (cost should be $0 or just power: $50/month)
- You use cheaper hardware (RTX 3080: $800 upfront = $222/month amortized)
- You rent spot instances (70% cheaper: $600/month)
- You use CPU-only (free, but 10x slower fine-tuning: more ops time needed)

**Real-world impact**:
- Startup without GPU: Borrow/rent $600-2000/month (realistic)
- Company with idle GPU: $0 hardware cost
- Using CPU-only: Add $200-400/month in ops time (retraining takes much longer)

---

### Assumption Set 2: Fine-tuning Frequency

**Stated**: "Fine-tuning (one-time): $2K" BUT "Need retraining every month ($2K each)"

**This is contradictory. Let me unpack the actual cost**:

The text says:
- One-time fine-tuning: $2K (consulting labor to set it up)
- Monthly retraining: $2K each (labor + compute)
- Total: $24K/year in retraining

**What this assumes about monthly retraining**:
- 8 hours of labor @ $150/hour = $1,200
- 4 hours of GPU compute @ $3.06/hour = $12-15
- Validation/testing time: 2 hours @ $75/hour = $150
- Total per month: ~$1,350-1,500 (author estimated $2K, which is fair including overhead)

**This assumption breaks if**:
- You don't actually need monthly retraining (see knowledge decay section)
- You batch retraining quarterly: $500/month average (75% savings)
- You use LoRA instead of full fine-tuning (2 hours instead of 8): -$600/month
- You have an ML engineer on staff (already billed to department): cost doesn't increase
- You automate retraining (CI/CD pipeline): -$500/month ops labor

**The hidden assumption**: You're retraining EVERY MONTH. This is the killer assumption.

---

### Assumption Set 3: "Product Catalog Stale After 1 Month"

**Stated**: This implies you need monthly retraining

**What this assumes**:
- Product catalog changes significantly month-to-month
- Model needs to know new product details
- Old product info causes measurable accuracy drop
- Users ask about new products more than old ones

**This assumption is WRONG for most customer support scenarios**:
- Most support questions are about existing products (80-90%)
- New products (10-20%) can be handled with retrieval context
- Stale product info causes maybe 5% accuracy drop, not catastrophic
- So you actually DON'T need monthly retraining; quarterly or semi-annual is sufficient

**Corrected analysis**: If retraining happens quarterly, not monthly:
- Fine-tuning cost: $500/month average ($2K ÷ 4 months)
- Hardware: $1K/month
- Ops: $500/month
- **Total: $2K/month ($24K/year)** ← Already better than stated

---

### Assumption Set 4: Local Inference Ops

**Stated**: "Local inference: $500/month ops"

**What this assumes**:
- Running Phi-3 Mini locally (4-bit quantized, 3GB model)
- Inference engine: vLLM or similar (open-source, free)
- Operations: monitoring, uptime, occasional debugging
- Estimated labor: 20 hours/month @ $25/hour = $500/month
- OR: SLA monitoring, alerting, escalation procedures

**This assumption breaks if**:
- You run on unmanaged hardware (Raspberry Pi): $0 ops (already included in amortization)
- You use managed inference service (modal, replicate): +$100-300/month
- You have high uptime requirements (99.99%): +$200-500/month
- You need load balancing/auto-scaling: +$300-1000/month
- You already have DevOps team: $0 incremental

**Real-world impact**:
- Simple setup (single machine, best effort): $0-100/month
- Production setup (monitoring, alerting): $300-700/month
- High-availability setup (redundancy, auto-scaling): $800-2000/month

---

### Option B Total Cost Sensitivity Analysis

```
Base estimate: $1,500/month = $18,000/year

Cost Variations by Scenario:

Lean Fine-tuning Setup (optimized, quarterly retraining):
  - Fine-tuning quarterly (not monthly): -$1,500/month
  - Use cheaper GPU (RTX 3080): -$200/month
  - Minimal ops (single machine): -$300/month
  - Already have on-staff ML engineer: -$0 (already allocated)
  - Use LoRA fine-tuning: -$300/month labor
  - Total: ~$700/month ($8,400/year) ← 53% savings
  
Heavy Fine-tuning Setup (enterprise, monthly retraining, managed):
  - Fine-tuning monthly: +$2,000/month
  - Use multiple GPUs: +$1,000/month
  - Managed inference service: +$200/month
  - Dedicated ML engineer: +$2,000/month
  - A/B testing, validation overhead: +$500/month
  - Total: ~$6,700/month ($80,400/year) ← 347% more expensive
  
Realistic startup setup (quarterly, optimized):
  - Fine-tuning quarterly: -$1,500/month
  - Amortized GPU ($500): $500/month
  - Part-time ops: $200/month
  - Total: ~$1,200/month ($14,400/year) ← 20% savings
```

**Key finding**: Fine-tuning-only cost varies 9.5x depending on retraining frequency and setup complexity.

---

## OPTION C: Hybrid ($2,100/month = $25,200/year)

### Assumption Set 1: Split Retraining Schedule

**Stated**: "Fine-tuning (monthly): $500/month"

**What this assumes**:
- Light fine-tuning (not full model retraining)
- Using LoRA or similar efficient technique (2-4 hours instead of 8)
- Cost: 2 hours labor @ $150 + 1 hour GPU @ $5 = ~$300/month
- Author budgeted $500/month (includes overhead, buffer)

**This assumption breaks if**:
- You don't actually update fine-tuned model monthly (see knowledge decay): -$500/month
- You use full fine-tuning instead of LoRA: +$1,000/month
- You batch updates quarterly: -$350/month
- You have ML engineer on staff already: -$500/month (no incremental cost)

**The hidden assumption**: You're actually seeing enough drift to need monthly updates. Most scenarios DON'T.

---

### Assumption Set 2: Hardware Sharing

**Stated**: "Hardware: $1K/month"

**What this assumes**:
- Hybrid architecture might use GPU for fine-tuning AND inference
- RTX 4090 ($1,500) amortized over 3 years = $500/month
- OR: Part-time cloud GPU rental: $1K/month
- Taking conservative middle: $1K/month

**This assumption breaks if**:
- You separate concerns:
  - Fine-tuning GPU (spot instance, bursty, $300/month)
  - Inference GPU (continuous, $500/month)
  - Total: $800/month (but more complex ops)
- You use CPU-only inference (Phi-3 Mini runs on CPU): $0 inference hardware
- You run on Raspberry Pi (already amortized): $0

---

### Assumption Set 3: Lightweight Vector DB

**Stated**: "Vector DB (lightweight): $100/month"

**What this assumes**:
- Not Pinecone enterprise ($500/month)
- Not self-hosted (free but ops-heavy)
- Using: Supabase pgvector ($20-50/month) or Milvus cloud ($50-100/month)
- Corpus size: ~10K-20K documents (product spec changes only)
- Query volume: 100K semantic searches/month (not all 1M queries need RAG)

**This assumption breaks if**:
- All 1M queries hit RAG: Upgrade to $300-500/month
- You self-host (DevOps complexity): $0-200/month
- You use simpler full-text search (Elasticsearch): $50-150/month

---

### Assumption Set 4: Inference Inference (Not RAG!)

**Stated**: "Local inference: $500/month ops"

**What this assumes**:
- Hybrid model: Local Phi-3 Mini handles 70% of queries
- RAG fallback handles 30% of queries (needs cloud or managed inference)
- Ops labor: 15 hours/month for local system (less complex than fine-tuning-only)
- Cost: 15 hours @ $25-30/hour = $400-450/month (author rounded to $500)

**This assumption breaks if**:
- All inference is local (no cloud fallback): -$100/month
- You have production SLAs (high uptime): +$200-400/month
- RAG queries timeout/fail frequently (bad architecture): +$300-500/month troubleshooting
- You manage this with existing DevOps: $0 incremental

---

### Assumption Set 5: Embedding Model Costs (Hidden!)

**NOT STATED but present**: Hybrid still needs embeddings for RAG

- If using OpenAI embeddings: +$100-150/month (author omitted this)
- If self-hosting: Free but included in ops labor already

**This is a hidden cost** not mentioned in the hybrid analysis. Should be +$100/month.

---

### Option C Total Cost Sensitivity Analysis

```
Stated estimate: $2,100/month = $25,200/year

But realistic costs vary significantly:

Lean Hybrid Setup (optimization-focused):
  - Fine-tuning quarterly (not monthly): -$350/month
  - Self-host vector DB: -$100/month
  - Self-host embeddings: Free (included in ops)
  - CPU-only inference hardware: -$500/month
  - Use existing ML engineer: -$300/month
  - Total: ~$850/month ($10,200/year) ← 60% savings
  
Heavy Hybrid Setup (enterprise, fully managed):
  - Fine-tuning monthly: +$500/month
  - Premium vector DB (Pinecone): +$400/month
  - Separate inference GPU: +$500/month
  - Dedicated ops team: +$1,500/month
  - A/B testing infrastructure: +$300/month
  - Total: ~$4,700/month ($56,400/year) ← 124% more expensive
  
Realistic mid-market setup:
  - Fine-tuning quarterly: -$350/month
  - Supabase pgvector: $50/month
  - Self-host embeddings: Free
  - Modest hardware ($500): $500/month
  - Ops labor: $300/month
  - Total: ~$1,300/month ($15,600/year) ← 38% savings
```

**Key finding**: Hybrid cost varies 5.5x depending on how aggressively you optimize.

---

## Comparative Sensitivity Table

### If You Change ONE Assumption

| Assumption | Original | Changed | Impact |
|-----------|----------|---------|--------|
| **RAG**: Cloud LLM pricing | GPT-4 $0.005 | Mistral $0.0014 | -$3,000/mo |
| **RAG**: Vector DB | Pinecone $500 | Self-hosted | -$500/mo |
| **Fine-tune**: Frequency | Monthly | Quarterly | -$1,500/mo |
| **Fine-tune**: Hardware | $1K rental | Own GPU | -$500/mo |
| **Fine-tune**: Full vs LoRA | Full (8hr) | LoRA (2hr) | -$900/mo |
| **Hybrid**: Split retraining | Monthly | Quarterly | -$350/mo |
| **Hybrid**: Embeddings | Hosted | Self-host | -$200/mo |

---

## The Most Critical Assumptions

### 1. Retraining Frequency (Biggest Lever)

**Stated assumption in fine-tuning-only**: Monthly retraining necessary

**Reality check**: Do you actually need this?
- Customer support product catalog changes FASTER than quarterly? Unusual.
- Most support FAQs stable 3-6 months? Common.
- New products should go through RAG retrieval, not wait for retraining? Better architecture.

**If you can move from monthly → quarterly**: Save $1,500/month on fine-tuning-only option

---

### 2. What Gets Fine-tuned vs RAG'd (Second Biggest Lever)

**Stated assumption in all options**: What goes where is fixed

**Reality**: You choose the split based on your data
- Fine-tuning 1000 high-value questions vs. all customer chats? -$1000/month difference
- RAG over latest product docs (100 docs) vs. all docs ever (10K docs)? -$200/month difference
- Fine-tuning with full examples vs. prompt templates? -$500/month difference

**If you optimize this split**: Save 20-40% on any option

---

### 3. Team Composition (Third Biggest Lever)

**Stated assumption**: You pay for all labor

**Reality**: Existing teams, resource allocation changes this dramatically
- ML engineer already on staff (not incremental cost): -$2,000-3,000/month
- DevOps already monitoring systems (not incremental): -$500/month
- Use vendor's managed service vs. self-hosting: Changes by 2-5x

**If you have existing teams**: All costs drop 30-50%

---

### 4. Scale Threshold Assumptions

**Stated assumption**: 1M queries/month (fixed scale)

**Reality**: Costs scale non-linearly
- At 100K queries/month: All costs drop 20-30% (lower minimums)
- At 10M queries/month: All costs increase 150-300% (scale penalties, SLA costs)

**This means the comparison is ONLY valid at 1M/month scale**

---

## Building Your Own Cost Model

### Variables You Must Define First

```yaml
Scale:
  queries_per_month: 1000000  # CHANGE THIS
  query_tokens_input: 500     # varies by complexity
  query_tokens_output: 200    # varies by response length
  
Product_Complexity:
  product_catalog_size: 10000    # documents
  update_frequency: monthly      # how often catalog changes
  new_products_per_month: 50     # drives RAG vs fine-tune split
  
Team_Constraints:
  has_ml_engineer: false         # if true, labor costs drop 50%
  has_devops: false              # if true, ops costs drop 70%
  existing_infrastructure: none  # BYOD can save 30-50%
  
Accuracy_Requirements:
  acceptable_hallucination_rate: 0.05  # 5% = light requirements
  acceptable_staleness_days: 30        # product info ok if <30 days old
  sla_uptime: 0.99                     # 99% vs 99.99% = 5x cost difference
  
Technology_Choices:
  inference_model: phi3_mini     # changes hardware requirement
  inference_location: local      # vs cloud changes cost 5-10x
  vector_db: pinecone            # vs self-hosted changes 5-10x
  embedding_model: openai        # vs self-hosted changes cost
```

### The Template

```
Your Cost Baseline = (
  + (queries_per_month * avg_token_cost)     # LLM inference
  + vector_db_cost                           # retrieval storage
  + embedding_cost                           # query embedding
  + fine_tuning_cost * (updates_per_year)    # training
  + hardware_amortized_monthly               # GPU/infra
  + ops_labor_monthly                        # keeping it running
)

Then multiply by:
  * 0.5 if you have existing team
  * 0.7 if you're scrappy (self-host everything)
  * 2.0 if you need enterprise SLA
  * 3.0 if you need high accuracy (more validation)
```

---

## Conclusion: The Stated Numbers Are A Reference Point, Not A Prediction

**The key insights stand**:
- RAG-only is expensive due to cloud LLM inference costs
- Fine-tuning-only requires frequent expensive retraining to stay current
- Hybrid is cheaper overall BUT depends heavily on architecture decisions

**But the specific dollar amounts ($5,800 vs $1,500 vs $2,100) should be treated as:**
- ✅ Valid for mid-market company with 1M queries/month, no existing team
- ✅ Useful for relative comparison (RAG-only is 2.8x more expensive)
- ❌ Not valid for startups (scale is wrong)
- ❌ Not valid for enterprises (team allocation different)
- ❌ Not valid if you have different product update frequency
- ❌ Not valid if you already own infrastructure

**To build your own model**: Define your 10 key variables (scale, team, tech stack, accuracy requirements) and adjust accordingly. The architecture principles hold regardless of your numbers.
