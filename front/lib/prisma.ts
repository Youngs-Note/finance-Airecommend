import { PrismaPg } from "@prisma/adapter-pg";
import "dotenv/config";
import { PrismaClient } from "../generated/prisma/client";

// Neon(PostgreSQL) 접속 문자열. 예: postgresql://USER:PASSWORD@HOST/DB?sslmode=require
const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  throw new Error("DATABASE_URL is required.");
}

const adapter = new PrismaPg({ connectionString, max: 5 });
const prisma = new PrismaClient({ adapter });

export { prisma };
