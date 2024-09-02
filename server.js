const express = require("express");
const mongoose = require("mongoose");
const path = require("path");
const session = require("express-session"); // Import express-session
const authRoutes = require("./auth");
const groupRoutes = require("./groupRoutes");
const studentRoutes = require("./studentRoutes");
const assignmentRoutes = require("./assignmentRoutes");
const { isAuthenticated } = require("./middlewares"); // Import middleware
require("dotenv").config();

const app = express();
const port = process.env.PORT || 5000;

// Connect to MongoDB
const mongoUri = process.env.MONGO_URI || "mongodb://localhost:27017/vir";

mongoose
  .connect(mongoUri, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((error) => console.error("Error connecting to MongoDB:", error));

// Middleware for handling JSON, URL-encoded bodies
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));

// Configure session middleware
app.use(
  session({
    secret: "Deiva",
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }, // 1 minute
  })
);

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));

// API Route to check session status
app.get("/api/checkSession", (req, res) => {
  if (req.session.user) {
    res.json({ authenticated: true });
  } else {
    res.json({ authenticated: false });
  }
});

// Routes that require authentication
app.get("/studentDashboard.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "studentDashboard.html"));
});

app.get("/teacherDashboard.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "teacherDashboard.html"));
});

app.get("/sprofile.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "sprofile.html"));
});

app.get("/chatbot.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "chatbot.html"));
});

app.get("/sallclassrooms.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "sallclassrooms.html"));
});

app.get("/sgroups.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "sgroups.html"));
});

app.get("/profile.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "profile.html"));
});

app.get("/chatbot.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "chatbot.html"));
});

app.get("/classrooms.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "classrooms.html"));
});

app.get("/groups.html", isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, "groups.html"));
});

// Dynamic redirection based on query parameters
/*app.get("/redirect", isAuthenticated, (req, res) => {
  const { page, phoneNo } = req.query; // Get `page` and `phoneNo` from query parameters

  let targetUrl;
  switch (page) {
    case "profile":
      targetUrl = `/sprofile.html?phoneNo=${phoneNo}`;
      break;
    case "chatbot":
      targetUrl = `/chatbot.html`;
      break;
    case "attendance":
      targetUrl = `/sallclassrooms.html`;
      break;
    case "groups":
      targetUrl = `/sgroups.html`;
      break;

    default:
      targetUrl = `/login.html`; // Fallback if page is not r`ecognized
  }

  res.redirect(targetUrl);
});
*/

// API Routes
app.use("/api/auth", authRoutes);
app.use("/api/groups", groupRoutes);
app.use("/api/students", studentRoutes);
app.use("/api", assignmentRoutes);

// Error handling middleware (optional)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something went wrong!");
});

// Start server
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
