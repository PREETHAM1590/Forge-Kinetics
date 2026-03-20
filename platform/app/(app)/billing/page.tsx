import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function FinOpsBillingPage() {
	return (
		<ForgeScreen
			section="Lab"
			withSidebar
			title="Billing & Credits"
			subtitle="Track token burn, purchase credit packs, and monitor top spending agents."
			kicker="Financial Operations"
			primaryCta="Refuel Forge"
			secondaryCta="Export CSV"
			metrics={[
				{ label: "Current Balance", value: "1,250 CR" },
				{ label: "Weekly Delta", value: "+12%" },
				{ label: "Top Burn", value: "420 CR" },
				{ label: "Auto-Refill", value: "Enabled" },
			]}
			cards={[
				{
					title: "Token Usage Flux",
					description:
						"Live consumption chart across active models and project workloads.",
					tags: ["Weekly", "Monthly"],
				},
				{
					title: "Purchase Credits",
					description:
						"Top-up plans for 5k and 15k credit packs with instant balance update.",
					tags: ["5,000", "15,000"],
				},
				{
					title: "Ledger Log",
					description:
						"Transaction history with settled and pending entries for transparent accounting.",
					tags: ["Settled", "Pending"],
				},
			]}
		/>
	);
}
