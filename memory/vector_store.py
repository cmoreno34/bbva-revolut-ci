"""
RAG Memory System for CI Agent using ChromaDB.
4 collections: bbva_intel, revolut_intel, market_context, historical.
"""

from __future__ import annotations
import chromadb
from chromadb.config import Settings

# Persistent storage in .chroma/ (excluded from git)
DB_PATH = ".chroma"


def get_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=DB_PATH)


def get_or_create_collections(client: chromadb.PersistentClient) -> dict:
    """Get or create the 4 CI collections."""
    names = ["bbva_intel", "revolut_intel", "market_context", "historical"]
    return {
        name: client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
        for name in names
    }


# ── Seed Data ──────────────────────────────────────────────

BBVA_DOCS = [
    {
        "id": "bbva_revenue_2024",
        "text": "BBVA reported total revenue of EUR 27.4 billion in 2024, with net interest income of EUR 22.1 billion. Net attributable profit reached EUR 9.4 billion, up 25% year-on-year. The net interest margin (NIM) stood at 3.2%.",
        "source_url": "https://www.bbva.com/en/annual-report/",
        "date": "2025-02-14",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_digital_users",
        "text": "BBVA's mobile banking app reached 16 million active users in Spain by Q4 2024. Digital sales accounted for 78% of all consumer product sales, up from 72% in 2023. The bank processed 2.1 billion digital transactions.",
        "source_url": "https://www.bbva.com/en/annual-report/",
        "date": "2025-02-14",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_branches_spain",
        "text": "BBVA operates approximately 1,800 branches in Spain as of 2024, down from 2,400 in 2020. The bank sold 300 retail branches in May 2024 as part of its digital transformation strategy. The branch network is complemented by over 4,500 ATMs.",
        "source_url": "https://www.bbva.com/en/bbva-branch-atm-search/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_tech_investment",
        "text": "BBVA invested EUR 3.2 billion in technology in 2024, representing 11.7% of total revenue. Key investments included AI-driven credit scoring, cloud migration to AWS, and the BBVA Spark fintech platform for startups.",
        "source_url": "https://www.bbva.com/en/annual-report/",
        "date": "2025-02-14",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_customer_cost",
        "text": "BBVA's cost per retail customer in Spain is approximately EUR 250 per year, driven by branch operating costs (EUR 150), technology infrastructure (EUR 60), and regulatory compliance (EUR 40). The bank targets reducing this to EUR 180 by 2027.",
        "source_url": "https://www.bbva.com/en/investor-relations/",
        "date": "2025-02-14",
        "confidence": "MEDIUM",
    },
    {
        "id": "bbva_deposit_share",
        "text": "BBVA holds approximately 15% of retail deposits in Spain, making it the second-largest deposit holder after CaixaBank (24%). Total deposits in Spain reached EUR 180 billion in 2024.",
        "source_url": "https://www.bde.es/bde/en/areas/estadis/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_young_customers",
        "text": "BBVA's share among customers aged 18-35 in Spain declined from 18% in 2022 to 14% in 2024. The bank launched 'BBVA Aqua' digital card and fee-free accounts targeting this demographic, but uptake has been limited at 1.2 million users.",
        "source_url": "https://www.bbva.com/en/sustainability-report/",
        "date": "2025-03-01",
        "confidence": "MEDIUM",
    },
    {
        "id": "bbva_sabadell_bid",
        "text": "BBVA launched a hostile takeover bid for Banco Sabadell in May 2024 valued at EUR 12.2 billion. If successful, the combined entity would hold approximately 25% of Spanish deposits and become the largest bank in Spain by branch count.",
        "source_url": "https://www.reuters.com/business/finance/bbva-sabadell-merger/",
        "date": "2024-05-09",
        "confidence": "HIGH",
    },
    {
        "id": "bbva_strategy_2025",
        "text": "BBVA's 2025-2027 strategic plan focuses on: (1) Accelerating digital transformation with EUR 1B annual cloud investment, (2) Growing in high-growth markets (Turkey, Mexico, Colombia), (3) Defending Spanish retail market through improved UX and fee restructuring.",
        "source_url": "https://www.bbva.com/en/strategy/",
        "date": "2025-01-30",
        "confidence": "MEDIUM",
    },
    {
        "id": "bbva_app_rating",
        "text": "The BBVA Spain app has a 4.5/5 rating on the App Store (1.2M ratings) and 4.3/5 on Google Play (850K ratings). It was ranked #1 banking app in Spain by Forrester in 2023 and 2024, ahead of CaixaBank (4.2) and Santander (3.9).",
        "source_url": "https://www.forrester.com/report/european-digital-banking/",
        "date": "2024-09-15",
        "confidence": "HIGH",
    },
]

