import Pagination from "@/features/station/components/pagination";
import StationsTable from "@/features/station/components/stations-table";
import {
  getStationData,
  getTotalPage,
} from "@/features/station/server/db/station";
import { redirect } from "next/navigation";

interface StationPageProps {
  searchParams?: Promise<{
    page: string;
  }>;
}
export default async function StationsPage(props: StationPageProps) {
  const searchParams = await props.searchParams;
  const currentPage = parseInt(searchParams?.page ?? "1");
  const response = await getStationData(currentPage);
  const totalPages = await getTotalPage();

  if (currentPage < 1) {
    redirect(`?page=1`);
  } else if (currentPage > totalPages) {
    redirect(`?page=${totalPages}`);
  }

  return (
    <div className="min-h-screen bg-blue-50">
      <main className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-6 text-blue-800">Stations</h1>
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <StationsTable stations={response} />
        </div>
        <Pagination currentPage={currentPage} totalPages={totalPages} />
      </main>
    </div>
  );
}
