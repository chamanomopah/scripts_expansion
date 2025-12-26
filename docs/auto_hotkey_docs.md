Using the Program

AutoHotkey doesn't do anything on its own; it needs a script to tell it what to do. A script is simply a plain text file with the .ahk filename extension containing instructions for the program, like a configuration file, but much more powerful. A script can do as little as performing a single action and then exiting, but most scripts define a number of hotkeys, with each hotkey followed by one or more actions to take when the hotkey is pressed.
#z::Run "https://www.autohotkey.com"  ; Win+Z

^!n::  ; Ctrl+Alt+N
{
    if WinExist("Untitled - Notepad")
        WinActivate
    else
        Run "Notepad"
}
S↓


Tip: If your browser supports it, you can download any code block (such as the one above) as a script file by clicking the ↓ button which appears in the top-right of the code block when you hover your mouse over it.

Table of Contents
•Create a Script
•Edit a Script
•Run a Script
•Tray Icon
•Main Window
•Embedded Scripts
•Command Line Usage
•Portability of AutoHotkey.exe
•Launcher
•Dash
•New Script
•Installation ◦Run with UI Access


Create a Script

There are a few common ways to create a script file:
•In Notepad (or a text editor of your choice), save a file with the .ahk filename extension. On some systems you may need to enclose the name in quotes to ensure the editor does not add another extension (such as .txt). 
Be sure to save the file as UTF-8 with BOM if it will contain non-ASCII characters. For details, see the FAQ.

•In Explorer, right-click in empty space in the folder where you want to save the script, then select New and AutoHotkey Script. You can then type a name for the script (taking care not to erase the .ahk extension if it is visible).
•In the Dash, select New script, type a name for the script (excluding the .ahk extension) and click Create or Edit. The template used to create the script and the location it will be saved can be configured within this window, and set as default if desired.

See Scripting Language for details about how to write a script.

Edit a Script

To open a script for editing, right-click on the script file and select Edit Script. If the script is already running, you can use the Edit function or right-click the script's tray icon and select Edit Script. If you haven't selected a default editor yet, you should be prompted to select one. Otherwise, you can change your default editor via Editor settings in the Dash. Of course, you can always open a text editor first and then open the script as you would any other text file.

After editing a script, you must run or reload the script for the changes to take effect. A running script can usually be reloaded via its tray menu.

Run a Script

With AutoHotkey installed, there are several ways to run a script:
•Double-click a script file (or shortcut to a script file) in Explorer.
•Call AutoHotkey.exe on the command line and pass the script's filename as a command-line parameter.
•After creating the default script, launch AutoHotkey via the shortcut in the Start menu to run it.
•If AutoHotkey is pinned to the taskbar or Start menu on Windows 7 or later, recent or pinned scripts can be launched via the program's Jump List.

Most scripts have an effect only while they are running. Use the tray menu or the ExitApp function to exit a script. Scripts are also forced to exit when Windows shuts down. To configure a script to start automatically after the user logs in, the easiest way is to place a shortcut to the script file in the Startup folder.

Scripts can also be compiled; that is, combined together with an AutoHotkey binary file to form a self-contained executable (.exe) file.

Tray Icon

By default, each script adds its own icon to the taskbar notification area (commonly known as the tray).

The tray icon usually looks like this:
 
green H icon The default tray icon. 
green icon with a Pause symbol The script is paused. 
green icon with a transparent H The script is suspended. 
green icon with a transparent Pause symbol The script is paused and suspended. 

Right-click the tray icon to show the tray menu, which has the following options by default:
•Open - Open the script's main window.
•Help - Open the AutoHotkey offline help file.
•Window Spy - Displays various information about a window.
•Reload Script - See Reload.
•Edit Script - See Edit.
•Suspend Hotkeys - Suspend or unsuspend hotkeys.
•Pause Script - Pause or unpause the script.
•Exit - Exit the script.

By default, double-clicking the tray icon shows the script's main window.