REVOLUT_DOCS = [
    {
        "id": "revolut_revenue_2024",
        "text": "Revolut reported revenue of GBP 3.1 billion (approximately EUR 3.6 billion) in 2024, a 72% increase year-on-year from GBP 1.8 billion in 2023. This marked the fourth consecutive year of profitability.",
        "source_url": "https://assets.revolut.com/pdf/annualreport2024.pdf",
        "date": "2025-04-22",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_profit_2024",
        "text": "Revolut achieved net profit of GBP 790 million in 2024, a 130% increase from GBP 344 million in 2023. Profit before tax was USD 1.4 billion. Net profit margin reached 26%.",
        "source_url": "https://assets.revolut.com/pdf/annualreport2024.pdf",
        "date": "2025-04-22",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_users_global",
        "text": "Revolut reached 52.5 million users globally by end of 2024, up 38% from 38 million in 2023. The company added 15 million users in a single year, driven by expansion in Southern and Eastern Europe.",
        "source_url": "https://www.businessofapps.com/data/revolut-statistics/",
        "date": "2025-01-15",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_spain_growth",
        "text": "Revolut's user base in Spain grew from 1.5 million to approximately 3.8 million in 2024, representing 200%+ growth. Spain became Revolut's 4th largest European market after UK, Poland, and Romania. The company targets 10 million Spanish users by 2027.",
        "source_url": "https://www.expansion.com/empresas/banca/2024/revolut-espana.html",
        "date": "2024-11-20",
        "confidence": "MEDIUM",
    },
    {
        "id": "revolut_eu_licence",
        "text": "Revolut obtained its specialized EU banking licence from the European Central Bank through the Bank of Lithuania in December 2018, which became fully operational in 2021. This allows Revolut to offer IBAN accounts, lending, and deposit protection across all EU member states.",
        "source_url": "https://www.lb.lt/en/news/revolut-receives-banking-licence",
        "date": "2021-12-13",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_uk_licence",
        "text": "Revolut received its full UK banking licence from the Prudential Regulation Authority (PRA) in March 2026, after initially getting a restricted licence in July 2024. This allows FSCS deposit protection up to GBP 120,000 for UK customers.",
        "source_url": "https://www.theguardian.com/business/2026/mar/11/revolut-full-banking-licence",
        "date": "2026-03-11",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_cost_advantage",
        "text": "Revolut's cost per customer is approximately EUR 30 per year, compared to EUR 250 for traditional banks like BBVA. This 8x cost advantage comes from zero branch costs, cloud-native infrastructure, and automated customer support (85% of queries handled by AI).",
        "source_url": "https://fintechmagazine.com/banking/revolut-cost-structure-analysis",
        "date": "2024-08-15",
        "confidence": "MEDIUM",
    },
    {
        "id": "revolut_products_spain",
        "text": "Revolut's product offering in Spain includes: multi-currency accounts, stock/crypto trading, savings vaults (3.5% APY), travel insurance, Junior accounts, and business accounts. Notably absent: mortgages, personal loans, and credit cards (planned for 2025).",
        "source_url": "https://www.revolut.com/en-ES/",
        "date": "2024-12-01",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_valuation",
        "text": "Revolut was valued at USD 45 billion in its 2024 secondary share sale, making it Europe's most valuable private fintech. Previous valuation was USD 33 billion in 2021 Series E round of USD 800 million.",
        "source_url": "https://www.ft.com/content/revolut-valuation-2024",
        "date": "2024-08-01",
        "confidence": "HIGH",
    },
    {
        "id": "revolut_hiring_spain",
        "text": "Revolut posted 45 job openings in Spain in Q4 2024, including: Head of Lending Spain, Compliance Officer Madrid, 12 software engineers, and 8 customer operations roles. The Madrid office expanded from 30 to 120 employees in 2024.",
        "source_url": "https://www.revolut.com/careers/",
        "date": "2024-12-15",
        "confidence": "MEDIUM",
    },
]

