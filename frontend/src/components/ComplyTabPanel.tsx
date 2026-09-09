import React from 'react';
import { CheckCircle2, FileCheck2, Leaf, TriangleAlert } from 'lucide-react';
import { MOCK_AGENT_DATA } from '../data/mockAgentData';

export const ComplyTabPanel: React.FC = () => {
  const { comply } = MOCK_AGENT_DATA;
  return (
    <div className="space-y-3">
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><Leaf className="h-3.5 w-3.5 text-[#5a9a7a]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Carbon Footprint</h3></div>
        <p className="text-[10px] leading-relaxed text-white/60">{comply.emissions}</p>
      </section>
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><FileCheck2 className="h-3.5 w-3.5 text-[#4a90e2]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Regulatory Check</h3></div>
        <div className="space-y-1.5">{comply.regulations.map((regulation) => { const passed = regulation.status === 'PASS'; return <div key={regulation.name} className="flex items-center justify-between text-[10px] text-white/60"><span>{regulation.name}</span>{passed ? <CheckCircle2 className="h-3 w-3 text-[#5a9a7a]" /> : <TriangleAlert className="h-3 w-3 text-[#f5a623]" />}</div>; })}</div>
      </section>
      <section className="rounded-sm border border-[#1a2332] bg-[#0f1621] p-3">
        <div className="mb-2 flex items-center gap-2"><CheckCircle2 className="h-3.5 w-3.5 text-[#5a9a7a]" /><h3 className="text-xs font-semibold uppercase tracking-wider text-white/70">Company Policy</h3></div>
        <p className="text-[10px] text-[#5a9a7a]">{comply.policy}</p>
      </section>
    </div>
  );
};
