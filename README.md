# MiniTweet

A **lightweight Twitter clone** built with **Flask**, **PostgreSQL**,
**Redis**, and **TailwindCSS**.\
It allows users to **register**, **follow others**, **post tweets**, and
**view a personalized feed** --- all optimized with **Redis caching**
for fast performance.

------------------------------------------------------------------------

## 🚀 Features

-   👤 **User Registration** --- Register new users instantly.
-   ➕ **Follow System** --- Follow other users and see their tweets.
-   📝 **Post Tweets** --- Share updates with your followers.
-   ⚡ **Real-time Feeds** --- Feeds are cached using **Redis** for fast
    retrieval.
-   🗄 **Database-backed** --- Uses **PostgreSQL** for persistence.
-   🎨 **Modern UI** --- Styled beautifully using **TailwindCSS**.

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Backend:** Flask (Python)
-   **Frontend:** HTML, TailwindCSS, JavaScript (Fetch API)
-   **Database:** PostgreSQL
-   **Caching:** Redis
-   **API:** RESTful endpoints
-   **CORS:** Enabled for cross-origin requests

------------------------------------------------------------------------

## 📂 Project Structure

    MiniTweet/
    ├── app.py                # Flask backend
    ├── templates/
    │   └── index.html        # Frontend UI
    ├── requirements.txt      # Dependencies
    └── README.md             # Project documentation

------------------------------------------------------------------------

## 🗄️ Database Schema

``` sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE
);

CREATE TABLE follows (
    id SERIAL PRIMARY KEY,
    follower_id INT REFERENCES users(id) ON DELETE CASCADE,
    following_id INT REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE tweets (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

------------------------------------------------------------------------

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

``` bash
git clone https://github.com/your-username/minitweet.git
cd minitweet
```

### 2️⃣ Create Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate   # For Linux / Mac
venv\Scripts\activate    # For Windows
```

### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4️⃣ Setup PostgreSQL Database

``` bash
createdb twitterdb
psql twitterdb < schema.sql
```

### 5️⃣ Start Redis

``` bash
redis-server
```

### 6️⃣ Run the Flask App

``` bash
python app.py
```

Your app will be live at: **http://127.0.0.1:5000**

------------------------------------------------------------------------

## 🔮 Future Improvements

-   🔑 Add authentication & JWT tokens.
-   ❤️ Add likes & comments.
-   🌐 Deploy to **Render**, **Vercel**, or **Heroku**.
-   ⚡ Use **WebSockets** for live updates.

