import { db } from "@/database";
import { stationInfo } from "@/database/migrations/schema";
import { count } from "drizzle-orm";

export async function getStationData(pageIndex: number, pageSize: number = 10) {
  const start = Math.max(0, pageIndex - 1) * pageSize;
  // await new Promise((resolve) => setTimeout(resolve, 3000));
  return await db.select().from(stationInfo).offset(start).limit(pageSize);
}

export async function getTotalPage(pageSize: number = 10) {
  const result = await db.select({ count: count() }).from(stationInfo);
  return Math.floor((result[0]?.count || 0) / pageSize);
}
