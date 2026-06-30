import { Activity, Database, Network, Radar, ShieldCheck, Workflow, type LucideIcon } from 'lucide-react'
import { useEffect, useState } from 'react'
import { getHealth, type HealthCheck } from './api/health'
import { getModules, type ReconModule } from './api/modules'

function App() {
  const [health, setHealth] = useState<HealthCheck | null>(null)
  const [modules, setModules] = useState<ReconModule[]>([])
  const [isDegraded, setIsDegraded] = useState(false)

  useEffect(() => {
    let isMounted = true

    Promise.all([getHealth(), getModules()])
      .then(([healthResponse, moduleResponse]) => {
        if (isMounted) {
          setHealth(healthResponse)
          setModules(moduleResponse)
          setIsDegraded(false)
        }
      })
      .catch(() => {
        if (isMounted) {
          setIsDegraded(true)
        }
      })

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100">
      <header className="border-b border-zinc-800 bg-zinc-950/95">
        <div className="mx-auto flex min-h-16 w-full max-w-7xl items-center justify-between px-6">
          <div className="flex items-center gap-3">
            <div className="flex size-9 items-center justify-center rounded bg-emerald-500 text-zinc-950">
              <Radar size={21} strokeWidth={2.4} aria-hidden="true" />
            </div>
            <div>
              <h1 className="text-base font-semibold tracking-normal text-white">ReconForge</h1>
              <p className="text-xs text-zinc-400">Reconnaissance Operations Platform</p>
            </div>
          </div>
          <div className="flex items-center gap-2 rounded border border-zinc-800 px-3 py-2 text-sm">
            <span
              className={`size-2 rounded-full ${isDegraded ? 'bg-amber-400' : 'bg-emerald-400'}`}
              aria-hidden="true"
            />
            <span className="text-zinc-300">{isDegraded ? 'API degraded' : 'API online'}</span>
          </div>
        </div>
      </header>

      <section className="mx-auto grid w-full max-w-7xl gap-6 px-6 py-8 lg:grid-cols-[1.4fr_0.8fr]">
        <div className="rounded border border-zinc-800 bg-zinc-900 p-6">
          <div className="mb-8 flex items-center justify-between gap-4">
            <div>
              <h2 className="text-2xl font-semibold tracking-normal text-white">Operations Overview</h2>
              <p className="mt-2 max-w-2xl text-sm leading-6 text-zinc-400">
                Central command surface for assets, scans, reports, plugins, and intelligence workflows.
              </p>
            </div>
            <ShieldCheck className="hidden text-emerald-400 sm:block" size={32} aria-hidden="true" />
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <MetricCard icon={Network} label="Modules" value={String(modules.length)} />
            <MetricCard icon={Activity} label="Active Scans" value="0" />
            <MetricCard icon={Workflow} label="Pipelines" value="0" />
          </div>
        </div>

        <aside className="rounded border border-zinc-800 bg-zinc-900 p-6">
          <div className="flex items-center gap-3">
            <Database className="text-cyan-300" size={24} aria-hidden="true" />
            <h2 className="text-lg font-semibold tracking-normal text-white">System Health</h2>
          </div>
          <dl className="mt-6 space-y-4 text-sm">
            <HealthRow label="Service" value={health?.service ?? 'ReconForge'} />
            <HealthRow label="Version" value={health?.version ?? '0.1.0'} />
            <HealthRow label="Database" value={health?.checks.database ?? 'pending'} />
          </dl>
        </aside>
      </section>

      <section className="mx-auto grid w-full max-w-7xl gap-4 px-6 pb-8 md:grid-cols-2 xl:grid-cols-4">
        {(modules.length > 0 ? modules.slice(0, 8) : fallbackModules).map((module) => (
          <div key={module.key} className="rounded border border-zinc-800 bg-zinc-900 p-5">
            <div className="flex items-start justify-between gap-3">
              <h3 className="text-sm font-semibold text-white">{module.name}</h3>
              <span className="rounded border border-zinc-700 px-2 py-1 text-xs text-zinc-300">{module.status}</span>
            </div>
            <p className="mt-3 text-sm leading-6 text-zinc-400">{module.description}</p>
          </div>
        ))}
      </section>
    </main>
  )
}

const fallbackModules: ReconModule[] = [
  {
    key: 'dashboard',
    name: 'Dashboard',
    description: 'Operational overview for scan activity, risk priorities, and attack surface changes.',
    status: 'foundation',
    route: '/dashboard',
    worker_queues: [],
  },
  {
    key: 'asset_discovery',
    name: 'Asset Discovery',
    description: 'Discovers domains, subdomains, DNS records, ASN, CIDR, certificates, and third-party assets.',
    status: 'planned',
    route: '/assets/discovery',
    worker_queues: ['scan.discovery'],
  },
  {
    key: 'ai_risk_engine',
    name: 'AI Risk Engine',
    description: 'Scores interesting records and explains why they deserve investigation.',
    status: 'planned',
    route: '/risk',
    worker_queues: ['ai.enrichment'],
  },
  {
    key: 'reports',
    name: 'Reports',
    description: 'Generates professional JSON, CSV, HTML, and PDF reports.',
    status: 'planned',
    route: '/reports',
    worker_queues: ['reports.render'],
  },
]

type MetricCardProps = {
  icon: LucideIcon
  label: string
  value: string
}

function MetricCard({ icon: Icon, label, value }: MetricCardProps) {
  return (
    <div className="rounded border border-zinc-800 bg-zinc-950 p-5">
      <div className="flex items-center justify-between">
        <span className="text-sm text-zinc-400">{label}</span>
        <Icon className="text-emerald-300" size={20} aria-hidden="true" />
      </div>
      <div className="mt-5 text-3xl font-semibold text-white">{value}</div>
    </div>
  )
}

type HealthRowProps = {
  label: string
  value: string
}

function HealthRow({ label, value }: HealthRowProps) {
  return (
    <div className="flex items-center justify-between border-b border-zinc-800 pb-3 last:border-b-0 last:pb-0">
      <dt className="text-zinc-400">{label}</dt>
      <dd className="font-medium text-zinc-100">{value}</dd>
    </div>
  )
}

export default App
