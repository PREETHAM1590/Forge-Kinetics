import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function PricingPage() {
	return (
		<ForgeScreen
			section="Market"
			title="Forged for Scale"
			subtitle="Simple credit-based pricing for Studio, Agency, and Enterprise workflows."
			kicker="Kinetic Credit System"
			primaryCta="Scale the Atelier"
			secondaryCta="Book a Demo"
			metrics={[
				{ label: "Studio", value: "$49 / 2,500" },
				{ label: "Agency", value: "$199 / 12,000" },
				{ label: "Enterprise", value: "Custom" },
				{ label: "Support", value: "24/7" },
			]}
			cards={[
				{
					title: "Studio",
					description: "For solo creators and early-stage product experiments.",
					tags: ["1 Active Lab", "Standard Speed"],
				},
				{
					title: "Agency",
					description: "For teams running multiple builds with faster synthesis.",
					tags: ["10 Active Labs", "Priority Tools"],
				},
				{
					title: "Enterprise",
					description: "Dedicated infrastructure, white-label controls, and custom governance.",
					tags: ["Dedicated Infra", "Custom Contracts"],
				},
			]}
		/>
	);
}
