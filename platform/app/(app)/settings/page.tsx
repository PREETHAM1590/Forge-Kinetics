import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function SettingsPage() {
	return (
		<ForgeScreen
			section="Lab"
			withSidebar
			title="Forge Control Nexus"
			subtitle="Manage global configuration for identity, integrations, team policy, and environment defaults."
			kicker="Settings"
			primaryCta="Save Configuration"
			secondaryCta="Open Integrations"
			metrics={[
				{ label: "Connected Providers", value: "08" },
				{ label: "Team Seats", value: "24" },
				{ label: "Policy Violations", value: "00" },
				{ label: "Last Sync", value: "2m ago" },
			]}
			cards={[
				{
					title: "Workspace Identity",
					description: "Branding, environment labels, and organization metadata for all project outputs.",
					tags: ["Brand", "Metadata"],
				},
				{
					title: "Policy & Governance",
					description: "HITL behavior, audit retention, and risk escalation rules for execution gates.",
					tags: ["HITL", "Audit", "Compliance"],
				},
				{
					title: "Runtime Defaults",
					description: "Token budgets, model strategy, and sandbox presets used by every new project.",
					tags: ["FinOps", "Sandbox"],
				},
			]}
		/>
	);
}
