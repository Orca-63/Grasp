# GRASP — Don’t just chat, GRASP it! 📚
<img width="754" height="242" alt="Screenshot 2025-07-14 225647" src="https://github.com/user-attachments/assets/55b81e41-2d21-4807-b13d-af7aa70d6a9a" />

A real-time collaborative learning platform that brings students together for seamless group study sessions with mathematical equation support and instant messaging.


## Features ✨



### Real-Time Collaboration 🔥
- **Instant Messaging**: Live chat with WebSocket-powered real-time communication
- **Group Study Rooms**: Create and join private or public study groups
- **Live User Presence**: See who's online and actively participating in discussions

<img width="1897" height="865" alt="Screenshot 2025-07-24 091703" src="https://github.com/user-attachments/assets/41423a4f-22f6-4669-b63f-1f785f2314bc" />

### Mathematical Excellence 📐
- **LaTeX Support**: Write and render complex mathematical equations using MathJax
- **Math Keyboard**: Built-in mathematical symbol keyboard for easy equation input
- **Academic Discussions**: Perfect for STEM subjects with proper formula rendering

<img width="1897" height="712" alt="Screenshot 2025-07-24 091954" src="https://github.com/user-attachments/assets/69ad973d-98fe-44b2-887b-ef028a0ba61f" />

### Modern Features 🚀
- **Rich Media Sharing**: Upload and share study materials, images, GIFs, and visual content with group members
- **File Sharing**: Upload and share study materials with group members
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **User Profiles**: Personalized avatars and user identification
- **Verified Email Security**: Only users with verified emails can join groups for enhanced safety
- **Smart Moderation**: Group admins can remove disruptive users to maintain a focused learning environment
- **Group Management**: Easy-to-use controls for joining, leaving, renaming, and cleaning up study groups

## Tech Stack 🛠️

- **Backend**: Django + Django Channels for WebSocket support
- **Database**: PostgreSQL for reliable data storage
- **Cache/Message Broker**: Redis for scalable real-time messaging
- **Math Rendering**: MathJax for LaTeX equation display
- **Containerization**: Docker for consistent deployment
- **Frontend**: Modern HTML/CSS/JavaScript, HTMX and Tailwind CSS with responsive design

## Quick Start 🏃‍♂️

### Prerequisites
- Docker Desktop
- Python 3.8+
- PostgreSQL
- Redis

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Orca-63/Grasp.git
   cd django-starter-main
   ```

2. **Set up environment variables**
   ```bash
   Edit .env with your configurations
   ```

3. **Run with Docker**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8000`
   - Create an account and start studying!


## 📱 How to Use

1. **Create Account**: Sign up with your email and create a profile
2. **Join Study Groups**: Browse available groups or create your own
3. **Start Collaborating**: Use the chat to discuss topics and share equations
4. **Share Math**: Use the built-in LaTeX keyboard to write complex formulas
5. **File Sharing**: Upload documents, notes, and study materials


## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request




---
**Start collaborating today!** Built with 💙 by students, for students - a platform designed to help peers excel in their studies together.

