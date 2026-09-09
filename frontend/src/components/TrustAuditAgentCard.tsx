import React from 'react';
import { ShieldCheck } from 'lucide-react';
import { AIAgentCard, AgentStatus } from './AIAgentCard';

interface TrustAuditAgentCardProps {
  status: AgentStatus;
  lastAction: string;
  onClick?: () => void;
  selected?: boolean;
  requiresApproval?: boolean;
}

export const TrustAuditAgentCard: React.FC<TrustAuditAgentCardProps> = ({ status, lastAction, onClick, selected = false, requiresApproval = false }) => (
  <button
    type="button"
    onClick={onClick}
    className={`w-full text-left rounded-sm transition-all ${selected ? 'ring-1 ring-[#c9a227]/70' : 'ring-1 ring-transparent hover:ring-[#c9a227]/30'}`}
  >
    <AIAgentCard icon={ShieldCheck} name="Trust & Audit" role="Decision guardrails & audit logging" status={status} lastAction={lastAction} statusBadge={requiresApproval ? 'REQUIRES APPROVAL' : undefined} statusBadgeColor={requiresApproval ? '#f5a623' : undefined} />
  </button>
);
