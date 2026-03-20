import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function ProjectWizardPage() {
	return (
		<ForgeScreen
			section="Lab"
			withSidebar
			title="Project Setup Wizard"
			subtitle="Define intent, assign your squad, and set budget constraints before ignition."
			kicker="Step 1/3 — Concept"
			primaryCta="IGNITE THE FORGE"
			secondaryCta="View All Agents"
			metrics={[
				{ label: "Token Cap", value: "5,000,000" },
				{ label: "Projected Cycles", value: "14" },
				{ label: "Estimated Delivery", value: "Oct 24" },
				{ label: "Investment", value: "$2,450" },
			]}
			cards={[
				{
					title: "Project Intent",
					description:
						"Capture core product goal and align it with technical and creative tags.",
					tags: ["Creative", "Technical", "Experimental"],
				},
				{
					title: "Squad Matchmaking",
					description:
						"Hire the right specialist agents for architecture, design, and execution.",
					tags: ["Rusty Spark", "Maya Flux"],
				},
				{
					title: "Budget Architect",
					description:
						"Set maximum burn and keep deployment within approved credit limits.",
					tags: ["Token Guard", "Timeline"],
				},
			]}
		/>
	);
}
