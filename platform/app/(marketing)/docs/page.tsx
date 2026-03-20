import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function DocsPage() {
	return (
		<ForgeScreen
			section="Lab"
			title="Forge Documentation Hub"
			subtitle="Architecture, constraints, stage guides, and integration references for the full Forge pipeline."
			kicker="Docs"
			primaryCta="Read Quickstart"
			secondaryCta="Open API Contracts"
			metrics={[
				{ label: "Guides", value: "42" },
				{ label: "API References", value: "18" },
				{ label: "Skills Indexed", value: "11" },
				{ label: "Last Updated", value: "Today" },
			]}
			cards={[
				{
					title: "Core Loop",
					description: "State, graph flow, PM/Architect handoff, and build-phase orchestration details.",
					tags: ["LangGraph", "ForgeState"],
				},
				{
					title: "Hard Constraints",
					description: "Mandatory HITL, per-agent sandboxing, and credit controls with compliance notes.",
					tags: ["C1-C14", "Compliance"],
				},
				{
					title: "Skill Library",
					description: "Curated playbooks for auth, data CRUD, Stripe, testing, and deployment.",
					tags: ["Skills", "Phase 1"],
				},
			]}
		/>
	);
}