MARKET_DOCS = [
    {
        "id": "ecb_rates_2024",
        "text": "The ECB maintained its main refinancing rate at 3.65% through Q4 2024 after cutting from 4.5% in June 2024. Further rate cuts of 25bps are expected in 2025. Higher rates have benefited traditional banks' NIM but compressed neobank savings margins.",
        "source_url": "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "spain_banking_market",
        "text": "Spain's retail banking market holds EUR 1.2 trillion in deposits across 12 major banks. The market is highly concentrated: top 5 banks (CaixaBank, Santander, BBVA, Sabadell, Bankinter) control 72% of deposits. Average bank switching rate is 4% annually.",
        "source_url": "https://www.bde.es/bde/en/areas/estadis/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "spain_demographics_banking",
        "text": "Spain has 47.8 million inhabitants. 38% of the population (18.2M) is aged 18-45. Digital banking penetration reached 76% in 2024. Among 18-35 year olds, 92% use mobile banking. Neobank penetration among under-35s reached 34% in 2024, up from 18% in 2022.",
        "source_url": "https://www.ine.es/en/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "eu_fintech_regulation",
        "text": "The EU Digital Operational Resilience Act (DORA) came into force in January 2025, requiring all financial institutions (including fintechs) to meet strict IT security standards. PSD3 draft regulation proposes open banking extensions that could benefit neobanks.",
        "source_url": "https://finance.ec.europa.eu/regulation-and-supervision/financial-services-legislation/",
        "date": "2025-01-17",
        "confidence": "HIGH",
    },
    {
        "id": "neobank_eu_landscape",
        "text": "European neobanks collectively reached 120 million customers in 2024. Major players: Revolut (52.5M), N26 (8M), Monzo (9M), Starling (4M). Combined revenue of top 10 EU neobanks: EUR 8.5 billion. Only 3 of top 10 are consistently profitable.",
        "source_url": "https://www.mckinsey.com/industries/financial-services/our-insights/european-neobanks",
        "date": "2024-10-15",
        "confidence": "MEDIUM",
    },
    {
        "id": "spain_fx_remittances",
        "text": "Spain processes EUR 12 billion in outbound remittances annually, primarily to Latin America (Colombia, Ecuador, Morocco). Traditional banks charge 3-5% FX fees. Revolut charges 0.5-1%. This represents a EUR 360-600M annual fee pool that neobanks are capturing.",
        "source_url": "https://www.worldbank.org/en/topic/migrationremittancesdiasporaissues/",
        "date": "2024-06-30",
        "confidence": "MEDIUM",
    },
    {
        "id": "spanish_deposit_guarantee",
        "text": "Spain's Deposit Guarantee Fund (FGD) covers EUR 100,000 per depositor per institution. EU-licensed banks (including Revolut via Lithuania) provide EUR 100,000 coverage under their home country scheme. UK-licensed entities are not covered for Spanish depositors.",
        "source_url": "https://www.fgd.es/en/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "ai_banking_adoption",
        "text": "55% of European banks have deployed AI in customer-facing operations as of 2024. Use cases: fraud detection (89%), credit scoring (67%), chatbots (54%), personalized offers (41%). Neobanks lead with 85% AI adoption rate vs 45% for traditional banks.",
        "source_url": "https://www.eba.europa.eu/regulation-and-policy/model-validation/",
        "date": "2024-11-30",
        "confidence": "MEDIUM",
    },
    {
        "id": "branch_closure_trend",
        "text": "Spanish banks closed 4,200 branches between 2020-2024, a 22% reduction. Total branch count fell from 19,000 to 14,800. CaixaBank closed 1,500 branches post-Bankia merger. BBVA closed 600. Projections suggest 10,000 branches by 2028.",
        "source_url": "https://www.bde.es/bde/en/areas/estadis/",
        "date": "2024-12-31",
        "confidence": "HIGH",
    },
    {
        "id": "crypto_banking_eu",
        "text": "The EU Markets in Crypto-Assets Regulation (MiCA) took full effect in December 2024. Both Revolut and BBVA offer crypto trading. Revolut processes EUR 2.5 billion monthly crypto volume in the EU. BBVA's crypto service in Switzerland handles EUR 200 million monthly.",
        "source_url": "https://www.esma.europa.eu/policy-activities/digital-finance-and-innovation/markets-crypto-assets-regulation-mica",
        "date": "2024-12-30",
        "confidence": "MEDIUM",
    },
]

