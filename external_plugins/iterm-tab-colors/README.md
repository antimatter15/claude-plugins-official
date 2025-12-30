# iTerm Tab Colors for Claude Code

Updates iTerm2 tab colors to correspond to Claude Code status. This makes it easy to see the status of your Claude sessions at a glance.

It (mostly) works even without iTerm2 Python API enabled, by raising an error containing iTerm escape sequences to update the tab color. This however confusingly leads to messages like this appearing in your console:

> SessionStart:startup says: Plugin hook "python3 /Users/kevin/Github/claude-plugins-official/external_plugins/iterm-tab-colors/scripts/set_tab_color.py 255 165 0" exited with code 1:
> Updated iTerm Tab Color (Enable the iTerm Python API in Settings > General > Magic > Enable Python API to hide this message)

### Enabling iTerm2 Python API

1. Open iTerm2 Preferences
2. Go to General > Magic
3. Check "Enable Python API"
4. Install the `iterm2` Python package: `pip3 install --break-system-packages iterm2`


## How It Works

The plugin uses Claude Code hooks to change the iTerm2 tab color at different points in the session:

- **SessionStart**: Orange - indicates Claude is ready
- **Stop**: Orange - Claude finished thinking, waiting for input
- **UserPromptSubmit**: Green - processing your request
- **PreToolUse/PostToolUse**: Green - actively working
- **PermissionRequest**: Purple - waiting for your approval
- **SessionEnd**: Clears the tab color (this does not work without the iTerm Python API)
