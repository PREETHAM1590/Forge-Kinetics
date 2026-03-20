import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function ArmoryPage() {
	return (
		<ForgeScreen
			section="Lab"
			withSidebar
			title="The Armory"
			subtitle="Manage neural API keys, webhook beacons, and global integration controls."
			kicker="Settings & API"
			primaryCta="Generate New Key"
			secondaryCta="Add Beacon"
			metrics={[
				{ label: "Credits Available", value: "4,820" },
				{ label: "API Keys", value: "2 Active" },
				{ label: "Webhooks", value: "2 Connected" },
				{ label: "Current Plan", value: "Kinetic Pro" },
			]}
			cards={[
				{
					title: "Neural Keys",
					description:
						"Rotate and copy secure keys for production and sandbox environments.",
					tags: ["forge_live", "forge_test"],
				},
				{
					title: "Webhook Beacons",
					description:
						"Route critical project and agent events into external systems.",
					tags: ["Slack", "Custom Server"],
				},
				{
					title: "Atelier Preferences",
					description: "Tune assist levels, motion profile, and tactical display options.",
					tags: ["High Energy", "Configurable"],
				},
			]}
		/>
	);
}
