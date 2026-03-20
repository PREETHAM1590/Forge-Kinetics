import type { HTMLAttributes } from "react";

export function Separator({ className = "", ...props }: HTMLAttributes<HTMLHRElement>) {
	return <hr className={`border-[var(--outline)] ${className}`.trim()} {...props} />;
}

export default Separator;
