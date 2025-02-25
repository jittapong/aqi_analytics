import { pgTable, unique, serial, integer, doublePrecision, varchar } from "drizzle-orm/pg-core"
import { sql } from "drizzle-orm"



export const stationInfo = pgTable("station_info", {
	id: serial().primaryKey().notNull(),
	uid: integer(),
	latitude: doublePrecision(),
	longitude: doublePrecision(),
	stationName: varchar("station_name", { length: 255 }),
}, (table) => [
	unique("station_info_uid_key").on(table.uid),
]);
