import type { HTMLAttributes } from "react";

export function DropdownMenu({ className = "", ...props }: HTMLAttributes<HTMLDivElement>) {
	return <div className={`forge-panel p-2 ${className}`.trim()} {...props} />;
}

export default DropdownMenu;