The behavior and appearance of the tray icon and menu can be customized:
•A_TrayMenu returns a Menu object which can be used to customise the tray menu.
•A_IconHidden or the #NoTrayIcon directive can be used to hide (or show) the tray icon.
•A_IconTip can be assigned new tooltip text for the tray icon.
•TraySetIcon can be used to change the icon.

Main Window

The script's main window is usually hidden, but can be shown via the tray icon or one of the functions listed below to gain access to information useful for debugging the script. Items under the View menu control what the main window displays:
•Lines most recently executed - See ListLines.
•Variables and their contents - See ListVars.
•Hotkeys and their methods - See ListHotkeys.
•Key history and script info - See KeyHistory.

Known issue: Keyboard shortcuts for menu items do not work while the script is displaying a message box or other dialog.

The built-in variable A_ScriptHwnd contains the unique ID (HWND) of the script's main window.

Closing this window with WinClose (even from another script) causes the script to exit, but most other methods just hide the window and leave the script running.

Minimizing the main window causes it to automatically be hidden. This is done to prevent any owned windows (such as GUI windows or certain dialog windows) from automatically being minimized, but also has the effect of hiding the main window's taskbar button. To instead allow the main window to be minimized normally, override the default handling with OnMessage. For example:
; This prevents the main window from hiding on minimize:
OnMessage 0x0112, PreventAutoMinimize ; WM_SYSCOMMAND = 0x0112
OnMessage 0x0005, PreventAutoMinimize ; WM_SIZE = 0x0005
; This prevents owned GUI windows (but not dialogs) from automatically minimizing:
OnMessage 0x0018, PreventAutoMinimize
Persistent

PreventAutoMinimize(wParam, lParam, uMsg, hwnd) {
    if (uMsg = 0x0112 && wParam = 0xF020 && hwnd = A_ScriptHwnd) { ; SC_MINIMIZE = 0xF020
        WinMinimize
        return 0 ; Prevent main window from hiding.
    }
    if (uMsg = 0x0005 && wParam = 1 && hwnd = A_ScriptHwnd) ; SIZE_MINIMIZED = 1
        return 0 ; Prevent main window from hiding.
    if (uMsg = 0x0018 && lParam = 1) ; SW_PARENTCLOSING = 1
        return 0 ; Prevent owned window from minimizing.
}



Main Window Title

The title of the script's main window is used by the #SingleInstance and Reload mechanisms to identify other instances of the same script. Changing the title prevents the script from being identified as such. The default title depends on how the script was loaded:


Loaded From

Title Expression

Example

.ahk file A_ScriptFullPath " - AutoHotkey v" A_AhkVersion E:\My Script.ahk - AutoHotkey v1.1.33.09 
Main resource (compiled script) A_ScriptFullPath E:\My Script.exe 
Any other resource A_ScriptFullPath " - " A_LineFile E:\My AutoHotkey.exe - *BUILTIN-TOOL.AHK 

The following code illustrates how the default title could be determined by the script itself (but the actual title can be retrieved with WinGetTitle):
title := A_ScriptFullPath
if !A_IsCompiled
    title .= " - AutoHotkey v" A_AhkVersion
; For the correct result, this must be evaluated by the resource being executed,
; not an #include (unless the #include was merged into the script by Ahk2Exe):
else if SubStr(A_LineFile, 1, 1) = "*" && A_LineFile != "*#1"
    title .= " - " A_LineFile




Embedded Scripts

Scripts may be embedded into a standard AutoHotkey .exe file by adding them as Win32 (RCDATA) resources using the Ahk2Exe compiler. To add additional scripts, see the AddResource compiler directive.

An embedded script can be specified on the command line or with #Include by writing an asterisk (*) followed by the resource name. For an integer ID, the resource name must be a hash sign (#) followed by a decimal number.

The program may automatically load script code from the following resources, if present in the file:


ID

Spec

Usage

