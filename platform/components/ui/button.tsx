import type { ButtonHTMLAttributes } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement>;

export function Button({ className = "", ...props }: Props) {
	return (
		<button
			className={`rounded-xl px-4 py-2 font-semibold ${className}`.trim()}
			{...props}
		/>
	);
}

export default Button;
