# 🖼 GoodyTreat Background Remover Bot (@goodytreatbot)

A complete, production-ready Telegram Bot built with Python that automatically removes backgrounds from uploaded images and returns transparent PNG files.

---

## 🌟 Features

* **Automatic Background Removal**: Powered by local AI segmentation (`rembg`/`u2netp`) with seamless fallback support for `Remove.bg API`.
* **Multiple Image Format Support**: Accepts JPEG, JPG, PNG, and WEBP formats sent either as photos or uncompressed documents.
* **Transparent PNG Output**: Delivers high-quality transparent PNG results.
* **Interactive UI**: Clean, inline buttons for simple navigation.
* **Concurrency Locking**: Prevents users from submitting duplicate simultaneous jobs.
* **Admin Capabilities**:
  * `/stats`: View total users, images processed, and success/failure counts.
  * `/broadcast`: Send broadcasts to all registered bot users.
* **Render Ready**: Includes built-in HTTP health check endpoint for zero-downtime deployment on Render Web Services.

---

## 🛠 Prerequisites

* Python 3.11+
* Telegram account to obtain API Token from `@BotFather`.
* GitHub account & Render account (for deployment).

---

## 🔑 Obtaining Telegram Bot Token

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a name and username for your bot (e.g., `goodytreatbot`).
4. Copy the HTTP API Token provided.

---

## 🚀 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/background-remover-bot.git](https://github.com/your-username/background-remover-bot.git)
   cd background-remover-bot
