export type DemoAgentStatus = 'idle' | 'thinking' | 'completed' | 'alert';

export const MOCK_AGENT_DATA = {
  digitalTwin: {
    name: 'Digital Twin',
    role: 'Live supply-chain simulation',
    result: '3 scenarios simulated. Best option: Reroute via Cape of Good Hope (+4.2 days, +$180K fuel, -12% risk).',
  },
  routeDealPlanner: {
    name: 'Route & Deal Planner',
    role: 'Multimodal routing & carrier negotiation',
    result: 'New route drafted: Sea->Cape route. 3 carrier quotes compared. Best offer: Maersk, $412K, ETA 32 days.',
  },
  trustAudit: {
    name: 'Trust & Audit',
    role: 'Decision guardrails & audit logging',
    result: 'All guardrails passed. Hallucination risk: 0.08 (low). Audit log #AEGIS-20260907-0143 recorded.',
    requiresApproval: false,
  },
  risk: {
    route: 'Shanghai -> Rotterdam via Cape of Good Hope',
    distance: '4,578 nm',
    duration: '~9.5d',
    riskLevel: 'HIGH',
    fuelCostDelta: '+$180K',
    freightVolatility: '18.4%',
    hedgeRecommendation: 'Hedge 60% of fuel exposure; review freight cover daily.',
    guardrails: [
      { label: 'Cost increase <= 25%', passed: true },
      { label: 'Carbon increase <= 20%', passed: true },
      { label: 'Regulatory compliance', passed: true },
    ],
    hallucinationRisk: '0.08 (low)',
  },
  comply: {
    emissions: 'Estimated emissions: 84.2 tons CO2 (Cape route) vs 71.5 tons CO2 (original Suez route)',
    regulations: [
      { name: 'EU CSRD', status: 'PASS' as const },
      { name: 'CBAM', status: 'REVIEW' as const },
      { name: 'Digital Product Passport', status: 'PASS' as const },
    ],
    policy: 'Max carbon per shipment: 90 tons - PASS',
  },
} as const;

export const FULL_DEMO_AGENT_ORDER = [
  'market_sentinel',
  'digital_twin',
  'route_deal_planner',
  'risk_hedger',
  'trust_audit',
] as const;
