type Station = {
  id: number;
  uid: number;
  latitude: number;
  longitude: number;
  stationName: string;
};

type StationsTableProps = {
  stations: Station[];
};

export default function StationsTable({ stations }: StationsTableProps) {
  return (
    <div className="overflow-x-auto w-full">
      <table className="min-w-full bg-white border border-blue-300">
        <thead>
          <tr className="bg-blue-100">
            <th className="px-4 py-2 text-left text-black">ID</th>
            <th className="px-4 py-2 text-left text-black">UID</th>
            <th className="px-4 py-2 text-left text-black">Latitude</th>
            <th className="px-4 py-2 text-left text-black">Longitude</th>
            <th className="px-4 py-2 text-left text-black">Station Name</th>
          </tr>
        </thead>
        <tbody>
          {stations.map((station) => (
            <tr key={station.id} className="border-t border-blue-200">
              <td className="px-4 py-2 text-black">{station.id}</td>
              <td className="px-4 py-2 text-black">{station.uid}</td>
              <td className="px-4 py-2 text-black">{station.latitude}</td>
              <td className="px-4 py-2 text-black">{station.longitude}</td>
              <td className="px-4 py-2 text-black">
                <div
                  className="max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl truncate"
                  title={station.stationName}
                >
                  {station.stationName}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
