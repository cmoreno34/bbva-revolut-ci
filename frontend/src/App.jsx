import { useState } from 'react'

const EXERCISES = [
  { id: 1, name: 'Environment Setup', tn: 'TN10 Ex.1', status: 'done', desc: 'Python env with anthropic, chromadb, langchain, fastapi' },
  { id: 2, name: 'ReAct Loop Agent', tn: 'TN10 Ex.2', status: 'done', desc: 'Think-Act-Observe cycle with web search and source citations' },
  { id: 3, name: 'RAG with ChromaDB', tn: 'TN10 Ex.3', status: 'pending', desc: '4 collections: bbva_intel, revolut_intel, market_context, historical' },
  { id: 4, name: 'Collector + AMC Analyst', tn: 'TN10 Ex.4', status: 'pending', desc: 'OSINT Collector feeds AMC scoring agent' },
  { id: 5, name: 'Full 5-Agent Pipeline', tn: 'TN10 Ex.5', status: 'pending', desc: 'Scenario Planner + ECOMO + Reporter' },
  { id: 6, name: 'Competitor Monitor', tn: 'TN10 Ex.6', status: 'pending', desc: 'Track Revolut pricing, products, hiring' },
  { id: 7, name: 'Confidence Scoring', tn: 'TN11 Ex.1', status: 'pending', desc: 'HIGH/MEDIUM/LOW/UNCERTAIN classification' },
  { id: 8, name: 'LangGraph + HITL', tn: 'TN11 Ex.2', status: 'pending', desc: 'Stateful orchestration with human checkpoints' },
  { id: 9, name: 'Anti-Hallucination Tests', tn: 'TN11 Ex.3', status: 'pending', desc: '20 test cases: 10 real + 10 fabricated' },
  { id: 10, name: 'War Gaming Simulation', tn: 'TN11 Ex.5', status: 'pending', desc: 'Red Team (Revolut) vs Blue Team (BBVA)' },
]

const CASE_DATA = {
  bbva: { name: 'BBVA', revenue: '27.4B', customers: '80M', costPerCustomer: '250', marketShare: '15%', founded: 1857 },
  revolut: { name: 'Revolut', revenue: '3.1B (2024)', customers: '52.5M', costPerCustomer: '30', marketShare: '<1% Spain', founded: 2015 },
}

const REACT_DEMO = {
  question: 'What is Revolut revenue 2024?',
  cycles: 5,
  answer: 'Revolut revenue for 2024 was GBP 3.1 billion (~$4B USD), a 72% increase YoY. Net profit: GBP 790M.',
  sources: [
    { title: 'Revolut Official Annual Report 2024', url: 'https://assets.revolut.com/pdf/annualreport2024.pdf' },
    { title: 'FinTech Futures', url: 'https://www.fintechfutures.com/digital-banking/revolut-scores-1.4bn-profit' },
    { title: 'Business of Apps', url: 'https://www.businessofapps.com/data/revolut-statistics/' },
  ],
  confidence: 'HIGH',
}

const tabs = ['Overview', 'OSINT Data', 'AMC Analysis', 'Scenarios', 'ECOMO', 'Executive Brief', 'Confidence Map']

function StatusBadge({ status }) {
  const colors = {
    done: 'bg-green-100 text-green-800 border-green-300',
    pending: 'bg-gray-100 text-gray-500 border-gray-300',
    running: 'bg-blue-100 text-blue-800 border-blue-300',
  }
  return (
    <span className={`px-2 py-0.5 rounded-full text-xs font-medium border ${colors[status]}`}>
      {status === 'done' ? 'DONE' : status === 'running' ? 'RUNNING' : 'PENDING'}
    </span>
  )
}

