#!/usr/bin/env python3
"""Set iTerm2 tab color for running script."""

import io
import os
import sys


async def main(connection):
    # Get session ID from environment (format: w0t2p0:UUID)
    session_env = os.environ.get("ITERM_SESSION_ID", "")
    if ":" in session_env:
        session_id = session_env.split(":")[1]
    else:
        session_id = session_env

    # Parse args: "R G B" to set color, "clear" to remove
    clear_mode = len(sys.argv) == 2 and sys.argv[1] == "clear"
    if not clear_mode and len(sys.argv) != 4:
        print("Usage: set_tab_color.py R G B | clear", file=sys.stderr)
        sys.exit(1)

    app = await iterm2.async_get_app(connection)
    for window in app.windows:
        for tab in window.tabs:
            for session in tab.sessions:
                if session.session_id == session_id:
                    change = iterm2.LocalWriteOnlyProfile()
                    if clear_mode:
                        change.set_use_tab_color(False)
                    else:
                        r, g, b = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
                        change.set_tab_color(iterm2.Color(r, g, b))
                        change.set_use_tab_color(True)
                    await session.async_set_profile_properties(change)
                    return


if __name__ == "__main__":
    # Parse args: "R G B" to set color, "clear" to remove
    clear_mode = len(sys.argv) == 2 and sys.argv[1] == "clear"
    if not clear_mode and len(sys.argv) != 4:
        print("Usage: set_tab_color.py R G B | clear", file=sys.stderr)
        sys.exit(1)

    fail_reason = None

    try:
        import iterm2
    except ImportError:
        fail_reason = "Run 'pip3 install iterm2' to hide this message"

    if not fail_reason:
        # Suppress stderr during connection to hide verbose library errors
        real_stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            iterm2.Connection().run_until_complete(main, retry=False, debug=False)
        except ConnectionRefusedError:
            sys.stderr = real_stderr
            fail_reason = "Enable the iTerm Python API in Settings > General > Magic > Enable Python API to hide this message"
        except Exception:
            sys.stderr = real_stderr
            raise
        finally:
            sys.stderr = real_stderr

    if fail_reason:
        if clear_mode:
            # This unfortunately doesn't work because the output is not printed for failing SessionEnd hooks
            print("\033]6;1;bg;*;default\a", end="")
        else:
            r, g, b = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
            print(
                f"\033]6;1;bg;red;brightness;{r}\a\033]6;1;bg;green;brightness;{g}\a\033]6;1;bg;blue;brightness;{b}\a"
            )
        print("Updated iTerm Tab Color ({})".format(fail_reason))
        sys.exit(1)