1 *#1 This is the means by which a compiled script is created from an .exe file. This script is executed automatically and most command line switches are passed to the script instead of being interpreted by the program. External scripts and alternative embedded scripts can be executed by using the /script switch. 
2 *#2 If present, this script is automatically "included" before any script that the program loads, and before any file specified with /include. 

When the source of the main script is an embedded resource, the program acts in "compiled script" mode, with the exception that A_AhkPath always contains the path of the current executable file (the same as A_ScriptFullPath). For resources other than *#1, the resource specifier is included in the main window's title to support #SingleInstance and Reload.

When referenced from code that came from an embedded resource, A_LineFile contains an asterisk (*) followed by the resource name.

Command Line Usage

See Passing Command Line Parameters to a Script for command line usage, including a list of command line switches which affect the program's behavior.

Portability of AutoHotkey.exe

The file AutoHotkey.exe is all that is needed to launch any .ahk script.

Renaming AutoHotkey.exe also changes which script it runs by default, which can be an alternative to compiling a script for use on a computer without AutoHotkey installed. For instance, MyScript.exe automatically runs MyScript.ahk if a filename is not supplied, but is also capable of running other scripts.

Launcher

The launcher enables the use of v1 and v2 scripts on one system, with a single filename extension, without necessarily giving preference to one version or requiring different methods of launching scripts. It does this by checking the script for clues about which version it requires, and then locating an appropriate exe to run the script.

If the script contains the #Requires directive, the launcher looks for an exe that satisfies the requirement. Otherwise, the launcher optionally checks syntax. That is, it checks for patterns that are valid only in one of the two major versions. Some of the common patterns it may find include:
•v1: MsgBox, with comma, MsgBox % "no end percent" and Legacy = assignment.
•v1: Multi-line hotkeys without braces or a function definition.
•Common directives such as #NoEnv and #If (v1) or #HotIf (v2).
•v2: Unambiguous use of continuation by enclosure or end-of-line continuation operators.
•v2: Unambiguous use of 'single quotes' or fat arrow => in an expression.

Detection is conservative; if a case is ambiguous, it should generally be ignored.

In any case where detection fails, by default a menu is shown for the user to select a version. This default can be changed to instead launch either v1 or v2.

Known limitations:
•Only the main file is checked.
•Since it is legal to include a line like /****/ in v1, but */ at line-end only closes comments in v2, the presence of such a line may cause a large portion of the script to be ignored (by both the launcher and the v1 interpreter).
•Only syntax is checked, not semantics. For instance, xyz, is invalid in v2, so is assumed to be a valid v1 command. xyz 1 could be a function statement in v2, but is assumed to also be a valid v1 command, and is therefore ignored.
•Since the patterns being detected are effectively syntax errors in one version, a script with actual syntax errors or incorrectly mixed syntax might be misidentified.

Note: Declaring the required version with #Requires at the top of the main file eliminates any ambiguity.

Launch Settings

The launcher can be enabled, disabled or configured via the Launch Settings GUI, which can be accessed via the dash.

Run all scripts with a specific interpreter disables the launcher and allows the user to select which exe to use to run all scripts, the traditional way. Be aware that selecting a v1 exe will make it difficult to run any of the support scripts, except via the "AutoHotkey" shortcut in the Start menu.

Auto-detect version when launching script enables the launcher. Additional settings control how the launcher selects which interpreter to use.

Criteria

When multiple interpreters with the same version number are found, the launcher can rank them according to a predetermined or user-defined set of criteria. The criteria can be expressed as a comma-delimited list of substrings, where each substring may be prefixed with "!" to negate a match. A score is calculated based on which substrings matched, with the left-most substring having highest priority.

Substrings are matched in the file's description, with the exception of "UIA", which matches if the filename contains "_UIA".

For example, _H, 64, !ANSI would prefer AutoHotkey_H if available, 64-bit if compatible with the system, and finally Unicode over ANSI.

Although the Launcher Settings GUI presents drop-down lists with options such as "Unicode 32-bit", a list of substrings can be manually entered.

