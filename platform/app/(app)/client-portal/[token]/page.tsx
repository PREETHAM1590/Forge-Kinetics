import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function ClientPortalTokenPage() {
	return (
		<ForgeScreen
			section="Quests"
			title="Client Portal Access"
			subtitle="View approved deliverables, deployment links, and project status snapshots through secure token access."
			kicker="Client Portal"
			primaryCta="Open Report"
			secondaryCta="Download Handoff"
			metrics={[
				{ label: "Portal Status", value: "Active" },
				{ label: "Shared Artifacts", value: "17" },
				{ label: "Last Update", value: "5m ago" },
				{ label: "Token TTL", value: "24h" },
			]}
			cards={[
				{
					title: "Deployment Overview",
					description: "Production URL, commit details, and post-launch checklist status.",
					tags: ["Live", "Verified"],
				},
				{
					title: "Approval Timeline",
					description: "Chronological record of all HITL approvals and release decisions.",
					tags: ["Audit Trail"],
				},
				{
					title: "Asset Package",
					description: "Download code bundle, summaries, and release notes for stakeholder review.",
					tags: ["Export", "Handoff"],
				},
			]}
		/>
	);
}
