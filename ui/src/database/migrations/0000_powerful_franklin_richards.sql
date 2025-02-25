-- Current sql file was generated after introspecting the database
-- If you want to run this migration please uncomment this code before executing migrations
/*
CREATE TABLE "station_info" (
	"id" serial PRIMARY KEY NOT NULL,
	"uid" integer,
	"latitude" double precision,
	"longitude" double precision,
	"station_name" varchar(255),
	CONSTRAINT "station_info_uid_key" UNIQUE("uid")
);

*/