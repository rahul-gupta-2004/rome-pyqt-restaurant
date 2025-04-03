Features:
* Restaurant & Table Management: Add, update, and delete restaurants and tables.
* Inventory & Menu Management: Manage food categories, stock, and availability.
* Order Management: View and process customer orders.
* Admin Authentication: Secure login/logout for restaurant owners.
* Dashboard Analytics: View statistics on restaurants, tables, orders, and inventory.
* Geolocation Integration: Convert restaurant addresses to coordinates for map-based features.

Technologies Used:
* Node.js + Express.js (Backend)
* EJS (Templating)
* Supabase (Database)
* SCSS (Styling)
* OpenStreetMap API (Geolocation)

Setup Instructions:
1. Install dependencies:
  ```
  npm install
  ```
3. Set up .env file with:
   ```
   SUPABASE_URL=
   SUPABASE_ANON_KEY=
   ADMIN_EMAIL=
   ADMIN_PASSWORD=
   ```
4. Start the server
   ```
   npm start
   ```
6. Access Admin Panel at: http://localhost:3000/admin/login