Additional (higher-priority) criteria can be specified on the command line with the /RunWith launcher switch.

Criteria can be specified within the script by using the #Requires directive, either as a requirement (if supported by the target AutoHotkey version), or appended to the directive as a comment beginning with "prefer" and ending with a full stop or line ending. For example:
#Requires AutoHotkey v1.1.35 ; prefer 64-bit, Unicode.  More comments.



Run *Launch

The installer registers a hidden shell verb named "launch", which executes the launcher with the /Launch switch. It can be utilized by following this example:
pid := RunWait('*Launch "' PathOfScript '"')



By contrast with the default action for .ahk files:
•/Launch causes the process ID (PID) of the newly launched script to be returned as the launcher's exit code, whereas it would normally return the launched script's exit code. Run's OutputVarPID parameter returns the PID of the launcher.
•/Launch causes the launcher to exit immediately after launching the script. If /Launch is not used, the launcher generally has to assume that its parent process might be doing something like RunWait(PathOfScript), which wouldn't work as expected if the launcher exited before the launched script.

Command Line Usage

The launcher can be explicitly executed at the command line for cases where .ahk files are not set to use the launcher by default, or for finer control over its behaviour. If the launcher is compiled, its usage is essentially the same as AutoHotkey.exe except for the additional launcher switches. Otherwise, the format for command line use is as follows:
AutoHotkeyUX.exe launcher.ahk [Switches] [Script Filename] [Script Parameters]



Typically full paths and quote marks would be used for the path to AutoHotkeyUX.exe and launcher.ahk, which can be found in the UX subdirectory of the AutoHotkey installation. An appropriate version of AutoHotkey32.exe or AutoHotkey64.exe can be used instead of AutoHotkeyUX.exe (which is just a copy).

Switches can be a mixture of any of the standard switches and the following launcher-only switches:


Switch

Meaning

/Launch Causes the launcher to exit immediately after launching the script, instead of waiting in the background for it to terminate. The launcher's exit code is the process ID (PID) of the new script process. 
/RunWith criteria Specifies additional criteria for determining which executable to use to launch the script. For example, /RunWith UIA. 
/Which 
Causes the launcher to identify which interpreter it would use and return it instead of running the script.

The launcher's exit code is the major version number (1 or 2) if identified by #Requires or syntax (if syntax detection is enabled), otherwise 0.

