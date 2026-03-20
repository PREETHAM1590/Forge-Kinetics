import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function ProjectsIndexPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="Project Quest Board"
			subtitle="Track active runs, pending approvals, and completed launches across all Forge squads."
			kicker="Projects"
			primaryCta="Create Project"
			secondaryCta="Open HITL Queue"
			metrics={[
				{ label: "Active Projects", value: "12" },
				{ label: "Awaiting HITL", value: "03" },
				{ label: "Completed This Week", value: "09" },
				{ label: "Credits Burned", value: "2,180" },
			]}
			cards={[
				{
					title: "Hyperlane Commerce",
					description: "Frontend polish in progress. Build logs healthy and deployment checks green.",
					tags: ["In Progress", "Frontend", "Low Risk"],
				},
				{
					title: "Nova CRM Portal",
					description: "Pipeline paused at HITL gate pending approval on security diff.",
					tags: ["HITL Pending", "Security", "Med Risk"],
				},
				{
					title: "Flux Inventory",
					description: "Deployment completed. Success report and handoff package available.",
					tags: ["Completed", "Report Ready"],
				},
			]}
		/>
	);
}