HISTORICAL_DOCS = [
    {
        "id": "ci_report_q3_2024",
        "text": "Q3 2024 CI Report: Revolut launched savings vaults in Spain at 3.5% APY, significantly above BBVA's 0.5% savings rate. Within 6 weeks, Revolut attracted EUR 500M in Spanish deposits. BBVA responded by raising its savings rate to 1.2% for new customers under 30.",
        "source_url": "internal://ci-reports/q3-2024",
        "date": "2024-10-15",
        "confidence": "HIGH",
    },
    {
        "id": "ci_report_q2_2024",
        "text": "Q2 2024 CI Report: Revolut obtained its specialized EU banking licence through Lithuania, enabling deposit protection for Spanish customers. This removed a key trust barrier. BBVA's competitive position assessment: Revolut AMC scores increased from A3/M4/C2 to A4/M5/C3.",
        "source_url": "internal://ci-reports/q2-2024",
        "date": "2024-07-15",
        "confidence": "HIGH",
    },
]


def seed_collections(collections: dict) -> dict:
    """Seed all collections with CI data. Returns counts per collection."""
    data_map = {
        "bbva_intel": BBVA_DOCS,
        "revolut_intel": REVOLUT_DOCS,
        "market_context": MARKET_DOCS,
        "historical": HISTORICAL_DOCS,
    }
    counts = {}
    for name, docs in data_map.items():
        coll = collections[name]
        existing = coll.count()
        if existing >= len(docs):
            counts[name] = existing
            continue
        coll.upsert(
            ids=[d["id"] for d in docs],
            documents=[d["text"] for d in docs],
            metadatas=[
                {
                    "source_url": d["source_url"],
                    "date": d["date"],
                    "confidence": d["confidence"],
                }
                for d in docs
            ],
        )
        counts[name] = coll.count()
    return counts


def query_collection(
    collection_name: str,
    query_text: str,
    n_results: int = 5,
    client: chromadb.PersistentClient | None = None,
) -> list[dict]:
    """
    Query a collection and return top-N results with metadata.

    Returns list of dicts with: text, source_url, date, confidence, distance.
    """
    if client is None:
        client = get_client()
    coll = client.get_collection(collection_name)
    results = coll.query(query_texts=[query_text], n_results=n_results)

    output = []
    for i in range(len(results["ids"][0])):
        output.append(
            {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "source_url": results["metadatas"][0][i].get("source_url", ""),
                "date": results["metadatas"][0][i].get("date", ""),
                "confidence": results["metadatas"][0][i].get("confidence", ""),
                "distance": results["distances"][0][i] if results["distances"] else None,
            }
        )
    return output


def query_all(query_text: str, n_results: int = 3) -> list[dict]:
    """Query all 4 collections and return combined results ranked by relevance."""
    client = get_client()
    all_results = []
    for name in ["bbva_intel", "revolut_intel", "market_context", "historical"]:
        try:
            results = query_collection(name, query_text, n_results=n_results, client=client)
            for r in results:
                r["collection"] = name
            all_results.extend(results)
        except Exception:
            continue
    all_results.sort(key=lambda x: x.get("distance", 999))
    return all_results


# ── CLI ────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Initializing ChromaDB RAG system...")
    client = get_client()
    collections = get_or_create_collections(client)
    counts = seed_collections(collections)

    print("\nCollection counts:")
    for name, count in counts.items():
        print(f"  {name}: {count} documents")

    # Test queries
    test_queries = [
        ("bbva_intel", "BBVA digital banking strategy"),
        ("revolut_intel", "Revolut growth in Spain"),
        ("market_context", "EU banking regulation fintech"),
        ("bbva_intel", "BBVA cost per customer branch network"),
    ]

    for coll_name, query in test_queries:
        print(f"\n{'='*60}")
        print(f"  Query: '{query}' (collection: {coll_name})")
        print(f"{'='*60}")
        results = query_collection(coll_name, query, n_results=3, client=client)
        for i, r in enumerate(results, 1):
            print(f"\n  #{i} [{r['confidence']}] (distance: {r['distance']:.4f})")
            print(f"  {r['text'][:150]}...")
            print(f"  Source: {r['source_url']}")
            print(f"  Date: {r['date']}")

    # Test cross-collection query
    print(f"\n{'='*60}")
    print(f"  CROSS-COLLECTION: 'Revolut threat to BBVA Spain'")
    print(f"{'='*60}")
    results = query_all("Revolut threat to BBVA Spain", n_results=2)
    for i, r in enumerate(results, 1):
        print(f"\n  #{i} [{r['collection']}] [{r['confidence']}] (dist: {r['distance']:.4f})")
        print(f"  {r['text'][:150]}...")
