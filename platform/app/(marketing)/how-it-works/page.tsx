import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function HowItWorksPage() {
  return (
    <ForgeScreen
      section="Lab"
      title="From Spark to Shipped"
      subtitle="The Kinetic Pipeline turns ideas into production systems through deterministic stages and HITL approval."
      kicker="The Kinetic Atelier"
      primaryCta="Setup Wizard"
      secondaryCta="View Artifacts"
      metrics={[
        { label: "Stage 1", value: "Idea" },
        { label: "Stage 2", value: "PRD + Spec" },
        { label: "Stage 3", value: "Build + Test" },
        { label: "Stage 4", value: "HITL + Deploy" },
      ]}
      cards={[
        {
          title: "Pipeline Console",
          description:
            "Real-time execution logs and artifact status for every agent transition.",
          tags: ["Live Logs", "Artifact Trail"],
        },
        {
          title: "Control Panel",
          description:
            "Toggle speed, inspect outputs, and adjust constraints before approval.",
          tags: ["Fast-Track", "Safety Flags"],
        },
        {
          title: "HITL Checkpoint",
          description:
            "Every production deploy is blocked until human approval is granted.",
          tags: ["Mandatory", "Policy Enforced"],
        },
      ]}
    />
  );
}
