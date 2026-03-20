import { ForgeScreen } from "../../../../../components/layout/forge-screen";

export default function ProjectHitlPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="Human-In-The-Loop Gate"
			subtitle="Review proposed changes, inspect risks, and approve or reject execution with complete auditability."
			kicker="HITL Gate"
			primaryCta="Approve Execution"
			secondaryCta="Reject & Annotate"
			metrics={[
				{ label: "Risk Score", value: "0.27" },
				{ label: "Files Changed", value: "14" },
				{ label: "Build Health", value: "Passing" },
				{ label: "Decision SLA", value: "18m" },
			]}
			cards={[
				{
					title: "Diff Summary",
					description: "Grouped patch review by area: UI, API, validation, and infra adjustments.",
					tags: ["Patch", "Risk Scoped"],
				},
				{
					title: "Execution Notes",
					description: "Agent rationale, assumptions, and fallback strategy for failed deployment checks.",
					tags: ["Explainability"],
				},
				{
					title: "Approval Controls",
					description: "Decision logging with approver identity and signed gate token metadata.",
					tags: ["Tokenized", "Audited"],
				},
			]}
		/>
	);
}
