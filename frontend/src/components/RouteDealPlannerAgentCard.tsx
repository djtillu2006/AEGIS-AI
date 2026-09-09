import React from 'react';
import { Route } from 'lucide-react';
import { AIAgentCard, AgentStatus } from './AIAgentCard';

interface RouteDealPlannerAgentCardProps {
  status: AgentStatus;
  lastAction: string;
  onClick?: () => void;
  selected?: boolean;
}

export const RouteDealPlannerAgentCard: React.FC<RouteDealPlannerAgentCardProps> = ({ status, lastAction, onClick, selected = false }) => (
  <button
    type="button"
    onClick={onClick}
    className={`w-full text-left rounded-sm transition-all ${selected ? 'ring-1 ring-[#4a90e2]/70' : 'ring-1 ring-transparent hover:ring-[#4a90e2]/30'}`}
  >
    <AIAgentCard icon={Route} name="Route & Deal Planner" role="Multimodal routing & carrier negotiation" status={status} lastAction={lastAction} />
  </button>
);
