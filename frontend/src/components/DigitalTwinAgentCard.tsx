import React from 'react';
import { BrainCircuit } from 'lucide-react';
import { AIAgentCard, AgentStatus } from './AIAgentCard';

interface DigitalTwinAgentCardProps {
  status: AgentStatus;
  lastAction: string;
  onClick?: () => void;
  selected?: boolean;
}

export const DigitalTwinAgentCard: React.FC<DigitalTwinAgentCardProps> = ({ status, lastAction, onClick, selected = false }) => (
  <button
    type="button"
    onClick={onClick}
    className={`w-full text-left rounded-sm transition-all ${selected ? 'ring-1 ring-[#4a90e2]/70' : 'ring-1 ring-transparent hover:ring-[#4a90e2]/30'}`}
  >
    <AIAgentCard icon={BrainCircuit} name="Digital Twin" role="Live supply-chain simulation" status={status} lastAction={lastAction} />
  </button>
);
