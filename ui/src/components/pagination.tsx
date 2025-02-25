import { ChevronLeft, ChevronRight } from "lucide-react"

type PaginationProps = {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

export default function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  return (
    <div className="flex justify-center items-center space-x-2 mt-4">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 bg-blue-500 text-white rounded-full disabled:bg-blue-300"
      >
        <ChevronLeft size={20} />
      </button>
      <span className="text-black">
        Page {currentPage} of {totalPages}
      </span>
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 bg-blue-500 text-white rounded-full disabled:bg-blue-300"
      >
        <ChevronRight size={20} />
      </button>
    </div>
  )
}

