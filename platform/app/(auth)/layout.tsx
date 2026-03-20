export default function AuthLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<div className="min-h-screen bg-[var(--background)] px-6 py-12">
			<div className="mx-auto max-w-5xl">
				<div className="forge-panel grid gap-8 p-8 md:grid-cols-2 md:p-12">
					<section className="space-y-4">
						<span className="forge-chip inline-block bg-[var(--primary-container)] text-[var(--primary)]">
							FORGE ACCESS
						</span>
						<h1 className="text-4xl font-black text-[var(--text)]">Enter the Forge</h1>
						<p className="text-sm text-[var(--muted)]">
							Authenticate to launch projects, monitor agents, and approve production gates.
						</p>
					</section>
					<section>{children}</section>
				</div>
			</div>
		</div>
	);
}
