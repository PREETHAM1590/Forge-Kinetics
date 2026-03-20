import { ForgeScreen } from "../../../../components/layout/forge-screen";

export default function AgentDeepDivePage() {
  return (
    <ForgeScreen
      section="Quests"
      withSidebar
      title="The Architect"
      subtitle="Deep profile view for mastery stats, quest history, and live cognitive stream."
      kicker="Agent Deep-Dive Profile"
      primaryCta="Deploy to Lab"
      secondaryCta="View Manifesto"
      metrics={[
        { label: "Tier", value: "Elite" },
        { label: "Node ID", value: "ARCH_772" },
        { label: "Compute Load", value: "78.2%" },
        { label: "Core Temp", value: "42°C" },
      ]}
      cards={[
        {
          title: "Skill Mastery",
          description: "Logic synthesis, conflict resolution, and creative entropy progression.",
          tags: ["Lvl 92", "Lvl 88", "Lvl 75"],
        },
        {
          title: "Brain State",
          description: "Live thought stream with event logs and behavioral insight markers.",
          tags: ["Live Feed", "Cognitive Trace"],
        },
        {
          title: "Quest History",
          description: "Completed mission archive for performance and reliability review.",
          tags: ["Verified", "Recent Wins"],
        },
      ]}
    />
  );
}
