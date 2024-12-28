# Santa’s Treasure Logistics Tracker
### Jingle Byte Christmas Coding Competition 2024

## Overview
Santa's Treasure is a web application designed to simulate Santa’s gift delivery logistics. The application optimizes the delivery route, allows users to select and pay for gifts, and provides an admin dashboard for real-time logistics monitoring. The system also integrates Razorpay for secure payment processing and includes OTP verification for deliveries, ensuring that orders are only marked as "Delivered" when the correct OTP is entered by the delivery partner.

## Features

### User Features:
- **User Registration & Authentication:** 
  - Create an account with name, email, and address.
  - Login/logout functionality for users.
  - Manage account details and delivery address.

- **Product Selection and Gift Distribution:**
  - Browse available gifts.
  - Choose the gift to be delivered to a specified address.

- **Order Management:**
  - Place orders and make payments via Razorpay.

- **Payment Integration:**
  - **Razorpay** is integrated for secure payment processing.
  - Users can pay for their gifts via Razorpay's payment gateway before the delivery process starts.
  - After successful payment, user receive order confirmation mail to their registered email id.

### Admin Features:
- **Admin Login & Authentication:** 
  - Admins can log in to manage deliveries.

- **Dashboard:**
  - Admins can get an overview of the deliveries, including the total number of gifts delivered and pending deliveries.
  
- **Order Management:**
  - Admins can view, update, and manage the delivery status of orders.
  
- **Route Optimization:**
  - Admin can view optimized routes for Santa’s sleigh based on delivery locations.

- **Tracking Orders:**
  - Admin has access to track the delivery status of gifts by using OrderID , including progress, and any delivery delays.
 
- **OTP Verification for Delivery:**
  - An OTP (One-Time Password) is sent to the customer's email when the delivery is scheduled.
  - The order will only be marked as "Delivered" when the correct OTP is entered by the user.
  


---

## Technologies Used

- **Frontend:**
  - HTML, CSS, JavaScript
  - Bootstrap (for responsive UI)
  - Google Maps API (for route visualization)

- **Backend:**
  - Python
  - Django
  - Route Optimization (Google Map API)
  - Razorpay API (for payment integration)
  - OTP Verification (using email services of SMTP)

- **Database:**
  - MySQL (for storing user data, orders, addresses, gifts, etc)

- **APIs:**
  - **Google Maps Geocoding API:** For Converting an address into latitude and longitude coordinates.
  - **Google Maps Directions API:** Provides directions between two locations, which includes the route, distance, and time taken.
  - **Razorpay API:** For secure payment transactions.
  - **Email Service (SMTP):** For sending OTP to customers.

---

