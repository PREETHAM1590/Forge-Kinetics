import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function DashboardPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="Forge Office"
			subtitle="2D RPG-inspired workspace to monitor agent output, traits, and team performance."
			kicker="Agent Command Room"
			primaryCta="Start New Project"
			secondaryCta="Inspect Agent"
			metrics={[
				{ label: "Office Efficiency", value: "94.2%" },
				{ label: "Active Agents", value: "18/25" },
				{ label: "Working", value: "12" },
				{ label: "Idle", value: "6" },
			]}
			cards={[
				{
					title: "Data Smith",
					description: "Lead Researcher with high logical throughput and reliable execution.",
					tags: ["Efficiency 88%", "Agility 92%"],
				},
				{
					title: "Pixel Pixie",
					description: "UI Artisan focused on rapid visual iteration and polishing.",
					tags: ["Creative", "Hyper"],
				},
				{
					title: "Expand Team",
					description: "Recruit new specialists from marketplace to fill workflow gaps.",
					tags: ["Marketplace", "Hiring"],
				},
			]}
		/>
	);
}
