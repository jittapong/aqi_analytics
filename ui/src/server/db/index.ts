'server-only'
import * as schema from "./schema";
import { NextResponse } from "next/server";

import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export const db = drizzle(pool, { schema });

export async function getStationData(): Promise<NextResponse> {
  try {
    // Fetch all records
    const stations = await db.select().from(schema.stationInfo);
    console.log("stations >>", stations);

    return NextResponse.json(stations);
  } catch (error) {
    console.error("Error fetching station data:", error);
    return NextResponse.json({ error: "Failed to fetch data" }, { status: 500 });
  }
}