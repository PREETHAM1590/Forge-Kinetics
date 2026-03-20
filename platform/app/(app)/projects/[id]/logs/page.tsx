import { ForgeScreen } from "../../../../../components/layout/forge-screen";

export default function ProjectLogsPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="Execution Logs Observatory"
			subtitle="Stream structured logs from sandbox runs, validation layers, and deployment checkpoints."
			kicker="Project Logs"
			primaryCta="Tail Live Stream"
			secondaryCta="Export Logs"
			metrics={[
				{ label: "Active Streams", value: "04" },
				{ label: "Warnings", value: "02" },
				{ label: "Errors", value: "00" },
				{ label: "Retention", value: "30d" },
			]}
			cards={[
				{
					title: "Agent Runtime",
					description: "Observe think-act cycles, retries, and checkpoint intervals in sequence.",
					tags: ["Runtime", "Loop"],
				},
				{
					title: "Validation Layer",
					description: "Pydantic schema events with pass/fail traces and corrective retries.",
					tags: ["Schema", "Quality Gate"],
				},
				{
					title: "Deploy Channel",
					description: "Build/deploy timeline with approval gate timestamps and release markers.",
					tags: ["Deploy", "Audit"],
				},
			]}
		/>
	);
}