Stdout receives the following UTF-8 strings, each terminated with `n:
•The version number. If #Requires was detected, this is whatever number it specified, excluding "v". Otherwise, it is an integer the same as the exit code, unless the version wasn't detected, in which case this is 0 to indicate that the user would have been prompted, or 1 or 2 to indicate the user's preferred version as configured in the Launch Settings.
•The path of the interpreter EXE that would be used, if one was found. This is blank if the user would have been prompted or no compatible interpreters were found.
•Any additional command-line switches that the launcher would insert, such as /CP65001.

Additional lines may be returned in future.
 

Dash

The dash provides access to support scripts and documentation. It can be opened via the "AutoHotkey" shortcut in the Start menu after installation, or by directly running UX\ui-dash.ahk from the installation directory. Currently it is little more than a menu containing the following items, but it might be expanded to provide controls for active scripts, or other convenient functions.
•New script: Create a new script from a template.
•Compile: Opens Ahk2Exe, or offers to automatically download and install it.
•Help files (F1): Shows a menu containing help files and online documentation for v1 and v2, and any other CHM files found in the installation directory.
•Window spy
•Launch settings: Configure the launcher.
•Editor settings: Set the default editor for .ahk files.

Note that although the Start menu shortcut launches the dash, if it is pinned to the taskbar (or to the Start menu in Windows 7 or 10), the jump list will include any recent scripts launched with the open, runas or UIAccess shell verbs (which are normally accessed via the Explorer context menu or by double-clicking a file). Scripts can be pinned for easy access.

New Script

The New Script GUI can be accessed via the dash or by right-clicking within a folder in Explorer and selecting New → AutoHotkey Script. It can be used to create a new script file from a preinstalled or user-defined template, and optionally open it for editing.

Right-clicking on a template in the list gives the following options:
•Edit template: Open the template in the default editor. If it is a preinstalled template, an editable copy is created instead of opening the original.
•Hide template: Adds the template name to a list of templates that will not be shown in the GUI. To unhide a template, delete the corresponding registry value from HKCU\Software\AutoHotkey\New\HideTemplate.
•Set as default: Sets the template to be selected by default.

By default, the GUI closes after creating a file unless the Ctrl key is held down.

Additional settings can be accessed via the settings button at the bottom-left of the GUI:
•Default to Create: Pressing Enter will activate the Create button, which creates the script and selects it in Explorer.
•Default to Edit: Pressing Enter will activate the Edit button, which creates the script and opens it in the default script editor.
•Stay open: If enabled, the window will not close automatically after creating a script.
•Set folder as default: Sets the current folder as the default location to save scripts. The default location is used if the New Script window is opened directly or via the Dash; it is not used when New Script is invoked via the Explorer context menu.
•Open templates folder: Opens the folder where user-defined templates can be stored.

Templates

Template files are drawn from UX\Templates (preinstalled) and %A_MyDocuments%\AutoHotkey\Templates (user), with a user-defined template overriding any preinstalled template which has the same name. If a file exists at %A_WinDir%\ShellNew\Template.ahk, it is shown as "Legacy" and can be overridden by a user-defined template of that name.

Each template may contain an INI section as follows:
/*
[NewScriptTemplate]
Description = Descriptive text
Execute = true|false|1|0
*/



If the INI section starts with /* and ends with */ as shown above, it is not included in the created file.

Description is optional. It is shown in the GUI, in addition to the file's name.

Execute is optional. If set to true, the template script is executed with A_Args[1] containing the path of the file to be created and A_Args[2] containing either "Create" or "Edit", depending on which button the user clicked. The template script is expected to create the file and open it for editing if applicable. If the template script needs to #include other files, they can be placed in a subdirectory to avoid having them shown in the template list.

Installation

This installer and related scripts are designed to permit multiple versions of AutoHotkey to coexist. The installer provides very few options, as most things can be configured after installation. Only the following choices must be made during installation:
•Where to install.
•Whether to install for all users or the current user.

By default the installer will install to "%A_ProgramFiles%\AutoHotkey" for all users. This is recommended, as the UI Access option requires the program to be installed under Program Files. If the installer is not already running as admin, it will attempt to elevate when the Install button is clicked, as indicated by the shield icon on the button.

Current user installation does not require admin rights, as long as the user has write access to the chosen directory. The default directory for a current user installation is "%LocalAppData%\Programs\AutoHotkey".

Installing with v1

There are two methods of installing v1 and v2 together:
1.Install v1 first, and then v2. In that case, the v1 files are left in the root of the installation directory, to avoid breaking any external tools or shortcuts that rely on their current path.
2.Install v1 as an additional version. Running a v1.1.34.03 or later installer gives this option. Alternatively, use the /install switch described below. Each version installs into its own subdirectory.

Running a v1.1.34.02 or older installer (or a custom install with v1.1.34.03 or newer) will overwrite some of the values set in the registry by the v2 installer, such as the version number, uninstaller entry and parts of the file type registration. It will also register the v1 uninstaller, which is not capable of correctly uninstalling both versions. To re-register v2, re-run any v2 installer or run UX\install.ahk using AutoHotkey32.exe or AutoHotkey64.exe.

Default Version

Unlike a v1 installation, a default version is not selected during installation. Defaults are instead handled more dynamically by the launcher, and can be configured per-user.

Command Line Usage

To directly install to the DESTINATION directory, use /installto or /to (the two switches are interchangeable) as shown below, from within the source directory. Use either a downloaded setup.exe or files extracted from a downloaded zip or other source.
AutoHotkey_setup.exe /installto "%DESTINATION%"


AutoHotkey32.exe UX\install.ahk /to "%DESTINATION%"



To install an additional version from SOURCE (which should be a directory containing AutoHotkey*.exe files), execute the following from within the current installation directory (adjusting the path of AutoHotkey32.exe as needed):
AutoHotkey32.exe UX\install.ahk /install "%SOURCE%"



The full command string for the above is registered as InstallCommand under HKLM\Software\AutoHotkey or HKCU\Software\AutoHotkey, with %1 as the substitute for the source directory. Using this registry value may be more future-proof.

To re-register the current installation:
AutoHotkey32.exe UX\install.ahk



To uninstall:
AutoHotkey32.exe UX\install.ahk /uninstall



Alternatively, read the QuietUninstallString value from one of the following registry keys, and execute it:
HKLM\Microsoft\Windows\CurrentVersion\Uninstall\AutoHotkey
HKCU\Microsoft\Windows\CurrentVersion\Uninstall\AutoHotkey



Use the /silent switch to suppress warning or confirmation dialogs and prevent the Dash from being shown when installation is complete. The following actions may be taken automatically, without warning:
•Terminate scripts to allow AutoHotkey*.exe to be overwritten.
•Overwrite files that were not previously registered by the installer, or that were modified since registration.

Taskbar Buttons

The v2 installer does not provide an option to separate taskbar buttons. This was previously achieved by registering each AutoHotkey executable as a host app (IsHostApp) ¬, but this approach has limitations, and becomes less manageable when multiple versions can be installed. Instead, each script should set the AppUserModelID ¬ of its process or windows to control grouping.

Run with UI Access

When installing under Program Files, the installer creates an additional set of AutoHotkey exe files that can be used to work around some common UAC-related issues. These files are given the "_UIA.exe" suffix. When one of these UIA.exe files is used by an administrator to run a script, the script is able to interact with windows of programs that run as admin, without the script itself running as admin.

The installer does the following:
•Copies each AutoHotkey*.exe to AutoHotkey*_UIA.exe.
•Sets the uiAccess attribute ¬ in each UIA.exe file's embedded manifest.
•Creates a self-signed digital certificate named "AutoHotkey" and signs each UIA.exe file.
•Registers the UIAccess shell verb, which appears in Explorer's context menu as "Run with UI access". By default this executes the launcher, which tries to select an appropriate UIA.exe file to run the script.

The launcher can also be configured to run v1 scripts, v2 scripts or both with UI Access by default, but this option has no effect if a UIA.exe file does not exist for the selected version and build.

Scripts which need to run other scripts with UI access can simply Run the appropriate UIA.exe file with the normal command line parameters. Alternatively, if the UIAccess shell verb is registered, it can be used via Run. For example: Run '*UIAccess "Script.ahk"'

Known limitations:
•UIA is only effective if the file is in a trusted location; i.e. a Program Files sub-directory.
•UIA.exe files created on one computer cannot run on other computers without first installing the digital certificate which was used to sign them.
•UIA.exe files cannot be started via CreateProcess due to security restrictions. ShellExecute can be used instead. Run tries both.
•UIA.exe files cannot be modified, as it would invalidate the file's digital signature.
•Because UIA programs run at a different "integrity level" than other programs, they can only access objects registered by other UIA programs. For example, ComObjActive("Word.Application") will fail because Word is not marked for UI Access.
•The script's own windows can't be automated by non-UIA programs/scripts for security reasons.
•Running a non-UIA script which uses a mouse hook (even as simple as InstallMouseHook) may prevent all mouse hotkeys from working when the mouse is pointing at a window owned by a UIA script, even hotkeys implemented by the UIA script itself. A workaround is to ensure UIA scripts are loaded last.
•UIA prevents the Gui +Parent option from working on an existing window if the new parent is always-on-top and the child window is not.

For more details, see Enable interaction with administrative programs ¬ on the archived forum.

Copyright © 2003-2025 - LIC: GNU GPLv2

