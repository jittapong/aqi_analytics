import { db } from "@/database";
import { stationInfo } from "@/database/migrations/schema";
import { NextResponse } from "next/server";

export async function getStationData(): Promise<NextResponse> {
    try {
      // Fetch all records
      const stations = await db.select().from(stationInfo);
      console.log("stations >>", stations);
  
      return NextResponse.json(stations);
    } catch (error) {
      console.error("Error fetching station data:", error);
      return NextResponse.json({ error: "Failed to fetch data" }, { status: 500 });
    }
  }