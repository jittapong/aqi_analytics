import type { Config } from "drizzle-kit";

console.log("process.env.DATABASE_URL", process.env.DATABASE_URL)

export default {
  //schema: "./src/server/db/schema.ts",
  schema: "./src/server/db/schema.ts",
  out: "./src/server/db",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL as string,
  }  
} satisfies Config;
