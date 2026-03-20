import type { InputHTMLAttributes } from "react";

export function Input({ className = "", ...props }: InputHTMLAttributes<HTMLInputElement>) {
	return (
		<input
			className={`w-full rounded-xl border border-[var(--outline)] bg-[var(--surface)] px-3 py-2 ${className}`.trim()}
			{...props}
		/>
	);
}

export default Input;
