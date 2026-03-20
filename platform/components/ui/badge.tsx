import type { HTMLAttributes } from "react";

export function Badge({ className = "", ...props }: HTMLAttributes<HTMLSpanElement>) {
	return <span className={`forge-chip bg-[var(--surface-low)] text-[var(--muted)] ${className}`.trim()} {...props} />;
}

export default Badge;
