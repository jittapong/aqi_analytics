"use client"

import { useState } from "react"
import StationsTable from "./stations-table"
import Pagination from "./pagination"

const ITEMS_PER_PAGE = 10

type Station = {
  id: number
  uid: number
  latitude: number
  longitude: number
  stationName: string
}

type StationsClientWrapperProps = {
  initialStations: Station[]
}

export default function StationsClientWrapper({ initialStations }: StationsClientWrapperProps) {
  const [currentPage, setCurrentPage] = useState(1)
  const totalPages = Math.ceil(initialStations.length / ITEMS_PER_PAGE)
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE
  const endIndex = startIndex + ITEMS_PER_PAGE
  const currentStations = initialStations.slice(startIndex, endIndex)

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  return (
    <div className="min-h-screen bg-blue-50">
      <main className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6 text-blue-800">Stations</h1>
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <StationsTable stations={currentStations} />
        </div>
        <Pagination currentPage={currentPage} totalPages={totalPages} onPageChange={handlePageChange} />
      </main>
    </div>
  )
}

