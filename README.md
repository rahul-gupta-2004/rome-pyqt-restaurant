This project is the **Restaurant Owner Desktop Software** for **R.O.M.E. (Restaurants Orders Made Easy)** — a complete restaurant order management ecosystem. It is designed to give restaurant owners a fast and intuitive interface to manage their tables, menu inventory, and profiles directly from a desktop environment using a graphical interface.

The application is built using **Python and PyQt5**, with a focus on a clean UI/UX that simplifies daily operations for restaurant staff.

<br>

**Key Features**

**1. Login System**  
Restaurant owners can securely log in using their registered credentials. Upon successful login, they are directed to their personalized dashboard.

**2. Table Management with QR Code Generation**  
Owners can add and manage tables within their restaurant. Each time a new table is added, the application automatically generates a unique QR code that links to the digital menu for that specific table. This QR code can be printed and placed on the table for customer use.

**3. Inventory Viewing**  
Restaurant owners can view their current inventory fetched from the database. Each item displays its name, price, category, and type (veg, non-veg, egg), along with its stock status. This allows the owner to keep track of available dishes and restock when necessary.

**4. Profile Management**  
Restaurant details such as name, address, and contact information are shown in a dedicated profile section. Owners can review their data and keep records in sync.

**5. Splash Screen & Smooth Navigation**  
The software includes a simple splash screen at startup, followed by a clear and responsive layout, allowing users to navigate between different modules effortlessly.

<br>

**Database**

The backend is powered by **Supabase**, a scalable PostgreSQL-based platform. All data related to restaurants, tables, and inventory is synced in real time using Supabase's API. This allows for seamless integration between the desktop software and the web-based customer/admin panels of the R.O.M.E. ecosystem.

<br>

**Purpose**

This desktop software is developed as part of a full-stack solution to make restaurant management easier and more modern. It connects directly to the centralized database and allows restaurants to manage their digital presence without needing any web interface.

By pairing this with the web portal for customers and the admin dashboard, restaurant owners have full control over their operations, all in one streamlined ecosystem.
