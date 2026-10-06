# Health Insurance Policy and Claims Management System

A database management system developed to manage customers, insurance policies, hospitals, treatments, claims, and claim payments.

## Project Overview

The Health Insurance Policy and Claims Management System is a relational database application designed to simplify the management of health insurance information.

The system uses MySQL as the database and a Python Tkinter interface to interact with the database.

## Objectives

- Manage customer information
- Manage insurance companies
- Manage different policy types
- Store and manage insurance policies
- Maintain hospital information
- Maintain treatment information
- Manage insurance claims
- Track claim payments
- Provide a simple graphical user interface for database operations

## Technologies Used

- Python
- Tkinter
- MySQL
- MySQL Connector/Python
- SQL
- Git & GitHub

## Database Structure

The system consists of the following major tables:

1. Customer
2. Insurance_Company
3. Policy_Type
4. Policy
5. Hospital
6. Treatment
7. Claim
8. Claim_Payment

### Main Relationships

- Customer → Policy
- Insurance Company → Policy
- Policy Type → Policy
- Policy → Claim
- Hospital → Claim
- Treatment → Claim
- Claim → Claim Payment

## Application Features

### Customer Management

- View customers
- Add new customers
- Delete customers
- Search customer records

### Policy Management

- View policies
- Add new policies
- Search policy records

### Claims Management

- View claims
- Display customer, policy, hospital and treatment information
- Search claim records

## Database Operations

The system demonstrates the use of:

- INSERT
- SELECT
- DELETE
- JOIN
- Primary Keys
- Foreign Keys
- Constraints
- Referential Integrity

## Application Architecture

```text
User
  ↓
Tkinter GUI
  ↓
Python
  ↓
MySQL Connector
  ↓
MySQL Database
