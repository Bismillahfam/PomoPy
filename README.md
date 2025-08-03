# 🍅 PomoPy - Graphical Pomodoro Timer

A beautiful and functional graphical pomodoro timer application built with Python and Pygame.

## Features

### ⏰ Timer Functionality

- **Work Timer**: 25-minute focused work sessions (customizable)
- **Short Break**: 5-minute breaks between work sessions (customizable)
- **Long Break**: 15-minute breaks after 4 pomodoros (customizable)
- **Auto-switching**: Automatically switches between work and break modes
- **Visual Progress Bar**: Real-time progress indicator for current session

### 🎛️ Controls

- **Start/Pause**: Click button to control timer execution
- **Reset**: Reset current session with one click
- **Mode Selection**: Easy switching between work, short break, and long break modes
- **Mouse-driven**: Intuitive click-based interface

### 📊 Statistics

- **Session Tracking**: Counts completed pomodoros
- **Work Time**: Tracks total work time in minutes
- **Real-time Updates**: Statistics update automatically

### ⚙️ Settings

- **Customizable Times**: Adjust work, short break, and long break durations
- **Pomodoro Cycles**: Set how many pomodoros before a long break
- **Persistent Settings**: Settings are saved and loaded automatically

### 🎨 User Interface

- **Modern Graphics**: Beautiful Pygame-based interface
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Visual Feedback**: Color-coded modes and hover effects
- **Notifications**: Popup dialogs when sessions complete

## Installation

### Prerequisites

- Python 3.6 or higher
- Pygame library

### Installing Dependencies

1. **Install Pygame** using pip:

```bash
pip install pygame
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### Running the Application

1. **Clone or download** the project files
2. **Navigate** to the project directory
3. **Run** the application:

```bash
python Pomo.py
```

## How to Use

### Basic Usage

1. **Launch** the application
2. **Click "Start"** to begin a work session
3. **Work** for 25 minutes (or your custom duration)
4. **Take a break** when the timer completes
5. **Repeat** the cycle

### Timer Modes

- **Work Mode** (Red): Focused work sessions
- **Short Break** (Blue): Quick breaks between work sessions
- **Long Break** (Purple): Extended breaks after multiple pomodoros

### Interface Controls

- **Start Button**: Begin the current timer
- **Pause Button**: Pause the running timer
- **Reset Button**: Reset the current session to full duration
- **Mode Buttons**: Switch between work, short break, and long break
- **Settings Button**: Access timer settings

### Settings

1. **Click "Settings"** to open the settings dialog
2. **Adjust** the timer durations as needed:
   - Work Time (default: 25 minutes)
   - Short Break (default: 5 minutes)
   - Long Break (default: 15 minutes)
   - Pomodoros before long break (default: 4)
3. **Save** your changes

## Pomodoro Technique

The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. It uses a timer to break work into intervals, traditionally 25 minutes in length, separated by short breaks.

### Benefits

- **Improved Focus**: Short, timed work sessions help maintain concentration
- **Reduced Burnout**: Regular breaks prevent mental fatigue
- **Better Productivity**: Structured approach to work and rest
- **Time Awareness**: Helps track how long tasks actually take

### How It Works

1. **Choose a task** to work on
2. **Set the timer** for 25 minutes
3. **Work** on the task until the timer rings
4. **Take a short break** (5 minutes)
5. **After 4 pomodoros**, take a longer break (15-30 minutes)

## File Structure

```
PomoPy/
├── Pomo.py              # Main application file
├── README.md            # This documentation
├── requirements.txt     # Python dependencies
└── pomodoro_settings.json  # Settings file (created automatically)
```

## Customization

### Timer Durations

You can customize all timer durations through the settings:

- **Work Time**: 1-60 minutes (recommended: 25 minutes)
- **Short Break**: 1-15 minutes (recommended: 5 minutes)
- **Long Break**: 5-30 minutes (recommended: 15 minutes)
- **Pomodoros before Long Break**: 1-10 (recommended: 4)

### Visual Elements

The application uses a modern color scheme:

- **Background**: Dark blue-gray (#2c3e50)
- **Panels**: Lighter blue-gray (#34495e)
- **Work Mode**: Red (#e74c3c)
- **Short Break**: Blue (#3498db)
- **Long Break**: Purple (#9b59b6)
- **Buttons**: Green (#27ae60), Orange (#f39c12), Red (#e74c3c)

## Technical Details

### Dependencies

- **pygame**: Graphics and game development library
- **threading**: For non-blocking timer functionality
- **json**: For settings persistence
- **time**: For timer implementation
- **os**: For file operations

### Architecture

- **Object-oriented design** with a main `PomodoroTimer` class
- **Pygame-based graphics** for modern UI
- **Threading** for background timer execution
- **Event-driven** UI updates
- **Settings persistence** using JSON files

### Platform Support

- **Windows**: Full support with native window management
- **macOS**: Full support with proper window handling
- **Linux**: Full support with X11/Wayland compatibility

## Troubleshooting

### Common Issues

**Pygame not found:**

```bash
pip install pygame
```

**Window doesn't appear:**

- Check if another application is blocking the window
- Try running from terminal/command prompt
- Ensure display drivers are up to date

**Timer doesn't start:**

- Ensure you're running Python 3.6+
- Check that Pygame is properly installed
- Try restarting the application

**Settings not saving:**

- Check file permissions in the project directory
- Ensure the application has write access

**Performance issues:**

- Close other graphics-intensive applications
- Update graphics drivers
- Reduce system load

### Performance

- The application uses moderate system resources
- Timer accuracy is maintained through threading
- Graphics are optimized for smooth 60 FPS performance

## Advantages of Pygame Version

### Benefits

- **Modern graphics**: Professional-looking interface
- **Cross-platform**: Works on all major operating systems
- **Responsive UI**: Smooth animations and hover effects
- **Visual feedback**: Clear progress indicators and status
- **Easy to use**: Intuitive click-based interface
- **Customizable**: Easy to modify colors and layout

### Use Cases

- **Desktop productivity**: Perfect for focused work sessions
- **Professional environments**: Clean, professional appearance
- **Visual learners**: Clear visual progress indicators
- **Accessibility**: Large buttons and clear text

## Contributing

Feel free to contribute to this project by:

- Reporting bugs
- Suggesting new features
- Improving the UI/UX
- Adding new functionality

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by the Pomodoro Technique by Francesco Cirillo
- Built with Python and Pygame
- Designed for productivity and focus

---

**Happy focusing! 🍅✨**
