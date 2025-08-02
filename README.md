# 🍅 PomoPy - Desktop Pomodoro Timer

A beautiful and functional desktop pomodoro timer application built with Python and Tkinter.

## Features

### ⏰ Timer Functionality

- **Work Timer**: 25-minute focused work sessions (customizable)
- **Short Break**: 5-minute breaks between work sessions (customizable)
- **Long Break**: 15-minute breaks after 4 pomodoros (customizable)
- **Auto-switching**: Automatically switches between work and break modes
- **Progress Bar**: Visual progress indicator for current session

### 🎛️ Controls

- **Start/Pause**: Control timer execution
- **Reset**: Reset current session
- **Mode Selection**: Manually switch between work, short break, and long break modes

### 📊 Statistics

- **Session Tracking**: Counts completed pomodoros
- **Work Time**: Tracks total work time in minutes
- **Real-time Updates**: Statistics update automatically

### ⚙️ Settings

- **Customizable Times**: Adjust work, short break, and long break durations
- **Pomodoro Cycles**: Set how many pomodoros before a long break
- **Persistent Settings**: Settings are saved and loaded automatically

### 🎨 User Interface

- **Modern Design**: Clean, dark theme with colorful accents
- **Responsive Layout**: Well-organized interface elements
- **Visual Feedback**: Color-coded modes and progress indicators
- **Notifications**: System alerts when sessions complete

## Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually included with Python)

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

### Controls

- **Start**: Begin the current timer
- **Pause**: Pause the running timer
- **Reset**: Reset the current session to full duration
- **Mode Buttons**: Switch between work, short break, and long break

### Settings

1. **Click "⚙️ Settings"** to open the settings window
2. **Adjust** the timer durations as needed:
   - Work Time (default: 25 minutes)
   - Short Break (default: 5 minutes)
   - Long Break (default: 15 minutes)
   - Pomodoros before long break (default: 4)
3. **Click "Save Settings"** to apply changes

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
└── pomodoro_settings.json  # Settings file (created automatically)
```

## Customization

### Colors and Themes

The application uses a dark theme with the following color scheme:

- **Background**: Dark blue-gray (#2c3e50)
- **Timer Frame**: Lighter blue-gray (#34495e)
- **Work Mode**: Red (#e74c3c)
- **Short Break**: Blue (#3498db)
- **Long Break**: Purple (#9b59b6)
- **Buttons**: Green (#27ae60), Orange (#f39c12), Red (#e74c3c)

### Timer Durations

You can customize all timer durations through the settings:

- **Work Time**: 1-60 minutes (recommended: 25 minutes)
- **Short Break**: 1-15 minutes (recommended: 5 minutes)
- **Long Break**: 5-30 minutes (recommended: 15 minutes)
- **Pomodoros before Long Break**: 1-10 (recommended: 4)

## Technical Details

### Dependencies

- **tkinter**: GUI framework (built-in with Python)
- **threading**: For non-blocking timer functionality
- **json**: For settings persistence
- **time**: For timer implementation
- **os**: For file operations

### Architecture

- **Object-oriented design** with a main `PomodoroTimer` class
- **Threading** for background timer execution
- **Event-driven** UI updates
- **Settings persistence** using JSON files

## Troubleshooting

### Common Issues

**Timer doesn't start:**

- Ensure you're running Python 3.6+
- Check that tkinter is installed
- Try restarting the application

**Settings not saving:**

- Check file permissions in the project directory
- Ensure the application has write access

**UI looks different:**

- The appearance may vary slightly between operating systems
- Colors and fonts are optimized for cross-platform compatibility

### Performance

- The application uses minimal system resources
- Timer accuracy is maintained through threading
- UI updates are optimized for smooth performance

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
- Built with Python and Tkinter
- Designed for productivity and focus

---

**Happy focusing! 🍅✨**
