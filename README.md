# __County Tax System System.__

### This is a Django and Django REST Framework (DRF) based system for managing users, permits, and parking tickets in a structured and secure way. The system provides APIs for user management, permit issuance, parking ticket management, and retrieval of related geographic data.

## __User Management__

- ### Users can register, login, and logout.

- ### Users can view and update their own profiles.

- ### Admins have full access to view, edit, and delete all users.

- ### Token-based authentication ensures secure access to API endpoints.

## __Permits__

- ### Users can create and manage permits of different types: daily, monthly, or yearly.

- ### Permit creation automatically calculates duration based on type.

- ### Users can generate PDF versions of their permits for download.

- ### Staff can view all permits, while regular users see only their own.

## __Parking Tickets__

_ ### Users can create parking tickets linked to vehicles, sections, areas, and towns.

- ### Vehicles are automatically created or retrieved when issuing tickets.

- ### Tickets include vehicle info and location hierarchy (town → area → section).

- ### PDF generation is supported for tickets.

- ### Staff can view all tickets; users only access their own tickets.

## __Location Data__

- ### Endpoints provide towns, areas, and parking sections for dynamic selection in the frontend.

- ### Areas can be filtered by town, and sections by area, allowing precise location-based operations.

- ### Permissions & Security

- ### Admins have full access to all resources.

- ### Users can only interact with their own permits, tickets, and profiles.

- ### APIs are secured with token authentication.

## __Key Features__
- ### Token-based authentication for secure API access.

- ### PDF generation for permits and tickets.

- ### Full CRUD operations for permits and tickets.

- ### Location hierarchy management (town → area → section).

- ### Clean separation between admin and user privileges.
