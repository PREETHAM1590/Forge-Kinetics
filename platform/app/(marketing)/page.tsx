import { ForgeScreen } from "../../components/layout/forge-screen";

export default function ForgeHomePage() {
	return (
		<ForgeScreen
			section="Quests"
			title="Your AI Office Team Builds While You Sip Coffee"
			subtitle="Deploy a squad of autonomous agents specialized in code, design, and ops across the Kinetic Atelier."
			kicker="KINETIC ATELIER IS LIVE"
			primaryCta="Start a Build"
			secondaryCta="See Agent Team"
			metrics={[
				{ label: "Projects Shipped", value: "14.2k" },
				{ label: "Bugs Fixed", value: "890k" },
				{ label: "Atelier Uptime", value: "99.9%" },
				{ label: "Active Forging", value: "24/7" },
			]}
			cards={[
				{
					title: "The Command Nexus",
					description:
						"Manage multiple squads of agents and jump into any project flow in real time.",
					tags: ["Real-time Collab", "Git Integration"],
				},
				{
					title: "Auto-Repair Logic",
					description:
						"Agents detect anomalies early and propose stable fixes before production risk increases.",
					tags: ["Quality Gate", "Pre-Deploy Checks"],
				},
				{
					title: "Ironclad Security",
					description:
						"Encrypted forge sessions and policy-first pipelines with mandatory approval flow.",
					tags: ["HITL", "Secure by Default"],
				},
			]}
		/>
	);
}
