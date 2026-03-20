import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function HitlDashboardPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="Kinetic Workspace"
			subtitle="Monitor pipeline graph, token burn, and Human-In-The-Loop gate decisions for active project runs."
			kicker="HITL Dashboard & Graph"
			primaryCta="Approve"
			secondaryCta="Reject"
			metrics={[
				{ label: "Token Burn Rate", value: "14.2k / min" },
				{ label: "Est. Session Cost", value: "$34.12" },
				{ label: "Pipeline State", value: "Awaiting HITL" },
				{ label: "Build Node", value: "Logic-Core-A1" },
			]}
			cards={[
				{
					title: "Pipeline Graph",
					description:
						"Ingest → Logic Core → HITL Gate sequence with live edge and node status updates.",
					tags: ["Live Graph", "Stage Health"],
				},
				{
					title: "Approval Pane",
					description:
						"Review proposed patches, risk metadata, and execution notes before final decision.",
					tags: ["Diff Review", "Human Gate"],
				},
				{
					title: "Build Terminal",
					description:
						"Streaming logs show gate trigger events and waiting state until operator action.",
					tags: ["Realtime", "Auditable"],
				},
			]}
		/>
	);
}

