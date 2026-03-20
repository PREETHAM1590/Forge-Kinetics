import type { HTMLAttributes } from "react";

export function Sheet({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
	return <div className={`forge-panel p-4 ${className}`.trim()} {...props} />;
}

export default Sheet;
