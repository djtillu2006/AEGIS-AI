import React from 'react';
import { AlertTriangle, CheckCircle2, DollarSign, ShieldCheck } from 'lucide-react';
import { MOCK_AGENT_DATA } from '../data/mockAgentData';

interface RiskTabPanelProps {
  selectedRoute?: { name: string; distance: number; estimatedTime: number; riskLevel: string } | null;
}

export const RiskTabPanel: React.FC<RiskTabPanelProps> = ({ selectedRoute }) => {
  const { risk } = MOCK_AGENT_DATA;
  const routeName = selectedRoute?.name || risk.route;
  const routeDistance = selectedRoute ? `${selectedRoute.distance.toLocaleString()} nm` : risk.distance;
  const routeDuration = selectedRoute ? `~${selectedRoute.estimatedTime}d` : risk.duration;
  const routeRisk = selectedRoute?.riskLevel?.toUpperCase() || risk.riskLevel;
  return (
    <div className="space-y-3">
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><AlertTriangle className="h-3.5 w-3.5 text-[#c94444]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Active Route Risk</h3></div>
        <p className="text-xs font-medium text-white/80">{routeName}</p>
        <div className="mt-2 flex items-center gap-3 text-[10px] text-white/50"><span>{routeDistance}</span><span>{routeDuration}</span><span className="font-bold text-[#c94444]">{routeRisk} RISK</span></div>
      </section>
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><DollarSign className="h-3.5 w-3.5 text-[#10b981]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Financial Exposure</h3></div>
        <div className="grid grid-cols-2 gap-2 text-[10px]"><div><span className="block text-white/40">Fuel delta</span><strong className="text-[#f5a623]">{risk.fuelCostDelta}</strong></div><div><span className="block text-white/40">Freight volatility</span><strong className="text-white/80">{risk.freightVolatility}</strong></div></div>
        <p className="mt-2 text-[10px] leading-relaxed text-white/55">{risk.hedgeRecommendation}</p>
      </section>
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><ShieldCheck className="h-3.5 w-3.5 text-[#c9a227]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Guardrail Status</h3></div>
        <div className="space-y-1.5">{risk.guardrails.map((guardrail) => <div key={guardrail.label} className="flex items-center justify-between text-[10px] text-white/60"><span>{guardrail.label}</span><CheckCircle2 className="h-3 w-3 text-[#5a9a7a]" /></div>)}</div>
        <p className="mt-2 border-t border-white/10 pt-2 text-[10px] text-white/50">Hallucination risk: <span className="text-[#5a9a7a]">{risk.hallucinationRisk}</span></p>
      </section>
    </div>
  );
};
