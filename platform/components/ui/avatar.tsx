import type { HTMLAttributes } from "react";

export function Avatar({ className = "", children, ...props }: HTMLAttributes<HTMLDivElement>) {
	return (
		<div className={`inline-flex h-10 w-10 items-center justify-center rounded-full bg-[var(--surface-low)] ${className}`.trim()} {...props}>
			{children}
		</div>
	);
}

export default Avatar;
