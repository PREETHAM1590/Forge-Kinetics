import type { TableHTMLAttributes } from "react";

export function Table({ className = "", ...props }: TableHTMLAttributes<HTMLTableElement>) {
	return <table className={`w-full border-collapse ${className}`.trim()} {...props} />;
}

export default Table;
