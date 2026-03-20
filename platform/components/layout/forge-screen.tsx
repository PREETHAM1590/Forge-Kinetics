import { ForgeChrome } from "./forge-chrome";

type Metric = {
  label: string;
  value: string;
};

type Card = {
  title: string;
  description: string;
  tags?: string[];
};

type ForgeScreenProps = {
  section: "Quests" | "Lab" | "Market";
  title: string;
  subtitle: string;
  kicker?: string;
  withSidebar?: boolean;
  primaryCta?: string;
  secondaryCta?: string;
  metrics?: Metric[];
  cards?: Card[];
};

export function ForgeScreen({
  section,
  title,
  subtitle,
  kicker,
  withSidebar,
  primaryCta,
  secondaryCta,
  metrics = [],
  cards = [],
}: ForgeScreenProps) {
  return (
    <div className="min-h-screen bg-[var(--background)]">
      <ForgeChrome section={section} withSidebar={withSidebar} />

      <main
        className={`px-8 pb-16 pt-28 ${withSidebar ? "lg:ml-64" : ""}`.trim()}
      >
        <div className="mx-auto max-w-7xl space-y-10">
          <section className="forge-panel p-8 md:p-12">
            {kicker ? (
              <span className="forge-chip mb-4 inline-block bg-[var(--primary-container)] text-[var(--primary)]">
                {kicker}
              </span>
            ) : null}
            <h1 className="text-4xl font-extrabold tracking-tight text-[var(--text)] md:text-6xl">
              {title}
            </h1>
            <p className="mt-4 max-w-3xl text-lg text-[var(--muted)]">{subtitle}</p>
            {(primaryCta || secondaryCta) && (
              <div className="mt-8 flex flex-wrap gap-4">
                {primaryCta ? (
                  <button className="rounded-xl bg-[var(--primary-container)] px-6 py-3 font-bold text-[var(--primary)]">
                    {primaryCta}
                  </button>
                ) : null}
                {secondaryCta ? (
                  <button className="rounded-xl bg-[var(--secondary-container)] px-6 py-3 font-bold text-[var(--secondary)]">
                    {secondaryCta}
                  </button>
                ) : null}
              </div>
            )}
          </section>

          {metrics.length > 0 ? (
            <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {metrics.map((metric) => (
                <div key={metric.label} className="forge-panel p-6">
                  <p className="text-xs font-bold uppercase tracking-widest text-[var(--muted)]">
                    {metric.label}
                  </p>
                  <p className="mt-2 text-3xl font-black text-[var(--secondary)]">
                    {metric.value}
                  </p>
                </div>
              ))}
            </section>
          ) : null}

          {cards.length > 0 ? (
            <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {cards.map((card) => (
                <article key={card.title} className="forge-panel p-6">
                  <h3 className="text-xl font-black text-[var(--text)]">{card.title}</h3>
                  <p className="mt-2 text-sm text-[var(--muted)]">{card.description}</p>
                  {card.tags?.length ? (
                    <div className="mt-4 flex flex-wrap gap-2">
                      {card.tags.map((tag) => (
                        <span
                          key={tag}
                          className="forge-chip bg-[var(--surface-low)] text-[var(--muted)]"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  ) : null}
                </article>
              ))}
            </section>
          ) : null}
        </div>
      </main>
    </div>
  );
}
