export default function SignInPage() {
	return (
		<div className="space-y-6">
			<div>
				<h2 className="text-2xl font-bold text-[var(--text)]">Sign in</h2>
				<p className="mt-1 text-sm text-[var(--muted)]">
					Use your workspace credentials to continue.
				</p>
			</div>
			<form className="space-y-4">
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
					className="w-full rounded-xl bg-[var(--primary-container)] px-4 py-3 font-bold text-[var(--primary)]"
				>
					Sign in
				</button>
			</form>
		</div>
	);
}
