-- CreateTable
CREATE TABLE "FinancialProduct" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "bankName" TEXT NOT NULL,
    "productName" TEXT NOT NULL,
    "productType" TEXT NOT NULL,
    "features" TEXT,
    "targetAudience" TEXT,
    "period" TEXT,
    "depositLimit" TEXT,
    "baseRate" TEXT,
    "primeRate" TEXT,
    "taxBenefits" TEXT,
    "protection" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
