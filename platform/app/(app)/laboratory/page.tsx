import { ForgeScreen } from "../../../components/layout/forge-screen";

export default function LaboratoryPage() {
  return (
    <ForgeScreen
      section="Lab"
      withSidebar
      title="The Laboratory"
      subtitle="Discover and install skill modules to extend your agent workforce capabilities."
      kicker="Experimental Phase"
      primaryCta="Learn & Install"
      secondaryCta="Initialize Forge"
      metrics={[
        { label: "Active Modules", value: "16" },
        { label: "Recommended", value: "Clerk Auth" },
        { label: "Discovery Speed", value: "2.5x" },
        { label: "Credit Range", value: "850-1,250" },
      ]}
      cards={[
        {
          title: "Clerk Auth Mastery",
          description:
            "Multi-factor identity and JWT workflow module for secure onboarding.",
          tags: ["Authentication", "v2.4.1"],
        },
        {
          title: "Stripe Payments",
          description: "Billing and checkout integration module for SaaS monetization.",
          tags: ["Financials", "850 Cr"],
        },
        {
          title: "Pinecone Vector Hub",
          description: "Long-term memory indexing with fast vector retrieval.",
          tags: ["Data Stores", "1,100 Cr"],
        },
      ]}
    />
  );
}
