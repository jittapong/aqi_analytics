import StationsClientWrapper from "@/components/stations-client-wrapper"
import { getStationData } from "@/feature/station/server/db/station"

export default async function StationsData() {
  const response = await getStationData()
  const stations = await response.json()

  return <StationsClientWrapper initialStations={stations} />
}