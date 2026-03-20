import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function CouncilPage() {
	return (
		<ForgeScreen
			section="Quests"
			withSidebar
			title="The Council"
			subtitle="Manage architects and field operators with role visibility and operational status."
			kicker="Team Management"
			primaryCta="Summon New Teammate"
			secondaryCta="Open Support Comms"
			metrics={[
				{ label: "Total Architects", value: "08" },
				{ label: "Active Operators", value: "14" },
				{ label: "Trust Score", value: "98%" },
				{ label: "Agents Online", value: "6" },
			]}
			cards={[
				{
					title: "Lead Architects",
					description:
						"High-tier strategy owners with override and admin protocol permissions.",
					tags: ["Master", "Lead", "Tiered Access"],
				},
				{
					title: "Field Operators",
					description:
						"Execution team roster with role, mission, and availability status.",
					tags: ["In Field", "Idle"],
				},
				{
					title: "Council Actions",
					description:
						"Recruit, update permissions, and coordinate support communications.",
					tags: ["Recruit", "Permissions"],
				},
			]}
		/>
	);
}
