# BBVA vs Revolut: Agentic CI System

## Project Context
This project builds an agentic CI system for analyzing
Revolut's competitive threat to BBVA in European retail
banking. The system implements these CI frameworks:

## 1. AMC Framework (Awareness-Motivation-Capability)
For each competitor, score three dimensions (1-5):
- AWARENESS: CI function quality, market monitoring
  capability, information systems
- MOTIVATION: Market importance, revenue at stake,
  strategic priority, executive incentives
- CAPABILITY: Financial resources, tech talent,
  organizational agility, regulatory position

Response Probability = A x M x C (normalized to %)

## 2. Exchange Value Methodology
EV = Reference Value + Differential Value
- Reference Value: outcome if BBVA takes no action
- Differential Value: change vs reference per scenario

Each scenario needs probability + economic outcome

## 3. ECOMO Cost-Benefit Model
For each strategic option calculate:
- Development Costs (one-time investment)
- Operating Costs (annual recurring)
- Opportunity Costs (foregone alternatives)
- Monetary Value (revenue, cost savings)
- Psychological Value (brand, learning, positioning)

NPV at 10% discount rate over 5 years
Expected Value = Sum(Probability x NPV) per scenario

## 4. Anti-Hallucination Rules
- Every claim must cite a source URL or document
- Confidence: HIGH (2+ sources), MEDIUM (1 source),
  LOW (inference), UNCERTAIN (conflicting)
- Never fabricate data - state uncertainty explicitly

## 5. Case Data: BBVA vs Revolut
- BBVA: Revenue EUR 27.4B, NIM 3.2%, 80M customers
  Cost/customer ~EUR 250/yr, 15% Spanish deposits
- Revolut: Revenue EUR 2.2B, 45M customers growing
  200% YoY in Spain, cost/customer ~EUR 30/yr
  EU banking licence since 2021 (Lithuania)
- Key tension: Revolut targets BBVA's young customers
  (18-35) with better FX, lower fees, better UX

## Tech Stack
- Python 3.11+ with anthropic SDK
- React frontend with Tailwind CSS
- Deploy: GitHub Pages (frontend) + Google Cloud Run
  (API backend)
