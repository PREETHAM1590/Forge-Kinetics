import { ForgeScreen } from "../../../../../components/layout/forge-screen";

export default function BuildTerminalHqPage() {
  return (
    <ForgeScreen
      section="Lab"
      withSidebar
      title="Build Terminal HQ"
      subtitle="Real-time oversight of kinetic synthesis tanks, capacity waves, and emergency controls."
      kicker="Terminal Control Center"
      primaryCta="PRIORITY BOOST"
      secondaryCta="EMERGENCY STOP"
      metrics={[
        { label: "Power Draw", value: "4.2 GW" },
        { label: "Load Capacity", value: "84%" },
        { label: "Active Tanks", value: "2" },
        { label: "Total Cores", value: "2,048" },
      ]}
      cards={[
        {
          title: "Cyber-Kinetics Prototype",
          description: "Synthesizing neural-mechanical pathways for Project Icarus.",
          tags: ["72%", "Tank 01"],
        },
        {
          title: "Liquid-Logic Engine",
          description: "Casting high-viscosity data streams into deployable form.",
          tags: ["18%", "Tank 02"],
        },
        {
          title: "Marketplace Agents",
          description: "Lease extra specialists to increase throughput by up to 40%.",
          tags: ["+31 Available", "Boost"],
        },
      ]}
    />
  );
}
