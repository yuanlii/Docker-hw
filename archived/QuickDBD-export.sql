-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "Customer" (
    "CustomerID" int   NOT NULL,
    "FirstName" string   NOT NULL,
    "LastName" string   NOT NULL,
    "StreetAddress" string   NOT NULL,
    "City" string   NULL,
    "State" string   NULL,
    "Zip" varchar(200)   NOT NULL,
    "CreateTime" NOT   NULL,
    CONSTRAINT "pk_Customer" PRIMARY KEY (
        "CustomerID"
     )
);

CREATE TABLE "Account" (
    "AccountID" int   NOT NULL,
    "Balance" money   NOT NULL,
    "CreateTime" NOT   NULL,
    CONSTRAINT "pk_Account" PRIMARY KEY (
        "AccountID"
     )
);

CREATE TABLE "CustomerAccount" (
    "CustomerAccountId" int   NOT NULL,
    "CustomerID" int   NOT NULL,
    "AccountID" int   NOT NULL,
    CONSTRAINT "pk_CustomerAccount" PRIMARY KEY (
        "CustomerAccountId"
     )
);

ALTER TABLE "CustomerAccount" ADD CONSTRAINT "fk_CustomerAccount_CustomerID" FOREIGN KEY("CustomerID")
REFERENCES "Customer" ("CustomerID");

ALTER TABLE "CustomerAccount" ADD CONSTRAINT "fk_CustomerAccount_AccountID" FOREIGN KEY("AccountID")
REFERENCES "Account" ("AccountID");

CREATE INDEX "idx_Customer_FirstName"
ON "Customer" ("FirstName");

CREATE INDEX "idx_Customer_LastName"
ON "Customer" ("LastName");

