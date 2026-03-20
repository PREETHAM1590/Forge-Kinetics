type ForgeChromeProps = {
  section: "Quests" | "Lab" | "Market";
  withSidebar?: boolean;
};

const sidebarItems = [
  "Dashboard",
  "AI Forge",
  "Inventory",
  "Teammates",
  "Settings",
];

export function ForgeChrome({ section, withSidebar = false }: ForgeChromeProps) {
  return (
    <>
      <header className="forge-glass fixed top-0 z-40 flex h-20 w-full items-center justify-between border-b border-white/40 px-8">
        <div className="flex items-center gap-8">
          <span className="text-2xl font-black italic text-blue-700">Forge AI</span>
          <nav className="hidden items-center gap-6 md:flex">
            {(["Quests", "Lab", "Market"] as const).map((item) => {
              const active = item === section;
              return (
                <span
                  key={item}
                  className={[
                    "font-bold",
                    active
                      ? "border-b-4 border-yellow-400 pb-1 text-blue-700"
                      : "text-slate-500",
                  ].join(" ")}
                >
                  {item}
                </span>
              );
            })}
          </nav>
        </div>
        <div className="flex items-center gap-3">
          <span className="rounded-full bg-[var(--secondary-container)] px-4 py-2 text-xs font-bold text-[var(--secondary)]">
            1,250 Credits
          </span>
          <div className="h-10 w-10 rounded-full border-2 border-yellow-300 bg-slate-300" />
        </div>
      </header>

      {withSidebar ? (
        <aside className="fixed left-0 top-20 hidden h-[calc(100vh-5rem)] w-64 flex-col gap-2 rounded-r-3xl border-r border-white/60 bg-slate-50/95 p-4 shadow-2xl lg:flex">
          <div className="mb-4 rounded-2xl bg-white p-3">
            <p className="text-xs font-bold text-slate-500">Level 14</p>
            <p className="text-sm font-black text-blue-800">Master Artificer</p>
          </div>
          {sidebarItems.map((item) => (
            <div
              key={item}
              className={`rounded-2xl px-4 py-3 text-sm font-semibold ${
                item === "AI Forge"
                  ? "bg-yellow-400 text-blue-900"
                  : "text-slate-600 hover:bg-blue-50"
              }`}
            >
              {item}
            </div>
          ))}
          <button className="mt-auto rounded-2xl bg-[var(--secondary)] py-3 font-bold text-white">
            Start New Project
          </button>
        </aside>
      ) : null}
    </>
  );
}
