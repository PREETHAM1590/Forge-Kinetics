import { ForgeScreen } from "../../../../../components/layout/forge-screen";

export default function ProjectSuccessReportPage() {
  return (
    <ForgeScreen
      section="Quests"
      withSidebar
      title="KINETIC PULSE READY"
      subtitle="Project deployment complete with synthesis report, share link, and next-quest recommendations."
      kicker="Project Deployed Successfully"
      primaryCta="Deploy to Vercel"
      secondaryCta="See Code"
      metrics={[
        { label: "Lines of Code", value: "12,482" },
        { label: "Agents Used", value: "04" },
        { label: "Credits Spent", value: "185" },
        { label: "State", value: "Production Live" },
      ]}
      cards={[
        {
          title: "Synthesis Report",
          description: "Consolidated build, quality, and deployment stats with generated artifacts.",
          tags: ["Exportable", "Shareable"],
        },
        {
          title: "Terminal Snapshot",
          description: "Final deployment log with edge optimization and live URL readiness.",
          tags: ["Build OK", "Edge Ready"],
        },
        {
          title: "Next Quests",
          description: "Suggested follow-up expansions for interface, marketplace, and collaboration.",
          tags: ["Neural Interface", "Marketplace"],
        },
      ]}
    />
  );
}
