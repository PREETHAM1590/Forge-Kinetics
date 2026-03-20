import type { TextareaHTMLAttributes } from "react";

export function Textarea({ className = "", ...props }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
	return (
		<textarea
			className={`w-full rounded-xl border border-[var(--outline)] bg-[var(--surface)] px-3 py-2 ${className}`.trim()}
			{...props}
		/>
	);
}

export default Textarea;