function OverviewTab() {
  const done = EXERCISES.filter(e => e.status === 'done').length
  const total = EXERCISES.length
  const pct = Math.round((done / total) * 100)

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Pipeline Progress</h3>
        <div className="w-full bg-gray-200 rounded-full h-4 mb-2">
          <div className="bg-blue-600 h-4 rounded-full transition-all" style={{ width: `${pct}%` }}></div>
        </div>
        <p className="text-sm text-gray-600">{done}/{total} exercises complete ({pct}%)</p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">The Case: BBVA vs Revolut</h3>
        <p className="text-gray-600 mb-4">
          You are a CI analyst at BBVA. Revolut has obtained its EU banking licence and is aggressively
          expanding into Spain. The CEO wants answers to three strategic questions:
        </p>
        <ol className="list-decimal list-inside space-y-2 text-gray-700">
          <li>How serious is Revolut's threat to BBVA's retail banking in Spain?</li>
          <li>Should BBVA launch a digital product, acquire a neobank, or defend through pricing?</li>
          <li>What is the expected economic value of each option over 5 years?</li>
        </ol>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Competitive Landscape</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b-2 border-gray-200">
                <th className="text-left py-2 px-3 text-gray-600">Dimension</th>
                <th className="text-left py-2 px-3 text-blue-700">BBVA</th>
                <th className="text-left py-2 px-3 text-purple-700">Revolut</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {[
                ['Founded', CASE_DATA.bbva.founded, CASE_DATA.revolut.founded],
                ['Revenue (EUR)', CASE_DATA.bbva.revenue, CASE_DATA.revolut.revenue],
                ['Customers', CASE_DATA.bbva.customers, CASE_DATA.revolut.customers],
                ['Cost/Customer', `EUR ${CASE_DATA.bbva.costPerCustomer}/yr`, `EUR ${CASE_DATA.revolut.costPerCustomer}/yr`],
                ['Spanish Market', CASE_DATA.bbva.marketShare, CASE_DATA.revolut.marketShare],
              ].map(([dim, bbva, rev]) => (
                <tr key={dim}>
                  <td className="py-2 px-3 font-medium text-gray-700">{dim}</td>
                  <td className="py-2 px-3 text-gray-600">{bbva}</td>
                  <td className="py-2 px-3 text-gray-600">{rev}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Exercises</h3>
        <div className="space-y-3">
          {EXERCISES.map(ex => (
            <div key={ex.id} className={`flex items-center justify-between p-3 rounded-lg border ${ex.status === 'done' ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
              <div className="flex items-center gap-3">
                <span className="text-lg font-mono text-gray-400 w-6">#{ex.id}</span>
                <div>
                  <p className="font-medium text-gray-800">{ex.name} <span className="text-xs text-gray-400 ml-1">{ex.tn}</span></p>
                  <p className="text-xs text-gray-500">{ex.desc}</p>
                </div>
              </div>
              <StatusBadge status={ex.status} />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function OSINTTab() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">ReAct Loop Demo</h3>
        <p className="text-sm text-gray-500 mb-4">Exercise 2: Think &gt; Act &gt; Observe cycle with live web search</p>

        <div className="bg-gray-900 rounded-lg p-4 text-sm font-mono text-green-400 space-y-2 mb-4 overflow-x-auto">
          <p className="text-gray-400"># Question: {REACT_DEMO.question}</p>
          <p><span className="text-yellow-400">[THINK]</span> I need to search for Revolut 2024 revenue data...</p>
          <p><span className="text-blue-400">[ACT]</span> web_search("Revolut revenue 2024 financial results")</p>
          <p><span className="text-cyan-400">[OBSERVE]</span> Got 5 results from DuckDuckGo</p>
          <p><span className="text-yellow-400">[THINK]</span> Found GBP 3.1B from official annual report. Verifying...</p>
          <p><span className="text-blue-400">[ACT]</span> web_search("Revolut annual report 2024 revenue profit")</p>
          <p><span className="text-cyan-400">[OBSERVE]</span> Confirmed by FinTech Futures + Business of Apps</p>
          <p><span className="text-green-400">[FINAL]</span> Answer ready after {REACT_DEMO.cycles} cycles</p>
        </div>

        <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
          <p className="font-medium text-blue-900 mb-2">Answer:</p>
          <p className="text-blue-800">{REACT_DEMO.answer}</p>
          <p className="mt-2">
            <span className="px-2 py-0.5 rounded text-xs font-bold bg-green-200 text-green-800">
              Confidence: {REACT_DEMO.confidence}
            </span>
          </p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Sources Collected</h3>
        <div className="space-y-2">
          {REACT_DEMO.sources.map((s, i) => (
            <div key={i} className="flex items-start gap-2 p-2 rounded bg-gray-50">
              <span className="text-green-500 mt-0.5">&#10003;</span>
              <div>
                <p className="text-sm font-medium text-gray-800">{s.title}</p>
                <a href={s.url} target="_blank" rel="noreferrer" className="text-xs text-blue-600 hover:underline break-all">{s.url}</a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function PlaceholderTab({ name }) {
  return (
    <div className="bg-white rounded-lg shadow p-12 text-center">
      <div className="text-6xl mb-4">&#128679;</div>
      <h3 className="text-xl font-semibold text-gray-400 mb-2">{name}</h3>
      <p className="text-gray-400">This section will be populated as more exercises are completed.</p>
    </div>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-gradient-to-r from-blue-800 to-purple-800 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
            <div>
              <h1 className="text-2xl font-bold">BBVA vs Revolut: Agentic CI System</h1>
              <p className="text-blue-200 text-sm mt-1">Corporate Intelligence Course &middot; Universidad Francisco de Vitoria</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-blue-200">Prof. Cesar Moreno Pascual PhD</p>
              <p className="text-xs text-blue-300">2025-2026 Academic Year</p>
            </div>
          </div>
        </div>
      </header>

      <nav className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex gap-1 overflow-x-auto py-1">
            {tabs.map((tab, i) => (
              <button
                key={tab}
                onClick={() => setActiveTab(i)}
                className={`px-4 py-2 text-sm font-medium rounded-t-lg whitespace-nowrap transition-colors cursor-pointer ${
                  activeTab === i
                    ? 'bg-blue-50 text-blue-700 border-b-2 border-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-4 py-6">
        {activeTab === 0 && <OverviewTab />}
        {activeTab === 1 && <OSINTTab />}
        {activeTab === 2 && <PlaceholderTab name="AMC Analysis" />}
        {activeTab === 3 && <PlaceholderTab name="Scenarios" />}
        {activeTab === 4 && <PlaceholderTab name="ECOMO Cost-Benefit" />}
        {activeTab === 5 && <PlaceholderTab name="Executive Brief" />}
        {activeTab === 6 && <PlaceholderTab name="Confidence Map" />}
      </main>

      <footer className="bg-gray-800 text-gray-400 text-xs text-center py-4 mt-12">
        Built with Claude Code + Anthropic API &middot; Deployed on GitHub Pages
      </footer>
    </div>
  )
}

export default App
