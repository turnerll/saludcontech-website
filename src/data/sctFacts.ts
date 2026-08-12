import raw from '../../data/facts.json';

export interface Fact {
  id: string;
  value: number;
  unit: string;
  universe: string;
  curated?: boolean;
  note?: string;
  entity: { en: string; es: string };
  source_org: string;
  source_title: string;
  source_url: string;
  as_of: string;
  review_by: string;
  verified?: boolean;
}

const byId = new Map<string, Fact>((raw.facts as Fact[]).map((f) => [f.id, f]));

export function fact(id: string): Fact {
  const f = byId.get(id);
  if (!f) {
    throw new Error(
      `facts.json does not know the id "${id}". Known ids: ${[...byId.keys()].join(', ')}`,
    );
  }
  return f;
}

// Approved hard-coded figures for visualizations. These are directionally accurate
// public research figures the design brief explicitly approved for viz use.
export const approvedViz = {
  latinoGdpTrillions: 4.1,
  latinoPopulation2045Pct: 25,
  latinoFounderVcSharePct: 2,
  latinoVcProfessionalsPct: 2,
};

export const SCT_FACTS = {
  founded: fact('sct.founded_year'),
  members: fact('sct.total_members'),
  slackMembers: fact('sct.slack_members'),
  slackMessages: fact('sct.slack_messages'),
  cityChapters: fact('sct.city_channels'),
  himss25: fact('sct.himss25_collaborator'),
  latinoGdp: fact('latino_gdp.value_2025'),
  latinoBusinessRevenue: fact('latino_owned_businesses.annual_revenue'),
  vcShare: fact('vc.latino_founder_funding_share'),
  approved: approvedViz,
};
