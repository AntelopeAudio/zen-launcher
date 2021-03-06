[Setup]
#define NAME "ZenStudio Control Panel"
#define DIR "ZenStudioControlPanel"
#define VERSION GetEnv("ZEN_LAUNCHER_VERSION")
; #define DEBUG

AppId="AntelopeAudioZenStudioCPLauncher"
AppName={#NAME}
AppPublisher="AntelopeAudio"
AppVersion={#VERSION}
Compression=lzma
DefaultDirName={pf}\{#DIR}
DefaultGroupName={#NAME}
OutputBaseFilename=ZenStudio_{#VERSION}
SetupIconFile="setup.ico"
SolidCompression=yes
VersionInfoVersion={#VERSION}
WizardImageFile="wizard.bmp"
; WizardSmallImageFile="wizard-small.bmp"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
#ifndef DEBUG
Source: "..\build_win\*"; DestDir: "{app}"; Flags: "recursesubdirs"
#endif

[Icons]
Name: "{app}\zen_launcher.exe"; Filename: "{app}\zen_launcher.exe"; IconFileName: "{app}\zen_launcher_resources\icons\zen.ico"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"
Name: "{group}\{#NAME}"; Filename: "{app}\zen_launcher.exe"; IconFileName: "{app}\zen_launcher_resources\icons\zen.ico"
Name: "{commondesktop}\{#NAME}"; Filename: "{app}\zen_launcher.exe"; Tasks: desktopicon; IconFileName: "{app}\zen_launcher_resources\icons\zen.ico"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#NAME}"; Filename: "{app}\zen_launcher.exe"; Tasks: desktopicon; IconFileName: "{app}\zen_launcher_resources\icons\zen.ico"

[Run]
Filename: {app}\zen_launcher.exe; Description: "{cm:LaunchProgram,{#NAME}}"; Flags: postinstall nowait skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Explorer\MenuOrder\Start Menu\Programs\{#NAME}"; Flags: uninsdeletekey
