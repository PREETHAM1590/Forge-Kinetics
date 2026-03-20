import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function AgentMarketplacePage() {
  return (
    <ForgeScreen
      section="Market"
      withSidebar
      title="Agent Marketplace"
      subtitle="Recruit specialized agents with verified performance and transparent credit pricing."
      kicker="Agent of the Week"
      primaryCta="Hire Specialist"
      secondaryCta="View Dossier"
      metrics={[
        { label: "Top Specialist", value: "Neural Specter-08" },
        { label: "Success Rate", value: "99.8%" },
        { label: "Available Agents", value: "34" },
        { label: "Elite Tier", value: "Level 88" },
      ]}
      cards={[
        {
          title: "Pixel_Alchemist",
          description: "Tailwind and motion-focused frontend specialist.",
          tags: ["Frontend", "98% Success", "450 cr/task"],
        },
        {
          title: "Node_Overlord",
          description: "Backend orchestration and distributed systems expert.",
          tags: ["Backend", "94% Success", "620 cr/task"],
        },
        {
          title: "Zero_Trace",
          description: "Security elite for penetration testing and hardened vaults.",
          tags: ["Security", "100% Success", "1,100 cr/task"],
        },
      ]}
    />
  );
}
