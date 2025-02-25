import { cn } from "@/lib/utils";
import { ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";

type PaginationProps = {
  currentPage: number;
  totalPages: number;
};

export default function Pagination({
  currentPage,
  totalPages,
}: PaginationProps) {
  return (
    <div className="flex justify-center items-center space-x-2 mt-4">
      <Link
        href={`?page=${currentPage - 1}`}
        className={cn(
          "p-2 bg-blue-500 text-white rounded-full disabled:bg-blue-300",
          {
            "pointer-events-none bg-gray-300": currentPage === 1,
          }
        )}
      >
        <ChevronLeft size={20} />
      </Link>

      <span className="text-black">
        Page {currentPage} of {totalPages}
      </span>
      <Link
        href={`?page=${currentPage + 1}`}
        className={cn(
          "p-2 bg-blue-500 text-white rounded-full disabled:bg-blue-300",
          {
            "pointer-events-none bg-gray-300": currentPage === totalPages,
          }
        )}
      >
        <ChevronRight size={20} />
      </Link>
    </div>
  );
}
