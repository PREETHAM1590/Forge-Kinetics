export default function SignUpPage() {
	return (
		<div className="space-y-6">
			<div>
				<h2 className="text-2xl font-bold text-[var(--text)]">Create account</h2>
				<p className="mt-1 text-sm text-[var(--muted)]">
					Start your Forge workspace and launch your first project quest.
				</p>
			</div>
			<form className="space-y-4">
				<input
					type="text"
					placeholder="Full name"
					className="w-full rounded-xl border border-[var(--outline)] bg-[var(--surface)] px-4 py-3"
				/>
				<input
					type="email"
					placeholder="Email"
					className="w-full rounded-xl border border-[var(--outline)] bg-[var(--surface)] px-4 py-3"
				/>
				<input
					type="password"
					placeholder="Password"
					className="w-full rounded-xl border border-[var(--outline)] bg-[var(--surface)] px-4 py-3"
				/>
				<button
					type="submit"
					className="w-full rounded-xl bg-[var(--secondary-container)] px-4 py-3 font-bold text-[var(--secondary)]"
				>
					Create account
				</button>
			</form>
		</div>
	);
}
