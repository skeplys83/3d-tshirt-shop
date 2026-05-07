# 3D T-Shirt Shop

A university project built during the **WS24/25** semester at **Reutlingen University** as part of my *MKI-Projet* Module.

The application is an immersive, fully interactive **3D online shop** where users can explore, select, and purchase T-shirts inside a three-dimensional virtual store - directly in the browser, no plugins required.

**Team:** Steffen Alber · Martin Hustoles · Kathrin Krell · Nick Maier · Simon Jell  
**Professor:** Uwe Kloos

[<video src="assets/trailer.mp4" controls width="100%"></video>](https://github.com/user-attachments/assets/f4dfbef2-5337-45a5-9e45-7ec4ac677be5)

---

## Getting Started



### Prerequisites

Make sure you have the following installed before continuing:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (with Docker Compose v2)
- Git

### 1. Environment Variables

The backend requires a `.env` file at `backend/shopcore/.env`. This file is already filled in for local development. The variables and what they do:

| Variable                    | Description                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| `SECRET_KEY`                | Django secret key — keep this private                             |
| `POSTGRES_DB`               | Name of the PostgreSQL database                                   |
| `POSTGRES_USER`             | PostgreSQL username                                               |
| `POSTGRES_PASSWORD`         | PostgreSQL password                                               |
| `STRIPE_SECRET_KEY`         | Stripe secret key (from Stripe Dashboard → Developers → API Keys) |
| `STRIPE_PUBLISHABLE_KEY`    | Stripe publishable key (same location)                            |
| `STRIPE_WEBHOOK_SECRET_KEY` | Webhook signing secret (see Stripe setup below)                   |
| `STRIPE_SITE_URL`           | The frontend URL Stripe redirects back to after checkout          |
| `EMAIL_HOST`                | SMTP server host (e.g. `smtp.gmail.com`)                          |
| `EMAIL_PORT`                | SMTP port (587 for TLS)                                           |
| `EMAIL_USE_TLS`             | Enable TLS for email — should be `True`                           |
| `EMAIL_HOST_USER`           | Gmail address used for sending order confirmation emails          |
| `EMAIL_HOST_PASSWORD`       | Gmail App Password (not your regular Gmail password)              |
| `DEFAULT_FROM_EMAIL`        | The "from" address shown in outgoing emails                       |
| `MEDIA_URL`                 | URL prefix for uploaded media files — set to `/media/`            |

The frontend has its own `.env` at `frontend/shop-app/.env` with a single variable:

```
VITE_API_URL='http://localhost:8000'
```

This points the frontend at the local Django server. Change it to the production URL when deploying.

### 2. Stripe Setup

The app uses Stripe in **test mode** for payments. To get it working:

1. Create a free account at [stripe.com](https://stripe.com) if you don't have one.
2. Go to **Developers → API Keys** and copy the **Secret key** and **Publishable key** into your `.env`.
3. For webhooks (required for order status to update after payment):
   - Install the [Stripe CLI](https://stripe.com/docs/stripe-cli)
   - Run `stripe listen --forward-to localhost:8000/api/v1/payments/webhook/` in a terminal
   - Copy the **webhook signing secret** it prints into `STRIPE_WEBHOOK_SECRET_KEY` in your `.env`
4. Each product needs a **Stripe Price ID**. Create products in the Stripe Dashboard under **Product catalogue**, then copy the `price_...` ID — you'll need it when creating products in the admin board.

For test payments use card number `4242 4242 4242 4242` with any future expiry date and any CVC.

### 3. Start the Project

From the root folder, run:

```bash
./start.sh
```

This script will:
- Create the shared `3d-shop` Docker network
- Build and start the backend (PostgreSQL + Django)
- Run Django migrations automatically
- Build and start the frontend (SvelteKit)

Once it finishes, the project is available at:

| Service      | URL                         |
| ------------ | --------------------------- |
| Frontend     | http://localhost:3000       |
| Backend API  | http://localhost:8000       |
| Django Admin | http://localhost:8000/admin |

To stop everything:

```bash
./stop.sh
```

### 4. First-Time Database Setup

On the very first run (or after model changes), apply database migrations:

```bash
./migrate.sh
```

This runs `makemigrations` and `migrate` inside the running Django container. It will also offer to create a superuser at the end — you can skip that and use the dedicated script instead.

### 5. Create a Superuser

A superuser is required to access the admin board and create products. Run:

```bash
./superuser.sh
```

Choose **option 1** to create a new superuser. You will be prompted for:

- Email address
- First name
- Last name
- Phone number
- Password

Choose **option 2** to delete an existing superuser — it will list all current superusers before asking which to remove.

### 6. Log In and Create Your First Product

1. Open http://localhost:3000 and click **Login** in the top right.
2. Sign in with the superuser credentials you just created.
3. After logging in, navigate to the **Admin Board** (available to superusers in the navigation).
4. Go to **Manage Products → Create New Product**.
5. Fill in the product details:
   - **Name** and **Description**
   - **Price** (e.g. `44.99`)
   - **Stripe Price ID** — the `price_...` ID from your Stripe Dashboard product (see Stripe Setup above)
   - **Stock** per size (S, M, L, XL)
   - **Category**
   - **Product image** (JPG/PNG)
   - **3D model** — a `.glb` file exported from Blender. The model is loaded dynamically from the database at runtime and displayed in the 3D shop scene.
6. Save the product. It will immediately appear in the 3D shop scene at http://localhost:3000.

---

## Project Structure

### Assets

The `assets/` folder at the root contains all project resources outside the application code:

```
assets/
├── trailer.mp4                  # Project trailer video
├── documentation/
│   ├── backend.pdf              # Technical documentation: Django backend architecture,
│   │                            #   API endpoints, data models, and production setup
│   ├── frontend.pdf             # Technical documentation: SvelteKit + Three.js frontend,
│   │                            #   component structure, and environment config
│   └── virtual-try-on feature.pdf  # Research and implementation notes for the AR
│                                #   virtual try-on feature (PoseNet + canvas overlay)
├── shirts/
│   ├── shirt1.jpg – shirt4.jpg  # Reference product images used during development
│   └── tshirt-transformed.glb  # Original Blender-exported T-shirt model (for reference;
│                                #   not loaded at runtime — models are served from the DB)
└── room_250130/
    ├── room_stand250121.blend   # Blender source file for the 3D shop environment
    └── Materials/               # Blender material textures for the shop model
```

The `Technische Dokumentation/` folder (mounted separately) contains the full set of technical documentation PDFs covering concept development, backend, frontend, and the virtual try-on feature research.

### Application

```
tshirt-shop/
├── backend/shopcore/            # Django backend
│   ├── shopcore/                # Project settings and URL config
│   ├── users/                   # Custom user model and auth endpoints
│   ├── products/                # Product model, CRUD endpoints
│   ├── orders/                  # Order model and management endpoints
│   ├── payment/                 # Stripe checkout session and webhook handler
│   ├── email_service/           # Order confirmation email logic (Gmail SMTP)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── .env
└── frontend/shop-app/           # SvelteKit frontend
    ├── src/
    │   ├── routes/              # SvelteKit pages: shop, checkout, login, register,
    │   │                        #   profile, admin board (products, orders, users)
    │   ├── lib/components/
    │   │   ├── 3D/              # Threlte/Three.js scene components:
    │   │   │   ├── shopModel.svelte        # The 3D shop environment
    │   │   │   ├── tshirt.svelte           # Individual product (loads .glb from DB)
    │   │   │   ├── pictureBillboard.svelte # Static image billboards in the scene
    │   │   │   └── interactiveBillboard.svelte  # Animated/clickable billboard
    │   │   ├── popUps/          # Cart, checkout, product detail overlays
    │   │   ├── cameraControls/ # Camera movement and position management
    │   │   └── messages/        # Toast / notification components
    │   ├── api/                 # API client functions (auth, products, orders,
    │   │                        #   checkout, email)
    │   └── stores/              # Svelte stores for shared state (cart, product
    │                            #   selection, camera)
    ├── static/                  # Static assets served directly:
    │   ├── shopModel-transformed.glb  # The 3D shop scene model
    │   ├── Billboards/          # Billboard images displayed in the 3D scene
    │   ├── sounds/              # Ambient music and interaction sound effects
    │   └── favicon.png
    ├── Dockerfile
    ├── docker-compose.yml
    └── .env
```

### Tech Stack

The **backend** is a Django REST API backed by PostgreSQL. It handles user authentication (session-based, with a custom user model), product and order management, Stripe payment sessions and webhooks, and order confirmation emails via Gmail SMTP. Everything runs in Docker.

The **frontend** is a SvelteKit application that renders the shop entirely in 3D using [Threlte](https://threlte.xyz/) (a Svelte wrapper around Three.js). Product `.glb` models are stored in the database as binary data and loaded dynamically into the scene at runtime. The checkout flow is handled through Stripe's hosted checkout page, with the order status updated automatically via Stripe webhooks.
