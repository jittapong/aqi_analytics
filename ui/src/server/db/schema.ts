import { serial, integer, doublePrecision, varchar, unique } from "drizzle-orm/pg-core"
// import { sql } from "drizzle-orm"

import { pgTableCreator } from "drizzle-orm/pg-core";

// export const stationInfo = pgTable("station_info", {
// 	id: serial().primaryKey().notNull(),
// 	uid: integer(),
// 	latitude: doublePrecision(),
// 	longitude: doublePrecision(),
// 	stationName: varchar("station_name", { length: 255 }),
// }, (table) => [
// 	unique("station_info_uid_key").on(table.uid),
// ]);

export const createTable = pgTableCreator((name) => `${name}`);

export const stationInfo = createTable(
  "station_info",
  {
	id: serial().primaryKey().notNull(),
	uid: integer(),
	latitude: doublePrecision(),
	longitude: doublePrecision(),
	stationName: varchar("station_name", { length: 255 }),
  },
  (table) => [
    unique("station_info_uid_key").on(table.uid),
  ],
);