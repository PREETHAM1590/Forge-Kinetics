import type { HTMLAttributes } from "react";

export function Card({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
	return <div className={`forge-panel p-4 ${className}`.trim()} {...props} />;
}

export default Card;
